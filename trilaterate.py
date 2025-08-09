import sys
import math
import serial
import time
import pygame

# Sensor positions (adjust to match your physical setup)
# These are in the same units as the ultrasonic sensor's output (e.g., cm)
x0, y0 = 0.0, 0.0
x1, y1 = 30.0, 0.0
x2, y2 = 15.0, 30.0

# Serial settings
SERIAL_PORT = "COM3"  # <-- Change to your Arduino's COM port (e.g., COM3, COM4, etc.)
BAUD_RATE = 115200

# Pygame screen settings for visualization
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# Scaling from your coordinate system to pixels
SCALE = SCREEN_WIDTH / (max(x0, x1, x2) * 1.5)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Successfully connected to Arduino on {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Could not open serial port {SERIAL_PORT}. Check connection.")
    sys.exit()

# Setup Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trilateration Tracker")
clock = pygame.time.Clock()
path = []

def trilaterate(d1, d2, d3):
    """
    Calculates the (x, y) coordinates of an object
    given three distances and three known sensor positions.
    """
    # System of linear equations derived from the circle equations
    A = 2 * (x1 - x0)
    B = 2 * (y1 - y0)
    C = d1**2 - d2**2 - x0**2 + x1**2 - y0**2 + y1**2
    D = 2 * (x2 - x1)
    E = 2 * (y2 - y1)
    F = d2**2 - d3**2 - x1**2 + x2**2 - y1**2 + y2**2

    # Determinant of the coefficient matrix
    det = A * E - B * D
    if det == 0:
        # Sensors are collinear, can't solve uniquely
        return None

    # Use Cramer's rule to solve for x and y
    x_coordinate = (C * E - B * F) / det
    y_coordinate = (A * F - C * D) / det

    return (x_coordinate, y_coordinate)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        value = ser.readline()
        valueInString = value.decode('utf-8').strip()
        if valueInString:
            distances = valueInString.split(',')
            if len(distances) == 3:
                try:
                    # Convert to float to handle potential decimal values
                    d1 = float(distances[0])
                    d2 = float(distances[1])
                    d3 = float(distances[2])
                    
                    # Call the trilaterate function to get the coordinates
                    pos = trilaterate(d1, d2, d3)
                    
                    if pos:
                        x, y = pos
                        print(f"Coordinates: X={x:.2f}, Y={y:.2f}")

                        # Scale coordinates for Pygame visualization
                        # y is inverted because Pygame's y-axis points down
                        pygame_x = int(x * SCALE)
                        pygame_y = int(SCREEN_HEIGHT - (y * SCALE))
                        
                        path.append((pygame_x, pygame_y))

                except ValueError:
                    print("Could not convert distance to number")
            else:
                print(f"Received an incomplete line: {valueInString}")
    except Exception as e:
        print(f"Error reading from serial: {e}")
        
    # Pygame drawing logic
    screen.fill((255, 255, 255)) # White background
    
    # Draw a line path
    if len(path) > 1:
        pygame.draw.lines(screen, (0, 100, 255), False, path, 2)
    
    # Draw the current position as a red circle
    if path:
        pygame.draw.circle(screen, (255, 0, 0), path[-1], 6)
        
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
ser.close()
sys.exit()