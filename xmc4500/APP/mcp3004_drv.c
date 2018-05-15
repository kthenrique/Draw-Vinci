/**
 * @file     mcp3004_drv.c
 * @version  V0.1
 * @date     March 2017
 * @author   Roman Beneder
 *
 * @brief   MCP3004 Driver Library
 *
 */

#include "mcp3004_drv.h"

uint8_t mcp3004_start = 0x01;
uint8_t mcp3004_nop = 0x00;

/*!
 *  @brief This function resets the Slave Select
 *  @param XMC_GPIO_PORT_t *const port, const uint8_t pin
 *  @return on success this function returns MCP3004_OK (0) otherwise it check
 *  the given port on validity
 */
uint8_t _mcp3004_reset_ss(XMC_GPIO_PORT_t *const port, const uint8_t pin)
{
  XMC_ASSERT("XMC_GPIO_Init: Invalid port", XMC_GPIO_CHECK_PORT(port));

  XMC_GPIO_SetOutputLow(port,pin);

  return MCP3004_OK;
}

/*!
 *  @brief This function sets the Slave Select
 *  @param XMC_GPIO_PORT_t *const port, const uint8_t pin
 *  @return on success this function returns MCP3004_OK (0) otherwise it check
 *  the given port on validity
 */
uint8_t _mcp3004_set_ss(XMC_GPIO_PORT_t *const port, const uint8_t pin)
{
  XMC_ASSERT("XMC_GPIO_Init: Invalid port", XMC_GPIO_CHECK_PORT(port));

  XMC_GPIO_SetOutputHigh(port,pin);

  return MCP3004_OK;
}

/*!
 *  @brief This function reads from the MCP3004
 *  @param channel ........ SPI channel
 *		   mcp3004_ctrl ... channel of the ADC
 *  @return received ADC value (0 - 255)
 */
uint8_t _mcp3004_read_byte(XMC_USIC_CH_t *const channel, uint8_t mcp3004_ctrl)
{
  uint8_t recv = 0, recv_tmp[3] = {0};

  XMC_ASSERT("XMC_USIC_CH_Enable: channel not valid", XMC_USIC_IsChannelValid(channel));

  _spi_transmit(channel,mcp3004_start);
  recv_tmp[0] = _spi_receive(channel);

  _spi_transmit(channel,mcp3004_ctrl);
  recv_tmp[1] = _spi_receive(channel);
  recv = recv_tmp[1]<<6;

  _spi_transmit(channel,mcp3004_nop);
  recv_tmp[2] = _spi_receive(channel);
  recv |= recv_tmp[2]>>2;

  return recv;
}
