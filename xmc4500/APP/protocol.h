/**
 * @file protocol.h
 *
 * @date: 03-2018
 * @author: Kelve T. Henrique
 *
 * @brief 
 */

#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

typedef struct{
    bool  isAvailable;
    char  port; // 1:P1.1; 2:P1.0; 3:P5.1; 4:P5.7;
    uint8_t duty;
}UART_PACKET;

bool scrutinise(char *str, volatile UART_PACKET *packet);

void SendNack(void);
void SendAck(void);

#endif
