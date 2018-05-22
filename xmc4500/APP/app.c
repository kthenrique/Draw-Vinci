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

#include "xmc4500_spi_lib.h"
#include "mcp23s08_drv.h"

#if SEMI_HOSTING
#include <debug_lib.h>
#endif

#if JLINK_RTT
#include <SEGGER_RTT.h>
#include <SEGGER_RTT_Conf.h>
#endif

/******************************************************************** DEFINES */

#define MAX_MSG_LENGTH         12
#define NUM_MSG                32

#define ENDPOINT_1      113
#define ENDPOINT_2      49
#define ENDPOINT_3      81
#define ENDPOINT_4      97

#define X_AXIS_POS 0x03
#define X_AXIS_NEG 0x02
#define Y_AXIS_POS 0x0C
#define Y_AXIS_NEG 0x08
/********************************************************* FILE LOCAL GLOBALS */
static  OS_TCB   AppTaskStart_TCB;
static  OS_TCB   AppTaskCom_TCB;
static  OS_TCB   AppTaskManMode_TCB;
static  OS_TCB   AppTaskAutoMode_TCB;
static  OS_TCB   AppTaskEndpoints_TCB;

static  CPU_STK  AppTaskStart_Stk  [APP_CFG_TASK_START_STK_SIZE];
static  CPU_STK  AppTaskCom_Stk    [APP_CFG_TASK_COM_STK_SIZE];
static  CPU_STK  AppTaskManMode_Stk[APP_CFG_TASK_MAN_MODE_STK_SIZE];
static  CPU_STK  AppTaskAutoMode_Stk[APP_CFG_TASK_AUTO_MODE_STK_SIZE];
static  CPU_STK  AppTaskEndpoints_Stk[APP_CFG_TASK_ENDPOINTS_STK_SIZE];
// Memory Block
OS_MEM      Mem_Partition;
CPU_CHAR    MyPartitionStorage[NUM_MSG][MAX_MSG_LENGTH]; // +1 to ensure the UART_ISR gets first error at post

// Message Queues
OS_Q        UART_QUEUE;

