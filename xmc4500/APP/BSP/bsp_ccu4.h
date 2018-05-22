/*
 * @file bsp_ccu4.h
 *
 * @date 04-2018
 * @author: Kelve T. Henrique
 */

#ifndef SRC_BSP_BSP_CCU4_H_
#define SRC_BSP_BSP_CCU4_H_

#include <xmc_ccu4.h>
#include <xmc_scu.h>

#define PRESCALER_CCU40       8U
#define PERIOD_CCU40          9374U
#define FOURTH_PERIOD_CCU40   293U

#define SLICE_CCU4_C          CCU40_CC40
#define MODULE_CCU4           CCU40
#define SLICE_NUMBER_C        (0U)
#define SLICE_TRANSFER_C      XMC_CCU4_SHADOW_TRANSFER_SLICE_0
#define GENERAL_CCUCON_CCU4   SCU_GENERAL_CCUCON_GSC40_Msk /**< Only CCU81 */

_Bool BSP_CCU4_Init (void) ;

#endif
