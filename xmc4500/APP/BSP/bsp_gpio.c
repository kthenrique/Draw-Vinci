/*
 * @file bsp_gpio.c
 *
 * @date: 05-2018
 * @author: Kelve T. Henrique
 * \brief Configures LEDs and Buttons
 */

#include <bsp_gpio.h>

_Bool BSP_GPIO_Init(void){

    // Initialise Pen Motor Pin
    P1_3_set_mode(OUTPUT_PP_AF3);
    P1_3_set_driver_strength(STRONG);
    P1_3_reset();

    // Initialise Endstop Pins
    // Endstop left
    P1_15_set_mode(OUTPUT_PP_AF3);
    P1_15_set_driver_strength(MEDIUM);
    P1_15_reset();

    // Endstop right
    P1_13_set_mode(OUTPUT_PP_AF3);
    P1_13_set_driver_strength(MEDIUM);
    P1_13_reset();

    // Endstop top
    P1_14_set_mode(OUTPUT_PP_AF3);
    P1_14_set_driver_strength(MEDIUM);
    P1_14_reset();

    // Endstop bottom
    P1_12_set_mode(OUTPUT_PP_AF3);
    P1_12_set_driver_strength(MEDIUM);
    P1_12_reset();

    return true;
}

/*! EOF */
