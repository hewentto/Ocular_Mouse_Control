import sys
import pygame
import pygame_gui
from pygame.locals import *
import User_select_MouSee
import Training_page_MouSee


def interactive(window_surface):
    pass
            # if mode == 2:
            #     test_width = 1920
            # test_height = 1080

            #  # Read a frame from the camera
            # success, image = cap.read()
            # if not success:
            #     print("Ignoring empty camera frame.")
            #     continue

            # # Get the landmarks from the face mesh and draw them on the image
            # results, image = get_landmarks(image, face_mesh)
            # landmark_dict = draw_landmarks(image, results)

            # # Show the image on the screen and wait for a key press (DONT NEED input monitoring SINCE PYGAME HANDLES EXIT)
            # cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
            # key = cv.waitKey(1)

            # # If the 'q' key is pressed, break the loop
            # if key == ord('q'):
            #         pygame.quit()
            #         # Release the camera and close all windows
            #         cap.release()
            #         cv.destroyAllWindows()

            #         sys.exit()

            # # get mouse x and y to move mouse later
            # x, y = pag.position()
            # # print(f'x = {x} y= {y}')
            
            # #Render all Items onto pygame window
            # window_surface.fill((235,235,235))
            # window_surface.blit(background_image, [infoObject.current_w//2 - 300, infoObject.current_h//2 - 300])
            # window_surface.blit(title, (infoObject.current_w//2 - title_rect[2]//2, 20))

            # time_delta = clock.tick(60)/1000.0

            # for k in range(len(circles)):
            #     circles[k].draw()
            #     circles[k].mover()   

            # # Check if landmark_dict is not None and if any of the required landmarks are missing
            # if landmark_dict is None or any(
            #     key not in landmark_dict
            #     for key in ['nose', 'left_eye', 'right_eye']
            # ):
            #     continue

            # # If all landmarks are present, call move_mouse
            # parse_test.move_mouse(landmark_dict, test_width, test_height, x, y)