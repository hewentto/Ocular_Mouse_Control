import pandas as pd
from sklearn.preprocessing import StandardScaler
import pyautogui
import joblib
import math
import tensorflow as tf 
import numpy as np
import keras



# Load the scaler before calling move_mouse
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")

loaded_model = keras.models.load_model("my_model2.keras")
svr_x = joblib.load("best_model_x.pkl")
svr_y = joblib.load("best_model_y.pkl")

def predict_coordinates(input_data, scaler):
    """Predicts the coordinates of the mouse pointer using the trained model"""
    x_pred = svr_x.predict(input_data)
    y_pred = svr_y.predict(input_data)

    return x_pred, y_pred


# Initialize a list to keep track of the previous predicted coordinates
prev_coords = []

def predict_and_smooth_coordinates(input_data, scaler, n=5):
    """Predicts the coordinates of the mouse pointer using the trained model and applies a low-pass filter"""
    x_pred, y_pred = predict_coordinates(input_data, scaler)

    # Add the current predicted coordinates to the list
    prev_coords.append((x_pred, y_pred))

    # If the list is longer than n, remove the oldest coordinates
    if len(prev_coords) > n:
        prev_coords.pop(0)

    # Take the average of the previous n predicted coordinates
    x_smoothed = np.mean([coord[0] for coord in prev_coords])
    y_smoothed = np.mean([coord[1] for coord in prev_coords])

    return x_smoothed, y_smoothed

# Update move_mouse function to use predict_and_smooth_coordinates
def move_mouse(landmark_dict, screen_width, screen_height, x, y):
    df = arrange_data(landmark_dict, screen_width, screen_height, x, y)
    df.drop('target', axis=1, inplace=True)

    x_smoothed, y_smoothed = predict_and_smooth_coordinates(df, scaler)

    pyautogui.moveTo(x_smoothed, y_smoothed, duration=0)




def arrange_data(landmark_dict, screen_width, screen_height, x, y):
    """
    Arranges the data into a dataframe with labeled columns
    Args:
        landmark_dict: dictionary of landmark coordinates
        distance_dict: dictionary of line distances
    Returns:
        a ready to save dataframe"""

    # Calculate distances between landmarks
    distance_dict = Get_distances(landmark_dict, screen_width, screen_height)

    # Combine the dictionaries
    combined_dict = {
        'nose_x': landmark_dict['nose'][0],
        'nose_y': landmark_dict['nose'][1],
        'nose_z': landmark_dict['nose'][2],
        'left_eye_x': landmark_dict['left_eye'][0],
        'left_eye_y': landmark_dict['left_eye'][1],
        'left_eye_z': landmark_dict['left_eye'][2],
        'right_eye_x': landmark_dict['right_eye'][0],
        'right_eye_y': landmark_dict['right_eye'][1],
        'right_eye_z': landmark_dict['right_eye'][2],
        'forehead_x': landmark_dict['forehead'][0],
        'forehead_y': landmark_dict['forehead'][1],
        'forehead_z': landmark_dict['forehead'][2],
        'chin_x': landmark_dict['chin'][0],
        'chin_y': landmark_dict['chin'][1],
        'chin_z': landmark_dict['chin'][2],
        'left_cheek_x': landmark_dict['left_cheek'][0],
        'left_cheek_y': landmark_dict['left_cheek'][1],
        'left_cheek_z': landmark_dict['left_cheek'][2],
        'screen_height': screen_height,
        'target': (x, y),
        'right_cheek_x': landmark_dict['right_cheek'][0],
        'right_cheek_y': landmark_dict['right_cheek'][1],
        'right_cheek_z': landmark_dict['right_cheek'][2],
        'center_x': landmark_dict['center'][0],
        'center_y': landmark_dict['center'][1],
        'center_z': landmark_dict['center'][2],   
    }
    # add the distances to the dictionary
    combined_dict |= distance_dict

    # Create a DataFrame from the dictionary
    df = pd.DataFrame([combined_dict])

    # pop target and add to end
    target = df.pop('target')
    df['target'] = target

    return df

def save_data(landmark_dict, screen_width, screen_height, x, y):

    df = arrange_data(landmark_dict, screen_width, screen_height, x, y)
    # file path
    file_path = 'data.csv'
    # add the data row to the csv file
    df.to_csv(file_path, mode='a', header=False, index=False)

def euclidean_distance_3(x1, y1, z1, x2, y2, z2):
    """
    Calculates the euclidean distance between two points
    Args:
        x1: x coordinate of point 1
        y1: y coordinate of point 1
        z1: z coordinate of point 1
        x2: x coordinate of point 2
        y2: y coordinate of point 2
        z2: z coordinate of point 2
    Returns:
        the euclidean distance between the two points"""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def euclidean_distance_2(x1, y1, x2, y2):
    """
    Calculates the euclidean distance between two points
    Args:
        x1: x coordinate of point 1
        y1: y coordinate of point 1
        x2: x coordinate of point 2
        y2: y coordinate of point 2
    Returns:
        the euclidean distance between the two points"""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def Get_distances(landmark_dict, screen_width, screen_height):
    """
    returns data frame with relevant euclidean distances lengths
    Args:
        landmark_dict: dictionary of landmark coordinates
    Returns:
        a dictionary of distances between landmarks"""
    return {
        'nose_to_left_eye3': euclidean_distance_3(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][2],
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][2],
        ),
        'nose_to_right_eye3': euclidean_distance_3(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][2],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][2],
        ),
        'nose_to_image_edge': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            screen_width,
            landmark_dict['nose'][1],
        ),
        'nose_to_image_top': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][0],
            0,
        ),
        'nose_to_image_bottom': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][0],
            screen_height,
        ),
        'left_eye_to_right_eye3': euclidean_distance_3(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][2],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][2],
        ),
        'left_eye_to_image_edge': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            0,
            landmark_dict['left_eye'][1],
        ),
        'left_eye_to_image_top': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][0],
            0,
        ),
        'left_eye_to_image_bottom': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][0],
            screen_height,
        ),
        'right_eye_to_image_edge': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            screen_width,
            landmark_dict['right_eye'][1],
        ),
        'right_eye_to_image_top': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][0],
            0,
        ),
        'right_eye_to_image_bottom': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][0],
            screen_height,
        ),
        'center_to_nose3': euclidean_distance_3(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][2],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][2],
        ),
        'center_to_left_eye3': euclidean_distance_3(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][2],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][2],
        ),
        'center_to_right_eye3': euclidean_distance_3(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][2],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][2],
        ),
        'center_to_image_edge': euclidean_distance_2(
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            screen_width,
            landmark_dict['center'][1],
        ),
        'center_to_image_top': euclidean_distance_2(
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][0],
            0,
        ),
        'center_to_image_bottom': euclidean_distance_2(
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][0],
            screen_height,
        ),
        'nose_to_left_eye2': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
        ),
        'nose_to_right_eye2': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
        ),
        'left_eye_to_right_eye2': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
        ),
        'left_eye_to_center2': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
        ),
        'right_eye_to_center2': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
        ),
        'nose_to_center2': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
        ),
    }