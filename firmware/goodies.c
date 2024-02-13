
// Delay apropiativo inexacto de uS
void delayInaccurateUs(int delay_us){
   volatile int i;
   volatile int delay;
   delay = INACCURATE_TO_US * delay_us;
   for( i=delay; i>0; i-- );
}

// MUEVE EL MOTOR INDICADO

void moverMotor(int dir_motor, int motor, int pasos, uint8_t direccion, int delay){
    gpioWrite(dir_motor, direccion);

	for(int i=0; i<pasos; i++){
	  gpioWrite( motor, ON);
	  delayInaccurateUs(delay);
	  gpioWrite( motor, OFF);
	  delayInaccurateUs(delay);
	}
}
