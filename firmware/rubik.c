//==================[inclusiones]============================================/

#include "sapi.h"        // <= Biblioteca sAPI
#include <string.h>
#include "goodies.h"

//==================[definiciones y macros]==================================/


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

#define speed 700 //delay entre pasos [uS] (micro-segundos)

//==================[definiciones de funciones]=========================/

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

    delayInaccurateUs(5000);

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


//INICIALIZACION DEL SISTEMA
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

//TRADUCE EL STRING ENVIADO POR BLUETOOTH A INFO QUE SE LE PUEDE ENVIAR AL DRIVER DEL MOTOR

void resolverCubo(char* instrucciones, uint8_t max){ 
	uint8_t dirPin;
	uint8_t stepPin;
	uint8_t pasos;
	uint8_t direccion;
	uint8_t delay
    for (uint8_t i = 0; i < max; i++){
        switch(instrucciones[i++]){
            case 'L': //B C R2
				dirPin= DIR6L; stepPin= STEP6L;
                break;
            case 'R':
				dirPin= DIR3R; stepPin= STEP3R
            	if (instrucciones[i] =='-'){ //90 grados antihorario
                    pasos= 50;
					direccion= ANTIHORARIO;
                    i++;
                } else if (instrucciones[i] == '2'){ //180 grados
                    pasos= 100;
					direccion= HORARIO;
                    i++;
                } else { //90 grados horario
                    pasos= 50;
					direccion= HORARIO;
                }
				 break;
            case 'D':
				dirPin= DIR5D; stepPin= STEP5D
            	if (instrucciones[i] =='-'){ //90 grados antihorario
                    pasos= 50;
					direccion= ANTIHORARIO;
                    i++;
                } else if (instrucciones[i] == '2'){ //180 grados
                    pasos= 100;
					direccion= HORARIO;
                    i++;
                } else { //90 grados horario
                    pasos= 50;
					direccion= HORARIO;
                }
				break;
            case 'B':
				dirPin= DIR2B; stepPin= STEP2B
				if (instrucciones[i] =='-'){ //90 grados antihorario
                    pasos= 50;
					direccion= ANTIHORARIO;
                    i++;
                } else if (instrucciones[i] == '2'){ //180 grados
                    pasos= 100;
					direccion= HORARIO;
                    i++;
                } else { //90 grados horario
                    pasos= 50;
					direccion= HORARIO;
                }
            	break;
            case 'U':  //CASO ESPECIAL: LOS SENTIDOS ESTAN INVERTIDOS
				dirPin= DIR4U; stepPin= STEP4U
            	if (instrucciones[i] =='-'){ //90 grados antihorario
                    pasos= 50;
					direccion= !ANTIHORARIO;
                    i++;
                } else if (instrucciones[i] == '2'){ //180 grados
                    pasos= 100;
					direccion= !HORARIO;
                    i++;
                } else { //90 grados horario
                    pasos= 50;
					direccion= !HORARIO;
                }
                break;
            case 'F': //CASO ESPECIAL: NO PUEDE GIRAR EN UN SENTIDO
				dirPin= DIR1F; stepPin= STEP1F
            	if (instrucciones[i] =='-'){ //90 grados antihorario
                    pasos= 150;
					direccion= ANTIHORARIO;
                    i++;
                } else if (instrucciones[i] == '2'){ //180 grados
                    pasos= 100;
					direccion= HORARIO;
                    i++;
                } else { //90 grados horario
                    pasos= 50;
					direccion= HORARIO;
                }
            	break;
        }
		moverMotor(dirPIN,stepPIN,pasos,direccion,speed);
        delayInaccurateUs(delay_Giro);
    }

}
