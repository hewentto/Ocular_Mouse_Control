import pygame, sys
import pygame_gui
from pygame.locals import *
from pygame import mixer
import User_select_MouSee



def start_page(window_surface):
    
    # Game Initialization
    pygame.init()
    pygame.mixer.init()


    # # Center the  Application

    # Game Resolution
    screen_width = 900
    screen_height = 600

    pygame.display.set_caption('MouSee Ocular Mouse Control')

    # Background imgae
    background_image = pygame.image.load("eyeball.png").convert()
    menu_manager = pygame_gui.UIManager((screen_width, screen_height))

    # Text Renderer
    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, False, textColor)

        return newText


    # Colors
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(235, 235, 235)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)

    # Game Fonts
    font = "Retro.ttf"


    # Game Framerate
    clock = pygame.time.Clock()
    FPS = 30

 

    click = False

    menu = True
    selected = "start"

    mx, my = pygame.mouse.get_pos()

    # UI elements
    title=text_format("Welcome to MouSee", None, 90, 'blue')
    text1=text_format("Press Enter to start", None, 25, 'blue')
    # text2=text_format("Start", None, 55, 'green')

    #UI element objects
    title_rect = title.get_rect()
    text1_rect = text1.get_rect()
    # text2_rect = text2.get_rect()

    # Main Menu Text
    window_surface.fill(gray)
    window_surface.blit(background_image, [150,0])
    window_surface.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
    window_surface.blit(text1, (screen_width/2 - (text1_rect[2]/2), 150))
    # window_surface.blit(text2, (screen_width/2 - (text2_rect[2]/2), 500))

    pygame.display.update()
    clock.tick(FPS)

    while menu:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected="start"
                elif event.key == pygame.K_DOWN:
                    selected="quit"
                if event.key == pygame.K_RETURN:
                    navigate = pygame.mixer.Sound('sound/navigating_menu.ogg')
                    navigate.play()
                    User_select_MouSee.user_select(window_surface,None)
#Initialize the Game
