import cv2 as cv
import mediapipe as mp
from pynput.mouse import Button, Controller, Listener
import threading
import csv
import math
import parse
# Set the DeviceID of the camera
device_id = r"USB\VID_1D6C&PID_0103&MI_00\8&C9FD7AC&0&0000"

def initialize_face_mesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    return mp.solutions.face_mesh.FaceMesh(
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
        center_x = int(center_x)
        center_y = int(center_y)
        # cv.circle(image, (center_x, center_y), center_radius, center_color, center_thickness)

        # Draw lines from center of head to nose and eyes
        nose_x, nose_y, _ = landmark_dict['nose']
        nose_x = int(nose_x)
        nose_y = int(nose_y)

        left_eye_x, left_eye_y, _ = landmark_dict['left_eye']
        left_eye_x = int(left_eye_x)
        left_eye_y = int(left_eye_y)

        right_eye_x, right_eye_y, _ = landmark_dict['right_eye']
        right_eye_x = int(right_eye_x)
        right_eye_y = int(right_eye_y)


        cv.line(image, (center_x, center_y), (nose_x, nose_y), line_color, line_thickness)
        cv.line(image, (center_x, center_y), (left_eye_x, left_eye_y), line_color, line_thickness)
        cv.line(image, (center_x, center_y), (right_eye_x, right_eye_y), line_color, line_thickness)

        # Draw lines for nose and eye landmarks
        cv.line(image, (nose_x, nose_y), (left_eye_x, left_eye_y), line_color, line_thickness)
        cv.line(image, (nose_x, nose_y), (right_eye_x, right_eye_y), line_color, line_thickness)
        cv.line(image, (left_eye_x, left_eye_y), (right_eye_x, right_eye_y), line_color, line_thickness)

        # Line from eyes to edge of screen
        cv.line(image, (left_eye_x, left_eye_y), (image.shape[1], left_eye_y), line_color, line_thickness)
        cv.line(image, (right_eye_x, right_eye_y), (0, right_eye_y), line_color, line_thickness)

    return landmark_dict


# Define the main function
def main():
    # Define the screen size
    screen_width = 1920
    screen_height = 1080

    # Initialize the face mesh
    face_mesh = initialize_face_mesh()

    # Initialize the camera
    cap = cv.VideoCapture(int(device_id.split("&")[-1], 16))

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

        # Show the image on the screen and wait for a key press
        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        key = cv.waitKey(1)

        # If the 'q' key is pressed, break the loop
        if key == ord('q'):
            break
    # Define a function to be called when the mouse is clicked
    def on_click(x, y, button, pressed):
        if button == Button.left and pressed:
            # Print the position of the mouse click
            print(f"Left button of the mouse is clicked - position ({x}, {y})")

            # If landmark_dict and distance_dict are not None, call parse.arrange_data
            if landmark_dict is not None:
                parse.save_data(landmark_dict, screen_width, screen_height, x, y)

    # Create a mouse controller and initialize a mouse listener

    mouse = Controller()
    mouse_listener = initialize_mouse_listener(on_click)

    # Create a thread for the mouse listener and start it
    mouse_thread = threading.Thread(target=start_mouse_listener, args=(mouse_listener,))
    mouse_thread.start()
    # Stop the mouse listener and join the mouse thread
    stop_mouse_listener(mouse_listener)
    mouse_thread.join()

    # Release the camera and close all windows
    cap.release()
    cv.destroyAllWindows()


# If this file is being run as the main program, call the main function
if __name__ == "__main__":
    main()