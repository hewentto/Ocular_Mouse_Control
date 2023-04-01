import pygame, sys
import pygame_gui
from pygame.locals import *
from pygame import mixer
import User_select_MouSee



def new_user(window_surface):
    
    pygame.init()
  
    clock = pygame.time.Clock()
    
    # it will display on screen
    window_surface = pygame.display.set_mode([900, 600])
    
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''

    width = 900
    height = 600 

    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, False, textColor)

        return newText
    
    level_manager = pygame_gui.UIManager((width, height))
    
    # create rectangle
    username = text_format('New Username', None, 50, 'blue')
    input_rect1 = pygame.Rect(200, 200, 340, 32)
    input_rect2 = pygame.Rect(200, 300, 340, 32)
    button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2 - 250, height/4 + 100), (125, 50)), text='Submit', manager=level_manager)
    button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2 + 50, height/4 + 100), (125, 50)), text='Go Back', manager=level_manager)

    title = text_format("Create New User", None, 90, 'blue')

    title_rect = title.get_rect()
    user_rect = username.get_rect()
    
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')
    
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    color1 = color_passive
    color2 = color_passive
    
    active1 = False
    active2 = False
    
    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
    
        # if user types QUIT then the window_surface will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            level_manager.process_events(event)

            level_manager.update(time_delta)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect1.collidepoint(event.pos):
                    active1 = True
                else:
                    active1 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect2.collidepoint(event.pos):
                    active2 = True
                else:
                    active2 = False
    
            if event.type == pygame.KEYDOWN:
    
                # Check for backspace
                if event.key == pygame.K_BACKSPACE and active1:
    
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode


            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                navigate = pygame.mixer.Sound('sound/navigating_menu.ogg')
                navigate.play()
                if event.ui_element == button1:
                    User_select_MouSee.user_select(window_surface,user_text)
                if event.ui_element == button2:
                    User_select_MouSee.user_select(window_surface,None)

        
        # it will set background color of window_surface
        window_surface.fill((235, 235, 235))
    
        if active1:
            color1 = color_active
            color2 = color_passive
        elif active2:
            color2 = color_active
            color1 = color_passive
        else:
            color1 = color_passive
            color2 = color_passive
            
        # draw rectangle and argument passed which should
        # be on window_surface
        pygame.draw.rect(window_surface, color1, input_rect1)
        # pygame.draw.rect(window_surface, color2, input_rect2)
    
        text_surface = base_font.render(user_text, True, (255, 255, 255))

        
        # render at position stated in arguments
        window_surface.blit(title, (900/2 - (title_rect[2]/2), 50))
        window_surface.blit(username, (input_rect1.x, input_rect1.y-35))
        window_surface.blit(text_surface, (input_rect1.x+5, input_rect1.y+5))
        level_manager.draw_ui(window_surface)
        # window_surface.blit(text_surface, (input_rect2.x+5, input_rect2.y+5))
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect1.w = max(100, text_surface.get_width()+10)
        # input_rect2.w = max(100, text_surface.get_width()+10)
        
        # display.flip() will update only a portion of the
        # window_surface to updated, not full area
        pygame.display.flip()
        
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)