/************************************************************ FUNCTIONS/TASKS */
static void AppTaskStart    (void *p_arg);
static void AppTaskCom      (void *p_arg);
static void AppTaskManMode  (void *p_arg);
static void AppTaskEndpoints(void *p_arg);
static void AppTaskAutoMode (void *p_arg);
static void initspi(void);
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

    //const uint8_t type[4] = {1, 2, 3, 4}; // To differentiate tasks

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

    // create AppTaskManMode
    OSTaskCreate ((OS_TCB     *) &AppTaskManMode_TCB,
                  (CPU_CHAR   *) "TaskManualMode",
                  (OS_TASK_PTR ) AppTaskManMode,
                  (void       *) 0,
                  (OS_PRIO     ) APP_CFG_TASK_MAN_MODE_PRIO,
                  (CPU_STK    *) &AppTaskManMode_Stk[0],
                  (CPU_STK_SIZE) APP_CFG_TASK_MAN_MODE_STK_SIZE / 10u,
                  (CPU_STK_SIZE) APP_CFG_TASK_MAN_MODE_STK_SIZE,
                  (OS_MSG_QTY  ) 5u,
                  (OS_TICK     ) 0u,
                  (void       *) 0,
                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
                  (OS_ERR     *) &err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSTaskCreate: AppTaskCreate : AppTaskManMode \n");

//    OSTaskCreate ((OS_TCB     *) &AppTaskEndpoints_TCB,
//                  (CPU_CHAR   *) "TaskEndpoints",
//                  (OS_TASK_PTR ) AppTaskEndpoints,
//                  (void       *) 0,
//                  (OS_PRIO     ) APP_CFG_TASK_ENDPOINTS_PRIO,
//                  (CPU_STK    *) &AppTaskEndpoints_Stk[0],
//                  (CPU_STK_SIZE) APP_CFG_TASK_ENDPOINTS_STK_SIZE / 10u,
//                  (CPU_STK_SIZE) APP_CFG_TASK_ENDPOINTS_STK_SIZE,
//                  (OS_MSG_QTY  ) 0u,
//                  (OS_TICK     ) 0u,
//                  (void       *) 0,
//                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
//                  (OS_ERR     *) &err);
//    if (err != OS_ERR_NONE)
//        APP_TRACE_DBG ("Error OSTaskCreate: AppTaskCreate : AppTaskCom\n");
    
    APP_TRACE_DBG ("Deleting AppTaskStart ...\n");
    do {
        OSTaskDel((OS_TCB *)0, &err); // SCHEDULING POINT
        if (err != OS_ERR_NONE)
            APP_TRACE_DBG ("Error OSTaskDel: AppTaskStart\n");
    }while(err != OS_ERR_NONE);

}
/*********************************** SPI Initialization --> MAYBE WE SHOULD MAKE IT AN BSP FILE FOR THAT?!?*/ 
static void initspi(void)
{
    if(_init_spi() != SPI_OK)
        APP_TRACE_DBG("Error Initialising SPI\n");

    _mcp23s08_reset();

    _mcp23s08_reset_ss(MCP23S08_SS);
    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_IODIR,0x00,MCP23S08_WR);
    _mcp23s08_set_ss(MCP23S08_SS);
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
    CODE volatile packet;

    (void) p_arg; // Just to silence compiler

    //init the spi interface
    initspi();

    APP_TRACE_INFO ("AppTaskCom Loop...\n");
    while (DEF_ON) {
        // empty the message buffer
        memset (&msg, 0, MAX_MSG_LENGTH);

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

        OSTaskQPost((OS_TCB    *) &AppTaskManMode_TCB,
                (void      *) &packet,
                (OS_MSG_SIZE) sizeof(packet),
                (OS_OPT     ) OS_OPT_POST_FIFO,
                (OS_ERR    *) &err);
        if (err != OS_ERR_NONE){
            APP_TRACE_DBG ("Error OSTaskQPost: AppTaskPwm1\n");
        }

        APP_TRACE_INFO ("=======================\n");
    }
}

/************************************************************************************/
/**
 * \function AppTaskManMode
 * \ params p_arg ... argument passed to AppTaskManMode() at creation
 * \returns none
 *
 * \brief It waits until a message arrives in its queue.
 *        After receiving something, it will adjust the duty cycle of the output
 *        in the respective pin.
 */

