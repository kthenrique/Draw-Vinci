/**
 * @file protocol.c
 *
 * @date: 03-2018
 * @author: Kelve T. Henrique
 *
 * @brief 
 *
 */

#include <protocol.h>
#include <app_cfg.h>
#include <xmc_uart.h>

bool scrutinise(char *str, volatile UART_PACKET *packet){
    unsigned long DUTY;
    char *endptr;

    // Assert Duty
    if (strlen(str) > 4) return false;

    // Convert Duty to long int || asserting it comprises only digits
    DUTY = strtoul((const char *)(str+1), (char **)&endptr, 10);
    if (*endptr != '\0') return false;

    if (DUTY > 100) return false;

    if (str[0] != '1'&& str[0] != '2'&& str[0] != '3'&& str[0] != '4')
         return false;

    packet->port = str[0];
    packet->duty = DUTY;

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
