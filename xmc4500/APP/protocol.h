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
    bool isFree;
    uint8_t cmd; // G00:0 G01:1 G90:2 G91:3 G28:4 G02:5
    int16_t x_axis;
    int16_t y_axis;
    uint8_t z_axis;         //z_axis = 0 -> pen up (no painting), z_axis = 1 -> pen down (painting)
    uint16_t speed;
}CODE;

bool scrutinise(char *str, volatile CODE *packet);

void SendNack(void);
void SendAck(void);

#endif
