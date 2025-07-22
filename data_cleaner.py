"""This script defines a class that cleans data files in CSV or Excel format."""
import pandas as pd
import numpy as np
import os
import sys
#This class cleans files containing data in CSV or Excel format.
class DataCleaner:
    def __init__(self,file):
        """Initializing the DataCleaner with a file path."""
        self.file = file
        self.data = None
    def load_data(self):
        """Loading the data into a Pandas Dataframe. Supports CSV or Excel files."""
        ext = os.path.splitext(self.file)[1].lower()
        if ext == '.csv':
            self.data = pd.read_csv(self.file)
        elif ext == '.xlsx' or ext == '.xls':
            self.data = pd.read_excel(self.file)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        print("File loaded successfully.")
        print(self.data.head())
    def handle_missing_values(self,method='drop', fill_value=None):
        """Drops missing values if method='drop' or fills missing values with fill_value if method='fill'."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data using load_data() method.")
        else:
            if method == 'drop':
                self.data.dropna(inplace=True)
            elif method == 'fill':
                if fill_value is None:
                    raise ValueError("fill_value must be provided when method is 'fill'.")
                else:
                    non_numeric_cols = self.data.select_dtypes(exclude=[np.number]).columns
                    for col in non_numeric_cols:
                        self.data[col] = self.data[col].fillna(fill_value)
                    print(f'Missing categorical values filled with {fill_value}.')
    def standardize_columns(self):
        """Standardizes all column names by removing leading/trailing spaces, converting to lowercase, and
        replacing spaces with underscores."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data using load_data() method.")
        
        self.data.columns = [col.strip().lower().replace(" ", "_") for col in self.data.columns]
        print("Columns standardized.")
    def remove_duplicates(self):
        """Removes duplicate rows in the Dataframe and informs the user of how many duplicates were removed."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data using load_data() method.")
        
        before = len(self.data)
        self.data.drop_duplicates(inplace=True)
        after = len(self.data)
        print(f"Removed {before - after} duplicate rows.")
    
    def convert_data_types(self):
        """Converts columns to their best possible data types (Pandas automatically picks optimal data types). 
        Attempts to parse any columns with 'date' in their name as datetime."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data using load_data() method.")
        
        self.data = self.data.convert_dtypes()

        for col in self.data.columns:
            if 'date' in col.lower():
                try:
                    self.data[col] = pd.to_datetime(self.data[col])
                except Exception:
                    pass
        print("Data types converted where applicable.")
    def normalize_categoricals(self):
        """Normalizes categorical data by ensuring that it is all of the string type and by making it
        consistent (lowercased and stripped)."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data using load_data() method.")
        
        for col in self.data.select_dtypes(include=['object']).columns:
            self.data[col] = self.data[col].astype(str).str.strip().str.lower()
        
        print("Categorical data normalized.")
    def save_data(self, output_file):
        """Saves the data as a CSV or Excel file and informs the user which file the data was saved to."""
        if self.data is None:
            raise ValueError("Data not loaded. Please load the data using load_data() method.")
        
        ext = os.path.splitext(output_file)[1].lower()
        if ext == '.csv':
            self.data.to_csv(output_file, index=False)
        elif ext == '.xlsx' or ext == '.xls':
            self.data.to_excel(output_file, index=False)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        full_path = os.path.abspath(output_file)
        print(f"Data saved to {full_path}.")
"""In the main function, the user must provide the input file and output file paths as command line arguments."""
def main():
    # Example usage
    if len(sys.argv) != 3:
        print("Usage: python data_cleaner.py <input_file> <output_file>")
        print("Example: python data_cleaner.py data.csv cleaned_data.csv")
        return
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist. Please provide a valid file path.")
        return
    cleaner = DataCleaner(input_file)
    cleaner.load_data()
    cleaner.handle_missing_values(method='fill', fill_value='Unknown')
    cleaner.standardize_columns()
    cleaner.remove_duplicates()
    cleaner.convert_data_types()
    cleaner.normalize_categoricals()
    cleaner.save_data(output_file)

if __name__ == "__main__":
    main()