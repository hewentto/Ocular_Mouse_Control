import sys
import pygame
import pygame_gui
from pygame.locals import *
from pygame import mixer
from os import  path
import Main_menu_MouSee

def cal_complete(window_surface, mode,user):
    pygame.init()

    pygame.mixer.init()

    pygame.mixer.music.load("sound/level_completed.ogg")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    
    width = 900
    height = 600 

    # Colors
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(50, 50, 50)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)

    pygame.display.set_caption('MouSee Ocular Mouse Control')
    window_surface = pygame.display.set_mode((width, height))

    end_manager = pygame_gui.UIManager((width, height))

    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, False, textColor)

        return newText
    
    subtitle = text_format("initialize", None, 90, blue)

    if mode == 2:
        title = text_format("GAME OVER", None, 90, blue)
        subtitle = text_format("You Win!", None, 90, blue)
    elif mode == 1:
        title = text_format("Training Completed", None, 90, blue)
    else:
        title = text_format("Calibration Completed", None, 90, blue)


    title_rect = title.get_rect()
    subtitle_rect = subtitle.get_rect()

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width//2 - 75, 100), (150, 50)),
                                                text='Continue',
                                                manager=end_manager)
    
    
    #Scoring section below can be used in future additions

    # yourScore = text_format("Your Score", None, 40, blue)
    # yourScore_rect = yourScore.get_rect()

    # newScore = text_format(str(score), None, 50, blue)
    # newHighscore = text_format(str(score), None, 50, blue)

    # highscoreLabel = text_format("Highscore", None, 40, blue)
    # highscore_rect = yourScore.get_rect()

    # file = open("highscore.txt", "r")

    # highscore = int(file.read())

    # file.close()


    # if score > highscore:
    #     file = open("highscore.txt",'w')
    #     file.write(str(score))
    #     file.close()
        
                                            
    # Background image
    background_image = pygame.image.load("eyeball.png").convert()

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                sys.exit()
                
            end_manager.process_events(event)

            end_manager.update(time_delta)
            if event.type == USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        navigate = pygame.mixer.Sound('sound/navigating_menu.ogg')
                        navigate.play()
                        if event.ui_element == back_button:
                            Main_menu_MouSee.main_menu(window_surface,user)

        window_surface.fill((235,235,235))    
        window_surface.blit(background_image, [150, 0])
        window_surface.blit(title, (width/2 - (title_rect[2]/2), 50))
        if mode == 2:
            window_surface.blit(subtitle, (width/2 - (subtitle_rect[2]/2), 125))
        # window_surface.blit(yourScore, (275, height/3))
        # window_surface.blit(newScore, (335, height/2))
        # window_surface.blit(highscoreLabel,(475,height/3))
        # window_surface.blit(newHighscore, (535, height/2))

        end_manager.draw_ui(window_surface)

        pygame.display.update()
