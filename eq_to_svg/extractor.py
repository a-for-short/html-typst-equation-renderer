"""Extract equations from HTML comments."""

import re
from typing import List, Tuple
from pathlib import Path

def find_equations(html_content: str) -> List[Tuple[str, str]]:
    """
    Find equations in HTML comments.
    
    Format: <!-- $equation$<name> -->
    - Spaces/newlines allowed around the comment
    - NO spaces allowed between $$ and <>
    Returns: List of (equation, name) tuples
    """
    # Pattern explanation:
    # <!--\s*     - Comment start, optional whitespace
    # \$(.*?)\$   - Equation between dollar signs
    # <([^>]+)>   - Name in angle brackets (no spaces between $ and <)
    # \s*-->      - Optional whitespace, comment end
    pattern = re.compile(r"<!--\s*\$(.*?)\$<([^>]+)>\s*-->")
    
    # For debugging: print found matches
    matches = pattern.findall(html_content)
    if matches:
        print(f"Found {len(matches)} equation(s):")
        for eq, name in matches:
            print(f"  - {name}: ${eq}$")
    
    return matches

def read_html(file_path: str) -> str:
    """Read HTML file content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_html(file_path: str, content: str):
    """Write HTML file content."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)