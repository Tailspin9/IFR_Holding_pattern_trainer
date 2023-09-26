import pygame
from pygame.locals import *
import math
import random
import pygame.math as pgmath

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Holds Trainer')
font = pygame.font.Font(None,36)


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


# Initial aircraft state
center_x, center_y = WIDTH // 2, HEIGHT // 2
edge = random.choice(["top", "bottom", "left", "right"])

if edge == "top":
    start_x = random.uniform(0, WIDTH)
    start_y = 0
elif edge == "bottom":
    start_x = random.uniform(0, WIDTH)
    start_y = HEIGHT
elif edge == "left":
    start_x = 0
    start_y = random.uniform(0, HEIGHT)
elif edge == "right":
    start_x = WIDTH
    start_y = random.uniform(0, HEIGHT)

delta_x = center_x - start_x
delta_y = center_y - start_y
aircraft_angle = math.degrees(math.atan2(delta_x, -delta_y))

aircraft_pos = [start_x, start_y]  # Direction in degrees, with 0 being up
aircraft_speed = 0.002
turn_speed = 0.0015  # Degrees per frame
acceleration = 0.00000001
max_speed = 0.035
min_speed = 0

pixels = []
pixel_gravity = 0.0001
disintegrated = False

def has_collided(pos):
    return pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT

def generate_pixels_for_line(start, end, thickness):
    pixels_for_line = []
    dx, dy = end[0] - start[0], end[1] - start[1]
    distance = int(math.sqrt(dx*dx + dy*dy))
    for i in range(distance):
        t = i / distance
        pixel_x = int(start[0] + t * dx)
        pixel_y = int(start[1] + t * dy)
        for j in range(-thickness // 2, thickness // 2):
            for k in range(-thickness // 2, thickness // 2):
                random_velocity_x = random.uniform(-0.5, 0.1)
                random_velocity_y = random.uniform(-2, 2)
                pixels_for_line.append([[pixel_x + j, pixel_y + k], [random_velocity_x, random_velocity_y]])
    return pixels_for_line

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen):
        # Change color if mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Add text to the button
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) / 2,
                                   self.y + (self.height - text_surface.get_height()) / 2))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height

