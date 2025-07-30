# conezen/cli.py

import sys
import shutil
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# This is the logic from your other file, now part of ConeZen
from . import logic

# --- GRADIENT & NAC EXTRACTION HELPERS ---

def _generate_state_headers(num_singlets=20, num_triplets=20):
    """Generates a dictionary mapping common state names to their file header patterns."""
    headers = {}
    # FIX: According to SHARC-Molcas convention (and the project's README),
    # the ground state S0 is s1 1, S1 is s1 2, and so on.
    # Therefore, state Sn corresponds to the header number n+1.
    for n in range(num_singlets): # n goes from 0 to 19
        state_name = f"S{n}"
        headers[state_name] = f"m1 1 s1 {n+1} ms1 0"

    # For triplets, T1 is typically the lowest, corresponding to s1 1 in the triplet manifold.
    for n in range(1, num_triplets + 1):
        state_name_base = f"T{n}"
        headers[f"{state_name_base}_ms-1"] = f"m1 3 s1 {n} ms1 -1"
        headers[f"{state_name_base}_ms0"]  = f"m1 3 s1 {n} ms1 0"
        headers[f"{state_name_base}_ms+1"] = f"m1 3 s1 {n} ms1 1"
    return headers

def _extract_gradient(file_path, state_name, state_headers):
    """
    Extracts a gradient for a given state, returning the header and numpy array.
    """
    header_to_find = state_headers.get(state_name.upper())
    if not header_to_find:
        print(f"❌ Error: State '{state_name}' is not defined in the header dictionary.")
        return None, None

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: The gradient source file '{file_path}' was not found.")
        return None, None

    for i, line in enumerate(lines):
        parts = line.strip().split()
        # Make the search more specific. The header line for gradients
        # should start with the number of atoms (a digit).
        if parts and parts[0].isdigit() and header_to_find in line and "m2" not in line:
            found_header_line = line.strip()
            gradient_data = []
            try:
                num_atoms = int(parts[0])
                if i + 1 + num_atoms > len(lines):
                    return None, None
                for j in range(num_atoms):
                    data_line = lines[i + 1 + j].strip().split()
                    gradient_data.append([float(x) for x in data_line])
                return found_header_line, np.array(gradient_data)
            except (ValueError, IndexError):
                return None, None
    return None, None

def _format_nac_part2(state_header_part):
    """Converts a gradient-style header part to a NAC part 2 style."""
    # e.g., "m1 1 s1 4 ms1 0" -> "m2 1 s2 4 ms2 0"
    parts = state_header_part.split()
    parts[0] = 'm2'
    parts[2] = 's2'
    parts[4] = 'ms2'
    return " ".join(parts)

def _extract_nac_vector(file_path, state1_name, state2_name, state_headers):
    """
    Extracts the NAC vector between two states, accounting for commutative headers.
    """
    part1_raw = state_headers.get(state1_name.upper())
    part2_raw = state_headers.get(state2_name.upper())

    if not part1_raw or not part2_raw:
        print(f"❌ Error: One or both states ('{state1_name}', '{state2_name}') are not defined.")
        return None, None

    # Construct the two possible header combinations, e.g., (S2,S3) and (S3,S2)
    header_combo1 = f"{part1_raw}   {_format_nac_part2(part2_raw)}"
    header_combo2 = f"{part2_raw}   {_format_nac_part2(part1_raw)}"

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: The NAC source file '{file_path}' was not found.")
        return None, None

    for i, line in enumerate(lines):
        # Check for both possible header orders
        if header_combo1 in line or header_combo2 in line:
            found_header_line = line.strip()
            nac_data = []
            try:
                num_atoms = int(line.strip().split()[0])
                if i + 1 + num_atoms > len(lines):
                    return None, None
                for j in range(num_atoms):
                    data_line = lines[i + 1 + j].strip().split()
                    nac_data.append([float(x) for x in data_line])
                return found_header_line, np.array(nac_data)
            except (ValueError, IndexError):
                return None, None
    return None, None


# --- USER INTERACTION HELPERS ---
def print_about():
    """Display script info and citation."""
    term_width = shutil.get_terminal_size().columns
    lines = [
        "="*60, "ConeZen: Conical Intersection Branching Plane Visualization", "="*60,
        "📄  Citation:", "    If you use ConeZen in your published work, please cite:",
        "    Kalpa Dihingia, ConeZen: Visualiser for Conical Intersection Branching Planes,",
        "    Zenodo DOI: [add your DOI here once minted]", "",
        "🔬  Generates a 3D model of potential energy surfaces near a CI.", "",
        "✏️  Author: Kalpa Dihingia", "🏛️  Institute: Banaras Hindu University (BHU)", "",
        "🔗  License: GPLv3. Please cite the relevant paper if used.", "="*60,
    ]
    for line in lines:
        print(line.center(term_width))

