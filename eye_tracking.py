import cv2 as cv
import mediapipe as mp
from pynput.mouse import Button, Controller, Listener
import threading
import csv
import math
import parse


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
    center_radius = 3
    center_thickness = -1
    center_color = (255, 0, 0)
    labels = ['center_nose', 'center_left_eye', 'center_right_eye', 'nose_left_eye', 'nose_right_eye', 'left_right_eye', 'left_image_edge', 'right_image_edge']
    landmark_labels = ['nose', 'left_eye', 'right_eye', 'forehead', 'chin', 'left_cheek', 'right_cheek', 'center']



    def extract_landmarks(face_landmarks, image_shape):
        landmark_dict = {}

        nose_x, nose_y, nose_z = int(face_landmarks.landmark[nose_tip_landmark_index].x * image_shape[1]), \
                                int(face_landmarks.landmark[nose_tip_landmark_index].y * image_shape[0]), \
                                face_landmarks.landmark[nose_tip_landmark_index].z
        landmark_dict[landmark_labels[0]] = (nose_x, nose_y, nose_z)

        left_eye_x, left_eye_y, left_eye_z = int(face_landmarks.landmark[473].x * image_shape[1]), \
                                            int(face_landmarks.landmark[473].y * image_shape[0]), \
                                            face_landmarks.landmark[473].z
        landmark_dict[landmark_labels[1]] = (left_eye_x, left_eye_y, left_eye_z)

        right_eye_x, right_eye_y, right_eye_z = int(face_landmarks.landmark[468].x * image_shape[1]), \
                                                int(face_landmarks.landmark[468].y * image_shape[0]), \
                                                face_landmarks.landmark[468].z
        landmark_dict[landmark_labels[2]] = (right_eye_x, right_eye_y, right_eye_z)

        additional_landmark_indices = {
            landmark_labels[3]: forehead_landmark_index,
            landmark_labels[4]: chin_landmark_index,
            landmark_labels[5]: left_cheek_landmark_index,
            landmark_labels[6]: right_cheek_landmark_index
        }

        for label, index in additional_landmark_indices.items():
            x, y, z = int(face_landmarks.landmark[index].x * image_shape[1]), \
                    int(face_landmarks.landmark[index].y * image_shape[0]), \
                    int(face_landmarks.landmark[index].z * image_shape[0])
            landmark_dict[label] = (x, y, z)

        center_x = int(sum(x for x, y, z in landmark_dict.values()) / len(landmark_dict))
        center_y = int(sum(y for x, y, z in landmark_dict.values()) / len(landmark_dict))
        center_z = sum(z for x, y, z in landmark_dict.values()) / len(landmark_dict)

        landmark_dict[landmark_labels[7]] = (center_x, center_y, center_z)

        return landmark_dict


    # save euclidean distance for each line
    def euclidean_distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def compute_distances(landmark_dict, image_shape, labels):
        distance_dict = {}

        center_x, center_y = landmark_dict['center'][:2]
        nose_x, nose_y = landmark_dict['nose'][:2]
        left_eye_x, left_eye_y = landmark_dict['left_eye'][:2]
        right_eye_x, right_eye_y = landmark_dict['right_eye'][:2]

        distance_dict[labels[0]] = euclidean_distance((center_x, center_y), (nose_x, nose_y))
        distance_dict[labels[1]] = euclidean_distance((center_x, center_y), (left_eye_x, left_eye_y))
        distance_dict[labels[2]] = euclidean_distance((center_x, center_y), (right_eye_x, right_eye_y))
        distance_dict[labels[3]] = euclidean_distance((nose_x, nose_y), (left_eye_x, left_eye_y))
        distance_dict[labels[4]] = euclidean_distance((nose_x, nose_y), (right_eye_x, right_eye_y))
        distance_dict[labels[5]] = euclidean_distance((left_eye_x, left_eye_y), (right_eye_x, right_eye_y))
        distance_dict[labels[6]] = euclidean_distance((left_eye_x, left_eye_y), (image_shape[1], left_eye_y))
        distance_dict[labels[7]] = euclidean_distance((right_eye_x, right_eye_y), (0, right_eye_y))

        return distance_dict




    for face_landmarks in results.multi_face_landmarks:
        landmark_dict = extract_landmarks(face_landmarks, image.shape)
        distance_dict = compute_distances(landmark_dict, image.shape, labels)


        # Draw a circle at the calculated center of the head
        center_x, center_y, _ = landmark_dict['center']
        cv.circle(image, (center_x, center_y), center_radius, center_color, center_thickness)

        # Draw lines from center of head to nose and eyes
        nose_x, nose_y, _ = landmark_dict['nose']
        left_eye_x, left_eye_y, _ = landmark_dict['left_eye']
        right_eye_x, right_eye_y, _ = landmark_dict['right_eye']

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

    return landmark_dict, distance_dict


# Define the main function
def main():
    # Define the screen size
    screen_width = 1920
    screen_height = 1080

    # Initialize the face mesh
    face_mesh = initialize_face_mesh()

    # Define a function to be called when the mouse is clicked
    def on_click(x, y, button, pressed):
        if button == Button.left and pressed:
            # Print the position of the mouse click
            print(f"Left button of the mouse is clicked - position ({x}, {y})")

            # If landmark_dict and distance_dict are not None, call parse.arrange_data
            if landmark_dict and distance_dict is not None:
                parse.arrange_data(landmark_dict, distance_dict, screen_width, screen_height, x, y)

    # Create a mouse controller and initialize a mouse listener
    mouse = Controller()
    mouse_listener = initialize_mouse_listener(on_click)

    # Create a thread for the mouse listener and start it
    mouse_thread = threading.Thread(target=start_mouse_listener, args=(mouse_listener,))
    mouse_thread.start()

    # Initialize the camera
    cap = cv.VideoCapture(0)

    # Loop until the 'q' key is pressed
    while True:
        # Read a frame from the camera
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Get the landmarks from the face mesh and draw them on the image
        results, image = get_landmarks(image, face_mesh)
        landmark_dict, distance_dict = draw_landmarks(image, results)

        # Show the image on the screen and wait for a key press
        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        key = cv.waitKey(1)

        # If the 'q' key is pressed, break the loop
        if key == ord('q'):
            break

    # Stop the mouse listener and join the mouse thread
    stop_mouse_listener(mouse_listener)
    mouse_thread.join()

    # Release the camera and close all windows
    cap.release()
    cv.destroyAllWindows()


# If this file is being run as the main program, call the main function
if __name__ == "__main__":
    main()