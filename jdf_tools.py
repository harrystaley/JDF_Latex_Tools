import pandas as pd
from typing import List, Union

def make_text_latex_safe(text):
    """
    This function takes a string and makes it LaTeX-safe by escaping special characters.
    It replaces characters that have special meaning in LaTeX with their escaped equivalents.
    """
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
        '[': r'\[',
        ']': r'\]'
    }
    
    # Escape special LaTeX characters
    for char, escaped_char in replacements.items():
        text = text.replace(char, escaped_char)
    
    return text


def process_row(row: Union[pd.Series, dict], column_names: List[str]) -> str:
    """
    Processes a single row of data into a LaTeX formatted string.

    Args:
        row (pd.Series or dict): The row data.
        column_names (List[str]): The list of column names.

    Returns:
        str: A LaTeX formatted row string.
    """
    return " & ".join([str(row[col]) for col in column_names]) + r" \\"


def create_jdf_table(data: pd.DataFrame, caption: str, include_index: bool = False, flex_cols: bool = False) -> str:
    """
    Generate LaTeX code for a table from a DataFrame using the to_latex function, 
    with flexible column widths using tabularx.

    Parameters:
        data (pd.DataFrame): The data to include in the table.
        caption (str): The caption for the table.
        include_index (bool): Include the index in the output table.
        flex_cols (bool): Automatically align columns.

    Returns:
        str: The LaTeX code for the table.
    """
    label = caption.replace(" ", "_")

    # Define a flexible column format (including index)
    num_cols = len(data.columns) + 1  # Include index column
    col_format = ' '.join(['X'] * num_cols)
    # Convert DataFrame to LaTeX without automatic column formatting
    latex_code = data.to_latex(
        index=include_index,
        caption=caption,
        label=f"tab:{label}",
        escape=True,
        float_format="%.5f",
        column_format=None,
    )
    if flex_cols:
        lines = latex_code.splitlines()
        for i, line in enumerate(lines):
            if line.startswith(r"\begin{tabular"):
                lines[i] = r"\begin{tabularx}{\textwidth}{" + col_format + "}"
    
        # Replace the \end{tabular} with \end{tabularx}
        latex_code = '\n'.join(lines).replace(r"\end{tabular}", r"\end{tabularx}")
    
    latex_code = latex_code.replace(r"\begin{table}", "\\begin{table}[H]\n\\centering")
    
    return latex_code

def create_jdf_image(image_path: str, width: str = "1\\textwidth") -> str:
    """
    Generate LaTeX code for including an image.

    Parameters:
        image_path (str): The path to the image file.
        width (str): The width of the image in LaTeX format (default is '1\\textwidth').

    Returns:
        str: The LaTeX code for including the image.
    """
    label = image_path.split('/')[-1].split('.')[0]
    caption = label.replace("_", " ").title()

    # Construct the LaTeX code for the image
    latex_out = []
    latex_out.append(r"\begin{figure}[H]")
    latex_out.append(r"\centering")
    latex_out.append(f"\\includegraphics[width={width}]{{{image_path}}}")
    latex_out.append(f"\\caption{{{caption}}}")
    latex_out.append(f"\\label{{fig:{label}}}")
    latex_out.append(r"\end{figure}")

    # Join the LaTeX components into a single string
    return "\n".join(latex_out)

