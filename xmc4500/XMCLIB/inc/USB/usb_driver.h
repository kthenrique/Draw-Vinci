/**
 * @file usb_driver.h
 * @version  V1
 * @date     Dez 2016
 * @author Guenter Arzberger
 *
 * @brief USB header file XMC4500 board.
 *
 * @revision 02-2018 M. Horauer
 */
#ifndef _usb_driver_
#define _usb_driver_

#include <usbd_olb.h>
#include <xmc_common.h>
#include <cpu_ctrl_xmc4.h>
#include <clock_xmc4.h>
#include <usbd.h>

/******************************************************** FUNCTION PROTOTYPES */
uint8_t  usb_init (void);
int8_t   usb_connected (void);
uint16_t usb_BytesReceive (void);
int8_t   usb_receive (int8_t* const data_buff, uint16_t const byte);
int8_t   usb_send (int8_t* const data, uint16_t const byte);

#endif
