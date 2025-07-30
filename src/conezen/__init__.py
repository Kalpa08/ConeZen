# conezen/__init__.py

# Expose key logic functions and the main API class at the top level
from .logic import (
    get_branching_plane_vectors,
    compute_surfaces,
    plot_surfaces,
    animate_surfaces,
    load_vector_file,
    extract_atom_symbols,
)

from .api import ConeZenAPI
