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

def trilaterate(d1,d2,d3):
    A=2*(x0-x1)
    B=2*(y0-y1)
    C=2*(x1-x2)
    D=2*(y1-y2)

    E=d2**2 - d1**2 - x1**2- y1**2 +x0**2 + y0**2
    F=d3**2-d2**2-x2**2-y2**2+x1**2+y1**2

    det=A*D-B*C
    if det==0:
        raise ValueError("Sensors are collinear")
    x_coordinate=(E*D-B*F)/det
    y_coordinate=(A*F-E*C)/det

    return (x_coordinate,y_coordinate)

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
                        # Example call to trilaterate:
                        x, y = trilaterate(d1, d2, d3)
                        print(f"Calculated Position -> x: {x:.2f}, y: {y:.2f}")
                    except ValueError:
                        print("Could not convert to integer")
                else:
                    print(f"Received an incomplete line: {valueInString}")
        except Exception as e:
            print(f"Error reading data: {e}")
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
    sys.exit()
