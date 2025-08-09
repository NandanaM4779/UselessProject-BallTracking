import sys
import math
import serial
import time
import pygame
import random

# Serial settings
SERIAL_PORT = 'COM7'
BAUD_RATE = 115200

# Pygame screen settings for visualization
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCALE = 15 # A fixed scale is better if your sensor coords are non-standard

# Sensor positions (adjust to match your physical setup)
# This places them at the bottom-left, bottom-right, and top-middle
x0, y0 = 0.0, SCREEN_HEIGHT / SCALE
x1, y1 = SCREEN_WIDTH / SCALE, SCREEN_HEIGHT / SCALE
x2, y2 = SCREEN_WIDTH / (2 * SCALE), 0.0

try:
    leo_images = [ pygame.image.load("C:\\Users\\HP\\Downloads\\Leonardo_DiCaprio_Laughing.jpg")]
    # Pick a random image at the start of the program
    leo_image = random.choice(leo_images)
    leo_image = pygame.transform.scale(leo_image, (40, 40)) # Scale it to a good size
except pygame.error:
    print("Warning: Could not load Leonardo DiCaprio images. Using a simple dot.")
    leo_image=None

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def trilaterate(d1, d2, d3):
    """
    Calculates the (x, y) coordinates of an object
    given three distances and three known sensor positions.
    """
    A = 2 * (x1 - x0)
    B = 2 * (y1 - y0)
    C = d1**2 - d2**2 - x0**2 + x1**2 - y0**2 + y1**2
    D = 2 * (x2 - x1)
    E = 2 * (y2 - y1)
    F = d2**2 - d3**2 - x1**2 + x2**2 - y1**2 + y2**2

    det = A * E - B * D
    if det == 0:
        return None

    x_coordinate = (C * E - B * F) / det
    y_coordinate = (A * F - C * D) / det

    return (x_coordinate, y_coordinate)

def draw_sensor_layout(screen, SCALE):
    """Draws a visual representation of the sensor layout."""
    font = pygame.font.Font(None, 24)
    s0_x, s0_y = int(x0 * SCALE), int(SCREEN_HEIGHT - (y0 * SCALE))
    s1_x, s1_y = int(x1 * SCALE), int(SCREEN_HEIGHT - (y1 * SCALE))
    s2_x, s2_y = int(x2 * SCALE), int(SCREEN_HEIGHT - (y2 * SCALE))

    # Draw circles for each sensor
    pygame.draw.circle(screen, GREEN, (s0_x, s0_y), 5)
    pygame.draw.circle(screen, GREEN, (s1_x, s1_y), 5)
    pygame.draw.circle(screen, GREEN, (s2_x, s2_y), 5)

    # Add text labels for sensor positions
    text0 = font.render(f"({x0}, {y0})", True, GREEN)
    text1 = font.render(f"({x1}, {y1})", True, GREEN)
    text2 = font.render(f"({x2}, {y2})", True, GREEN)
    screen.blit(text0, (s0_x + 10, s0_y))
    screen.blit(text1, (s1_x + 10, s1_y))
    screen.blit(text2, (s2_x + 10, s2_y))

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Successfully connected to Arduino on {SERIAL_PORT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wheres the ball")
    clock = pygame.time.Clock()
    path = []
    
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
                        d1 = float(distances[0])
                        d2 = float(distances[1])
                        d3 = float(distances[2])
                        pos = trilaterate(d1, d2, d3)

                        if pos:
                            x, y = pos
                            print(f"Coordinates: X={x:.2f}, Y={y:.2f}")

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
        screen.fill(BLACK)
        draw_sensor_layout(screen, SCALE)
        
        # Draw a colorful trail of dots
        for i, pos_on_screen in enumerate(path):
            dot_color = (int(255 * (i % 3) / 2), int(255 * ((i+1) % 3) / 2), int(255 * ((i+2) % 3) / 2))
            pygame.draw.circle(screen, dot_color, pos_on_screen, 3)

        if path:
            pygame.draw.circle(screen, RED, path[-1], 6)
        
        pygame.display.flip()
        clock.tick(30)

except serial.SerialException as e:
    print(f"Could not open serial port {SERIAL_PORT}. Check connection. Error: {e}")
    sys.exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit()
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    if pygame.get_init():
        pygame.quit()
    sys.exit()