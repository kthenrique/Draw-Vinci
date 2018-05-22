/*
 * @file bsp_ccu4.c
 *
 * @date: 04-2018
 * @author: Kelve T. Henrique
 * \brief Configures 2 CCU4 modules to be used as PWM signals,
 *        namely the slices 2 and 3 of module 0, which are responsible for
 *        the two onboard leds P1.1 and P1.0.
 *
 */

#include <bsp_ccu4.h>

_Bool BSP_CCU4_Init (void){

XMC_CCU4_SLICE_COMPARE_CONFIG_t sliceCompareConfig = {
    .timer_mode 		 = XMC_CCU4_SLICE_TIMER_COUNT_MODE_EA,
    .monoshot   		 = false,
    .shadow_xfer_clear   = 0U,
    .dither_timer_period = 0U,
    .dither_duty_cycle   = 0U,
    .prescaler_mode	     = XMC_CCU4_SLICE_PRESCALER_MODE_NORMAL,
    .mcm_enable		     = 0U,
    .prescaler_initval   = PRESCALER_CCU40,    // According to table 22-7 of the Ref. Manual: ftccu4 = fccu4/2048
    .float_limit		 = 0U,
    .dither_limit		 = 0U,
    .passive_level 	     = XMC_CCU4_SLICE_OUTPUT_PASSIVE_LEVEL_LOW,
    .timer_concatenation = 0U
};

    /* INITIALIZATION SEQUENCE ACCORDING TO THE XMC4500 REFERENCE MANUAL SECTION 22.6.1 */

    // 1. Apply reset to the CCU4, via the specific SCU bitfield on the PRSET0/PRSET1 register.
    // 2. Release reset of the CCU4, via the specific SCU bitfield on the PRCLR0/PRCLR1 register.
    // 3. Enable the CCU4 clock via the specific SCU register, CLKSET.
      //NOTE:  Calls to XMC_SCU_RESET_DeassertPeripheralReset(), XMC_SCU_CLOCK_EnablePeripheralClock
      //       are removed as XMC_CCU4_Init is calling these functions.

    XMC_SCU_CLOCK_SetCcuClockDivider(1);//ATTENTION: initialising the fCCU, fCPU and fPERIPH for 120MHz according to the
    XMC_SCU_CLOCK_SetCcuClockDivider(1);//           XMC4500 REFERENCE MANUAL SECTION table 11-5 => ftccu4 = 58593,75
    XMC_SCU_CLOCK_SetCcuClockDivider(1);

    XMC_SCU_CLOCK_EnableClock(XMC_SCU_CLOCK_CCU);                        /**< CCU module clock. */
    XMC_CCU4_SetModuleClock(CCU40, XMC_CCU4_CLOCK_SCU);

    XMC_CCU4_Init(CCU40, XMC_CCU4_SLICE_MCMS_ACTION_TRANSFER_PR_CR);

    XMC_CCU4_EnableClock(MODULE_CCU4, SLICE_NUMBER_C);                                    /**< Timer Slice CC42. */

/* Call to XMC_SCU_CLOCK_Init() is removed as clock is initialized by startup code. */

    // 4. Enable the prescaler block, by writing 1B to the GIDLC.SPRB field.
    // 5. Configure the global CCU4 register GCTRL
    XMC_CCU4_StartPrescaler(MODULE_CCU4);

    // 6. Configure all the registers related to the required Timer Slice(s) functions,
    //    including the interrupt/service request configuration.
    XMC_CCU4_SLICE_CompareInit(CCU40_CC40, &sliceCompareConfig);          /* Init compare mode */

    XMC_CCU4_SLICE_EnableEvent(SLICE_CCU4_C, XMC_CCU4_SLICE_IRQ_ID_PERIOD_MATCH);      /* Enable compare match events */
    XMC_CCU4_SLICE_EnableEvent(SLICE_CCU4_C, XMC_CCU4_SLICE_IRQ_ID_COMPARE_MATCH_UP);  /* Enable period match events */

    // 7. If needed, configure the startup value for a specific Compare Channel Status,
    //    of a Timer Slice, by writing 1B to the specific GCSS.SyTS.
    XMC_CCU4_SLICE_SetTimerPeriodMatch (SLICE_CCU4_C, PERIOD_CCU40);  // ATENTION: Calculating the PWM period according to the XMC4500
    XMC_CCU4_SLICE_SetTimerCompareMatch(SLICE_CCU4_C, 8905U);  //           REFERENCE MANUAL Section 23.2.5.1 for a 50Hz PWM with

    // 8. Enable the specific timer slice(s), CC4y, by writing 1B to the specific GIDLC.CSyl.
    XMC_CCU4_EnableShadowTransfer(MODULE_CCU4, SLICE_TRANSFER_C);/* Enable shadow transfer */

    // 9. For all the Timer Slices that should be started synchronously via SW, the
    //    specific system register localized in the SCU, CCUCON, that enables a synchronous
    //    timer start should be addressed. The SCU.GSC4x input signal needs to be configured
    //    previously as a start function, see Section 22.2.7.1 .
    XMC_CCU4_SLICE_StartTimer(SLICE_CCU4_C);

    XMC_SCU_SetCcuTriggerHigh(GENERAL_CCUCON_CCU4);/* Generate an external start trigger */

    return true;
}

/*! EOF */
