import logging
import sys
import os
import time
from datetime import datetime
import pandas as pd
import webbrowser
from pathlib import Path

# Append the path to the utils module to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the logger module
from utils import shcLogger1 as logger

# Define the log file path relative to the current script directory
log_file_path = os.path.join(os.path.dirname(__file__), 'shc.log')

# Set up logging
logger.setup_logging(log_file=log_file_path)

def create_dataframe():
    try:
        logger.log_info("Creating dataframe.")
        data = {
            'name': ['Arun', 'Nam', 'Difference'],
            'num1': [1, 1.2, None],
            'num2': [3, 3, None],
            'num3': [0.25, 0.75, None],
            'num4': [1.0, 1.2, None],
            'num5': [1.2, 1.0, None],
            'num6': [-0.5, 0.5, None],
            'num7': [1.5, -1.6, None],
            'num8': [0.63, 1.32, None],
            'num9': [-0.75, 0.85, None],
            'num10': [1.115, 0.996, None]
        }
        df = pd.DataFrame(data)
        df.loc[2, 'num1':'num10'] = df.loc[0, 'num1':'num10'] - df.loc[1, 'num1':'num10']
        logger.log_info("Dataframe created successfully.")
        return df
    except Exception as e:
        logger.log_error(f"Error creating dataframe: {e}")
        raise

def color_difference(df):
    def apply_color(row):
        if row.name == 2:
            colors = []
            for cell_value in row[1:]:  # Skip the 'name' column
                if isinstance(cell_value, (int, float)):  # Only apply to numeric values
                    if cell_value < 0:
                        colors.append('background-color: red')
                    elif cell_value == 0:
                        colors.append('background-color: blue')
                    elif cell_value > 0:
                        colors.append('background-color: green')
                    else:
                        colors.append('background-color: white')
                else:
                    colors.append('background-color: white')
            return ['background-color: white'] + colors  # Add white background for the 'name' column
        else:
            return ['background-color: white'] * len(row)

    styled_df = df.style.apply(apply_color, axis=1)
    return styled_df

def display_html(df):
    try:
        logger.log_info("Converting dataframe to HTML with styling.")
        styled_df = color_difference(df)
        html = styled_df.to_html()  # Using to_html instead of render
        file_path = Path('output.html')
        file_path.write_text(html, encoding='utf-8')
        logger.log_info(f"HTML conversion successful. File saved as {file_path}")
        webbrowser.open(file_path.resolve().as_uri())
    except Exception as e:
        logger.log_error(f"Error converting dataframe to HTML: {e}")
        raise

def main():
    start_time = time.time()
    df = create_dataframe()
    display_html(df)
    end_time = time.time()
    logger.log_execution_time(start_time, end_time)

if __name__ == "__main__":
    main()
