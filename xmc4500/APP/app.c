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
#include <bsp_spi.h>

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
//#define BUG_IT

#define MAX_MSG_LENGTH         40
#define NUM_MSG                32

#define Y_AXIS_POS 0x03
#define Y_AXIS_NEG 0x02
#define X_AXIS_POS 0x0C
#define X_AXIS_NEG 0x08
#define DONT_MOVE 0

#define PEN_DOWN  (uint16_t)((7.5) * PERIOD_CCU40/100)
#define PEN_UP    (uint16_t)((5) * PERIOD_CCU40/100)

#define SLEEP_COUNTER 0xffff

/********************************************************* FILE LOCAL GLOBALS */
static  OS_TCB   AppTaskStart_TCB;
static  OS_TCB   AppTaskCom_TCB;
static  OS_TCB   AppTaskPlot_TCB;

static  CPU_STK  AppTaskStart_Stk  [APP_CFG_TASK_START_STK_SIZE];
static  CPU_STK  AppTaskCom_Stk    [APP_CFG_TASK_COM_STK_SIZE];
static  CPU_STK  AppTaskPlot_Stk   [APP_CFG_TASK_PLOT_STK_SIZE];

// Memory Block
OS_MEM      Mem_Partition;
CPU_CHAR    MyPartitionStorage[NUM_MSG][MAX_MSG_LENGTH]; // +1 to ensure the UART_ISR gets first error at post

// Message Queues
OS_Q        UART_QUEUE;

/************************************************************ FUNCTIONS/TASKS */
static void AppTaskStart    (void *p_arg);
static void AppTaskCom      (void *p_arg);
static void AppTaskPlot     (void *p_arg);

void init_plotter(uint16_t *dimension){
    volatile uint16_t counter = SLEEP_COUNTER;
    CPU_CHAR    debug_msg[MAX_MSG_LENGTH + 90];

    // delay to raise the pen
    while(ENDLEFT != 0 && ENDTOP != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,(Y_AXIS_NEG | X_AXIS_NEG),MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);
    }
    while(ENDTOP != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,Y_AXIS_NEG,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);
    }
    while(ENDLEFT != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,X_AXIS_NEG,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);
    }
    while(ENDBOTTOM != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,Y_AXIS_POS,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        dimension[0]++;
#ifdef BUG_IT
sprintf (debug_msg, "dimension: (%d, %d)\n", dimension[0], dimension[1]);
APP_TRACE_INFO (debug_msg);
#endif
    }
    while(ENDRIGHT != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,X_AXIS_POS,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        dimension[1]++;
#ifdef BUG_IT
sprintf (debug_msg, "dimension: (%d, %d)\n", dimension[0], dimension[1]);
APP_TRACE_INFO (debug_msg);
#endif
    }
    while(ENDLEFT != 0 && ENDTOP != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,(Y_AXIS_NEG | X_AXIS_NEG),MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);
    }
    while(ENDTOP != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,Y_AXIS_NEG,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);
    }
    while(ENDLEFT != 0){
        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,X_AXIS_NEG,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);

        while(--counter);
        counter = SLEEP_COUNTER;

        _mcp23s08_reset_ss(MCP23S08_SS);
        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
        _mcp23s08_set_ss(MCP23S08_SS);
    }
}
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
                  (OS_MSG_QTY  ) NUM_MSG,
                  (OS_TICK     ) 0u,
                  (void       *) 0,
                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
                  (OS_ERR     *) &err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSTaskCreate: AppTaskCreate : AppTaskCom\n");

    // create AppTaskPlot
    OSTaskCreate ((OS_TCB     *) &AppTaskPlot_TCB,
                  (CPU_CHAR   *) "TaskPlot",
                  (OS_TASK_PTR ) AppTaskPlot,
                  (void       *) 0,
                  (OS_PRIO     ) APP_CFG_TASK_PLOT_PRIO,
                  (CPU_STK    *) &AppTaskPlot_Stk[0],
                  (CPU_STK_SIZE) APP_CFG_TASK_PLOT_STK_SIZE / 10u,
                  (CPU_STK_SIZE) APP_CFG_TASK_PLOT_STK_SIZE,
                  (OS_MSG_QTY  ) NUM_MSG,
                  (OS_TICK     ) 0u,
                  (void       *) 0,
                  (OS_OPT      ) (OS_OPT_TASK_STK_CHK | OS_OPT_TASK_STK_CLR),
                  (OS_ERR     *) &err);
    if (err != OS_ERR_NONE)
        APP_TRACE_DBG ("Error OSTaskCreate: AppTaskCreate : AppTaskManMode \n");

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
    CPU_CHAR    debug_msg[MAX_MSG_LENGTH + 50];

    bool volatile valid;
    CODE volatile packet[NUM_MSG];
    uint8_t volatile current = 0;

    for(uint8_t j = 0; j < NUM_MSG; j++){
        packet[j].isFree = true;
        packet[j].x_axis = 0;
        packet[j].y_axis = 0;
    }
    (void) p_arg; // Just to silence compiler
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
        valid = scrutinise(msg, &packet[current]);
        if (!valid){
             APP_TRACE_INFO ("NO COMPLIANCE\n");
            // send NACK in return
            SendNack();
            continue;
        }

        OSTaskQPost((OS_TCB    *) &AppTaskPlot_TCB,
                (void      *) &packet[current],
                (OS_MSG_SIZE) sizeof(packet[current]),
                (OS_OPT     ) OS_OPT_POST_FIFO,
                (OS_ERR    *) &err);
        if (err != OS_ERR_NONE){
            APP_TRACE_DBG("ERROR OSTaskQPost: AppTaskPlot\n");
            if (err == OS_ERR_Q_MAX)
                APP_TRACE_DBG("OS_ERR_Q_MAX");
            if (err == OS_ERR_MSG_POOL_EMPTY)
                APP_TRACE_DBG("OS_ERR_MSG_POOL_EMPTY");
            continue;
        }
        // here the packets should be set to false
        // and reset
        while(!packet[current].isFree){
            current++;
            current %= NUM_MSG;
            packet[current].x_axis = 0;
            packet[current].y_axis = 0;
            packet[current].z_axis = 2;
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

static void AppTaskPlot(void *p_arg){
    OS_ERR      err;
    OS_MSG_SIZE msg_size;
    CODE volatile *packet;
    bool volatile isRelative = false, penUp = true;
    int16_t step_x, dir_x, step_y, dir_y, center[2];
    uint16_t dimension[2] = {0x0, 0x0};
    int error = 0, error_ = 0;
    int8_t s_x, s_y, quadrant = 1;
    int current_position[2] = {0x0, 0x0};
    int next_position[2]    = {0x0, 0x0};
    int end_position[2]     = {0x0, 0x0};
    volatile uint16_t counter = 0xfff;

#ifdef BUG_IT
CPU_CHAR    debug_msg[MAX_MSG_LENGTH + 90];
#endif

    // raise the pen
    XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, PEN_UP);
    XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);
    penUp = true;
    OSTimeDlyHMSM(0, 0, 0, 150, OS_OPT_TIME_HMSM_STRICT, &err);

