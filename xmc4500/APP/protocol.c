/**
 * @file protocol.c
 *
 * @date: 05-2018
 * @author: Kelve T. Henrique - Andreas Hofschweiger
 *
 * @brief
 *
 */

#include <app_cfg.h>
#include <protocol.h>
#include <xmc_uart.h>
#include <string.h>

#if SEMI_HOSTING
#include <debug_lib.h>
#endif

#if JLINK_RTT
#include <SEGGER_RTT.h>
#include <SEGGER_RTT_Conf.h>
#endif

bool scrutinise(char *str, volatile CODE *packet){
    char *endptr = NULL, *token_ptr = NULL, *sav_p;
    const char delim[] = ":";
    uint8_t i;

    packet->isFree = false;
    for (i = 0; i != 4; i++, str = NULL){
        token_ptr = strtok_r(str, delim, &sav_p); // strtok_r preferable for reentrancy
        if (strncmp((const char *)token_ptr,(const char *)"G00",3) == 0){
            packet->cmd    = 0;
            packet->x_axis = 0;
            packet->y_axis = 0;
            packet->z_axis = 2;
        } else
            if (strncmp((const char *)token_ptr,(const char *)"G01",3) == 0){
                APP_TRACE_DBG ("G01...\n");
                packet->cmd    = 1;
            } else
                if (strncmp((const char *)token_ptr,(const char *)"G90",3) == 0){
                    packet->cmd    = 2;
                } else 
                    if (strncmp((const char *)token_ptr,(const char *)"G91",3) == 0){
                        packet->cmd    = 3;
                        packet->x_axis = 0;
                        packet->y_axis = 0;
                        packet->z_axis = 2;
                    } else
                        if (strncmp((const char *)token_ptr,(const char *)"G28",3) == 0){
                            packet->cmd = 4;
                        }
                        if ((token_ptr[0] == 'x') || (token_ptr[0] == 'X')){
                            APP_TRACE_DBG ("Changing value of X...\n");
                            packet->x_axis = strtol((const char *)&token_ptr[1], &endptr, 10);
                        } else
                            if ((token_ptr[0] == 'y') || (token_ptr[0] == 'Y')){
                                packet->y_axis = strtol((const char *)&token_ptr[1], &endptr, 10);
                            } else
                                if ((token_ptr[0] == 'z') || (token_ptr[0] == 'Z')){
                                    packet->z_axis = strtol((const char *)&token_ptr[1], &endptr, 10);
                                } //else
                                    //return false;
        if (token_ptr == NULL){
            break;
        }
    }
    return true;
}


void SendNack(void){
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'N');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'A');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'C');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'K');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, '\n');
}

void SendAck(void){
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'A');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'C');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, 'K');
    XMC_UART_CH_Transmit (XMC_UART1_CH1, '\n');
}
