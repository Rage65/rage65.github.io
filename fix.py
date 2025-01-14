import re

def clean_css_indentation(css_code, indent_spaces=2):
    """
    Cleans up unnecessary indents in the provided CSS code.

    Args:
    - css_code (str): The raw CSS code to be cleaned.
    - indent_spaces (int): The number of spaces for each level of indentation. Default is 2 spaces.

    Returns:
    - str: Cleaned CSS code with uniform indentation.
    """
    lines = css_code.splitlines()  # Split the CSS into lines
    cleaned_lines = []
    current_indent_level = 0

    for line in lines:
        stripped_line = line.strip()  # Remove leading/trailing whitespaces
        
        if not stripped_line:  # Skip empty lines
            continue

        # Determine if the line should be indented or not based on braces
        if stripped_line.endswith('}'):
            current_indent_level -= 1
        
        # Add the appropriate indent and line to the cleaned list
        cleaned_lines.append(' ' * (current_indent_level * indent_spaces) + stripped_line)

        if stripped_line.endswith('{'):
            current_indent_level += 1

    return '\n'.join(cleaned_lines)


# Example usage
if __name__ == "__main__":
    # Sample CSS code with unnecessary indentation
    css_code = """
    body {
            background-color: #fff;
    }
    .container {
        margin: 0 auto;
        padding: 10px;
        .child {
            display: flex;
                justify-content: center;
        }
    }
    """

    cleaned_css = clean_css_indentation(css_code)
    print(cleaned_css)
