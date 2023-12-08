import serial
import time

# El que dice saliente con SerialPort
serialPort = serial.Serial(port='COM4', baudrate=9600, timeout=0, parity=serial.PARITY_EVEN, stopbits=1)
#serialPortSaliente = serial.Serial(port='COM5', baudrate=9600, timeout=0, parity=serial.PARITY_EVEN, stopbits=1)

print("Starting...")

while True:
    time.sleep(5)

    serialPort.flush()
    # limpiar buffer

    # serialPort.write(str.encode('Fp Up F2 R L U2 Bp'))
    serialPort.write(str.encode('#hola!'))

# # while True:
# #     data = serialPort.readline(size)

# #     if data:
# #         print(data)
# #         # escribir dato en serialPortSaliente
# #         serialPort.flush()
# #         # limpiar buffer
# #         serialPort.write(str.encode('h'))