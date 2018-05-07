/*
 * @file bsp_ccu8.c
 *
 * @date: 04-2018
 * @author: Kelve T. Henrique
 * \brief Configures 2 CCU8 modules to be used as PWM signals,
 *        namely the slices 0 and 3 of module 1, which are responsible for
 *        the two pins P5.7 and P5.1, respectively.
 *
 */

#include <bsp_ccu8.h>

_Bool BSP_CCU8_Init (void){

XMC_CCU8_SLICE_COMPARE_CONFIG_t sliceCompareConfig = {
  .timer_mode          = XMC_CCU8_SLICE_TIMER_COUNT_MODE_EA,
  .monoshot            = false,
  .shadow_xfer_clear   = false,
  .dither_timer_period = false,
  .dither_duty_cycle   = false,
  .prescaler_mode      = XMC_CCU8_SLICE_PRESCALER_MODE_NORMAL,
  .mcm_ch1_enable      = false,
  .mcm_ch2_enable      = false,
  .slice_status        = XMC_CCU8_SLICE_STATUS_CHANNEL_1,
  .passive_level_out0  = XMC_CCU8_SLICE_OUTPUT_PASSIVE_LEVEL_LOW,
  .passive_level_out1  = XMC_CCU8_SLICE_OUTPUT_PASSIVE_LEVEL_LOW,
  .passive_level_out2  = XMC_CCU8_SLICE_OUTPUT_PASSIVE_LEVEL_LOW,
  .passive_level_out3  = XMC_CCU8_SLICE_OUTPUT_PASSIVE_LEVEL_LOW,
  .asymmetric_pwm      = false,
  .invert_out0         = false,
  .invert_out1         = false,
  .invert_out2         = false,
  .invert_out3         = false,
  .prescaler_initval   = PRESCALER_CCU81,
  .float_limit         = 0U,
  .dither_limit        = 0U,
  .timer_concatenation = false
};

    /* INITIALIZATION SEQUENCE ACCORDING TO THE XMC4500 REFERENCE MANUAL SECTION 23.6.1 */
    XMC_CCU8_SetModuleClock(MODULE_CCU8, XMC_CCU8_CLOCK_SCU);

    XMC_CCU8_Init(MODULE_CCU8, XMC_CCU8_SLICE_MCMS_ACTION_TRANSFER_PR_CR);

    XMC_CCU8_EnableClock(MODULE_CCU8, SLICE_NUMBER_A);
    XMC_CCU8_EnableClock(MODULE_CCU8, SLICE_NUMBER_B);

    XMC_CCU8_StartPrescaler(MODULE_CCU8);

    XMC_CCU8_SLICE_CompareInit(SLICE_CCU8_A, &sliceCompareConfig);          /* Init compare mode */
    XMC_CCU8_SLICE_CompareInit(SLICE_CCU8_B, &sliceCompareConfig);          /* Init compare mode */

    XMC_CCU8_SLICE_EnableEvent(SLICE_CCU8_A, XMC_CCU8_SLICE_IRQ_ID_PERIOD_MATCH);      /* Enable compare match events */
    XMC_CCU8_SLICE_EnableEvent(SLICE_CCU8_A, XMC_CCU8_SLICE_IRQ_ID_COMPARE_MATCH_UP_CH_1);  /* Enable period match events */
    XMC_CCU8_SLICE_EnableEvent(SLICE_CCU8_A, XMC_CCU8_SLICE_IRQ_ID_COMPARE_MATCH_UP_CH_2);  /* Enable period match events */
    XMC_CCU8_SLICE_EnableEvent(SLICE_CCU8_B, XMC_CCU8_SLICE_IRQ_ID_PERIOD_MATCH);      /* Enable compare match events */
    XMC_CCU8_SLICE_EnableEvent(SLICE_CCU8_B, XMC_CCU8_SLICE_IRQ_ID_COMPARE_MATCH_UP_CH_1);  /* Enable period match events */
    XMC_CCU8_SLICE_EnableEvent(SLICE_CCU8_B, XMC_CCU8_SLICE_IRQ_ID_COMPARE_MATCH_UP_CH_2);  /* Enable period match events */

    XMC_CCU8_SLICE_SetTimerPeriodMatch (SLICE_CCU8_A, PERIOD_CCU81);  // ATENTION: Calculating the PWM period according to the XMC4500
    XMC_CCU8_SLICE_SetTimerCompareMatch(SLICE_CCU8_A, XMC_CCU8_SLICE_COMPARE_CHANNEL_1, 1200U);  //           REFERENCE MANUAL Section 23.2.5.1 for a 50Hz PWM with
    XMC_CCU8_SLICE_SetTimerCompareMatch(SLICE_CCU8_A, XMC_CCU8_SLICE_COMPARE_CHANNEL_2, 1200U);
    XMC_CCU8_SLICE_SetTimerPeriodMatch (SLICE_CCU8_B, PERIOD_CCU81);
    XMC_CCU8_SLICE_SetTimerCompareMatch(SLICE_CCU8_B, XMC_CCU8_SLICE_COMPARE_CHANNEL_1, 1200U);
    XMC_CCU8_SLICE_SetTimerCompareMatch(SLICE_CCU8_B, XMC_CCU8_SLICE_COMPARE_CHANNEL_2, 1200U);

    XMC_CCU8_EnableShadowTransfer(MODULE_CCU8, SLICE_TRANSFER_A);/* Enable shadow transfer */
    XMC_CCU8_EnableShadowTransfer(MODULE_CCU8, SLICE_TRANSFER_B);/* Enable shadow transfer */

    XMC_CCU8_SLICE_StartTimer(SLICE_CCU8_A);
    XMC_CCU8_SLICE_StartTimer(SLICE_CCU8_B);

    XMC_SCU_SetCcuTriggerHigh(GENERAL_CCUCON_CCU8);/* Generate an external start trigger */

    return true;
}

/*! EOF */
