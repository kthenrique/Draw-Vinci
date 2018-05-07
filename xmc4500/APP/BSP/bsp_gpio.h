/*
 * @file bsp_gpio.h
 *
 * @date 03-2018
 * @author: Kelve T. Henrique
 */

#ifndef SRC_BSP_BSP_GPIO_H_
#define SRC_BSP_BSP_GPIO_H_

#include <xmc_gpio.h>
#include <GPIO.h>

#define TICKS_PER_SECOND 1000
#define TICKS_WAIT 500

#define LED1 P1_1
#define LED2 P1_0

#define BUTTON1 P1_14
#define BUTTON2 P1_15

_Bool BSP_GPIO_Init (void) ;

#endif
