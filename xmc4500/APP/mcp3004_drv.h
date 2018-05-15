/**
 * @file     mcp3004_drv.h
 * @version  V0.1
 * @date     March 2017
 * @author   Roman Beneder
 *
 * @brief   MCP3004 Driver Library
 *
 */

#ifndef INC_MCP3004_DRV_H_
#define INC_MCP3004_DRV_H_

#include "xmc_gpio.h"
#include "xmc_spi.h"
#include "xmc4500_spi_lib.h"
#include "errno.h"

#define MCP3004_OK 0

#define MCP3004_CTRL_CH0 			0x80		/* Joystick left - right */
#define MCP3004_CTRL_CH1 			0x90		/* Joystick up - down	 */
#define MCP3004_CTRL_CH2 			0xA0		/* Joystickplate switch  */
#define MCP3004_CTRL_CH3 			0xB0		/* IO-Expander G7		 */
#define MCP3004_CTRL_DIFF_CH0_CH1 	0x00
#define MCP3004_CTRL_DIFF_CH1_CH0 	0x10
#define MCP3004_CTRL_DIFF_CH2_CH3 	0x20
#define MCP3004_CTRL_DIFF_CH3_CH2 	0x30

uint8_t _mcp3004_reset_ss(XMC_GPIO_PORT_t *const port, const uint8_t pin);
uint8_t _mcp3004_set_ss(XMC_GPIO_PORT_t *const port, const uint8_t pin);
uint8_t _mcp3004_read_byte(XMC_USIC_CH_t *const channel, uint8_t mcp3004_ctrl);

#endif /* INC_MCP3004_DRV_H_ */
