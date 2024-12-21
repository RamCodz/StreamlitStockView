import os
import pandas as pd
from collections import Counter

def list_unique_stocks_with_counts_by_report(folder_path, file_extension=".csv", stock_column="Security Id", report_column="Report", extra_columns=None):
    """
    Reads all files in the folder, separates data by report types, and lists unique stock names 
    along with counts for each type.
    
    :param folder_path: Path to the folder containing files.
    :param file_extension: File extension to filter files (default: '.csv').
    :param stock_column: Column name containing stock names (default: 'Security Id').
    :param report_column: Column name indicating report type (default: 'Report').
    :param extra_columns: List of other column names to extract (default: None).
    :return: Two DataFrames - one for each report type ("C" and "G").
    """
    if extra_columns is None:
        extra_columns = []

    # Initialize lists to store data
    data_c = []
    data_g = []

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(file_extension):
            file_path = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(file_path)
                if stock_column in df.columns and report_column in df.columns:
                    # Separate records by report type
                    df_c = df[df[report_column] == "C"]
                    df_g = df[df[report_column] == "G"]

                    # Extract required columns and add source file info
                    selected_columns = [stock_column, report_column] + [col for col in extra_columns if col in df.columns]
                    if not df_c.empty:
                        df_c = df_c[selected_columns].copy()
                        df_c['Source File'] = filename
                        data_c.append(df_c)
                    if not df_g.empty:
                        df_g = df_g[selected_columns].copy()
                        df_g['Source File'] = filename
                        data_g.append(df_g)
                else:
                    print(f"Columns '{stock_column}' or '{report_column}' not found in {filename}. Skipping...")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Combine data for each report type
    combined_c = pd.concat(data_c, ignore_index=True) if data_c else pd.DataFrame()
    combined_g = pd.concat(data_g, ignore_index=True) if data_g else pd.DataFrame()

    # Count occurrences for each stock name
    if not combined_c.empty:
        stock_counts_c = Counter(combined_c[stock_column])
        combined_c['Appearance Count'] = combined_c[stock_column].map(stock_counts_c)
        combined_c = combined_c.drop_duplicates(subset=[stock_column]).reset_index(drop=True)

    if not combined_g.empty:
        stock_counts_g = Counter(combined_g[stock_column])
        combined_g['Appearance Count'] = combined_g[stock_column].map(stock_counts_g)
        combined_g = combined_g.drop_duplicates(subset=[stock_column]).reset_index(drop=True)

    return combined_c, combined_g

# Usage Example
folder_path = "path/to/your/folder"  # Replace with the folder containing your files
output_columns = ["Security Id", "Company Name", "Sector"]  # Specify additional columns to include
report_type_c, report_type_g = list_unique_stocks_with_counts_by_report(folder_path, extra_columns=output_columns)

# Save the results to separate files
output_path_c = "path/to/report_type_C_stocks.csv"
output_path_g = "path/to/report_type_G_stocks.csv"

if not report_type_c.empty:
    report_type_c.to_csv(output_path_c, index=False)
    print(f"Report type 'C' results saved to {output_path_c}")

if not report_type_g.empty:
    report_type_g.to_csv(output_path_g, index=False)
    print(f"Report type 'G' results saved to {output_path_g}")
