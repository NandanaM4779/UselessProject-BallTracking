import serial
import pygame
import sys
import time

# Serial settings (change COM port as needed)
SERIAL_PORT = 'COM7'
BAUD_RATE = 9600

# Pygame screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Setup serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Give the connection time to establish
    print(f"Successfully connected to Arduino on {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Could not open serial port {SERIAL_PORT}. Check connection. Error: {e}")
    sys.exit()

# Setup Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ultrasonic Sensor Path")
clock = pygame.time.Clock()

# List to store the history of path points
path_points = []
# Maximum number of points to keep in the path
MAX_PATH_POINTS = 500

def get_distance():
    """Reads a single distance value from the serial port."""
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            return float(line)
    except Exception as e:
        pass
    return None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    distance = get_distance()

    screen.fill((255, 255, 255))  # Clear screen with white background

    if distance is not None:
        # Map the distance value to a Y-coordinate on the screen
        # We invert the value so that closer objects appear higher on the screen
        mapped_y = int(SCREEN_HEIGHT - (distance / 200.0) * SCREEN_HEIGHT)

        # Add the new point to our list
        # We use the current path length as the X-coordinate
        new_point = (len(path_points), mapped_y)
        path_points.append(new_point)

        # Keep the path from growing indefinitely
        if len(path_points) > MAX_PATH_POINTS:
            path_points.pop(0)
    
    # If there are at least two points, draw a line connecting them
    if len(path_points) > 1:
        # Transform points to fit the screen as they move
        display_points = []
        path_length = len(path_points)
        for i, point in enumerate(path_points):
            x = (i / path_length) * SCREEN_WIDTH
            display_points.append((x, point[1]))

        pygame.draw.lines(screen, (0, 100, 255), False, display_points, 2)
        
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 FPS

pygame.quit()
ser.close()