import pandas as pd
import os

def mark_occurrences(input_dataframe, folder_path):
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

    # Filter records with the specified report and flag values
    filtered_data = all_data[(all_data['Report'] == 'C') & (all_data['1Y_FLG'] == 'Y')]

    # Count occurrences of each stock
    occurrence_counts = filtered_data["Security Id"].value_counts().reset_index()
    occurrence_counts.columns = ["Security Id", 'Occurrence']

    # Merge occurrence counts back to the input DataFrame
    updated_dataframe = input_dataframe.merge(occurrence_counts, on="Security Id", how='left')

    return updated_dataframe
