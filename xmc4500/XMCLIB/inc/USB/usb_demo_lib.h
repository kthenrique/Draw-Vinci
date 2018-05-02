/**
 * @file compass_lib.h
 * @version  V1
 * @date     Nov 2016
 * @author Guenter Arzberger
 *
 * @brief compass lib header file.
 *
 * @revision 02-2018 M. Horauer
 */
#ifndef _usb_demo_lib_
#define _usb_demo_lib_

#include <error_led.h>
#include <usb_driver.h>

/******************************************************************** DEFINES */
#define RECEIVE 1
#define ERROR_RECEIVE -1
#define NON_RECEIVE 0
#define SIZE 0x20

/******************************************************** FUNCTION PROTOTYPES */
uint8_t init (void);
int8_t usb_incomming (char *receivedata);
int8_t usb_transfer (char *send);
void change (char *word);

#endif

