/**
 * @file protocol.h
 *
 * @date: 05-2018
 * @author: Kelve T. Henrique - Andreas Hofschweiger
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
    uint8_t  MID[2];
    uint8_t  CMD;               //0:BL1 1:BL2 2:TL1 3:TL2 4:RES
    union{
        uint64_t BLINK;          // in case it is BLx or RES
        struct{                 // in case it is TLx
            uint32_t HIGH;
            uint32_t LOW;
        } DURATION;
    } DATA;
}UART_PACKET;

bool scrutinise(char *str, volatile UART_PACKET *packet);

void SendNack(void);
void SendAck(void);

#endif
