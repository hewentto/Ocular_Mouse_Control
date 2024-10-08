import sys
import pygame
import pygame_gui
from pygame.locals import *
import User_select_MouSee
import Training_page_MouSee
import Interactive_Mode

def main_menu(window_surface,user):
    pygame.init()

    # pygame.mixer.init()


    # pygame.mixer.music.set_volume(0.1)
    # pygame.mixer.music.play(-1)
    
    width = 900
    height = 600 

    # Colors
    yellow=(255, 255, 0)
    grey = (235, 235, 235)

    # pygame.display.set_caption('MouSee')

    background = pygame.Surface((width, height))
    background.fill('grey')

    level_manager = pygame_gui.UIManager((width, height))

    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, False, textColor)

        return newText
    

    title = text_format("What would you like to do?", None, 70, 'blue')

    title_rect = title.get_rect()
    button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2 - 90, height/4), (200, 50)), text='Training Mode', manager=level_manager)
    button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2 - 90, height/4 + 80), (200, 50)), text='Interactive Mode', manager=level_manager)
    button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2 - 50, height/4 + 160), (125, 50)), text='Go Back', manager=level_manager)

    # Background image
    background_image = pygame.image.load("eyeball.png").convert()

    clock = pygame.time.Clock()
    is_running = True

    # activeDictionary = dic.adddictanswer
    # activeProblem = dic.adddictprob

    #user input logic
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                sys.exit()
            if event.type == USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    navigate = pygame.mixer.Sound('sound/navigating_menu.ogg')
                    navigate.play()
                    if event.ui_element == button1:
                        Training_page_MouSee.training(window_surface,1,user)
                    if event.ui_element == button2:
                        Training_page_MouSee.training(window_surface,2,user)
                    if event.ui_element == button3:
                        User_select_MouSee.user_select(window_surface,None)

                        
            

            level_manager.process_events(event)

            level_manager.update(time_delta)

            #render screen
            window_surface.fill(grey)
            window_surface.blit(background_image, [150, 0])
            window_surface.blit(title, (width/2 - (title_rect[2]/2), 50))
            level_manager.draw_ui(window_surface)

        pygame.display.update()

