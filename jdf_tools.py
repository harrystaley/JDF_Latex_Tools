import pandas as pd


# Function to create LaTeX table using tabularx
def create_jdf_table(data, caption: str, label: str, column_names: list):
    """
    Generate LaTeX code for a table from a DataFrame or list of dictionaries in the specified format.

    Parameters:
    data (pd.DataFrame or list of dicts): The data to include in the table.
    caption (str): The caption for the table.
    label (str): The label for the table.
    column_names (list of str): The column names for the table.

    Returns:
    str: The LaTeX code for the table.
    """
    caption = caption.replace("_", " ").title()
    label = label.replace(" ", "\\_")
    backslash = "\\"  # fixes an issue with python 3.11 where a slash could not be used in f-string.

    # Generate the LaTeX code for the table header
    latex_out = f"""
\\begin{{table}}[H]
\\centering
\\small
\\caption{{{caption}}}
\\label{{{'tab:'+label}}}
\\begin{{tabularx}}{{\\textwidth}}{{ {' '.join(['X' for _ in column_names])} }}
\\textbf{{{column_names[0]}}} & {' & '.join([f'{backslash}textbf{{{name}}}' for name in column_names[1:]])} \\\\
\\toprule[0.5pt]
"""

    # Function to process each row of data
    def process_row(row):
        return " & ".join([str(row[col]) for col in column_names]) + " \\\\"

    # Add the data rows
    if isinstance(data, pd.DataFrame):
        for i, row in data.iterrows():
            latex_out += process_row(row) + "\n"
            if i < len(data) - 1:
                latex_out += "\\midrule\n"
    elif isinstance(data, list):
        for i, row in enumerate(data):
            latex_out += process_row(row) + "\n"
            if i < len(data) - 1:
                latex_out += "\\midrule\n"

    # Add the closing lines
    latex_out += """
\\end{tabularx}
\\end{table}
"""

    return latex_out


def create_jdf_image(image_path: str) -> str:
    """
    Generate LaTeX code for including an image.
    :param image_path: The path to the image file.
    :Returns: The LaTeX code for including the image.
    """
    label = image_path.split('/')[-1].split('.')[0]
    caption = label.replace("_", " ").title()
    latex_out = f"""
\\begin{{figure}}[H]
\\centering
\\includegraphics[width=1\\textwidth]{{{image_path}}}
\\caption{{{caption}}}
\\label{{{'fig:'+label}}}
\\end{{figure}}
"""
    return latex_out
