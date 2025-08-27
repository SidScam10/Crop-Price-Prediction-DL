# All .xls files have been deleted and converted into CSV files under the "root/1_Un3_Cleaned CSVs" folder
import pandas as pd
import os
import glob


def batch_convert_html_to_csv(input_folder, output_folder):
    """
    Finds all '.xls' files in an input folder, treats them as HTML,
    extracts the first table from each, and saves it as a CSV file
    in a specified output folder.

    Args:
        input_folder (str): The path to the folder containing the input .xls files.
        output_folder (str): The path to the folder where CSV files will be saved.
    """
    # Create the output directory if it doesn't already exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: '{output_folder}'")

    # Create a search pattern to find all files ending with .xls
    search_pattern = os.path.join(input_folder, "*.xls")

    # Use glob to find all files matching the pattern
    file_list = glob.glob(search_pattern)

    if not file_list:
        print(f"No '.xls' files found in the directory: '{input_folder}'")
        return

    print(f"Found {len(file_list)} files to process...")

    # Loop through each found file
    for html_filename in file_list:
        print("-" * 40)
        print(f"Processing file: '{html_filename}'")

        try:
            # pandas.read_html reads all tables from an HTML file and returns a list of DataFrames.
            list_of_tables = pd.read_html(html_filename)

            if not list_of_tables:
                print("Warning: No tables were found in this file. Skipping.")
                continue

            # Select the first table (DataFrame) from the list
            df = list_of_tables[0]

            # Create the new CSV filename
            base_filename = os.path.basename(html_filename)
            csv_filename = os.path.splitext(base_filename)[0] + ".csv"
            output_path = os.path.join(output_folder, csv_filename)

            # Save the DataFrame to a CSV file.
            df.to_csv(output_path, index=False)

            print(f"Successfully converted and saved data to '{output_path}'")

        except Exception as e:
            print(f"An error occurred while processing '{html_filename}': {e}")


if __name__ == "__main__":
    # The script will look for .xls files in the same directory it is run from.
    input_directory = "."

    # The converted CSV files will be saved in a new folder named 'converted_csvs'.
    output_directory = "converted_csvs"

    # Run the conversion function
    batch_convert_html_to_csv(input_directory, output_directory)
