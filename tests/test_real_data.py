# tests/test_real_data.py

import numpy as np
import pytest
from pathlib import Path

# Assuming your package structure is src/conezen
from conezen import logic
# Import the internal helper functions from the CLI for testing the extraction
from conezen.cli import _generate_state_headers, _extract_gradient, _extract_nac_vector

@pytest.fixture
def real_data_path():
    """
    A pytest fixture that provides the path to the test data directory.
    This makes tests cleaner by not repeating the path everywhere.
    """
    path = Path("tests/test_data")
    if not path.exists():
        pytest.fail(f"Test data directory not found at {path.resolve()}")
    # Ensure the required QM source file exists for the new test
    if not (path / "QM.out").is_file():
        pytest.fail(f"Required test file 'QM.out' not found in {path.resolve()}")
    return path

# --- Original Tests for File Loading (Still Valuable) ---

def test_load_gradient_A(real_data_path):
    """
    Verifies that the `load_vector_file` function can correctly parse
    a pre-made gradient file.
    """
    grad_file = real_data_path / "gradientA.out"
    data, skipped = logic.load_vector_file(grad_file)

    assert data.shape == (7, 3)
    assert skipped == 0
    # CORRECTED: Updated the value to match the actual data in the file.
    assert np.isclose(data[0, 0], 0.003831737668625)

def test_extract_atom_symbols_from_real_xyz(real_data_path):
    """
    Ensures atom symbols are correctly extracted in the right order
    from the provided `orca.xyz` file.
    """
    xyz_file = real_data_path / "orca.xyz"
    atom_list = logic.extract_atom_symbols(xyz_file)
    assert len(atom_list) == 7
    assert atom_list == ["C", "H", "H", "H", "N", "O", "O"]


# --- NEW End-to-End Integration Test ---

def test_extraction_matches_premade_files_and_calculates_correctly(real_data_path):
    """
    This is an integration test to validate the entire automatic workflow.
    1. It loads data from pre-existing gradient/NAC files.
    2. It extracts the same data from a source QM.out file.
    3. It asserts that the extracted data is identical to the pre-made data.
    4. It validates the subsequent scientific calculation using this data.
    """
    # 1. SETUP: Define paths and parameters
    qm_source_file = real_data_path / "QM.out"
    # Note: gradientA.out corresponds to S2, gradientB.out to S3
    lower_state = "S2"
    upper_state = "S3"

    # 2. LOAD PRE-EXISTING FILES
    grad_A_premade, _ = logic.load_vector_file(real_data_path / "gradientA.out")
    grad_B_premade, _ = logic.load_vector_file(real_data_path / "gradientB.out")
    h_ab_premade, _ = logic.load_vector_file(real_data_path / "NAC.out")

    # 3. EXTRACT FROM QM.TXT
    state_headers = _generate_state_headers(num_singlets=13, num_triplets=5)
    _, grad_A_extracted = _extract_gradient(qm_source_file, lower_state, state_headers)
    _, grad_B_extracted = _extract_gradient(qm_source_file, upper_state, state_headers)
    _, h_ab_extracted = _extract_nac_vector(qm_source_file, lower_state, upper_state, state_headers)

    # Assert that all data was successfully extracted
    assert grad_A_extracted is not None, f"Failed to extract gradient for {lower_state}"
    assert grad_B_extracted is not None, f"Failed to extract gradient for {upper_state}"
    assert h_ab_extracted is not None, f"Failed to extract NAC vector for {lower_state}-{upper_state}"

    # 4. COMPARE: Assert that extracted data is identical to the pre-made files
    assert np.allclose(grad_A_premade, grad_A_extracted), "Extracted Gradient A does not match premade file."
    assert np.allclose(grad_B_premade, grad_B_extracted), "Extracted Gradient B does not match premade file."
    assert np.allclose(h_ab_premade, h_ab_extracted), "Extracted NAC vector does not match premade file."

    # 5. CALCULATION: Perform the core calculation using one set of the data (premade)
    params = logic.get_branching_plane_vectors(grad_A_premade, grad_B_premade, h_ab_premade)

    # 6. VALIDATION: Validate the mathematical properties of the final output
    assert params['x_hat'].shape == (21,)
    assert params['y_hat'].shape == (21,)

    # Check that key physical quantities were calculated
    assert isinstance(params['del_gh'], float)
    assert isinstance(params['delta_gh'], float)
    assert isinstance(params['sigma'], float)

    # Check fundamental mathematical properties: the branching plane vectors must be orthonormal
    assert np.isclose(np.linalg.norm(params['x_hat']), 1.0), "x_hat vector is not normalized"
    assert np.isclose(np.linalg.norm(params['y_hat']), 1.0), "y_hat vector is not normalized"
    assert np.isclose(np.dot(params['x_hat'], params['y_hat']), 0.0), "x_hat and y_hat are not orthogonal"
