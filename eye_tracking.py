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


    for face_landmarks in results.multi_face_landmarks:
        nose_x, nose_y, nose_z = int(face_landmarks.landmark[nose_tip_landmark_index].x * image.shape[1]), \
                                 int(face_landmarks.landmark[nose_tip_landmark_index].y * image.shape[0]), \
                                 face_landmarks.landmark[nose_tip_landmark_index].z

        left_eye_x, left_eye_y, left_eye_z = int(face_landmarks.landmark[473].x * image.shape[1]), \
                                             int(face_landmarks.landmark[473].y * image.shape[0]), \
                                             face_landmarks.landmark[473].z
        right_eye_x, right_eye_y, right_eye_z = int(face_landmarks.landmark[468].x * image.shape[1]), \
                                                 int(face_landmarks.landmark[468].y * image.shape[0]), \
                                                 face_landmarks.landmark[468].z

        landmark_list.extend(
            (
                [nose_x, nose_y, nose_z],
                [left_eye_x, left_eye_y, left_eye_z],
                [right_eye_x, right_eye_y, right_eye_z],
            )
        )
        # Define landmark indices for eyebrows
        eyebrow_landmarks = [105, 107, 336, 334]

        # Draw circles for eyebrow landmarks
        for landmark_index in eyebrow_landmarks:
            x, y, z = int(face_landmarks.landmark[landmark_index].x * image.shape[1]), int(
                face_landmarks.landmark[landmark_index].y * image.shape[0]),int(
                face_landmarks.landmark[landmark_index].z * image.shape[0])
            dot_color = (255, 0, 255)
            landmark_list.append([x, y, z])
            cv.circle(image, (x, y), dot_radius, dot_color, dot_thickness)


        # Get the landmark coordinates
        landmarks = [(nose_x, nose_y, nose_z), (left_eye_x, left_eye_y, left_eye_z), (right_eye_x, right_eye_y, right_eye_z)]
        for index in [forehead_landmark_index, chin_landmark_index, left_cheek_landmark_index, right_cheek_landmark_index]:
            x, y, z = int(face_landmarks.landmark[index].x * image.shape[1]), int(face_landmarks.landmark[index].y * image.shape[0]), int(face_landmarks.landmark[index].z * image.shape[0])
            landmark_list.append([x, y, z])
            landmarks.append((x, y, z))

        # Calculate the average position of the landmarks
        center_x = int(sum(x for x, y, z in landmarks) / len(landmarks))
        center_y = int(sum(y for x, y, z in landmarks) / len(landmarks))
        center_z = sum(z for x, y, z in landmarks) / len(landmarks)

        landmark_list.append([center_x, center_y, center_z])

        # Draw a circle at the calculated center of the head
        cv.circle(image, (center_x, center_y), center_radius, center_color, center_thickness)

        # Draw lines from center of head to nose and eyes
        cv.line(image, (center_x, center_y), (nose_x, nose_y), line_color, line_thickness)
        cv.line(image, (center_x, center_y), (left_eye_x, left_eye_y), line_color, line_thickness)
        cv.line(image, (center_x, center_y), (right_eye_x, right_eye_y), line_color, line_thickness)
        # Draw lines for nose and eye landmarks
        cv.line(image, (nose_x, nose_y), (left_eye_x, left_eye_y), line_color, line_thickness)
        cv.line(image, (nose_x, nose_y), (right_eye_x, right_eye_y), line_color, line_thickness)
        cv.line(image, (left_eye_x, left_eye_y), (right_eye_x, right_eye_y), line_color, line_thickness)

        # save euclidean distance for each line
        def euclidean_distance(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        line_list = []
        line_list.append(euclidean_distance((center_x, center_y), (nose_x, nose_y)))
        line_list.append(euclidean_distance((center_x, center_y), (left_eye_x, left_eye_y)))
        line_list.append(euclidean_distance((center_x, center_y), (right_eye_x, right_eye_y)))
        line_list.append(euclidean_distance((nose_x, nose_y), (left_eye_x, left_eye_y)))
        line_list.append(euclidean_distance((nose_x, nose_y), (right_eye_x, right_eye_y)))
        line_list.append(euclidean_distance((left_eye_x, left_eye_y), (right_eye_x, right_eye_y)))

        
        return landmark_list, line_list


def main():
    screen_width = 1920
    screen_height = 1080

    face_mesh = initialize_face_mesh()

    def on_click(x, y, button, pressed):
        if button == Button.left and pressed:
            print(f"Left button of the mouse is clicked - position ({x}, {y})")
        if landmark_list and line_list is not None:
            row_data = [
                coord for point in landmark_list for coord in point
            ] + list(line_list)
            print(row_data)

    mouse = Controller()
    mouse_listener = initialize_mouse_listener(on_click)
    mouse_thread = threading.Thread(target=start_mouse_listener, args=(mouse_listener,))
    mouse_thread.start()

    cap = cv.VideoCapture(0)

    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        results, image = get_landmarks(image, face_mesh)

        landmark_list, line_list = draw_landmarks(image, results)

        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        key = cv.waitKey(1)

        if key == ord('q'):
            break

    stop_mouse_listener(mouse_listener)
    mouse_thread.join()
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
