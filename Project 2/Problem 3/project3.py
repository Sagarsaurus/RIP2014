import pygame, math, numpy

# initialize pygame
pygame.init()

# Define some colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 191, 255)

# Set the width and height of the screen [width, height]
size = (640, 480)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Project 3")

done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

offset_x = 70
offset_y = 70
scale_factor = 20

# l_i * cos (q_i), l_i * sin (q_i)
# l_1, l_2, l_3 = 2, 2, 1
# q_1, q_2, q_3 =
# jacobian = numpy.mat([[1, 2], [3, 4]])
# print jacobian

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    angle_1 = 0.785
    angle_2 = angle_1 - 0.785
    angle_3 = 0.785

    # --- Game logic should go here
    first_circle_loc = (offset_x + 0, offset_y - 0)
    second_circle_loc = (int(first_circle_loc[0] + (2 * scale_factor * math.cos(angle_1))),
                         int(first_circle_loc[1] - (2 * scale_factor * math.sin(angle_1))))
    third_circle_loc = (int(second_circle_loc[0] + (2 * scale_factor * math.cos(angle_2))),
                        int(second_circle_loc[1] - (2 * scale_factor * math.sin(angle_2))))
    fourth_circle_loc = (int(third_circle_loc[0] + (2 * scale_factor * math.cos(angle_3))),
                         int(third_circle_loc[1] - (2 * scale_factor * math.sin(angle_3))))

    # ARMS
    arm_1_start, arm_1_end = (first_circle_loc, second_circle_loc)
    arm_2_start, arm_2_end = (second_circle_loc, third_circle_loc)
    arm_3_start, arm_3_end = (third_circle_loc, fourth_circle_loc)

# --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    #Circles
    pygame.draw.circle(screen, RED, first_circle_loc, 5, 0)
    pygame.draw.circle(screen, RED, second_circle_loc, 5, 0)
    pygame.draw.circle(screen, RED, third_circle_loc, 5, 0)
    pygame.draw.circle(screen, RED, fourth_circle_loc, 5, 0)

    #Arms
    pygame.draw.line(screen, BLUE, arm_1_start, arm_1_end, 5)
    pygame.draw.line(screen, BLUE, arm_2_start, arm_2_end, 5)
    pygame.draw.line(screen, BLUE, arm_3_start, arm_3_end, 5)


# --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()