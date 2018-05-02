/*
 * @file bsp_ccu8.h
 *
 * @date 04-2018
 * @author: Kelve T. Henrique
 */

#ifndef SRC_BSP_BSP_CCU8_H_
#define SRC_BSP_BSP_CCU8_H_

#include <xmc_ccu8.h>
#include <xmc_scu.h>

#define PRESCALER_CCU81       0U // ftclk=120MHz according to Table 23-8
#define PERIOD_CCU81          2399U // fPWM = 50KHz
#define FOURTH_PERIOD_CCU81   600U

#define SLICE_CCU8_A          CCU81_CC83  // P5.1
#define SLICE_CCU8_B          CCU81_CC80  // P5.7
#define MODULE_CCU8           CCU81
#define SLICE_NUMBER_A        (3U)
#define SLICE_NUMBER_B        (0U)
#define SLICE_TRANSFER_A      XMC_CCU8_SHADOW_TRANSFER_SLICE_3
#define SLICE_TRANSFER_B      XMC_CCU8_SHADOW_TRANSFER_SLICE_0
#define GENERAL_CCUCON_CCU8   SCU_GENERAL_CCUCON_GSC81_Msk /**< Only CCU81 */

_Bool BSP_CCU8_Init (void) ;

#endif
