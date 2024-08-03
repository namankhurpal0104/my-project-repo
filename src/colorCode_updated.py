import logging
import sys
import pandas as pd
import webbrowser
from pathlib import Path
import yaml

def load_config(environment: str) -> dict:
    """
    Load the configuration file for the specified environment.

    Args:
        environment (str): The environment for which to load the configuration.

    Returns:
        dict: The loaded configuration.

    Raises:
        FileNotFoundError: If the config file does not exist.
    """
    try:
        script_dir = Path(__file__).resolve().parent
        config_file = script_dir / 'utils' / 'config' / f'config_{environment}.yaml'
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        with config_file.open('r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        sys.exit(1)

def create_dataframe() -> pd.DataFrame:
    """
    Create a DataFrame with predefined data and calculate the difference.

    Returns:
        pd.DataFrame: The created DataFrame with the difference row added.
    """
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
    return df

def display_html(df: pd.DataFrame, file_path: Path, css_file: Path) -> None:
    """
    Display the DataFrame as an HTML file with styling.

    Args:
        df (pd.DataFrame): The DataFrame to display.
        file_path (Path): The path where the HTML file will be saved.
        css_file (Path): The path to the CSS file for styling.
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        styled_df = df.style.apply(color_difference, axis=1, subset=pd.IndexSlice[2, 'num1':'num10'])
        html = styled_df.to_html()

        # Add HTML5 features
        html_with_style = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="{css_file}">
    <title>DataFrame Display</title>
</head>
<body>
    <header>
        <h1>DataFrame Display</h1>
    </header>
    <section>
        <details>
            <summary>DataFrame Details</summary>
            {html}
        </details>
    </section>
</body>
</html>
'''
        file_path.write_text(html_with_style, encoding='utf-8')
        webbrowser.open(file_path.resolve().as_uri())
    except Exception as e:
        logging.error(f"Error displaying HTML: {e}")
        sys.exit(1)

def color_difference(row: pd.Series) -> list:
    """
    Apply color formatting based on the value.

    Args:
        row (pd.Series): The row of the DataFrame to format.

    Returns:
        list: A list of styles for each cell in the row.
    """
    return [
        'background-color: green' if val > 0 else
        'background-color: red' if val < 0 else
        'background-color: yellow' if val == 0 else ''
        for val in row
    ]

def main() -> None:
    """
    Main function to run the script.
    """
    environment = 'prod'
    config = load_config(environment)
    logging.basicConfig(level=logging.INFO)

    try:
        logging.info("Creating dataframe...")
        df = create_dataframe()

        logging.info("Displaying dataframe as HTML...")
        file_path = Path(config['output']['file_path'])
        css_file = Path(config['output']['css_file'])
        display_html(df, file_path, css_file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
