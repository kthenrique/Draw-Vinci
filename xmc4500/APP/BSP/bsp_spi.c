/*
 * @file bsp_spi.c
 *
 * @date: 05-2018
 * @author: Kelve T. Henrique & Andreas Hofschweiger
 * \brief Configures spi channel
 */


#include <bsp_spi.h>

_Bool BSP_SPI_Init(void){

    if(_init_spi() != SPI_OK)
        return false;

    _mcp23s08_reset();

    _mcp23s08_reset_ss(MCP23S08_SS);
    _mcp23s08_reg_xfer(XMC_SPI1_CH0,MCP23S08_IODIR,0x00,MCP23S08_WR);
    _mcp23s08_set_ss(MCP23S08_SS);

    return true;
}

/*! EOF */
