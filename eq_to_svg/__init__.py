"""Equation to SVG renderer package."""

from .config import Config
from .extractor import find_equations, read_html, write_html
from .typst_processor import write_typst_files, compile_typst_files
from .html_updater import insert_svg_divs

__version__ = "1.0.0"