def ask_yes_no(prompt: str) -> bool:
    """Prompt user for yes/no."""
    while True:
        answer = input(prompt + " [y/n]: ").strip().lower()
        if answer in {'y', 'yes'}: return True
        if answer in {'n', 'no'}: return False
        print("❌ Invalid input. Please enter 'y' or 'n'.")

def get_numeric(prompt: str, default=None, type_cast=float):
    """Prompt user for a numeric (float or int) value."""
    while True:
        val = input(prompt + (f" (default: {default}): " if default is not None else ": ")).strip()
        if val == "" and default is not None: return default
        try:
            return type_cast(val)
        except ValueError:
            print(f"❌ Invalid input. Please enter a {type_cast.__name__} value.")

def get_file(prompt: str, must_exist=True, default=None):
    """Prompt user for a filename, optionally requiring existence."""
    while True:
        fname = input(prompt + (f" (default: {default}): " if default else ": ")).strip() or default
        if fname is None:
            print("❌ Filename required."); continue
        path = Path(fname)
        if must_exist and not path.is_file():
            print(f"❌ File '{fname}' not found."); continue
        return path

def get_state_name(prompt: str) -> str:
    """Get a non-empty state name from the user."""
    while True:
        state_name = input(prompt).strip().upper()
        if state_name:
            return state_name
        print("❌ State name cannot be empty. Please enter a value.")


def safe_save_path(prompt: str, default: str):
    """Prompt for a save path, warn if exists."""
    while True:
        fname = input(prompt + f" (default: {default}): ").strip() or default
        path = Path(fname)
        if path.exists():
            if ask_yes_no(f"File '{fname}' exists. Overwrite?"): return path
        else:
            return path

