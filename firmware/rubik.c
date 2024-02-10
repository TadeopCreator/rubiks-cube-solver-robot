//==================[inlcusiones]============================================/

#include "sapi.h"        // <= Biblioteca sAPI
#include <string.h>

//==================[definiciones y macros]==================================/

#define UART_PC        UART_USB
#define UART_BLUETOOTH UART_232

#define STEP6L GPIO7
#define DIR6L GPIO8
#define STEP3R GPIO3
#define DIR3R GPIO5
#define STEP5D LCD1
#define DIR5D GPIO1
#define STEP2B LCD3
#define DIR2B LCD2
#define STEP4U LCD4 // ESTA ES ANTIHORARIA
#define DIR4U LCDRS
#define STEP1F SPI_MISO
#define DIR1F SPI_MOSI

#define desfase 5
#define delay_Giro 2000 //delay entre giros [uS] (micro-segundos)

#define HORARIO 0
#define ANTIHORARIO 1

#define INACCURATE_TO_US 20
#define speed 700 //delay entre pasos [uS] (micro-segundos)

//==================[definiciones de datos internos]=========================/

void delayInaccurateMsB(int delay_ms);

//==================[definiciones de datos externos]=========================/

void moverMotor(int dir_motor, int motor, int pasos, uint8_t direccion, int velocidad);

void resolverCubo(char* instrucciones, uint8_t max);

void initSystem();

//==================[funcion principal]======================================/

// FUNCION PRINCIPAL, PUNTO DE ENTRADA AL PROGRAMA LUEGO DE ENCENDIDO O RESET.
int main( void )
{
	initSystem();
    uint8_t data = 0;
    char buffer[121];
    uint8_t i = 0;

    delayInaccurateMsB(5000);

    while(1) {
    	if( uartReadByte( UART_BLUETOOTH, &data ) ) {
    		if(data == '!') {
    			buffer[i]='\0';
    			resolverCubo(buffer, i);
    			i = 0;
    		} else
    			buffer[i++]= data;
    	}
    }

    return 0;
}

//==================[definiciones de funciones internas]=====================/

void initSystem(){
    boardConfig();

    //PONGO A TODOS LOS PUERTOS PARA LOS MOTORES COMO SALIDAS
    //SENTIDO HORARIO DEFAULT
    gpioConfig( STEP6L, GPIO_OUTPUT );
    gpioConfig( DIR6L, GPIO_OUTPUT );
    gpioWrite(DIR6L, ON);
    gpioConfig( STEP3R, GPIO_OUTPUT );
    gpioConfig( DIR3R, GPIO_OUTPUT );
    gpioWrite(DIR3R, ON);
    gpioConfig( STEP5D, GPIO_OUTPUT );
    gpioConfig( DIR5D, GPIO_OUTPUT );
    gpioWrite(DIR5D, ON);
    gpioConfig( STEP2B, GPIO_OUTPUT );
    gpioConfig( DIR2B, GPIO_OUTPUT );
    gpioWrite(DIR2B, ON);
    gpioConfig( STEP4U, GPIO_OUTPUT );
    gpioConfig( DIR4U, GPIO_OUTPUT );
    gpioWrite(DIR4U, ON);
    gpioConfig( STEP1F, GPIO_OUTPUT );
    gpioConfig( DIR1F, GPIO_OUTPUT );
    gpioWrite(DIR1F, ON);

    // Inicializar UART_232 para conectar al modulo bluetooth
    uartConfig( UART_BLUETOOTH, 9600 );
}

// Delay apropiativo inexacto
void delayInaccurateMsB(int delay_us){
   volatile int i;
   volatile int delay;
   delay = INACCURATE_TO_US * delay_us;
   for( i=delay; i>0; i-- );
}

void moverMotor(int dir_motor, int motor, int pasos, uint8_t direccion, int delay){
    gpioWrite(dir_motor, direccion);
	//gpioWrite( LED1, ON );

	for(int i=0; i<pasos; i++){
	  gpioWrite( motor, ON);
	  delayInaccurateMsB(delay);
	  gpioWrite( motor, OFF);
	  delayInaccurateMsB(delay);
	}
	//gpioWrite( LED1, OFF );
}

void resolverCubo(char* instrucciones, uint8_t max){
    for (uint8_t i = 0; i < max; i++){
        switch(instrucciones[i++]){
            case 'L': //B C R2
                if (instrucciones[i] =='-'){ //90 grados antihorario
                    moverMotor(DIR6L,STEP6L,50,ANTIHORARIO,speed);
                    delayInaccurateMsB(delay_Giro);
                    i++;
                } else if (instrucciones[i] == '2'){ //180 grados
                    moverMotor(DIR6L,STEP6L,100,HORARIO,speed);
                    delayInaccurateMsB(delay_Giro);
                    i++;
                } else { //90 grados horario
                    moverMotor(DIR6L,STEP6L,50,HORARIO,speed);
                    delayInaccurateMsB(delay_Giro);
                }

                break;
            case 'R':
            	if (instrucciones[i] =='-'){ //90 grados antihorario
            	    moverMotor(DIR3R,STEP3R,50,ANTIHORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else if (instrucciones[i] == '2'){ //180 grados
            	                    moverMotor(DIR3R,STEP3R,100,HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else { //90 grados horario
            	                    moverMotor(DIR3R,STEP3R,50,HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                }

            	                break;
            case 'D':
            	if (instrucciones[i] =='-'){ //90 grados antihorario
            	                    moverMotor(DIR5D,STEP5D,50,ANTIHORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else if (instrucciones[i] == '2'){ //180 grados
            	                    moverMotor(DIR5D,STEP5D,100,HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else { //90 grados horario
            	                    moverMotor(DIR5D,STEP5D,50,HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                }

            	                break;
            case 'B':
            	if (instrucciones[i] =='-'){ //90 grados antihorario
            	    moverMotor(DIR2B,STEP2B,50,ANTIHORARIO,speed);
            	    delayInaccurateMsB(delay_Giro);
            	    i++;
            	} else if (instrucciones[i] == '2'){ //180 grados
            	    moverMotor(DIR2B,STEP2B,100,HORARIO,speed);
            	    delayInaccurateMsB(delay_Giro);
            	    i++;
            	} else { //90 grados horario
            	    moverMotor(DIR2B,STEP2B,50,HORARIO,speed);
            	    delayInaccurateMsB(delay_Giro);
            	}

            	break;
            case 'U':
            	if (instrucciones[i] =='-'){ //90 grados antihorario
            	    moverMotor(DIR4U,STEP4U,50,!ANTIHORARIO,speed);
            	    delayInaccurateMsB(delay_Giro);
            	    i++;
            	                } else if (instrucciones[i] == '2'){ //180 grados
            	                    moverMotor(DIR4U,STEP4U,100,!HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else { //90 grados horario
            	                    moverMotor(DIR4U,STEP4U,50,!HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                }

            	                break;
            case 'F':
            	if (instrucciones[i] =='-'){ //90 grados antihorario
            	                    moverMotor(DIR1F,STEP1F,150,ANTIHORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else if (instrucciones[i] == '2'){ //180 grados
            	                    moverMotor(DIR1F,STEP1F,100,HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                    i++;
            	                } else { //90 grados horario
            	                    moverMotor(DIR1F,STEP1F,50,HORARIO,speed);
            	                    delayInaccurateMsB(delay_Giro);
            	                }

            	                break;
        }
    }

}
