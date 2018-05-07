/*
 * @file bsp_gpio.c
 *
 * @date: 03-2018
 * @author: Kelve T. Henrique
 * \brief Configures LEDs and Buttons
 */

#include <bsp_gpio.h>

_Bool BSP_GPIO_Init (void){

    // Initialise LEDs
    P1_1_set_mode(OUTPUT_PP_AF3);
    P1_1_set_driver_strength(STRONG);
    P1_1_reset();

    P1_0_set_mode(OUTPUT_PP_AF3);
    P1_0_set_driver_strength(STRONG);
    P1_0_reset();

    // Initialise Buttons
    XMC_GPIO_SetMode(BUTTON2, XMC_GPIO_MODE_INPUT_TRISTATE);
    XMC_GPIO_SetMode(BUTTON1, XMC_GPIO_MODE_INPUT_TRISTATE);

    // Initialise Ports for the CCU8
    P5_7_set_mode(OUTPUT_PP_AF3);
    P5_7_set_driver_strength(STRONG);
    P5_7_reset();

    P5_1_set_mode(OUTPUT_PP_AF3);
    P5_1_set_driver_strength(STRONG);
    P5_1_reset();

    return true;
}

/*! EOF */