static void AppTaskManMode (void *p_arg){
    OS_ERR      err;
    OS_MSG_SIZE msg_size;
    CODE volatile *packet;
    bool volatile isRelative = false, penUp = true;
    uint16_t count_x, step_x, dir_x, count_y, step_y, dir_y;
    uint16_t pos[2] = {0xd00, 0xd00};
    uint16_t volatile compare;
    volatile uint16_t counter = 0xfff;

    APP_TRACE_INFO ("AppTaskManMode Loop...\n");
    while (DEF_ON){
        packet = (CODE volatile *)OSTaskQPend (0,
                OS_OPT_PEND_BLOCKING,
                &msg_size,
                NULL,
                &err);
        if (err != OS_ERR_NONE)
            APP_TRACE_DBG ("Error OSTaskQPend: AppTaskManMode\n");

        switch(packet->cmd){
            case 0:                             // G00 
                APP_TRACE_DBG ("G00\n");
                break;
            case 1:                             // G01
                APP_TRACE_DBG ("G01\n");
                // PEN UP X PEN DOWN
                if(packet->z_axis == 1 && penUp){
                    APP_TRACE_DBG ("Pen down\n");
                    compare = (uint16_t)((100 - 10) * 93.74);
                    XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, compare);
                    XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);
                    packet->z_axis = 2;
                }
                if(packet->z_axis == 0 && !penUp){
                    APP_TRACE_DBG ("Pen up\n");
                    compare = (uint16_t)((100 - 5) * 93.74);
                    XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, compare);
                    XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);
                    packet->z_axis = 2;
                }
                // MOVE PLOTTER HORIZONTALLY
                APP_TRACE_DBG ("Default\n");
                if(!isRelative){                        // ABSOLUTE
                    // X_AXIS
                    packet->x_axis -= pos[0];
                    // Y_AXIS
                    packet->y_axis -= pos[1];
                }
                // X_AXIS
                if (packet->x_axis < 0) dir_x = X_AXIS_NEG;
                if (packet->x_axis > 0) dir_x = X_AXIS_POS;
                step_x = abs(packet->x_axis);
                // Y_AXIS
                if (packet->y_axis < 0) dir_y = Y_AXIS_NEG;
                if (packet->y_axis > 0) dir_y = Y_AXIS_POS;
                step_y = abs(packet->y_axis);
                // MOVE!
                for(count_x = 0, count_y = 0; count_x < step_x || count_y < step_y; count_x++, count_y++){
                    _mcp23s08_reset_ss(MCP23S08_SS);
                    if(count_x < step_x) _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,dir_x,MCP23S08_WR);
                    if(count_y < step_y) _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,dir_y,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);

                    while(--counter);
                    counter = 0xfff;

                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);
                }
                packet->x_axis = 0;
                packet->y_axis = 0;
                break;
            case 2:                             // G90
                APP_TRACE_DBG ("G90\n");
                isRelative = false;
                break;
            case 3:                             // G91
                APP_TRACE_DBG ("G91\n");
                isRelative = true;
                break;
            case 4:                             // G28
                APP_TRACE_DBG ("G28\n");
                while(P1_15_read() != 0x8000UL || P1_14_read() != 0x4000UL){ // while not on bottom-left
                    _mcp23s08_reset_ss(MCP23S08_SS);
                    if(P1_15_read() != 0x8000UL) _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,X_AXIS_NEG,MCP23S08_WR);
                    if(P1_14_read() != 0x4000UL) _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,Y_AXIS_NEG,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);

                    while(--counter);
                    counter = 0xfff;

                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);
                }
                pos[0] = 0;
                pos[1] = 0;
                break;
            case 5:                             // G02
                APP_TRACE_DBG ("G02\n");
                break;
                //default:
        }
    }
}


//    _mcp23s08_reset();
//    
///*    _mcp23s08_reset_ss(MCP23S08_SS);*/
///*    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_IODIR,0x01,MCP23S08_WR);*/
///*    _mcp23s08_set_ss(MCP23S08_SS);*/
//    
//    APP_TRACE_INFO ("AppTaskEndpoints Loop...\n");
//    while(DEF_ON){
//        _mcp23s08_reset_ss(MCP23S08_SS);
//        reg_val = _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0,MCP23S08_RD);
//        _mcp23s08_set_ss(MCP23S08_SS);
//
//        if(reg_val == ENDPOINT_1)
//        {
//            XMC_GPIO_SetOutputHigh(D5);
//            XMC_GPIO_SetOutputLow(D6);
//            XMC_GPIO_SetOutputHigh(D7);
//            XMC_GPIO_SetOutputHigh(D8);
//        }
//        if(reg_val == ENDPOINT_2)
//        {
//            XMC_GPIO_SetOutputLow(D5);
//            XMC_GPIO_SetOutputHigh(D6);
//            XMC_GPIO_SetOutputHigh(D7);
//            XMC_GPIO_SetOutputHigh(D8);
//        }
//        if(reg_val == ENDPOINT_3)
//        {
//            XMC_GPIO_SetOutputHigh(D5);
//            XMC_GPIO_SetOutputHigh(D6);
//            XMC_GPIO_SetOutputLow(D7);
//            XMC_GPIO_SetOutputHigh(D8);
//        }
//        if(reg_val == ENDPOINT_4)
//        {
//            XMC_GPIO_SetOutputHigh(D5);
//            XMC_GPIO_SetOutputHigh(D6);
//            XMC_GPIO_SetOutputHigh(D7);
//            XMC_GPIO_SetOutputLow(D8);
//        }

/************************************************************************ EOF */
