import pandas as pd
from sklearn.preprocessing import StandardScaler

def arrange_data(landmark_dict, distance_dict, screen_width, screen_height, x, y,user):
    """
    Arranges the data into a dataframe with labeled columns
    Args:
        landmark_dict: dictionary of landmark coordinates
        distance_dict: dictionary of line distances
    Returns:
        a ready to save dataframe"""

    # file name 
    if user == 0 or user == 2:
        file_path = 'caleb.csv'
    if user == 1:
        file_path = 'data.csv'
        
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
        'right_cheek_x': landmark_dict['right_cheek'][0],
        'right_cheek_y': landmark_dict['right_cheek'][1],
        'right_cheek_z': landmark_dict['right_cheek'][2],
        'nose_left_eye': distance_dict['nose_left_eye'],
        'nose_right_eye': distance_dict['nose_right_eye'],
        'left_right_eye': distance_dict['left_right_eye'],
        'left_image_edge': distance_dict['left_image_edge'],
        'right_image_edge': distance_dict['right_image_edge'],
        'screen_width': screen_width,
        'screen_height': screen_height,
        'x': x,
        'y': y,
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame([combined_dict], columns=['nose_x', 'nose_y', 'nose_z', 'left_eye_x', 'left_eye_y', 'left_eye_z', 'right_eye_x', 'right_eye_y', 'right_eye_z', 'forehead_x', 'forehead_y', 'forehead_z', 'chin_x', 'chin_y', 'chin_z', 'left_cheek_x', 'left_cheek_y', 'left_cheek_z', 'right_cheek_x', 'right_cheek_y', 'right_cheek_z', 'nose_left_eye', 'nose_right_eye', 'left_right_eye', 'left_image_edge', 'right_image_edge', 'screen_width', 'screen_height', 'x', 'y'])


    # add the data row to the csv file
    df.to_csv(file_path, mode='a', header=False, index=False)#type: ignore
