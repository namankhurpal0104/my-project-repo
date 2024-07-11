import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.shcLogger import setup_logging
import logging

setup_logging()

def create_dataframe():
    try:
        logging.info("Creating dataframe.")
        data = {
            'name': ['Arun', 'Nam', 'Difference'],
            'num1': [1, 1.2, None],
            'num2': [3, 3, None],
            'num3': [0.25, 0.75, None]
        }
        df = pd.DataFrame(data)
        df.loc[2, 'num1':'num3'] = df.loc[0, 'num1':'num3'] - df.loc[1, 'num1':'num3']
        logging.info("Dataframe created successfully.")
        return df
    except Exception as e:
        logging.error(f"Error creating dataframe: {e}")
        raise

def display_heatmap(df):
    try:
        logging.info("Displaying heatmap.")
        mask = df[['num1', 'num2', 'num3']].notnull()
        mask.iloc[0:2, :] = False  # Mask the first two rows

        plt.figure(figsize=(5, 3))
        sns.heatmap(df[['num1', 'num2', 'num3']], annot=True, cmap='coolwarm', cbar=False, linewidths=.5, mask=~mask, linecolor='black')
        
        # Plot white background for first two rows
        for i in range(2):
            for j in range(df.shape[1] - 1):
                plt.gca().add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color='white', edgecolor='black'))
                plt.text(j + 0.5, i + 0.5, str(df.iloc[i, j+1]), ha='center', va='center', color='black')
        
        plt.show()
        logging.info("Heatmap displayed successfully.")
    except Exception as e:
        logging.error(f"Error displaying heatmap: {e}")
        raise

def color_difference(df):
    def apply_color(row):
        if row.name == 2:
            colors = []
            for cell_value in row:
                if cell_value < 0:
                    colors.append('background-color: red')
                elif cell_value == 0:
                    colors.append('background-color: blue')
                elif cell_value > 0:
                    colors.append('background-color: green')
                else:
                    colors.append('background-color: white')
            return colors
        else:
            return ['background-color: white'] * len(row)

    styled_df = df.style.apply(apply_color, axis=1)
    return styled_df

def display_html(df):
    try:
        logging.info("Converting dataframe to HTML with styling.")
        styled_df = color_difference(df)
        html = styled_df.render()
        logging.info("HTML conversion successful.")
        return html
    except Exception as e:
        logging.error(f"Error converting dataframe to HTML: {e}")
        raise

def main():
    df = create_dataframe()
    display_heatmap(df)
    html_output = display_html(df)
    print(html_output)

if __name__ == "__main__":
    main()
