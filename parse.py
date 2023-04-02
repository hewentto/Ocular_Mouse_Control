import pandas as pd


def arrange_data(landmark_list, line_list):
    """
    Arranges the data into a dataframe with labeled columns
    Args:
        landmark_list: list of landmark coordinates
        line_list: list of line coordinates
    Returns:
        a ready to save dataframe"""

    # create a list of column names
    landmark_columns = []
    for i in range(0, len(landmark_list)):
        landmark_columns.append(f"landmark_{i}")

    line_columns = []
    for i in range(0, len(line_list)):
        line_columns.append(f"line_{i}")

    # create a list of data
    data = landmark_list + line_list

    # create a dataframe
    df = pd.DataFrame(data, columns=["x", "y", "z"])

    # transpose the dataframe
    df = df.T

    # rename the columns
    df.columns = landmark_columns + line_columns

    return df