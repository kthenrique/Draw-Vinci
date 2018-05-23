/*
 * @file bsp_gpio.h
 *
 * @date 05-2018
 * @author: Kelve T. Henrique
 */

#ifndef SRC_BSP_BSP_GPIO_H_
#define SRC_BSP_BSP_GPIO_H_

#include <xmc_gpio.h>
#include <GPIO.h>

#define TICKS_PER_SECOND 1000
#define TICKS_WAIT 500

#define ENDRIGHT  P1_12_read()
#define ENDLEFT   P1_14_read()
#define ENDBOTTOM P1_13_read()
#define ENDTOP    P1_15_read()

_Bool BSP_GPIO_Init (void) ;

#endif
