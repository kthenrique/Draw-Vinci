/*******************************************************************************
 * \file app.c                                                                 *
 *                                                                             *
 * \mainpage DRAW-VINCI [BEL4 - Technikum Wien]                                *
 *                                                                             *
 * Build: make debug OR make flash                                             *
 * Connect a TTL USB cable to UART1, launch the GUI and connect                *
 *                                                                             *
 * @author Kelve T. Henrique - Andreas Hofschweiger                            *
 *                                                                             *
 * @revision 1.0                                                               *
 * @date 05-2018                                                               *
 *******************************************************************************/

/******************************************************************* INCLUDES */
#include <app_cfg.h>
#include <cpu_core.h>
#include <os.h>

#include <bsp.h>
#include <bsp_sys.h>
#include <bsp_int.h>

#include <bsp_gpio.h>
#include <bsp_ccu8.h>
#include <bsp_ccu4.h>

#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

#include <xmc_uart.h>
#include <xmc_gpio.h>

#include <GPIO.h>

#include <lib_math.h>

#include <protocol.h>

#if SEMI_HOSTING
#include <debug_lib.h>
#endif

#if JLINK_RTT
#include <SEGGER_RTT.h>
#include <SEGGER_RTT_Conf.h>
#endif

/******************************************************************** DEFINES */

#define MAX_MSG_LENGTH         8
#define NUM_MSG                32

/********************************************************* FILE LOCAL GLOBALS */
static  OS_TCB   AppTaskStart_TCB;
static  OS_TCB   AppTaskCom_TCB;
static  OS_TCB   AppTaskPwm1_TCB; // Led1

static  CPU_STK  AppTaskStart_Stk  [APP_CFG_TASK_START_STK_SIZE];
static  CPU_STK  AppTaskCom_Stk    [APP_CFG_TASK_COM_STK_SIZE];
static  CPU_STK  AppTaskPwm1_Stk   [APP_CFG_TASK_PWM_STK_SIZE];

// Memory Block
OS_MEM      Mem_Partition;
CPU_CHAR    MyPartitionStorage[NUM_MSG][MAX_MSG_LENGTH]; // +1 to ensure the UART_ISR gets first error at post

// Message Queues
OS_Q        UART_QUEUE;

/************************************************************ FUNCTIONS/TASKS */
static void AppTaskStart (void *p_arg);
static void AppTaskCom   (void *p_arg);
static void AppTaskPwm   (void *p_arg);

/*********************************************************************** MAIN */
/**
 * \function main
 * \params none
 * \returns should never return
 *
 * \brief This is the standard entry point for C code. it Handles:
 *           . interrupts initialisation;
 *           . OS initialisation;
 *           . objects creation: Mem. Partition, Msg. Queue... before OSStart as documented (vide note);
 *           . one only task as documented (vide note);
 *           . OS multitasking initialisation;
 *
 */
