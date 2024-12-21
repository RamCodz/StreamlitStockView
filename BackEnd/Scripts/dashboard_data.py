import pandas as pd
import os

def mark_occurrences(input_dataframe, folder_path):
    # Check if required columns exist in input_dataframe
    if not {'Security Id', 'Report', '1Y_FLG'}.issubset(input_dataframe.columns):
        raise ValueError("Input DataFrame must contain 'Security Id', 'Report', and '1Y_FLG' columns.")

    # Initialize an empty DataFrame to hold data from all files
    all_data = pd.DataFrame()

    # Read all files from the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            # Read the CSV file
            data = pd.read_csv(file_path)
            # Append to the main DataFrame
            all_data = pd.concat([all_data, data], ignore_index=True)

    # Check if required columns exist in the consolidated DataFrame
    required_columns = {'Report', '1Y_FLG', 'Security Id'}
    if not required_columns.issubset(all_data.columns):
        raise ValueError(f"Missing required columns in CSV files. Expected: {required_columns}")

    # Filter records with the specified report and flag values
    filtered_data = all_data[(all_data['Report'] == 'C') & (all_data['1Y_FLG'] == 'Y')]

    # Count occurrences of each stock
    occurrence_counts = filtered_data['Security Id'].value_counts().reset_index()
    occurrence_counts.columns = ['Security Id', 'Occurrence']

    # Merge occurrence counts back to the input DataFrame
    input_dataframe = input_dataframe.merge(occurrence_counts, on='Security Id', how='left')

    # For records that meet the condition in the input DataFrame, keep the "Occurrence" column
    input_dataframe.loc[
        ~(input_dataframe['Report'] == 'C') | ~(input_dataframe['1Y_FLG'] == 'Y'),
        'Occurrence'
    ] = pd.NA

    # Ensure 'Occurrence' is of integer type where applicable
    input_dataframe['Occurrence'] = input_dataframe['Occurrence'].astype('Int64')

    return input_dataframe
