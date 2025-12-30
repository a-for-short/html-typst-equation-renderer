"""Handle Typst file creation and compilation."""

import re
import subprocess
from pathlib import Path
from typing import List, Tuple

def extract_css_color(css_content: str, css_color_var: str = "--color-quote-border") -> str:
    """Extract color from CSS variable or return default."""
    # Escape the variable name for regex
    escaped_var = re.escape(css_color_var)
    pattern = rf'{escaped_var}:\s*(#[0-9a-fA-F]{{3,8}}|[a-zA-Z]+|rgb\([^)]+\)|rgba\([^)]+\)|hsl\([^)]+\)|hsla\([^)]+\));'
    match = re.search(pattern, css_content)
    return match.group(1) if match else "#000000"

def create_typst_header(css_file: str = None, text_size: int = 20, 
                       text_color: str = "", css_color_var: str = "--color-quote-border") -> str:
    """Create Typst header with styling. CSS file is optional."""
    
    # Determine the color to use based on priority
    color = "#000000"  # Default black
    
    # Priority 1: Use text_color from config if specified
    if text_color:
        color = text_color
        print(f"Using color from config.text_color: {color}")
    
    # Priority 2: Extract from CSS file if text_color not specified
    elif css_file and Path(css_file).exists():
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                # Use the specified CSS variable name
                color = extract_css_color(css_content, css_color_var)
                print(f"Using color from CSS variable '{css_color_var}': {color}")
        except Exception as e:
            print(f"Warning: Could not read CSS file {css_file}: {e}. Using default color.")
    
    elif css_file:
        print(f"Warning: CSS file not found at {css_file}. Using default color.")
    else:
        print("Using default color: #000000")
    return f"""/* ===== START OF HEADER ===== */
#set text(
  size: {text_size}pt,
  fill: rgb("{color}")
)

#set page(
  width: auto,
  height: auto,
  margin: 0pt,
  background: none,
  fill: none,
)
/* ===== END OF HEADER ===== */
"""

def write_typst_files(equations: List[Tuple[str, str]], 
                     typ_folder: str,
                     css_file: str = None,
                     text_size: int = 20,
                     text_color: str = "",
                     css_color_var: str = "--color-quote-border"):
    """Write equations to .typ files with headers."""
    header = create_typst_header(css_file, text_size, text_color, css_color_var)
    
    for equation, name in equations:
        typ_file = Path(typ_folder) / f"{name}.typ"
        content = f"{header}\n$ {equation} $"
        typ_file.write_text(content, encoding="utf-8")

def compile_typst_files(typ_folder: str, svg_folder: str, typst_cmd: str = "typst"):
    """Compile all .typ files to SVG."""
    typ_path = Path(typ_folder)
    
    for typ_file in typ_path.glob("*.typ"):
        svg_file = Path(svg_folder) / f"{typ_file.stem}.svg"
        cmd = [typst_cmd, "compile", "-f", "svg", str(typ_file), str(svg_file)]
        try:
            subprocess.run(cmd, check=True)
            print(f"Compiled: {typ_file.name} -> {svg_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {typ_file.name}: {e}")