restart_button = Button(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50, "Restart", (0, 128, 0), (0, 255, 0))
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
triangle_color = GREEN
triangle_touched = False


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if disintegrated and restart_button.is_clicked():
                # Reset everything
                aircraft_pos = [WIDTH // 2, HEIGHT // 2]
                aircraft_angle = 0
                aircraft_speed = 0.02
                pixels = []
                disintegrated = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        aircraft_angle -= turn_speed
    if keys[pygame.K_RIGHT]:
        aircraft_angle += turn_speed
    if keys[pygame.K_UP]:
        aircraft_speed += acceleration
        if aircraft_speed > max_speed:
            aircraft_speed = max_speed
    if keys[pygame.K_DOWN]:
        aircraft_speed -= acceleration
        if aircraft_speed < min_speed:
            aircraft_speed = min_speed


    # Update aircraft position based on direction and speed
    dx = aircraft_speed * math.sin(math.radians(aircraft_angle))
    dy = -aircraft_speed * math.cos(math.radians(aircraft_angle))
    aircraft_pos[0] += dx
    aircraft_pos[1] += dy

    screen.fill(WHITE)
    GREEN = (0, 255, 0)
    PURPLE = (148, 0, 211)
    s = 10
    cx, cy = WIDTH // 2, HEIGHT // 2
    half_height = math.sqrt(3) * s / 2
    vertex1 = (cx, cy - half_height)
    vertex2 = (cx - s / 2, cy + half_height)
    vertex3 = (cx + s / 2, cy + half_height)

    # Define the holding pattern parameters
    straight_path_length = 200  # The length of the straight path in the holding pattern
    arc_radius = straight_path_length // 2  # The radius of each arc is half the length of the straight path

    # Calculate the center points for the arcs
    left_arc_center = (cx - straight_path_length, cy)
    right_arc_center = (cx + straight_path_length, cy)



    # Update the top and bottom arc center
    bottom_arc_center = (cx, cy + arc_radius)
    top_arc_center = (cx, cy - arc_radius)

    # Calculate the start and end points for the straight paths
    left_straight_start = (cx - arc_radius, bottom_arc_center[1])
    left_straight_end = (cx - arc_radius, top_arc_center[1])

    right_straight_start = (cx + arc_radius, bottom_arc_center[1])
    right_straight_end = (cx + arc_radius, top_arc_center[1])

    # Draw the arcs and the straight paths
    #pygame.draw.arc(screen, BLACK,(left_arc_center[0] - arc_radius, left_arc_center[1] - arc_radius, 2 * arc_radius, 2 * arc_radius),0, math.pi, 2)
    pygame.draw.arc(screen, BLACK, (
    bottom_arc_center[0] - arc_radius, bottom_arc_center[1] - arc_radius, 2 * arc_radius, 2 * arc_radius), math.pi,
                    2 * math.pi, 2)
    pygame.draw.arc(screen, BLACK,
                    (top_arc_center[0] - arc_radius, top_arc_center[1] - arc_radius, 2 * arc_radius, 2 * arc_radius), 0,
                    math.pi, 2)  # Correctly flipped the top arc
    pygame.draw.line(screen, BLACK, left_straight_start, left_straight_end, 2)
    pygame.draw.line(screen, BLACK, right_straight_start, right_straight_end, 2)

    # Calculate the triangle vertices based on current position and direction
    cross_length_horizontal = 60
    cross_length_vertical = 40
    cross_thickness = 2
    horizontal_offset = 10
    vert_start = (
        aircraft_pos[0] - cross_length_vertical // 2 * math.sin(math.radians(aircraft_angle)),
        aircraft_pos[1] + cross_length_vertical // 2 * math.cos(math.radians(aircraft_angle))
    )
    vert_end = (
        aircraft_pos[0] + cross_length_vertical // 2 * math.sin(math.radians(aircraft_angle)),
        aircraft_pos[1] - cross_length_vertical // 2 * math.cos(math.radians(aircraft_angle))
    )

    # Calculate the offset position for the wings
    offset_x = aircraft_pos[0] + horizontal_offset * math.sin(math.radians(aircraft_angle))
    offset_y = aircraft_pos[1] - horizontal_offset * math.cos(math.radians(aircraft_angle))

    # For the wings, the changes in x and y should be based on the angle perpendicular to the current direction
    horiz_start = (
        offset_x - cross_length_horizontal // 2 * math.cos(math.radians(aircraft_angle)),
        offset_y - cross_length_horizontal // 2 * math.sin(math.radians(aircraft_angle))
    )
    horiz_end = (
        offset_x + cross_length_horizontal // 2 * math.cos(math.radians(aircraft_angle)),
        offset_y + cross_length_horizontal // 2 * math.sin(math.radians(aircraft_angle))
    )
    aircraft_vec = pygame.math.Vector2(aircraft_pos[0], aircraft_pos[1])
    triangle_center = pygame.math.Vector2(cx, cy)
    dist = aircraft_vec.distance_to(triangle_center)
    inside_triangle = dist < half_height


    if not triangle_touched:
        aircraft_vec = pygame.math.Vector2(aircraft_pos[0], aircraft_pos[1])
        triangle_center = pygame.math.Vector2(cx, cy)
        dist = aircraft_vec.distance_to(triangle_center)
        inside_triangle = dist < half_height

        # If inside, change triangle color to PURPLE and set the flag to True
    if inside_triangle:
        triangle_color = PURPLE
        triangle_touched = True

    pygame.draw.polygon(screen, triangle_color, [vertex1, vertex2, vertex3])
    # Draw the cross (aircraft)
    kias = int(aircraft_speed * 90000)
    speed_text = font.render(f"KIAS: {kias} kts", True, (0, 0, 0))
    text_position = (WIDTH - speed_text.get_width() - 10, 10)

    if not disintegrated:
        pygame.draw.line(screen, BLUE, vert_start, vert_end, cross_thickness)
        pygame.draw.line(screen, BLUE, horiz_start, horiz_end, cross_thickness)
    else:
        aircraft_speed = 0.0

    if not disintegrated and has_collided(aircraft_pos):
        pixels.extend(generate_pixels_for_line(vert_start, vert_end, cross_thickness))
        pixels.extend(generate_pixels_for_line(horiz_start, horiz_end, cross_thickness))
        aircraft_speed = 0
        disintegrated = True

    for pixel in pixels:
        pixel[1][1] += pixel_gravity
        pixel[0][0] += pixel[1][0]
        pixel[0][1] += pixel[1][1]
        if pixel[0][1] > HEIGHT:
            pixel[0][1] = HEIGHT
            pixel[1][1] = 0
        pygame.draw.rect(screen, BLUE, (pixel[0][0], pixel[0][1], cross_thickness, cross_thickness))

    if disintegrated:
        restart_button.draw(screen)
        # Draw the text on the screen
    screen.blit(speed_text, text_position)
    pygame.display.flip()

pygame.quit()