#!/usr/bin/env python3
"""Main CLI for rendering equations."""

import sys
from pathlib import Path

# Add parent directory to path to import our package
sys.path.insert(0, str(Path(__file__).parent.parent))

from eq_to_svg import (
    Config, find_equations, read_html, write_html,
    write_typst_files, compile_typst_files, insert_svg_divs
)

def main():
    """Main rendering pipeline."""
    # Load configuration
    try:
        config = Config.from_yaml()
        print(f"Configuration loaded: {config}")
    except Exception as e:
        print(f"Error loading config.yaml: {e}")
        print("Using default configuration...")
        config = Config()
    
    # Create directories if they don't exist
    config.ensure_dirs()
    
    # Check if HTML file exists
    if not Path(config.html_file).exists():
        print(f"Error: HTML file not found: {config.html_file}")
        print(f"Current directory: {Path.cwd()}")
        return
    
    print(f"Processing HTML file: {config.html_file}")
    
    # Extract equations
    try:
        html_content = read_html(config.html_file)
        equations = find_equations(html_content)
    except Exception as e:
        print(f"Error reading HTML: {e}")
        return
    
    if not equations:
        print("No equations found in the format: <!-- $equation$<name> -->")
        print("Example: <!-- $E=mc^2$<energy> -->")
        return
    
    print(f"\nProcessing {len(equations)} equation(s)...")
    
# Create Typst files
    try:
        write_typst_files(equations, config.typ_folder, 
                        config.css_file, config.text_size,
                        config.text_color, config.css_color_var)
        print(f"✓ Created .typ files in {config.typ_folder}")
    except Exception as e:
        print(f"✗ Error creating Typst files: {e}")
        return
    
    # Compile to SVG
    try:
        compile_typst_files(config.typ_folder, config.svg_folder, config.typst_command)
        print(f"✓ Compiled SVG files to {config.svg_folder}")
    except Exception as e:
        print(f"✗ Error compiling Typst files: {e}")
        print("Make sure Typst is installed: https://github.com/typst/typst")
        return
    
    # Update HTML
    try:
        updated_html = insert_svg_divs(html_content, equations, 
                                      config.svg_folder, config.html_file)
        write_html(config.html_file, updated_html)
        print(f"✓ Updated {config.html_file}")
    except Exception as e:
        print(f"✗ Error updating HTML: {e}")
        return
    
    print("\n✅ All done!")

if __name__ == "__main__":
    main()