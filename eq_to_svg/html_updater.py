"""Update HTML with SVG references."""

import re
from pathlib import Path
from typing import List, Tuple

def create_svg_div(name: str, svg_path: str, equation: str) -> str:
    """Create HTML div with SVG image."""
    return f'''<div class="equation">
  <img src="{svg_path}" alt="{equation}">
</div>'''

def get_relative_path(from_path: Path, to_path: Path) -> str:
    """
    Get relative path from one file to another.
    
    Args:
        from_path: Starting file path
        to_path: Target file path
    
    Returns:
        Relative path as string
    """
    # Make sure both paths are absolute
    from_abs = from_path.resolve()
    to_abs = to_path.resolve()
    
    # Get relative path
    try:
        rel_path = to_abs.relative_to(from_abs.parent)
        return str(rel_path).replace('\\', '/')  # Use forward slashes for URLs
    except ValueError:
        # If not in same directory tree, return absolute path
        return str(to_abs).replace('\\', '/')

def insert_svg_divs(html_content: str, 
                   equations: List[Tuple[str, str]], 
                   svg_folder: str,
                   html_file: str) -> str:
    """Insert SVG divs after equation comments with correct relative paths."""
    
    # Get the HTML file's parent directory for relative path calculation
    html_path = Path(html_file).resolve()
    svg_folder_path = Path(svg_folder).resolve()
    
    for equation, name in equations:
        # Construct the full path to the SVG file
        svg_file_path = svg_folder_path / f"{name}.svg"
        
        # Get relative path from HTML to SVG
        relative_svg_path = get_relative_path(html_path, svg_file_path)
        
        # Create the div with correct path
        svg_div = create_svg_div(name, relative_svg_path, equation)
        
        # STRICT pattern: no spaces between $ and <
        # We need to escape the equation for regex
        escaped_equation = re.escape(equation)
        comment_pattern = rf"(^[ \t]*)<!--\s*\${escaped_equation}\$<{name}>\s*-->"
        pattern = re.compile(comment_pattern, re.MULTILINE)
        
        def repl(match):
            indent = match.group(1)  # captures leading tabs/spaces before comment
            div_html = svg_div
            # prepend the indent to every line of div_html
            div_html_indented = "\n".join(indent + line for line in div_html.splitlines())
            
            # Check if div already exists in next 200 characters
            following = html_content[match.end():match.end()+200]
            if '<div class="equation">' in following:
                return match.group(0)  # already exists, skip inserting
            else:
                return match.group(0) + "\n" + div_html_indented
        
        html_content = pattern.sub(repl, html_content)
    
    return html_content