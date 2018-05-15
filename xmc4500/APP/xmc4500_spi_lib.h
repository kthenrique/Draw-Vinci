/*
 * xmc4500_spi_lib.h
 *
 *  Created on: 29 Mar 2017
 *      Author: rbeneder
 */

#ifndef INC_XMC4500_SPI_LIB_H_
#define INC_XMC4500_SPI_LIB_H_

#include "xmc_spi.h"
#include "xmc_gpio.h"
#include "errno.h"

#define SPI_MISO 	P0_4
#define SPI_MOSI 	P0_5
#define SPI_SCLK 	P0_11
#define MCP23S08_SS P1_2
#define MCP3004_SS  P1_4

#define SPI_OK 		0x00

uint8_t _init_spi(void);
uint8_t _spi_transmit(XMC_USIC_CH_t *const channel, uint8_t spi_data);
uint8_t _spi_receive(XMC_USIC_CH_t *const channel);

#endif /* INC_XMC4500_SPI_LIB_H_ */
