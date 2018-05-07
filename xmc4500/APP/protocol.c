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

bool scrutinise(char *str, volatile UART_PACKET *packet){
    long long DATA;
    long MID;
    char *endptr;
    uint8_t i, len;
    char *pieces[4];
    char *sav_p;
    const char delim[] = ":";
    char *str_;

    for (i = 0, str_ = str; i != 4; i++, str_ = NULL){
        pieces[i] = strtok_r(str_, delim, &sav_p); // using strtok_r for reentrancy
        if (pieces[i] == NULL) break;
    }

    APP_TRACE_INFO ("Separated in tokens ...\n");

    // Assert there is 3 elements: MID-CMD-DATA
    if (i != 3) return false;

    // Assert MID
    if ((len = strlen(pieces[0])) > 2) return false; // MID <= 99
    // Convert MID to long int || asserting it comprises only digits
    MID = strtoul((const char *)pieces[0], (char **)&endptr, 10);
    if (*endptr != '\0') return false;

    APP_TRACE_INFO ("MID scrutinised ...\n");

    packet->MID[0]           = (uint8_t) pieces[0][0]; // MID;
    packet->MID[1]           = (uint8_t) pieces[0][1]; // MID;

    // Assert CMD
    if ((len = strlen(pieces[1])) != 3) return false; // CMD = 3
    // Assert acceptable CMD
    if ((strcmp((const char *)pieces[1], (const char *)"BL1")) == 0 ||
        (strcmp((const char *)pieces[1], (const char *)"BL2")) == 0){ // BLx

    APP_TRACE_INFO ("CMD scrutinised ...\n");

        // Assert DATA <= 10 digits
        if (!((len = strlen(pieces[2])) <= 10)) return false;

        // Convert DATA to long long int || asserting it comprises only digits
        DATA = strtoull((const char *)pieces[2], (char **)&endptr, 10);
        if (*endptr != '\0') return false;

        // Return
        (pieces[1][2] == '1') ? (packet->CMD = (uint8_t) 0) :
                                (packet->CMD = (uint8_t) 1);
        packet->DATA.BLINK    = (uint64_t) DATA;

        APP_TRACE_INFO ("DATA acquired!\n");
        return true;
    }

    if ((strcmp((const char *)pieces[1], (const char *)"TL1")) == 0 ||
        (strcmp((const char *)pieces[1], (const char *)"TL2")) == 0){ // TLx

    APP_TRACE_INFO ("CMD scrutinised ...\n");

        // Assert DATA <= 10 characters
        if (!((len = strlen(pieces[2])) <= 10)) return false;

        // Convert DATA to long int || asserting it comprises only digits
        if (pieces[2][0] != 'H') return false;
        DATA = strtoul((const char *)&pieces[2][1], (char **)&endptr, 10);
        if (*endptr == '\0' || endptr == &pieces[2][1]) return false;
        packet->DATA.DURATION.HIGH = (uint32_t) DATA;

        if (endptr[0] != 'L' || endptr[1] == '\0') return false;
        DATA = strtoul((const char *)&endptr[1], (char **)&endptr, 10);
        if (*endptr != '\0') return false;
        packet->DATA.DURATION.LOW = (uint32_t) DATA;

        // Return
        (pieces[1][2] == '1')      ? (packet->CMD = (uint8_t) 2) :
                                     (packet->CMD = (uint8_t) 3);

        APP_TRACE_INFO ("DATA acquired!\n");
        return true;
    }

    if (((strcmp((const char *)pieces[1], (const char *)"RES")) == 0) &&
        (((strcmp((const char *)pieces[2], (const char *)"ON")) == 0) ||
         ((strcmp((const char *)pieces[2], (const char *)"OFF")) == 0))){ // RES

    APP_TRACE_INFO ("CMD scrutinised ...\n");

        // Return
        packet->CMD                = (uint8_t)   4;
        (pieces[2][1] == 'N')      ? (packet->DATA.BLINK = (uint64_t) 1) : // ON
                                     (packet->DATA.BLINK = (uint64_t) 0);  // OFF

        APP_TRACE_INFO ("DATA acquired!\n");
        return true;
    }

    return false;
}
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
