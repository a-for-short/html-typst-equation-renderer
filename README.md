# Equation Renderer

Convert Typst equations in HTML comments to embedded SVG images.

## Quick Start

1. Install [Typst](https://github.com/typst/typst)
2. Clone and set up:
   ```bash
   git clone https://github.com/a-for-short/html-typst-equation-renderer
   cd html-typst-equation-renderer
   python3 -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Add equations to your HTML:
   ```html
   <!-- $x^2 + y^2 = z^2$<pythagoras> -->
   ```
4. Configure (optional) in `config.yaml`:
   ```yaml
   html_file: "your-document.html"
   text_color: "#336699"  # or leave empty to extract from CSS
   text_size: 24
   ```
5. Run:
   ```bash
   python scripts/render_equations.py
   ```

## How It Works

1. Scans HTML for comments like `<!-- $equation$<name> -->`
2. Creates Typst files for each equation
3. Compiles them to SVG using Typst
4. Inserts the SVG images back into your HTML

## Configuration

Edit `config.yaml` to customize:

- `html_file`: Your HTML document
- `typ_folder`, `svg_folder`: Where to store intermediate files
- `css_file`: Optional CSS for color extraction
- `text_color`: Direct color override (hex, rgb, color names)
- `css_color_var`: Which CSS variable to extract (default: `--color-quote-border`)
- `text_size`: Font size in points

**Color priority**: `text_color` > CSS variable > black

## Re-rendering

If needed edit your equations and run the script again — it only updates what's needed.

## Example

See the `example/` folder for a complete working setup.