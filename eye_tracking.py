import cv2 as cv
import mediapipe as mp
from pynput.mouse import Button, Controller, Listener
import threading
import parse
import ctypes

# Set the DeviceID of the camera
device_id = r"USB\VID_1D6C&PID_0103&MI_00\8&C9FD7AC&0&0000"

def initialize_face_mesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    return mp.solutions.face_mesh.FaceMesh(
        max_num_faces=max_num_faces,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence
    )

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
        return None

    # Define parameters for drawing
    line_color = (0, 255, 0)
    line_thickness = 1

    def extract_landmarks(face_landmarks, image_shape):
        landmark_labels = ['nose', 'left_eye', 'right_eye', 'forehead', 'chin', 'left_cheek', 'right_cheek', 'center']
        landmark_indices = {
            'nose': 4,
            'left_eye': 473,
            'right_eye': 468,
            'forehead': 10,
            'chin': 152,
            'left_cheek': 234,
            'right_cheek': 454
        }
        landmark_dict = {}

        for label, index in landmark_indices.items():
            x = face_landmarks.landmark[index].x * image_shape[1]
            y = face_landmarks.landmark[index].y * image_shape[0]
            z = face_landmarks.landmark[index].z
            landmark_dict[label] = (x, y, z)

        # Calculate the center point of the face
        center_x = sum(x for x, y, z in landmark_dict.values()) / len(landmark_dict)
        center_y = sum(y for x, y, z in landmark_dict.values()) / len(landmark_dict)
        center_z = sum(z for x, y, z in landmark_dict.values()) / len(landmark_dict)
        landmark_dict['center'] = (center_x, center_y, center_z)

        return landmark_dict

    face_landmarks = results.multi_face_landmarks[0]
    landmark_dict = extract_landmarks(face_landmarks, image.shape)

    # Draw lines from the center to key landmarks
    center_x, center_y, _ = landmark_dict['center']
    nose_x, nose_y, _ = landmark_dict['nose']
    left_eye_x, left_eye_y, _ = landmark_dict['left_eye']
    right_eye_x, right_eye_y, _ = landmark_dict['right_eye']

    cv.line(image, (int(center_x), int(center_y)), (int(nose_x), int(nose_y)), line_color, line_thickness)
    cv.line(image, (int(center_x), int(center_y)), (int(left_eye_x), int(left_eye_y)), line_color, line_thickness)
    cv.line(image, (int(center_x), int(center_y)), (int(right_eye_x), int(right_eye_y)), line_color, line_thickness)

    # Draw lines between nose and eyes
    cv.line(image, (int(nose_x), int(nose_y)), (int(left_eye_x), int(left_eye_y)), line_color, line_thickness)
    cv.line(image, (int(nose_x), int(nose_y)), (int(right_eye_x), int(right_eye_y)), line_color, line_thickness)
    cv.line(image, (int(left_eye_x), int(left_eye_y)), (int(right_eye_x), int(right_eye_y)), line_color, line_thickness)

    # Draw lines from eyes to screen edges
    cv.line(image, (int(left_eye_x), int(left_eye_y)), (image.shape[1], int(left_eye_y)), line_color, line_thickness)
    cv.line(image, (int(right_eye_x), int(right_eye_y)), (0, int(right_eye_y)), line_color, line_thickness)

    return landmark_dict

def main():
    # Find and define monitor width and height
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    # Initialize face mesh and camera
    face_mesh = initialize_face_mesh()
    cap = cv.VideoCapture(int(device_id.split("&")[-1], 16))

    def on_click(x, y, button, pressed):
        if button == Button.left and pressed:
            print(f"Left button clicked at position ({x}, {y})")
            if landmark_dict is not None:
                parse.save_data(landmark_dict, screen_width, screen_height, x, y)

    # Initialize the mouse listener
    mouse = Controller()
    mouse_listener = initialize_mouse_listener(on_click)


    # Start the mouse listener in a separate thread
    mouse_thread = threading.Thread(target=start_mouse_listener, args=(mouse_listener,))
    mouse_thread.start()

    # Main loop
    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        results, image = get_landmarks(image, face_mesh)
        landmark_dict = draw_landmarks(image, results)

        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        if cv.waitKey(1) == ord('q'):
            break

    # Cleanup
    stop_mouse_listener(mouse_listener)
    mouse_thread.join()
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