int main (void){
    OS_ERR  err;

    // Disable all interrupts
    BSP_IntDisAll();
    // Enable Interrupt UART
    BSP_IntEn (BSP_INT_ID_USIC1_01); //**
    BSP_IntEn (BSP_INT_ID_USIC1_00); //**

    // init SEMI Hosting DEBUG Support
#if SEMI_HOSTING      // 1
    initRetargetSwo();
#endif

    // init JLINK RTT DEBUG Support
#if JLINK_RTT        // 0
    SEGGER_RTT_ConfigDownBuffer (0, NULL, NULL, 0, SEGGER_RTT_MODE_BLOCK_IF_FIFO_FULL);
    SEGGER_RTT_ConfigUpBuffer (0, NULL, NULL, 0, SEGGER_RTT_MODE_BLOCK_IF_FIFO_FULL);
#endif

    // Init uC/OS-III
    OSInit (&err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSInit: main\n");

    // create application objects
    APP_TRACE_INFO ("Creating Application Objects...\n");
    // Create Shared Memory
    OSMemCreate ((OS_MEM    *) &Mem_Partition,
                 (CPU_CHAR  *) "Mem Partition",
                 (void      *) &MyPartitionStorage[0][0],
                 (OS_MEM_QTY ) NUM_MSG,
                 (OS_MEM_SIZE) MAX_MSG_LENGTH * sizeof (CPU_CHAR),
                 (OS_ERR    *) &err);

    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSMemCreate: AppObjCreate\n");

    // Create Message Queue
    OSQCreate ((OS_Q     *) &UART_QUEUE,
               (CPU_CHAR *) "ISR Queue",
               (OS_MSG_QTY) NUM_MSG,
               (OS_ERR   *) &err);

    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSQCreate: AppObjCreate\n");

    /* Create the start task */
    OSTaskCreate ((OS_TCB     *) &AppTaskStart_TCB,
                  (CPU_CHAR   *) "Startup Task",
                  (OS_TASK_PTR ) AppTaskStart,
                  (void       *) 0,
                  (OS_PRIO     ) APP_CFG_TASK_START_PRIO,
                  (CPU_STK    *) &AppTaskStart_Stk[0],
                  (CPU_STK_SIZE) APP_CFG_TASK_START_STK_SIZE / 10u,
                  (CPU_STK_SIZE) APP_CFG_TASK_START_STK_SIZE,
                  (OS_MSG_QTY  ) 0u,
                  (OS_TICK     ) 0u,
                  (void       *) 0,
                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
                  (OS_ERR     *) &err);

    // Start multitasking (i.e., give control to uC/OS-III)
    OSStart (&err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSStart: main\n");

}

/*************************************************************** STARTUP TASK */
/**
 * \function AppTaskStart
 * \params p_arg ... argument passed to AppTaskStart() by
 *                    OSTaskCreate()
 * \returns none
 *
 * \brief Startup (init) task that loads board support functions,
 *        initializes CPU services, the memory, the systick timer,
 *        etc. and finally invokes other application tasks.
 */
static void AppTaskStart (void *p_arg){
    CPU_INT32U  cpu_clk_freq;
    CPU_INT32U  cnts;
    OS_ERR      err;

    const uint8_t type[4] = {1, 2, 3, 4}; // To differentiate tasks

    (void) p_arg;

    BSP_Init();
    CPU_Init();

    cpu_clk_freq = BSP_SysClkFreqGet();
    cnts = cpu_clk_freq / (CPU_INT32U) OSCfg_TickRate_Hz;
    OS_CPU_SysTickInit (cnts);

    Mem_Init();
    Math_Init();

    // compute CPU capacity with no task running
#if (OS_CFG_STAT_TASK_EN > 0u)
    OSStatTaskCPUUsageInit (&err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSStatTaskCPUUsageInit: AppTaskStart\n");
#endif

    APP_TRACE_INFO ("Creating Application Tasks...\n");
    // create AppTaskCom
    OSTaskCreate ((OS_TCB     *) &AppTaskCom_TCB,
                  (CPU_CHAR   *) "TaskCOM",
                  (OS_TASK_PTR ) AppTaskCom,
                  (void       *) 0,
                  (OS_PRIO     ) APP_CFG_TASK_COM_PRIO,
                  (CPU_STK    *) &AppTaskCom_Stk[0],
                  (CPU_STK_SIZE) APP_CFG_TASK_COM_STK_SIZE / 10u,
                  (CPU_STK_SIZE) APP_CFG_TASK_COM_STK_SIZE,
                  (OS_MSG_QTY  ) 0u,
                  (OS_TICK     ) 0u,
                  (void       *) 0,
                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
                  (OS_ERR     *) &err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSTaskCreate: AppTaskCreate : AppTaskCom\n");

    // create AppTaskPwm1
    OSTaskCreate ((OS_TCB     *) &AppTaskPwm1_TCB,
                  (CPU_CHAR   *) "TaskLed1",
                  (OS_TASK_PTR ) AppTaskPwm,
                  (void       *) &type[0],
                  (OS_PRIO     ) APP_CFG_TASK_PWM_PRIO,
                  (CPU_STK    *) &AppTaskPwm1_Stk[0],
                  (CPU_STK_SIZE) APP_CFG_TASK_PWM_STK_SIZE / 10u,
                  (CPU_STK_SIZE) APP_CFG_TASK_PWM_STK_SIZE,
                  (OS_MSG_QTY  ) 5u,
                  (OS_TICK     ) 0u,
                  (void       *) 0,
                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
                  (OS_ERR     *) &err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSTaskCreate: AppTaskCreate : AppTaskPwm1 \n");

    APP_TRACE_DBG ("Deleting AppTaskStart ...\n");
    do {
        OSTaskDel((OS_TCB *)0, &err); // SCHEDULING POINT
        if (err != OS_ERR_NONE)
            APP_TRACE_DBG ("Error OSTaskDel: AppTaskStart\n");
    }while(err != OS_ERR_NONE);

}

/*********************************** Communication Application Task */
/**
 * \function AppTaskCom
 * \ params p_arg ... argument passed to AppTaskCom() by
 *                    AppTaskStart()
 * \returns none
 *
 * \brief It communicates with the UART_ISR (getting the messages comming from
 *        PC) and with the AppTaskPwm Task (to manage the memory used by the packets
 *        structs).
 *        After receiving the msgs from UART_ISR, they're sent to a compliance test
 *        (scrutinise()); according to the msg, this task send messages to the relevant
 *        task queue.
 *
 *        Debug trace mesages are output to the SEGGER J-Link GDB Server.
 *
 *        (1) Debug or Flash the application.
 *        (2) Connect a TTL-USB UART cable:
 *            GND (BLACK) - GND, TX (GREEN) - P0.0, RX (WHITE) - P0.1
 *        (3) Launch a terminal program and connect with 9600-8N1 or launch the GUI or
 *            use the buttons to control the brightness of the leds on board
 */
static void AppTaskCom (void *p_arg){
    void        *p_msg;
    OS_ERR      err, err_;
    OS_MSG_SIZE msg_size;
    CPU_CHAR    msg[MAX_MSG_LENGTH];
    CPU_CHAR    debug_msg[MAX_MSG_LENGTH + 30];

    bool volatile valid;
    COORDINATES volatile packet;
/*    uint8_t volatile actual = 0, actual_;*/

    (void) p_arg; // Just to silence compiler

    // initialise packets: Make them all available to use
/*    for(uint8_t j = 0; j < (NUM_MSG+1); j++)*/
/*        packet[j].isAvailable = true;*/

    APP_TRACE_INFO ("AppTaskCom Loop...\n");
    while (DEF_ON) {
        // empty the message buffer
        memset (&msg, 0, MAX_MSG_LENGTH);

        // Make sure there is always at least one packet of memory available for a eventual message
/*        actual = actual % (NUM_MSG + 1);*/
/*        actual_ = actual;*/
/*        while (!packet[actual].isAvailable){ // #packets > NUM_MSG => this loop should never block*/
/*            actual++;*/
/*            actual = actual % (NUM_MSG + 1);*/
/*            if (actual_ == actual){*/
/*                actual_ = NUM_MSG + 1;*/
/*                break;*/
/*            }*/
/*        }*/

/*        if (actual_ == NUM_MSG +1){ // i.e. there's no packet of memory available*/
/*            APP_TRACE_INFO ("SENDING MSGS TOO FAST\n"); // NEVER HAPPENED DURING TESTS =) but who knows?!*/
/*            continue;*/
/*        }*/

        // Check if there is message
        p_msg = OSQPend (&UART_QUEUE,
                         0,
                         OS_OPT_PEND_BLOCKING,
                         &msg_size,
                         (CPU_TS *)0,
                         &err_);
        if (err_ != OS_ERR_NONE)
            APP_TRACE_DBG ("Error OSQPend: AppTaskCom\n");

        APP_TRACE_INFO ("======================= AppTaskCom\n");
        // obtain message we received
        memcpy (msg, (CPU_CHAR*) p_msg, msg_size - 1);

        // release the memory partition allocated in the UART service routine
        APP_TRACE_DBG ("Putting Memory Partition back\n");
        OSMemPut (&Mem_Partition, p_msg, &err);
        if (err != OS_ERR_NONE)
            APP_TRACE_DBG ("Error OSMemPut: AppTaskCom\n");

        // print the received message to the debug interface
        sprintf (debug_msg, "MSG: %s\tLENGTH: %d\n", msg, msg_size - 1);
        APP_TRACE_INFO (debug_msg);

        // scrutinise received msg for compliance with protocol
        APP_TRACE_INFO ("Calling scrutinise() ...\n");
        valid = scrutinise(msg, &packet);
        if (!valid){
             APP_TRACE_INFO ("NO COMPLIANCE\n");
            // send NACK in return
            SendNack();
            continue;
        }

        // Distribute commands to tasks
/*        packet[actual].isAvailable = false;*/
/*        switch (packet[actual].port){*/
/*            case '1':       // P1.1 -> AKA LED1*/
/*                OSTaskQPost((OS_TCB    *) &AppTaskPwm1_TCB,*/
/*                            (void      *) &packet[actual],*/
/*                            (OS_MSG_SIZE) sizeof(packet[actual]),*/
/*                            (OS_OPT     ) OS_OPT_POST_FIFO,*/
/*                            (OS_ERR    *) &err);*/
/*                if (err != OS_ERR_NONE){*/
/*                    APP_TRACE_DBG ("Error OSTaskQPost: AppTaskPwm1\n");*/
/*                    packet[actual].isAvailable = true;*/
/*                    SendNack();*/
/*                }else{*/
/*                   actual++;*/
/*                   SendAck();*/
/*                }*/
/*                break;*/
/*            case '2':       // P1.0 -> AKA LED2*/
/*                OSTaskQPost((OS_TCB    *) &AppTaskPwm2_TCB,*/
/*                            (void      *) &packet[actual],*/
/*                            (OS_MSG_SIZE) sizeof(packet[actual]),*/
/*                            (OS_OPT     ) OS_OPT_POST_FIFO,*/
/*                            (OS_ERR    *) &err);*/
/*                if (err != OS_ERR_NONE){*/
/*                    APP_TRACE_DBG ("Error OSTaskQPost: AppTaskPwm2\n");*/
/*                    packet[actual].isAvailable = true;*/
/*                    SendNack();*/
/*                }else{*/
/*                   actual++;*/
/*                   SendAck();*/
/*                }*/
/*                break;*/
/*            case '3':       // P5.1*/
/*                OSTaskQPost((OS_TCB    *) &AppTaskPwm3_TCB,*/
/*                            (void      *) &packet[actual],*/
/*                            (OS_MSG_SIZE) sizeof(packet[actual]),*/
/*                            (OS_OPT     ) OS_OPT_POST_FIFO,*/
/*                            (OS_ERR    *) &err);*/
/*                if (err != OS_ERR_NONE){*/
/*                    APP_TRACE_DBG ("Error OSTaskQPost: AppTaskPwm3\n");*/
/*                    packet[actual].isAvailable = true;*/
/*                    SendNack();*/
/*                }else{*/
/*                   actual++;*/
/*                   SendAck();*/
/*                }*/
/*                break;*/
/*            case '4':       // P5.7*/
/*                OSTaskQPost((OS_TCB    *) &AppTaskPwm4_TCB,*/
/*                            (void      *) &packet[actual],*/
/*                            (OS_MSG_SIZE) sizeof(packet[actual]),*/
/*                            (OS_OPT     ) OS_OPT_POST_FIFO,*/
/*                            (OS_ERR    *) &err);*/
/*                if (err != OS_ERR_NONE){*/
/*                    APP_TRACE_DBG ("Error OSTaskQPost: AppTaskPwm4\n");*/
/*                    packet[actual].isAvailable = true;*/
/*                    SendNack();*/
/*                }else{*/
/*                   actual++;*/
/*                   SendAck();*/
/*                }*/
/*                break;*/
/*            default:*/
/*                SendNack();*/
/*        }*/

        APP_TRACE_INFO ("=======================\n");
    }
}

/***************************************************** LED Application Task */
/**
 * \function AppTaskPwm
 * \ params p_arg ... argument passed to AppTaskPwm() at creation
 * \returns none
 *
 * \brief It waits until a message arrives in its queue.
 *        After receiving something, it will adjust the duty cycle of the output
 *        in the respective pin.
 */

static void AppTaskPwm (void *p_arg){}
/*    OS_ERR      err;*/
/*    uint16_t volatile compare;*/
/*    UART_PACKET volatile *packet;*/
/*    OS_MSG_SIZE msg_size;*/
/*    const uint8_t *pwm_pin = (uint8_t *) p_arg;*/

/*    APP_TRACE_INFO ("AppTaskPwm Loop...\n");*/
/*    while (DEF_ON){*/
/*        packet = (UART_PACKET volatile *)OSTaskQPend (0,*/
/*                                                      OS_OPT_PEND_BLOCKING,*/
/*                                                      &msg_size,*/
/*                                                      NULL,*/
/*                                                      &err);*/
/*        if (err != OS_ERR_NONE && err != OS_ERR_TIMEOUT)*/
/*            APP_TRACE_DBG ("Error OSTaskQPend: AppTaskPwm\n");*/
/*       */
/*        // Configure different Tasks for the same code*/
/*        APP_TRACE_INFO ("===============================================================\n");*/
/*        switch (*pwm_pin){*/
/*            case 1:       // P1.1 -> AKA LED1*/
/*                compare = (uint16_t)((100 - packet->duty) * 11.71);*/
/*                XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, compare);*/
/*                XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);*/
/*                break;*/
/*            case 2:       // P1.0 -> AKA LED2*/
/*                compare = (uint16_t)((100 - packet->duty) * 11.71);*/
/*                XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_D, compare);*/
/*                XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_D);*/
/*                break;*/
/*            case 3:       // P5.1*/
/*                compare = (uint16_t)((100 - packet->duty) * 24);*/
/*                XMC_CCU8_SLICE_SetTimerCompareMatch(SLICE_CCU8_A, XMC_CCU8_SLICE_COMPARE_CHANNEL_2, compare);*/
/*                XMC_CCU8_EnableShadowTransfer(MODULE_CCU8, SLICE_TRANSFER_A);*/
/*                break;*/
/*            case 4:       // P5.7*/
/*                compare = (uint16_t)((100 - packet->duty) * 24);*/
/*                XMC_CCU8_SLICE_SetTimerCompareMatch(SLICE_CCU8_B, XMC_CCU8_SLICE_COMPARE_CHANNEL_2, compare);*/
/*                XMC_CCU8_EnableShadowTransfer(MODULE_CCU8, SLICE_TRANSFER_B);*/
/*                break;*/
/*            default:*/
/*                    APP_TRACE_DBG ("eu aqui\n");*/
/*                SendNack();*/
/*        }*/

/*        packet->isAvailable = true;*/
/*    }*/
/*}*/
/************************************************************************ EOF */
