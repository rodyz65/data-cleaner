# Data Cleaner Script (for CSV and Excel files)

This data cleaner script defines a class with various methods for cleaning CSV and Excel files.

## Features

- Handles missing values (both categorical and numerical)
- Removes duplicate rows
- Normalizes categorical data within columns
- Standardizes column names
- Converts data types based on panda's optimized types
- Saves cleaned data to CSV or Excel


## Usage

This script runs from the command line and it requires the user to provide both an input file and output file as arguments.

Example:

```bash
python data_cleaner.py input_file.csv output_file.csv
```
