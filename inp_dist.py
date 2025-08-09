import sys
import math
import serial
import time

x0,y0=0.0,0.0
x1,y1=30.0,0.0
x2,y2=15.0,30.0
d1,d2,d3=0,0,0
SERIAL_PORT= "COM7"
BAUD_RATE=115200

# Open the serial port outside the main loop
try:
    ser=serial.Serial(SERIAL_PORT,BAUD_RATE,timeout=1)
    time.sleep(2)
    print(f"Succesfully connected to arduino from {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Could not open serial port {SERIAL_PORT}")
    sys.exit()

# trilaterate function (removed for brevity, as it was not in your loop)

try:
    while True:
        try:
            value = ser.readline()
            valueInString = value.decode('utf-8').strip()
            if valueInString:
                distances = valueInString.split(',')
                if len(distances) == 3:
                    try:
                        d1 = int(distances[0])
                        d2 = int(distances[1])
                        d3 = int(distances[2])
                        print(f"Distance 1:{d1},Distance 2:{d2}, Distance 3:{d3}")
                    except ValueError:
                        print("Could not convert to integer")
                else:
                    print(f"Received an incomplete line: {valueInString}")
        except Exception as e:
            # Handle potential errors within the loop
            print(f"Error reading data: {e}")

# The finally block will always execute, whether an error occurs or not.
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
    sys.exit()