/*******************************************************************************
 * @file bsp.c                                                                 *
 * @brief Main board support package for uCOS-III targeting the RelaxKit board.*
 *                                                                             *
 * @author Martin Horauer, UAS Technikum Wien                                  *
 *         Modified by: Kelve T. Henrique                                      *
 * @revision 0.1                                                               *
 * @date 05-2018                                                               *
 *******************************************************************************/

/******************************************************************* INCLUDES */
#include  <bsp.h>
#include  <bsp_sys.h>
#include  <bsp_int.h>

#include  <bsp_uart.h>
#include  <bsp_gpio.h>
#include  <bsp_ccu4.h>
#include  <bsp_spi.h>

/********************************************************* FILE LOCAL DEFINES */

/******************************************************* FILE LOCAL CONSTANTS */

/*********************************************************** FILE LOCAL TYPES */

/********************************************************* FILE LOCAL GLOBALS */

/****************************************************** FILE LOCAL PROTOTYPES */

/****************************************************************** FUNCTIONS */
/**
 * @function BSP_Init()
 * @params none
 * @returns none
 * @brief Initialization of the board support.
 */
void  BSP_Init (void)
{
	BSP_IntInit();
	BSP_UART_Init();
	BSP_GPIO_Init();
	BSP_CCU4_Init();
    BSP_SPI_Init();
}
/** EOF */
