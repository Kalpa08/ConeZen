# conezen/cli.py

import sys
import shutil
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from . import logic

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
        # -- Input files
        grad_fileA = get_file("Enter the gradient file name for State A", default="gradientA.out")
        grad_fileB = get_file("Enter the gradient file name for State B", default="gradientB.out")
        nac_file = get_file("Enter the NAC vector file name", default="NAC.out")
        
        grad_A, skipped_A = logic.load_vector_file(grad_fileA)
        grad_B, skipped_B = logic.load_vector_file(grad_fileB)
        h, skipped_h = logic.load_vector_file(nac_file)

        if any([skipped_A, skipped_B, skipped_h]):
             print(f"⚠️  Skipped malformed lines in one or more input files.")

        # -- Numeric/energy inputs
        E_X = get_numeric("Enter the energy of the intersection point (Hartree)", default=logic.DEFAULT_EX)

        # -- Core calculation
        params = logic.get_branching_plane_vectors(grad_A, grad_B, h)
        print("\n" + "="*40)
        print("  Branching Plane Key Quantities")
        print(f"theta_s (θ_s) in degrees: {logic.np.degrees(params['theta_s_rad']):.6f}")
        print(f"del_gh (δ_gh): {params['del_gh']:.6f}")
        print(f"delta_gh (Δ_gh): {params['delta_gh']:.6f}")
        print(f"sigma (σ): {params['sigma']:.6f}")
        print("="*40 + "\n")

       # -- (Optional) Save key quantities to a file
        if ask_yes_no("Save branching plane key quantities to a file?"):
            params_path = safe_save_path("Enter filename for parameters", default="ci_parameters.txt")
            with open(params_path, "w") as f:
                f.write("Branching Plane Key Quantities\n")
                f.write("="*40 + "\n")
                f.write(f"theta_s (θ_s) in degrees: {logic.np.degrees(params['theta_s_rad']):.6f}\n")
                f.write(f"del_gh (δ_gh): {params['del_gh']:.6f}\n")
                f.write(f"delta_gh (Δ_gh): {params['delta_gh']:.6f}\n")
                f.write(f"sigma (σ): {params['sigma']:.6f}\n")
            print(f"✅ Key quantities saved to '{params_path}'\n")

        xyz_file = get_file("Enter the xyz file name for atom labels", default="orca.xyz")
        atom_list = logic.extract_atom_symbols(xyz_file)
        
        N = len(atom_list)
        x_hat_2d = params['x_hat'].reshape(N, 3)
        y_hat_2d = params['y_hat'].reshape(N, 3)

        with open("x_vectors.out", "w") as f:
            f.write("atoms x vectors\n")
            pd.DataFrame({'Atom': atom_list, 'x': x_hat_2d[:,0], 'y': x_hat_2d[:,1], 'z': x_hat_2d[:,2]}).to_csv(f, sep=' ', index=False, header=False, float_format="%.10f")
        with open("y_vectors.out", "w") as f:
            f.write("atoms y vectors\n")
            pd.DataFrame({'Atom': atom_list, 'x': y_hat_2d[:,0], 'y': y_hat_2d[:,1], 'z': y_hat_2d[:,2]}).to_csv(f, sep=' ', index=False, header=False, float_format="%.10f")
        print("✅ x_hat and y_hat vectors saved to x_vectors.out and y_vectors.out")

        X, Y, E_A, E_B, had_neg_sqrt = logic.compute_surfaces(params, E_X)
        if had_neg_sqrt:
            print("⚠️  Some negative values in sqrt term were set to zero during surface calculation.")

        # -- Plotting & Animation
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
            plt.close(fig) # Close the figure to free up memory
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
