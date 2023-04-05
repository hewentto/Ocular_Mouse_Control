import cv2 as cv
import mediapipe as mp
from pynput.mouse import Button, Controller, Listener
import parse_test
import pyautogui as pag
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

# Set the DeviceID of the camera
device_id = "USB\VID_1D6C&PID_1278&MI_00\8&1ACFF732&0&0000"

def initialize_face_mesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    return mp.solutions.face_mesh.FaceMesh( # type: ignore
        max_num_faces=max_num_faces,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence)

def initialize_mouse_listener(on_click):
    return Listener(on_click=on_click)

def start_mouse_listener(mouse_listener):
    mouse_listener.start()

def stop_mouse_listener(mouse_listener):
    mouse_listener.stop()

def get_landmarks(image, face_mesh):
    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    return results, image

def draw_landmarks(image, results):
    if not results.multi_face_landmarks:
        return None, None

    # Define parameters for drawing
    dot_radius = 2
    dot_thickness = -1
    line_thickness = 1
    line_color = (0, 255, 0)

    landmark_list = []

    # Draw the specified landmarks and lines
    nose_tip_landmark_index = 4
    # Define landmark indices for different regions of the face
    forehead_landmark_index = 10
    chin_landmark_index = 152
    left_cheek_landmark_index = 234
    right_cheek_landmark_index = 454
    center_radius = 3
    center_thickness = -1
    center_color = (255, 0, 0)
    labels = ['center_nose', 'center_left_eye', 'center_right_eye', 'nose_left_eye', 'nose_right_eye', 'left_right_eye', 'left_image_edge', 'right_image_edge']



    def extract_landmarks(face_landmarks, image_shape):
        landmark_labels = ['nose', 'left_eye', 'right_eye', 'forehead', 'chin', 'left_cheek', 'right_cheek', 'center']
        landmark_dict = {}

        nose_x, nose_y, nose_z = face_landmarks.landmark[nose_tip_landmark_index].x * image_shape[1], \
                                face_landmarks.landmark[nose_tip_landmark_index].y * image_shape[0], \
                                face_landmarks.landmark[nose_tip_landmark_index].z
        landmark_dict[landmark_labels[0]] = (nose_x, nose_y, nose_z)

        left_eye_x, left_eye_y, left_eye_z = face_landmarks.landmark[473].x * image_shape[1], \
                                            face_landmarks.landmark[473].y * image_shape[0], \
                                            face_landmarks.landmark[473].z
        landmark_dict[landmark_labels[1]] = (left_eye_x, left_eye_y, left_eye_z)

        right_eye_x, right_eye_y, right_eye_z = face_landmarks.landmark[468].x * image_shape[1], \
                                                face_landmarks.landmark[468].y * image_shape[0], \
                                                face_landmarks.landmark[468].z
        landmark_dict[landmark_labels[2]] = (right_eye_x, right_eye_y, right_eye_z)

        additional_landmark_indices = {
            landmark_labels[3]: forehead_landmark_index,
            landmark_labels[4]: chin_landmark_index,
            landmark_labels[5]: left_cheek_landmark_index,
            landmark_labels[6]: right_cheek_landmark_index
        }

        for label, index in additional_landmark_indices.items():
            x, y, z = face_landmarks.landmark[index].x * image_shape[1], \
                    face_landmarks.landmark[index].y * image_shape[0], \
                    face_landmarks.landmark[index].z * image_shape[0]
            landmark_dict[label] = (x, y, z)

        center_x = sum(x for x, y, z in landmark_dict.values()) / len(landmark_dict)
        center_y = sum(y for x, y, z in landmark_dict.values()) / len(landmark_dict)
        center_z = sum(z for x, y, z in landmark_dict.values()) / len(landmark_dict)

        landmark_dict[landmark_labels[7]] = (center_x, center_y, center_z)

        return landmark_dict


    for face_landmarks in results.multi_face_landmarks:

        landmark_dict = extract_landmarks(face_landmarks, image.shape)

        # Draw a circle at the calculated center of the head
        center_x, center_y, _ = landmark_dict['center']
        # cv.circle(image, (int(center_x), int(center_y)), center_radius, center_color, center_thickness)

        # Draw lines from center of head to nose and eyes
        nose_x, nose_y, _ = landmark_dict['nose']
        left_eye_x, left_eye_y, _ = landmark_dict['left_eye']
        right_eye_x, right_eye_y, _ = landmark_dict['right_eye']


        cv.line(image, (int(center_x), int(center_y)), (int(nose_x), int(nose_y)), line_color, line_thickness)
        cv.line(image, (int(center_x), int(center_y)), (int(left_eye_x), int(left_eye_y)), line_color, line_thickness)
        cv.line(image, (int(center_x), int(center_y)), (int(right_eye_x), int(right_eye_y)), line_color, line_thickness)

        # Draw lines for nose and eye landmarks
        cv.line(image, (int(nose_x), int(nose_y)), (int(left_eye_x), int(left_eye_y)), line_color, line_thickness)
        cv.line(image, (int(nose_x), int(nose_y)), (int(right_eye_x), int(right_eye_y)), line_color, line_thickness)
        cv.line(image, (int(left_eye_x), int(left_eye_y)), (int(right_eye_x), int(right_eye_y)), line_color, line_thickness)

        # Line from eyes to edge of screen
        cv.line(image, (int(left_eye_x), int(left_eye_y)), (image.shape[1], int(left_eye_y)), line_color, line_thickness)
        cv.line(image, (int(right_eye_x), int(right_eye_y)), (0, int(right_eye_y)), line_color, line_thickness)

    return landmark_dict #type: ignore 