//    init_plotter(dimension);

#ifdef BUG_IT
sprintf (debug_msg, "DIMENSION: (%d, %d)\n", dimension[0], dimension[1]);
APP_TRACE_INFO (debug_msg);
#endif

    APP_TRACE_INFO ("AppTaskManMode Loop...\n");
    while (DEF_ON){
        packet = (CODE volatile *)OSTaskQPend (0,
                OS_OPT_PEND_BLOCKING,
                &msg_size,
                NULL,
                &err);
        if (err != OS_ERR_NONE)
            APP_TRACE_DBG ("Error OSTaskQPend: AppTaskManMode\n");

        APP_TRACE_INFO ("*********************** AppTaskPlot\n");
        switch(packet->cmd){
            case 1:                             // G01
                APP_TRACE_DBG ("G01\n");
                // PEN UP X PEN DOWN
                if(packet->z_axis == 1 && penUp){
                    APP_TRACE_DBG ("Pen down\n");
                    XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, PEN_DOWN);
                    XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);
                    penUp = false;
                    // delay to lower the pen
                    //OSTimeDlyHMSM(0, 0, 0, 650, OS_OPT_TIME_HMSM_STRICT, &err);
                }
                if(packet->z_axis == 0 && !penUp){
                    APP_TRACE_DBG ("Pen up\n");
                    XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, PEN_UP);
                    XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);
                    penUp = true;
                    // delay to raise the pen
                    //OSTimeDlyHMSM(0, 0, 0, 650, OS_OPT_TIME_HMSM_STRICT, &err);
                }

                // MOVE PLOTTER HORIZONTALLY
                // beginning position
                next_position[0] = current_position[0];
                next_position[1] = current_position[1];
                // End position
                end_position[0] = current_position[0] + packet->x_axis;
                end_position[1] = current_position[1] + packet->y_axis;
                if(!isRelative){                        // ABSOLUTE
                    APP_TRACE_DBG ("Absolute Positioning\n");
                    end_position[0] = packet->x_axis;
                    end_position[1] = packet->y_axis;
                    // X_AXIS
                    packet->x_axis -= current_position[0];
                    // Y_AXIS
                    packet->y_axis -= current_position[1];

                }
                // X_AXIS
                if (packet->x_axis < 0){dir_x = X_AXIS_NEG; s_x = -1;}
                if (packet->x_axis > 0){dir_x = X_AXIS_POS; s_x = 1;}
                step_x = abs(packet->x_axis);
                // Y_AXIS
                if (packet->y_axis < 0){dir_y = Y_AXIS_NEG; s_y = -1;}
                if (packet->y_axis > 0){dir_y = Y_AXIS_POS; s_y = 1;}
                step_y = -abs(packet->y_axis);
                error = step_x + step_y;

                // MOVE!
                while(1){
                    APP_TRACE_DBG ("moving G01\n");
                    while(current_position[0] != next_position[0]){
                        APP_TRACE_DBG ("moving G01: x axis\n");
                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,dir_x,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        while(--counter);
                        counter = 0xff;

                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        current_position[0] += s_x;
                    }
                    while(current_position[1] != next_position[1]){
                        APP_TRACE_DBG ("moving G01: y axis\n");
                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,dir_y,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        while(--counter);
                        counter = 0xff;

                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        current_position[1] += s_y;
                    }

                    if(current_position[0] == end_position[0] && current_position[1] == end_position[1]) break;
                    error_ = 2 * error;
                    if(error_ >= step_y){ error += step_y; next_position[0] += s_x;}
                    if(error_ <= step_x){ error += step_x; next_position[1] += s_y;}
                }

                step_x         = 0;
                step_y         = 0;
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
                // raise the pen
                XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, PEN_UP);
                XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);
                packet->z_axis = 0;
                penUp = true;
                // delay to raise the pen
                OSTimeDlyHMSM(0, 0, 0, 100, OS_OPT_TIME_HMSM_STRICT, &err);
                while(ENDLEFT != 0 && ENDTOP != 0){
                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,(Y_AXIS_NEG | X_AXIS_NEG),MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);

                    while(--counter);
                    counter = 0xff;

                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);
                }
                while(ENDTOP != 0){
                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,Y_AXIS_NEG,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);

                    while(--counter);
                    counter = 0xff;

                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);
                }
                while(ENDLEFT != 0){
                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,X_AXIS_NEG,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);

                    while(--counter);
                    counter = 0xff;

                    _mcp23s08_reset_ss(MCP23S08_SS);
                    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                    _mcp23s08_set_ss(MCP23S08_SS);
                }
                current_position[0] = 0;
                current_position[1] = 0;
                break;
            case 5:                             // G02
                APP_TRACE_DBG ("G02\n");
                // beginning position
                next_position[0] = current_position[0];
                next_position[1] = current_position[1];
                // End position
                end_position[0] += packet->x_axis;
                end_position[1] += packet->y_axis;
                if(!isRelative){                        // ABSOLUTE
                    APP_TRACE_DBG ("Absolute Positioning\n");
                    end_position[0] = packet->x_axis;
                    end_position[1] = packet->y_axis;
                }

                // can we use sqrt() from math lib?
                //s_x = -sqrt((abs(packet->i_offset) + abs(packet->j_offset)));
                error_ = abs(packet->i_offset); // this is radius
                step_x = -error_;
                step_y = 0;
                error = 2-2*error_;
                // Circle center
                center[0] = current_position[0]+packet->i_offset;
                center[1] = current_position[1]+packet->j_offset;

                // Begin with first quadrant
                quadrant = 1;

                // MOVE!
                do{
                    APP_TRACE_DBG ("moving G02\n");
                    switch(quadrant){
                        case 1:
                            next_position[0] = center[0] - step_x;
                            next_position[1] = center[1] + step_y;
                            s_x = -1;
                            s_y = 1;
                            break;
                        case 2:
                            next_position[0] = center[0] - step_y;
                            next_position[1] = center[1] - step_x;
                            s_x = -1;
                            s_y = -1;
                            break;
                        case 3:
                            next_position[0] = center[0] + step_x;
                            next_position[1] = center[1] - step_y;
                            s_x = 1;
                            s_y = -1;
                            break;
                        case 4:
                            next_position[0] = center[0] + step_y;
                            next_position[1] = center[1] + step_x;
                            s_x = 1;
                            s_y = 1;
                            break;
                    }
                    if (s_x < 0) dir_x = X_AXIS_NEG;
                    else         dir_x = X_AXIS_POS;
                    if (s_y < 0) dir_y = Y_AXIS_NEG;
                    else         dir_y = Y_AXIS_POS;
                    while(current_position[0] != next_position[0]){
                        APP_TRACE_DBG ("moving G02: x axis\n");
                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,dir_x,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        while(--counter);
                        counter = 0xff;

                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        current_position[0] += s_x;
                    }
                    while(current_position[1] != next_position[1]){
                        APP_TRACE_DBG ("moving G02: y axis\n");
                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,dir_y,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        while(--counter);
                        counter = 0xff;

                        _mcp23s08_reset_ss(MCP23S08_SS);
                        _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_GPIO,0x00,MCP23S08_WR);
                        _mcp23s08_set_ss(MCP23S08_SS);

                        current_position[1] += s_y;
                    }

                    error_ = error;
                    if(error_ <= step_y) error += ++step_y*2+1;
                    if(error_ > step_x || error > step_y) error += ++step_x*2+1;

                    if (step_x >= 0){
                        error_ = abs(packet->i_offset); // this is radius
                        step_x = -error_;
                        step_y = 0;
                        error = 2-2*error_;
                        quadrant ++;
                    }
                } while(quadrant < 5);

                step_x    = 0;
                step_y    = 0;
                break;
        }

        if(!isRelative){
            packet->x_axis = current_position[0];
            packet->y_axis = current_position[1];
        } else{
            packet->x_axis = 0;
            packet->y_axis = 0;
        }
        step_x         = 0;
        step_y         = 0;

        packet->isFree = true;
        APP_TRACE_INFO ("********************************\n");
    }
}

/************************************************************************ EOF */