# --- MAIN COMMAND-LINE ENTRY POINT ---
def main():
    """Main function to run the command-line tool."""
    try:
        print_about()

        params = None
        # This variable will hold one of the original vector files (e.g., grad_A or x_hat)
        # to determine the number of atoms, N, for reshaping arrays later.
        vector_for_atom_count = None

        # --- Stage 1: Get parameters via one of three workflows ---

        if ask_yes_no("Do you want to automatically extract gradients and NACs from a QM output file? (sharc-molcas only)"):
            # --- WORKFLOW 1: Automatic Extraction from QM.out ---
            grad_source_file = get_file("Enter the source QM file name", default="QM.out")
            num_singlets = get_numeric("Enter the total number of singlet states", default=20, type_cast=int)
            num_triplets = get_numeric("Enter the total number of triplet states", default=20, type_cast=int)
            state_headers = _generate_state_headers(num_singlets=num_singlets, num_triplets=num_triplets)

            lower_state = get_state_name("Enter the lower state (e.g., S2): ")
            upper_state = get_state_name("Enter the upper state (e.g., S3): ")

            header_A, grad_A_data = _extract_gradient(grad_source_file, lower_state, state_headers)
            if grad_A_data is not None:
                grad_fileA = Path(f"{lower_state}_gradient.out")
                with open(grad_fileA, 'w') as f: f.write(header_A + '\n'); np.savetxt(f, grad_A_data, fmt='%18.10f')
                print(f"✅ Successfully extracted and saved '{grad_fileA}'")
            else:
                print(f"❌ Failed to extract gradient for '{lower_state}'. Exiting."); sys.exit(1)

            header_B, grad_B_data = _extract_gradient(grad_source_file, upper_state, state_headers)
            if grad_B_data is not None:
                grad_fileB = Path(f"{upper_state}_gradient.out")
                with open(grad_fileB, 'w') as f: f.write(header_B + '\n'); np.savetxt(f, grad_B_data, fmt='%18.10f')
                print(f"✅ Successfully extracted and saved '{grad_fileB}'")
            else:
                print(f"❌ Failed to extract gradient for '{upper_state}'. Exiting."); sys.exit(1)

            header_NAC, nac_data = _extract_nac_vector(grad_source_file, lower_state, upper_state, state_headers)
            if nac_data is not None:
                nac_file = Path(f"NAC_{lower_state}_{upper_state}.out")
                with open(nac_file, 'w') as f: f.write(header_NAC + '\n'); np.savetxt(f, nac_data, fmt='%18.10f')
                print(f"✅ Automatically extracted and saved '{nac_file}'")
            else:
                print(f"❌ Failed to automatically extract NAC vector. Please provide it manually.")
                nac_file = get_file("Enter the NAC vector file name", default="NAC.out")

            grad_A, skipped_A = logic.load_vector_file(grad_fileA)
            grad_B, skipped_B = logic.load_vector_file(grad_fileB)
            h, skipped_h = logic.load_vector_file(nac_file)
            vector_for_atom_count = grad_A
            if any([skipped_A, skipped_B, skipped_h]): print(f"⚠️  Skipped malformed lines in one or more input files.")
            params = logic.get_branching_plane_vectors(grad_A, grad_B, h)

        else:
            if ask_yes_no("Do you have the raw gradient and non-adiabatic coupling vectors to calculate the parameters?"):
                # --- WORKFLOW 2: Manual Gradient/NAC files ---
                grad_fileA = get_file("Enter the gradient file name for State A", default="gradientA.out")
                grad_fileB = get_file("Enter the gradient file name for State B", default="gradientB.out")
                nac_file = get_file("Enter the NAC vector file name", default="NAC.out")

                grad_A, skipped_A = logic.load_vector_file(grad_fileA)
                grad_B, skipped_B = logic.load_vector_file(grad_fileB)
                h, skipped_h = logic.load_vector_file(nac_file)
                vector_for_atom_count = grad_A
                if any([skipped_A, skipped_B, skipped_h]): print(f"⚠️  Skipped malformed lines in one or more input files.")
                params = logic.get_branching_plane_vectors(grad_A, grad_B, h)

            else:
                # --- WORKFLOW 3: Manual x/y vectors and parameters ---
                print("\n➡️  Entering manual mode: Provide orthonormal vectors (x_hat, y_hat) and CI parameters directly.")
                x_vec_file = get_file("Enter the file for the x_hat vector", default="x_vectors.in")
                y_vec_file = get_file("Enter the file for the y_hat vector", default="y_vectors.in")

                x_hat_vec, skipped_x = logic.load_vector_file(x_vec_file)
                y_hat_vec, skipped_y = logic.load_vector_file(y_vec_file)
                vector_for_atom_count = x_hat_vec

                if skipped_x or skipped_y: print("⚠️  Skipped malformed lines in one or more vector files.")
                if x_hat_vec.shape != y_hat_vec.shape:
                    print(f"❌ Error: x_hat ({x_hat_vec.shape}) and y_hat ({y_hat_vec.shape}) vectors have mismatched shapes. Exiting.")
                    sys.exit(1)

                print("\nPlease enter the conical intersection parameters:")
                del_gh = get_numeric("Enter del_gh (δ_gh)")
                delta_gh = get_numeric("Enter delta_gh (Δ_gh)")
                sigma = get_numeric("Enter sigma (σ)")
                theta_s_deg = get_numeric("Enter theta_s (θ_s) in degrees")
                theta_s_rad = np.radians(theta_s_deg)

                params = {
                    'x_hat': x_hat_vec.flatten(),
                    'y_hat': y_hat_vec.flatten(),
                    'del_gh': del_gh,
                    'delta_gh': delta_gh,
                    'sigma': sigma,
                    'theta_s_rad': theta_s_rad
                }

        # --- Stage 2: Common processing using the 'params' dictionary ---

        if params is None:
            print("\n❌ A workflow was not completed. Cannot proceed. Exiting.")
            sys.exit(1)

        print("\n" + "="*40)
        print("  Branching Plane Key Quantities")
        print(f"theta_s (θ_s) in degrees: {np.degrees(params['theta_s_rad']):.6f}")
        print(f"del_gh (δ_gh): {params['del_gh']:.6f}")
        print(f"delta_gh (Δ_gh): {params['delta_gh']:.6f}")
        print(f"sigma (σ): {params['sigma']:.6f}")
        print("="*40 + "\n")

        if ask_yes_no("Save branching plane key quantities to a file?"):
            params_path = safe_save_path("Enter filename for parameters", default="ci_parameters.txt")
            with open(params_path, "w") as f:
                f.write("Branching Plane Key Quantities\n" + "="*40 + "\n")
                f.write(f"theta_s (θ_s) in degrees: {np.degrees(params['theta_s_rad']):.6f}\n")
                f.write(f"del_gh (δ_gh): {params['del_gh']:.6f}\n")
                f.write(f"delta_gh (Δ_gh): {params['delta_gh']:.6f}\n")
                f.write(f"sigma (σ): {params['sigma']:.6f}\n")
            print(f"✅ Key quantities saved to '{params_path}'\n")

        E_X = get_numeric("Enter the energy of the intersection point (Hartree)", default=logic.DEFAULT_EX)

        # --- Stage 3: Output vectors, compute surfaces, plot ---

        N = vector_for_atom_count.shape[0]
        x_hat_2d = params['x_hat'].reshape(N, 3)
        y_hat_2d = params['y_hat'].reshape(N, 3)

        if ask_yes_no("Add atom labels from an XYZ file to the output vectors?"):
            xyz_file = get_file("Enter the xyz file name for atom labels", default="orca.xyz")
            atom_list = logic.extract_atom_symbols(xyz_file)
            if len(atom_list) != N:
                print(f"⚠️  Warning: XYZ file has {len(atom_list)} atoms, but vector files have {N}. Output may be misaligned.")
            with open("x_vectors.out", "w") as f:
                f.write("atoms x y z\n"); df = pd.DataFrame(x_hat_2d, columns=['x', 'y', 'z']); df.insert(0, 'Atom', atom_list)
                df.to_csv(f, sep=' ', index=False, header=False, float_format="%.10f")
            with open("y_vectors.out", "w") as f:
                f.write("atoms x y z\n"); df = pd.DataFrame(y_hat_2d, columns=['x', 'y', 'z']); df.insert(0, 'Atom', atom_list)
                df.to_csv(f, sep=' ', index=False, header=False, float_format="%.10f")
        else:
            with open("x_vectors.out", "w") as f: f.write("x y z\n"); np.savetxt(f, x_hat_2d, fmt='%18.10f')
            with open("y_vectors.out", "w") as f: f.write("x y z\n"); np.savetxt(f, y_hat_2d, fmt='%18.10f')
        print("✅ x_hat and y_hat vectors saved to x_vectors.out and y_vectors.out")

        X, Y, E_A, E_B, had_neg_sqrt = logic.compute_surfaces(params, E_X)
        if had_neg_sqrt:
            print("⚠️  Some negative values in sqrt term were set to zero during surface calculation.")

        if ask_yes_no("Show 3D surface plot now?"):
            fig_w = get_numeric("Figure width (inches)", default=logic.DEFAULT_FIGSIZE[0])
            fig_h = get_numeric("Figure height (inches)", default=logic.DEFAULT_FIGSIZE[1])
            logic.plot_surfaces(X, Y, E_A, E_B, fig_w, fig_h)
            plt.show()

        if ask_yes_no("Save the 3D plot as image?"):
            outpath = safe_save_path("Image filename", "conical_intersection.png")
            dpi = get_numeric("DPI", default=logic.DEFAULT_DPI, type_cast=int)
            fig, ax = logic.plot_surfaces(X, Y, E_A, E_B, logic.DEFAULT_FIGSIZE[0], logic.DEFAULT_FIGSIZE[1])
            fig.savefig(outpath, dpi=dpi, bbox_inches='tight')
            plt.close(fig)
            print(f"✅ Saved static image as '{outpath}'")

        if ask_yes_no("Create a rotation animation?"):
            if ask_yes_no("Save animation as MP4?"):
                mp4_path = safe_save_path("MP4 filename", "conical_intersection_rotation.mp4")
                logic.animate_surfaces(X, Y, E_A, E_B, logic.DEFAULT_FIGSIZE[0], logic.DEFAULT_FIGSIZE[1], logic.DEFAULT_ANIM_DPI, logic.DEFAULT_ANIM_FPS, mp4_path, writer='ffmpeg')
            if ask_yes_no("Save animation as GIF?"):
                gif_path = safe_save_path("GIF filename", "conical_intersection_rotation.gif")
                logic.animate_surfaces(X, Y, E_A, E_B, logic.DEFAULT_FIGSIZE[0], logic.DEFAULT_FIGSIZE[1], logic.DEFAULT_ANIM_DPI, logic.DEFAULT_ANIM_FPS, gif_path, writer='pillow')

        print("\n All Done! Thank you for using ConeZen.")

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting gracefully.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
