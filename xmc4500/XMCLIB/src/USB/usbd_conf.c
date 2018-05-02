/*********************************************************************************************************************
* DAVE APP Name : USBD       APP Version: 4.0.6
*
* NOTE:
* This file is generated by DAVE. Any manual modification done to this file will be lost when the code is regenerated.
*********************************************************************************************************************/

/**
 * @cond
 ***********************************************************************************************************************
 * USBD v4.0.4 - The USB core driver for XMC4000 family of controllers. It does the USB protocol handling.
 *
 * Copyright (c) 2015, Infineon Technologies AG
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,are permitted provided that the
 * following conditions are met:
 *
 *   Redistributions of source code must retain the above copyright notice, this list of conditions and the  following
 *   disclaimer.
 *
 *   Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
 *   following disclaimer in the documentation and/or other materials provided with the distribution.
 *
 *   Neither the name of the copyright holders nor the names of its contributors may be used to endorse or promote
 *   products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE  FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY,OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  OF THE
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * To improve the quality of the software, users are encouraged to share modifications, enhancements or bug fixes
 * with Infineon Technologies AG (dave@infineon.com).
 ***********************************************************************************************************************
 *
 * Change History
 * --------------
 *
 * 2015-02-16:
 *     - Initial version.
 * 2015-06-20:
 *     - Updated the file header.
 *
 * @endcond
 *
 */

/***********************************************************************************************************************
 * HEADER FILES
 **********************************************************************************************************************/
#include <stdlib.h>
#include <usbd.h>
#include <events.h>
#include <device.h>

/**********************************************************************************************************************
 * MACROS
 **********************************************************************************************************************/



/**********************************************************************************************************************
* DATA STRUCTURES
**********************************************************************************************************************/
/**
 * @ingroup USBD_datastructures
 * @{
 */
/**
* This structure contains the event call back functions for the USBD events.
* The call back functions shall be registered from the top level apps.
**/
USBD_Event_CB_t usb_event_cb = {
	.connect = NULL,/*!< USB connect event*/
	.disconnect = NULL,/*!< USB Disconnect event*/
	.config_changed = NULL,/*!< USB configuration change event*/
	.control_request = NULL,/*!< USB control request event*/
	.set_address = NULL,/*!< USB set address event*/
	.get_descriptor = NULL,/*!< USB get descriptor event*/
	.wakeup = NULL,/*!< USB wake up event*/
	.suspend = NULL,/*!< USB suspend event*/
	.start_of_frame = NULL,/*!< USB start of frame event*/
	.reset = NULL/*!< USB reset event*/

};

/**
 *  This structure contains configuration definition according to user input
 */
USBD_t USBD_0 = {
	.usb_init.usbd = USB0,/*!< The pointer to the USB register base address*/
	.usb_init.usbd_max_num_eps = (XMC_USBD_MAX_NUM_EPS_t) 7U, /*!< Maximum number of Endpoints*/
	.usb_init.usbd_transfer_mode = XMC_USBD_USE_DMA,/*!< USB data transfer mode: DMA/FIFO*/
	.event_cb = &usb_event_cb /*!< The USBD Event call back routines*/
};

USBD_t *USBD_handle = &USBD_0;

/**
 * @}
 */

