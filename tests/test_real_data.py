# tests/test_real_data.py

import numpy as np
import pytest
from pathlib import Path

# Assuming your package structure is src/conezen
from conezen import logic

@pytest.fixture
def real_data_path():
    """
    A pytest fixture that provides the path to the test data directory.
    This makes tests cleaner by not repeating the path everywhere.
    """
    path = Path("tests/test_data")
    if not path.exists():
        pytest.fail(f"Test data directory not found at {path.resolve()}")
    return path

# --- Tests for File Loading with Real Data ---

def test_load_gradient_A(real_data_path):
    """
    Verifies that the `load_vector_file` function can correctly parse
    the real `gradientA.out` file, loading the correct number of atoms
    and skipping no lines.
    """
    grad_file = real_data_path / "gradientA.out"
    data, skipped = logic.load_vector_file(grad_file)

    assert data.shape == (7, 3)
    assert skipped == 0
    # Check if the first value matches the file
    assert np.isclose(data[0, 0], 3.264320588434E-003)

def test_load_gradient_B(real_data_path):
    """
    Verifies that the `load_vector_file` function can correctly parse
    the real `gradientB.out` file.
    """
    grad_file = real_data_path / "gradientB.out"
    data, skipped = logic.load_vector_file(grad_file)
    assert data.shape == (7, 3)
    assert skipped == 0
    # Check if the first value matches the file
    assert np.isclose(data[0, 0], -1.560028982257E-003)

def test_extract_atom_symbols_from_real_xyz(real_data_path):
    """
    Ensures atom symbols are correctly extracted in the right order
    from the provided `orca.xyz` file.
    """
    xyz_file = real_data_path / "orca.xyz"
    atom_list = logic.extract_atom_symbols(xyz_file)
    assert len(atom_list) == 7
    assert atom_list == ["C", "H", "H", "H", "N", "O", "O"]


# --- Test for Core Logic with Real Data ---

# ⚠️ IMPORTANT: You must provide a real 'NAC.out' file in the 'tests/test_data'
#    directory for this test to work. Once you have it, uncomment the test.
#
def test_branching_plane_vectors_with_real_data(real_data_path):
    """
    This is an integration test to validate the core scientific calculation.
    It checks that the branching plane vectors (`x_hat`, `y_hat`) derived
    from real data are mathematically sound (i.e., orthonormal).
    """
    # 1. Load all necessary vector files
    grad_A, _ = logic.load_vector_file(real_data_path / "gradientA.out")
    grad_B, _ = logic.load_vector_file(real_data_path / "gradientB.out")
    nac_file = real_data_path / "NAC.out"
    h_ab, _ = logic.load_vector_file(nac_file)

    # 2. Perform the core calculation
    params = logic.get_branching_plane_vectors(grad_A, grad_B, h_ab)

    # 3. Validate the mathematical properties of the output
    assert params['x_hat'].shape == (21,)
    assert params['y_hat'].shape == (21,)

    # Check that key physical quantities were calculated
    assert isinstance(params['del_gh'], float)
    assert isinstance(params['delta_gh'], float)
    assert isinstance(params['sigma'], float)

    # Check fundamental mathematical properties
    # The branching plane vectors must be orthonormal
    assert np.isclose(np.linalg.norm(params['x_hat']), 1.0), "x_hat vector is not normalized"
    assert np.isclose(np.linalg.norm(params['y_hat']), 1.0), "y_hat vector is not normalized"
    assert np.isclose(np.dot(params['x_hat'], params['y_hat']), 0.0), "x_hat and y_hat are not orthogonal"
