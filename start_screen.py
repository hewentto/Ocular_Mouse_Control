import pygame
import os
import sys
import pygame_button as Button
import random
# create a ui screen that takes up whole screen
# create a button that says "start"
# when button is clicked, start the game


# create screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# display screen until x is pressed
running = True
while running:
    # fill screen with white
    screen.fill((255,255,255))
    for event in pygame.event.get():
        # check if x is pressed
        if event.type == pygame.QUIT:
            # quit
            pygame.quit()
            sys.exit()
        # if escape key is pressed quit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    # update screen
    pygame.display.update()