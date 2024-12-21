import pandas as pd
import os

def mark_occurrences(input_dataframe, folder_path, report_value, flag_column):
    """
    Process files in the folder to calculate occurrences of stocks and update the provided DataFrame.

    Parameters:
        folder_path (str): Path to the folder containing CSV files.
        report_value (str): Value in the "report" column to filter by.
        flag_column (str): Column name representing the flag.
        input_dataframe (pd.DataFrame): The input DataFrame to update with occurrence counts.

    Returns:
        pd.DataFrame: The updated DataFrame with an added "Occurrence" column.
    """
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
    filtered_data = all_data[(all_data['report'] == report_value) & (all_data[flag_column] == 'Y')]

    # Count occurrences of each stock
    occurrence_counts = filtered_data["Security Id"].value_counts().reset_index()
    occurrence_counts.columns = ["Security Id", 'Occurrence']

    # Merge occurrence counts back to the input DataFrame
    updated_dataframe = input_dataframe.merge(occurrence_counts, on="Security Id", how='left')

    return updated_dataframe
