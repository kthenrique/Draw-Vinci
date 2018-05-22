/*
 * @file bsp_gpio.c
 *
 * @date: 05-2018
 * @author: Kelve T. Henrique
 * \brief Configures LEDs and Buttons
 */

#include <bsp_gpio.h>

_Bool BSP_GPIO_Init (void){

    // Initialise Pen Motor
    P1_3_set_mode(OUTPUT_PP_AF3);
    P1_3_set_driver_strength(STRONG);
    P1_3_reset();

    return true;
}

/*! EOF */
