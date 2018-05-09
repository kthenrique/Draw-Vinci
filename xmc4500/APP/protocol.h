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
    int8_t x_axis;
    int8_t y_axis;
    uint8_t z_axis;         //z_axis = 0 -> pen up (no painting), z_axis = 1 -> pen down (painting)
    uint8_t pos_mode;       //pos_mode = 0 -> absolute positioning, pos_mode = 1 -> relative addressing
    uint16_t speed;
}COORDINATES;

bool scrutinise(char *str, volatile COORDINATES *packet);

void SendNack(void);
void SendAck(void);

#endif
