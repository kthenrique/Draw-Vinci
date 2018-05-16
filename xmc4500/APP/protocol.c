/**
 * @file protocol.c
 *
 * @date: 05-2018
 * @author: Kelve T. Henrique - Andreas Hofschweiger
 *
 * @brief
 *
 */

#include <protocol.h>
#include <app_cfg.h>
#include <xmc_uart.h>
#include <string.h>


bool scrutinise(char *str, volatile COORDINATES *packet){
    char *endptr = NULL;
    char *token_ptr = NULL;
    const char delim[] = ":";

    APP_TRACE_INFO ("Separated in tokens ...\n");
    token_ptr = strtok(str, delim);
    while(1){
        if (strncmp((const char *)token_ptr,(const char *)"G00",3) == 0){
            packet->x_axis = 0;
            packet->y_axis = 0;
            packet->z_axis = 0;
            packet->pos_mode = 0;
        } else
            if (strncmp((const char *)token_ptr,(const char *)"G1",3) == 0){
                APP_TRACE_INFO ("G1...\n");
        } else
            if (strncmp((const char *)token_ptr,(const char *)"G90",3) == 0){
                packet->pos_mode = 0;
            } else 
                if (strncmp((const char *)token_ptr,(const char *)"G91",3) == 0){
                    packet->pos_mode = 1;
                } else
                    if ((token_ptr[0] == 'x') || (token_ptr[0] == 'X')){
                        APP_TRACE_INFO ("Changing value of X...\n");
                        packet->x_axis = strtol((const char *)&token_ptr[1], &endptr, 10);
                    } else
                        if ((token_ptr[0] == 'y') || (token_ptr[0] == 'Y')){
                            packet->y_axis = strtol((const char *)&token_ptr[1], &endptr, 10);
                        } else
                            if ((token_ptr[0] == 'z') || (token_ptr[0] == 'Z')){
                                packet->z_axis = strtol((const char *)&token_ptr[1], &endptr, 10);
                            } else
                                if (token_ptr[0] == 'M'){

                                } else
                                    if (token_ptr[0] == 'F'){
                                        packet->speed = strtol((const char *)&token_ptr[1], &endptr, 10);
                                    } else
                                        return false;
        token_ptr = strtok(NULL, delim);
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
