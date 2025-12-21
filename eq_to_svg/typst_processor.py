"""Handle Typst file creation and compilation."""

import re
import subprocess
from pathlib import Path
from typing import List, Tuple

def extract_css_color(css_content: str) -> str:
    """Extract --color-quote-border from CSS or return default."""
    match = re.search(r'--color-quote-border:\s*(#[0-9a-fA-F]{6}|[a-zA-Z]+);', css_content)
    return match.group(1) if match else "#000000"

def create_typst_header(css_file: str = None, text_size: int = 20) -> str:
    """Create Typst header with styling. CSS file is optional."""
    color = "#000000"  # Default black color
    
    if css_file and Path(css_file).exists():
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
                color = extract_css_color(css_content)
                print(f"Using color from CSS: {color}")
        except Exception as e:
            print(f"Warning: Could not read CSS file {css_file}: {e}. Using default color.")
    elif css_file:
        print(f"Warning: CSS file not found at {css_file}. Using default color.")
    
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
                     text_size: int = 20):
    """Write equations to .typ files with headers."""
    header = create_typst_header(css_file, text_size)
    
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