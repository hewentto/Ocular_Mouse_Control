# Circle class to be implemented in game
import random
import time

import pygame
import pygame_gui
# import circle_positions as cp

font = "Retro.ttf"



class Circle:
    pygame.init()

    infoObject = pygame.display.Info()

    width = infoObject.current_w
    height = infoObject.current_h 

    calibration_positions_x = [
        20, #topleft and bottom left
        width - 20, #topright and bottom right
        width // 2 # middle
    ]
    calibration_positions_y = [
        20, #topleft and topright
        height - 100, #bottom left  and bottom right
        height // 2 # middle
    ]
    
    def __init__(self, index, screen,mode):
        self.index = index
        self.screen = screen
        self.mode = mode
        self.color = 'red'
        self.clicked = False



        if self.mode == 0: #calibration
            if self.index == 0: #middle
                self.x = Circle.calibration_positions_x[2]
                self.y = Circle.calibration_positions_y[2]
            if self.index == 1:#topright
                self.x = Circle.calibration_positions_x[1]
                self.y = Circle.calibration_positions_y[0]
            if self.index == 2:#topleft
                self.x = Circle.calibration_positions_x[0]
                self.y = Circle.calibration_positions_y[0]
            if self.index == 3: #bottomleft
                self.x = Circle.calibration_positions_x[0]
                self.y = Circle.calibration_positions_y[1]
            if self.index == 4: #bottomright
                self.x = Circle.calibration_positions_x[1]
                self.y = Circle.calibration_positions_y[1]  

        if self.mode == 1: #Training
            self.x = random.randrange(20, Circle.width - 20, 1)
            self.y = random.randrange(20, Circle.height - 20, 1)

        if self.mode == 2: # Interactive
            # creats random direction and speed for the object
            self.x = random.randrange(20, Circle.width - 20, 1)
            self.y = random.randrange(20, Circle.height - 20, 1)
            self.vx = random.randrange(-3, 3, 1)
            self.vy = random.randrange(-3, 3, 1)
            if self.vx == 0:
                self.vx = random.randrange(-3, 3, 1)
            elif self.vy == 0:
                self.vy = random.randrange(-3, 3, 1)


        # print(f'I am a circle with index {self.index}')



    def draw(self):
        # renderText = pygame.font.SysFont(font, 20).render(self.equation, True, self.color)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 15)
        self.rect = self.screen.get_rect()
        # self.screen.blit(self.rect, (self.x + 38, self.y + 75))

        #pygame.draw.rect(self.screen, (255, 255, 255), self.hitbox, 1)

    def draw_calibrate(self):

        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 15)
        self.rect = self.screen.get_rect()


    def mover(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= Circle.width:
            self.vx *= -1
            self.x = Circle.width
        if self.x <= 0:
            self.vx *= -1
            self.x = 0
        if self.y >= Circle.height:
            self.vy *= -1
            self.y = Circle.height
        if self.y <= 0:
            self.vy *= -1
            self.y = 0

        # Update the hit box location
        # self.hitbox.update(self.x, self.y, self.size[0], self.size[1])


