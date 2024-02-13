//==================[inclusiones]============================================/

#include "sapi.h"        // <= Biblioteca sAPI

//==================[definiciones y macros]==================================/

#define INACCURATE_TO_US 20 //PARA EL DELAY

//==================[definiciones de funciones]=========================/

void delayInaccurateUs(int delay_ms);

void moverMotor(int dir_motor, int motor, int pasos, uint8_t direccion, int velocidad);
