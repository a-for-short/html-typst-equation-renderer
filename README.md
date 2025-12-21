# Equation Renderer

Convert Typst equations in HTML comments to embedded SVG images.

## Usage

1. Install Typst: https://github.com/typst/typst
2. Clone the repository, create a venv and activate it
    ```
    git clone https://github.com/a-for-short/html-typst-equation-renderer

    cd html-typst-equation-renderer

    python3 -m venv .venv

    source ./.venv/bin/activate
    ```
3. Install Python dependencies: `pip install -r requirements.txt`
4. Place equations in HTML comments:
   ```html
   <!-- $x^2 + y^2 = z^2$<pythagoras> -->
   ```
4. Run: python scripts/render_equations.py
5. Note: you can edit the equations and run the script again

Have fun!