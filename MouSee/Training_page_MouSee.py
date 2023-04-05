import pygame
import pygame_gui
from pygame.locals import *
from pygame import mixer
import sys
import ctypes
import CircleClass
import Main_menu_MouSee
import End_screen
import Calibration_complete
import eye_tracking_test
import parse_test

import cv2 as cv
import mediapipe as mp
from pynput.mouse import Button, Controller, Listener
import threading
import csv
import math


#################################################################
#################################################################

def training(window_surface,mode,user):
    # pygame.init()

    # pygame.mixer.init()


    eye_tracking_test.run(window_surface,mode,user)


    # # Colors
    # white=(255, 255, 255)
    # black=(0, 0, 0)
    # gray=(50, 50, 50)
    # red=(255, 0, 0)
    # green=(0, 255, 0)
    # blue=(0, 0, 255)
    # yellow=(255, 255, 0)

    # pygame.display.set_caption('MouSee Training')
    # pygame.display.set_mode((0,0),pygame.RESIZABLE)
    # if sys.platform == "win32":
    #     HWND = pygame.display.get_wm_info()['window']
    #     SW_MAXIMIZE = 3
    #     ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

    # infoObject = pygame.display.Info()
    # width = infoObject.current_w
    # height = infoObject.current_h
    
    # background = pygame.Surface((infoObject.current_w, infoObject.current_h))
    # background.fill((235, 235, 235))

    # game_manager = pygame_gui.UIManager((infoObject.current_w, infoObject.current_h))

    # def text_format(message, textFont, textSize, textColor):
    #     newFont = pygame.font.Font(textFont, textSize)
    #     newText = newFont.render(message, False, textColor)

    #     return newText
    # font = "Retro.ttf"

    # score = 0



    # title = text_format("Click the Red dots", None, 60, black)
    # # displayProblem = text_format("", font, 90, black)
    # title_rect = title.get_rect()
    # # problem_rect = displayProblem.get_rect()

    # main_menu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width//2 - 50, 70), (100, 50)), text='Main Menu', manager=game_manager)

    # # # Background image
    # background_image = pygame.image.load("eyeball.png").convert()

    # # #circles
    # number_circles = 5
    # circles = [CircleClass.Circle(i,window_surface,mode) for i in range(number_circles)]

    # clock = pygame.time.Clock()
    # is_running = True


    # delThis = False
    # indexToDelete = 0
    # index_calibrate = 0

    # if mode == 2:
    #     pygame.mixer.music.load("sound/gameplay_music.ogg")
    #     pygame.mixer.music.set_volume(0.1)
    #     pygame.mixer.music.play(-1)
    
    # # problemsListLength = 5
    # reload = pygame.mixer.Sound('sound/gun_click.ogg')




    #EYE TRACKING INITIALIZATION
    ####################################################
    
    # while is_running:

    #     # eye_tracking_test.run(width, height)

        
    # #    renderText = pygame.font.SysFont("Retro.ttf", 50).render(str(score), True, yellow)
    #     window_surface.fill((235,235,235))
    #     window_surface.blit(background_image, [infoObject.current_w//2 - 300, infoObject.current_h//2 - 300])
    #     window_surface.blit(title, (infoObject.current_w//2 - 175, 20))
    # #    window_surface.blit(renderText,(800, 20))

    #     time_delta = clock.tick(60)/1000.0

    #     #draw circles all at once
    #     if mode != 0:
    #         for k in range(len(circles)):
    #             circles[k].draw()
    #             if mode == 2:
    #                 circles[k].mover()

    #     #if calibration mode draw one at a time
    #     if mode == 0:
    #         calibrate_circle = CircleClass.Circle(index_calibrate,window_surface,mode)
    #         calibrate_circle.draw()

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             is_running = False
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             shoot = pygame.mixer.Sound('sound/gun_shot.ogg')
    #             shoot.play()
    #             mouseLocation = pygame.mouse.get_pos()
    #             for k in range(len(circles)):
    #                 #if click within hitbox of circle
    #                 if mouseLocation[0] >= circles[k].x-11 and mouseLocation[0] <= circles[k].x+11:
    #                     if mouseLocation[1] >= circles[k].y-11 and mouseLocation[1] <= circles[k].y+11:
    #                         # print(circles[k].index)

    #                         indexToDelete = k
    #                         delThis = True
    #                         score += 1
    #                         number_circles -= 1
    #                         if mode == 0:
    #                             index_calibrate+= 1
    #                         # print(number_circles)

    #                         if number_circles == 0 and mode!= 0:
    #                             End_screen.endScreen(score, window_surface,mode)
    #                         elif number_circles == 0:
    #                             Calibration_complete.cal_complete(window_surface, 0)

    #             reload.play()       
    #         #main menu navigation                     
    #         if event.type == USEREVENT:
    #             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
    #                 navigate = pygame.mixer.Sound('sound/navigating_menu.ogg')
    #                 navigate.play()
    #                 if event.ui_element == main_menu:
    #                     Main_menu_MouSee.main_menu(window_surface)

    #         #delete circle if clicked
    #         if delThis:
    #             # print(f'deleting circle index {indexToDelete}')
    #             del circles[indexToDelete]
    #             delThis = False

    #         game_manager.process_events(event)
    #         game_manager.update(time_delta) 

    #     game_manager.draw_ui(window_surface)

    #     pygame.display.update()