# Define the main function
def run(window_surface,mode,user):
    #############################################
    pygame.init()

    pygame.mixer.init()
    



    ##############################################
    # Define the screen size
    # screen_width = 1920
    # screen_height = 1080

    # Initialize the face mesh
    face_mesh = initialize_face_mesh()

    # # Define a function to be called when the mouse is clicked
    # def on_click(x, y, button, pressed):
    #     if button == Button.left and pressed:
    #         # Print the position of the mouse click
    #         print(f"Left button of the mouse is clicked - position ({x}, {y})")

    #         # If landmark_dict and distance_dict are not None, call parse.arrange_data
    #         if landmark_dict and distance_dict is not None:
    #             parse_test.arrange_data(landmark_dict, distance_dict, width, height, x, y)

    # # Create a mouse controller and initialize a mouse listener

    # mouse = Controller()
    # mouse_listener = initialize_mouse_listener(on_click)

    # # Create a thread for the mouse listener and start it
    # mouse_thread = threading.Thread(target=start_mouse_listener, args=(mouse_listener,))
    # mouse_thread.start()

    # Initialize the camera
    cap = cv.VideoCapture(int(device_id.split("&")[-1], 16))
    ####################################################################

    # Colors
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(50, 50, 50)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)

    pygame.display.set_caption('MouSee Training')
    pygame.display.set_mode((0,0),pygame.RESIZABLE)
    if sys.platform == "win32":
        HWND = pygame.display.get_wm_info()['window']
        SW_MAXIMIZE = 3
        ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

    infoObject = pygame.display.Info()
    width = infoObject.current_w
    height = infoObject.current_h

    test_width = 1920
    test_height = 1080

    print(f'w = {width}')
    print(f'h = {height}')

    background = pygame.Surface((infoObject.current_w, infoObject.current_h))
    background.fill((235, 235, 235))

    game_manager = pygame_gui.UIManager((infoObject.current_w, infoObject.current_h))

    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, False, textColor)

        return newText
    font = "Retro.ttf"

    score = 0



    title = text_format("Click the Red dots", None, 90, blue)
    subtitle = text_format("Make sure to look where you click to properly train the model", None, 60, blue)
    # displayProblem = text_format("", font, 90, black)
    title_rect = title.get_rect()
    subtitle_rect = subtitle.get_rect()
    # problem_rect = displayProblem.get_rect()

    main_menu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width//2 - 50, 150), (100, 50)), text='Main Menu', manager=game_manager)

    # # Background image
    background_image = pygame.image.load("eyeball.png").convert()

    # #circles
    number_circles = 5
    circles = [CircleClass.Circle(i,window_surface,mode) for i in range(number_circles)]

    clock = pygame.time.Clock()
    is_running = True


    delThis = False
    indexToDelete = 0
    index_calibrate = 0

    if mode == 2:
        pygame.mixer.music.load("sound/gameplay_music.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    
    # problemsListLength = 5
    reload = pygame.mixer.Sound('sound/gun_click.ogg')
    ####################################################################

    # Loop until the 'q' key is pressed
    while True:

        # Read a frame from the camera
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Get the landmarks from the face mesh and draw them on the image
        results, image = get_landmarks(image, face_mesh)
        landmark_dict = draw_landmarks(image, results)

        # Show the image on the screen and wait for a key press (DONT NEED input monitoring SINCE PYGAME HANDLES EXIT)
        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        key = cv.waitKey(1)

        # If the 'q' key is pressed, break the loop
        if key == ord('q'):
                pygame.quit()
                # Release the camera and close all windows
                cap.release()
                cv.destroyAllWindows()

                sys.exit()

        # get mouse x and y to move mouse later
        x, y = pag.position()
        # print(f'x = {x} y= {y}')
        
        #Render all Items onto pygame window
        window_surface.fill((235,235,235))
        window_surface.blit(background_image, [infoObject.current_w//2 - 300, infoObject.current_h//2 - 300])
        window_surface.blit(title, (infoObject.current_w//2 - title_rect[2]//2, 20))
        if mode != 2:
            window_surface.blit(subtitle, (infoObject.current_w//2 - (subtitle_rect[2]//2), 80))


        time_delta = clock.tick(60)/1000.0

        #draw circles all at once
        if mode != 0:
            for k in range(len(circles)):
                circles[k].draw()
                if mode == 2:
                    circles[k].mover()

        #if calibration mode draw one at a time
        if mode == 0:
            calibrate_circle = CircleClass.Circle(index_calibrate,window_surface,mode)
            calibrate_circle.draw()

        #mode move automatically if mode is interactive mode
        if mode == 2:
            if landmark_dict is None or any(
                key not in landmark_dict
                for key in ['nose', 'left_eye', 'right_eye']
            ):
                continue

            parse_test.move_mouse(landmark_dict, test_width, test_height, x, y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                # Release the camera and close all windows
                cap.release()
                cv.destroyAllWindows()

                sys.exit()

            #when mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot = pygame.mixer.Sound('sound/gun_shot.ogg')
                shoot.play()
                mouseLocation = pygame.mouse.get_pos()
                x = mouseLocation[0]
                y = mouseLocation[1]
                # Print the position of the mouse click
                print(f"Left button of the mouse is clicked - position ({x}, {y})")

                # If landmark_dict and  are not None, and not in interative mode save data to csv
                if mode != 2:
                    if landmark_dict  is not None:
                        parse_test.save_data(landmark_dict, width, height, x, y,user)

                for k in range(len(circles)):
                    #if click within hitbox of circle
                    if mouseLocation[0] >= circles[k].x-11 and mouseLocation[0] <= circles[k].x+11:
                        if mouseLocation[1] >= circles[k].y-11 and mouseLocation[1] <= circles[k].y+11:
                            # print(circles[k].index)

                            indexToDelete = k
                            delThis = True
                            score += 1
                            number_circles -= 1
                            if mode == 0:
                                index_calibrate+= 1
                            # print(number_circles)

                            if number_circles == 0 and mode!= 0:
                                End_screen.endScreen(score, window_surface,mode,user)
                            elif number_circles == 0:
                                Calibration_complete.cal_complete(window_surface, 0,user)

                reload.play()       
            #main menu navigation                     
            if event.type == USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    navigate = pygame.mixer.Sound('sound/navigating_menu.ogg')
                    navigate.play()
                    if event.ui_element == main_menu:
                        Main_menu_MouSee.main_menu(window_surface,user)

            #delete circle if clicked
            if delThis:
                # print(f'deleting circle index {indexToDelete}')
                del circles[indexToDelete]
                delThis = False

            game_manager.process_events(event)
            game_manager.update(time_delta) 

        game_manager.draw_ui(window_surface)

        pygame.display.update()



# # If this file is being run as the main program, call the main function
# if __name__ == "__main__":
#     main()