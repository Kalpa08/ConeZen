#!/usr/bin/env python3
# ==============================================================================
# ConeZen: Visualiser for Conical Intersection Branching Planes
# ==============================================================================
#
# 📄 If you use this script in your published work, please cite:
#   Kalpa Dihingia, ConeZen: Visualiser for Conical Intersection Branching Planes,
#   Zenodo DOI: [add your DOI here once minted]
#
# ------------------------------------------------------------------------------
# Copyright (C) 2025 Kalpa Dihingia
#
# This script is distributed under the GNU General Public License v3.0 (GPLv3).
# You are free to use, modify, and share it under the terms of the license.
# See the LICENSE file for details.
#
# Portions of the theory and equations are derived from:
#   Ignacio Fdez. Galván, Mickaël G. Delcey, Thomas Bondo Pedersen,
#   Francesco Aquilante, and Roland Lindh,
#   "Analytical State-Average Complete-Active-Space Self-Consistent Field
#   Nonadiabatic Coupling Vectors: Implementation with Density-Fitted Two-Electron
#   Integrals", JCTC 2016, 12(8), 3636–3653. DOI: 10.1021/acs.jctc.6b00384
#
# 🏛️  Developed at Banaras Hindu University (BHU).
#
# 🔗  For full citation and metadata, see CITATION.cff and .zenodo.json.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# ==============================================================================

import numpy as np
import pandas as pd
import shutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path
import sys

# ------------------------ CONSTANTS & DEFAULTS -------------------------------

DEFAULT_DPI = 300
DEFAULT_FIGSIZE = (10, 8)
DEFAULT_ANIM_DPI = 200
DEFAULT_ANIM_FPS = 20
R_GRID = np.linspace(0, 0.001, 500)
THETA_GRID = np.linspace(0, 2 * np.pi, 500)
DEFAULT_EX=0 # hartree energy at crossing point

# -------------------------- UTILITY FUNCTIONS --------------------------------

def print_about():
    """Display script info and citation."""
    term_width = shutil.get_terminal_size().columns
    lines = [
        "="*60,
        "Conical Intersection Branching Plane Visualization",
        "="*60,
        "📄  Citation:",
        "    If you use ConeZen in your published work, please cite:",
        "    Kalpa Dihingia, ConeZen: Visualiser for Conical Intersection Branching Planes,",
        "    Zenodo DOI: [add your DOI here once minted]",
        "",
        "🔬  Generates a 3D model of potential energy surfaces near a CI.",
        "",
        "✏️  Author: Kalpa Dihingia",
        "🏛️  Institute: Banaras Hindu University (BHU)",
        "",
        "📄  Usage:",
        "   1) Prepare input files: gradients (A & B), NAC vector file.",
        "   2) Run: python3 ci_branching_plane.py",
        "   3) Follow prompts for input and output.",
        "",
        "🔗  License: GPLv3. Please cite the relevant paper if used.",
        "="*60,
    ]
    for line in lines:
        print(line.center(term_width))

def ask_yes_no(prompt: str) -> bool:
    """Prompt user for yes/no."""
    while True:
        answer = input(prompt + " [y/n]: ").strip().lower()
        if answer in {'y', 'yes'}:
            return True
        if answer in {'n', 'no'}:
            return False
        print("❌ Invalid input. Please enter 'y' or 'n'.")

def get_numeric(prompt: str, default=None, type_cast=float):
    """Prompt user for a numeric (float or int) value."""
    while True:
        val = input(prompt + (f" (default: {default}): " if default is not None else ": ")).strip()
        if val == "" and default is not None:
            return default
        try:
            return type_cast(val)
        except ValueError:
            print(f"❌ Invalid input. Please enter a {type_cast.__name__} value.")

def get_file(prompt: str, must_exist=True, default=None):
    """Prompt user for a filename, optionally requiring existence."""
    while True:
        fname = input(prompt + (f" (default: {default}): " if default else ": ")).strip() or default
        if fname is None:
            print("❌ Filename required.")
            continue
        path = Path(fname)
        if must_exist and not path.is_file():
            print(f"❌ File '{fname}' not found.")
            continue
        return path

def safe_save_path(prompt: str, default: str):
    """Prompt for a save path, warn if exists."""
    while True:
        fname = input(prompt + f" (default: {default}): ").strip() or default
        path = Path(fname)
        if path.exists():
            overwrite = ask_yes_no(f"File '{fname}' exists. Overwrite?")
            if overwrite:
                return path
        else:
            return path

def load_vector_file(path: Path):
    """Load 3D vector data (skipping header) from file."""
    data = []
    skipped = 0
    with path.open() as f:
        lines = f.readlines()[1:]  # Skip header
        for i, line in enumerate(lines, start=2):
            parts = line.strip().split()
            if len(parts) < 3:
                skipped += 1
                continue
            try:
                data.append([float(x) for x in parts[:3]])
            except ValueError:
                skipped += 1
    if skipped:
        print(f"⚠️  Skipped {skipped} malformed lines in {path.name}.")
    return np.array(data)
def extract_atom_symbols(xyz_file):
    atom_list = []
    with open(xyz_file, "r") as f:
        lines = f.readlines()
        for line in lines[2:]:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            atom_list.append(parts[0])
    return atom_list

# --------------------------- CORE LOGIC FUNCTIONS ----------------------------

def get_branching_plane_vectors(grad_A, grad_B, h):
    """Compute the branching plane vectors and related quantities[Eq. 36, 37]."""
    g_ab = 0.5 * (grad_B - grad_A)
    s_ab = 0.5 * (grad_B + grad_A)
    g_ab = g_ab.flatten()
    s_ab = s_ab.flatten()      
    h_ab = h.flatten()
    #print("original |g_ab|", np.linalg.norm(g_ab))
    #print("original |h_ab|", np.linalg.norm(h_ab))
    # Scaling h_ab to g_ab before orthogonalization
    h_ab=h_ab*(np.linalg.norm(g_ab)/np.linalg.norm(h_ab))
    #print("original g_ab", g_ab)
    #print("original h_ab scaled", h_ab)
    #print("magnitute of scaled g or |g|", np.linalg.norm(g_ab))
    #print("magnitute of scaled h or |h|", np.linalg.norm(h_ab))
    #angle_gh = np.arccos(np.clip(np.dot(g_ab, h_ab) / (np.linalg.norm(g_ab) * np.linalg.norm(h_ab)), -1.0, 1.0))
    #print(f"Initial angle between g and h vectors: {np.degrees(angle_gh):.3f} degrees")
    numerator = 2 * np.dot(g_ab, h_ab)
    denominator = np.dot(g_ab, g_ab) - np.dot(h_ab, h_ab)
    beta_rad = 0.5 * np.arctan2(numerator, denominator)
    cosb, sinb = np.cos(beta_rad), np.sin(beta_rad)
    # Rotation of two intersecting states by an angle beta/2 causes transformation in the
    # corresponding g_ab and h_ab vectors [Eq 38 and 39]
    g_tilde = g_ab * cosb + h_ab * sinb
    h_tilde = h_ab * cosb - g_ab * sinb
    g2, h2 = np.dot(g_tilde, g_tilde), np.dot(h_tilde, h_tilde)
    x_hat = g_tilde / np.sqrt(g2) # Eq. 41
    y_hat = h_tilde / np.sqrt(h2) # Eq. 41
    del_gh = np.sqrt(0.5 * (g2 + h2)) #Eq. 44
    delta_gh = (g2 - h2) / (g2 + h2)  # Eq. 45
    s_x = np.dot(s_ab, x_hat) / del_gh  # Eq. 49 
    s_y = np.dot(s_ab, y_hat) / del_gh
    sigma = np.sqrt(s_x ** 2 + s_y ** 2) # Eq 48
    theta_s_rad = np.arctan2(s_y, s_x) # Eq. 52, tan(theta_s)=s_y/s_x
    print("\n" + "="*40)
    print("  Branching Plane Key Quantities")
    print(f"theta_s (θ_s) in degrees: {np.degrees(theta_s_rad):.6f}")
    print(f"del_gh (δ_gh): {del_gh}")
    print(f"delta_gh (Δ_gh): {delta_gh}")
    print(f"sigma (σ): {sigma}")
    print("="*40 + "\n")
    return {
        'x_hat': x_hat, 'y_hat': y_hat,
        'del_gh': del_gh, 'delta_gh': delta_gh,
        'sigma': sigma, 'theta_s_rad': theta_s_rad
    }

def compute_surfaces(params, E_X):
    """Compute grid and energy surfaces."""
    R, Theta = np.meshgrid(R_GRID, THETA_GRID)
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    delta_gh, del_gh, sigma, theta_s_rad = params['delta_gh'], params['del_gh'], params['sigma'], params['theta_s_rad']
    theta_rad = Theta
    part1 = del_gh * R * (sigma * np.cos(theta_rad - theta_s_rad)) # A part of Eq 52
    sqrt_term = 1 + delta_gh * np.cos(2 * theta_rad)
    if np.any(sqrt_term < 0):
        print("⚠️  Some negative values in sqrt term; setting them to zero.")
        sqrt_term = np.maximum(sqrt_term, 0)
    part2 = del_gh * R * np.sqrt(sqrt_term)   # A part of Eq. 52
    E_A = E_X + part1 + part2    # Full Eq. 52
    E_B = E_X + part1 - part2
    E_A = E_A * 27.2114
    E_B = E_B * 27.2114
    return X, Y, E_A, E_B

def plot_surfaces(X, Y, E_A, E_B, fig_width, fig_height, elev=28, azim=-133, title=None):
    """Plot the two energy surfaces."""
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111, projection='3d')
    surf1 = ax.plot_surface(X, Y, E_A, cmap='viridis', edgecolor='none', alpha=0.8, antialiased=True)
    surf2 = ax.plot_surface(X, Y, E_B, cmap='plasma', edgecolor='none', alpha=0.9, antialiased=True)
    ax.set_xlabel('g ', fontsize=12, labelpad=15)
    ax.set_ylabel('h ', fontsize=12, labelpad=15)
    ax.set_zlabel('Energy (eV)', fontsize=12, labelpad=15)
    if title:
        ax.set_title(title)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    return fig, ax

def animate_surfaces(X, Y, E_A, E_B, fig_width, fig_height, anim_dpi, anim_fps, outpath, writer='ffmpeg'):
    """Create a rotation animation and save as GIF or MP4."""
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, E_A, cmap="viridis", alpha=0.8, edgecolor='none')
    ax.plot_surface(X, Y, E_B, cmap="plasma", alpha=0.8, edgecolor='none')
    ax.set_xlabel("g")
    ax.set_ylabel("h")
    ax.set_zlabel("Energy (eV)")
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False
    ax.grid(True, linestyle='--', alpha=0.3)

    def update_rotation(frame):
        ax.view_init(elev=30, azim=frame)
        return fig,

    print(f"🎥 Generating animation ({writer})...")
    anim = FuncAnimation(fig, update_rotation, frames=np.arange(0, 360, 2), interval=60)
    if writer == 'ffmpeg':
        anim.save(str(outpath), writer='ffmpeg', dpi=anim_dpi)
    elif writer == 'pillow':
        anim.save(str(outpath), writer=PillowWriter(fps=anim_fps))
    print(f"✅ Animation saved as {outpath}")

# --------------------------- MAIN SCRIPT LOGIC --------------------------------

def main():
    print_about()
    # -- Input files
    grad_fileA = get_file("Enter the gradient file name for State A", default="gradientA.out")
    grad_fileB = get_file("Enter the gradient file name for State B", default="gradientB.out")
    nac_file = get_file("Enter the NAC vector file name", default="NAC.out")
    grad_A = load_vector_file(grad_fileA)
    grad_B = load_vector_file(grad_fileB)
    h = load_vector_file(nac_file)

    # -- Numeric/energy inputs
    E_X = get_numeric("Enter the energy of the intersection point (Hartree)", default=DEFAULT_EX)

    # -- Core calculation
    params = get_branching_plane_vectors(grad_A, grad_B, h)
    xyz_file = get_file("Enter the xyz file name for atom labels", default="orca.xyz")
    atom_list = extract_atom_symbols(xyz_file)
    # Print and save branching plane vectors
    N = len(atom_list)
    x_hat_2d = params['x_hat'].reshape(N, 3)
    y_hat_2d = params['y_hat'].reshape(N, 3)
    print("\n" + "*" * 40)
    print("⭐ x̃ vector (normalized):\n", x_hat_2d)
    print("*" * 40)
    print("⭐ ỹ vector (normalized):\n", y_hat_2d)
    print("*" * 40 + "\n")
    with open("x_vectors.out", "w") as f:
        f.write("atoms x vectors\n")
        pd.DataFrame({'Atom': atom_list,
                      'x': x_hat_2d[:,0], 
                      'y': x_hat_2d[:,1],
                      'z': x_hat_2d[:,2]
                      }).to_csv(f, sep=' ', index=False, header=False,float_format="%.10f")
    with open("y_vectors.out", "w") as f:
        f.write("atoms y vectors\n")
        pd.DataFrame({'Atom': atom_list, 
                      'x': y_hat_2d[:,0], 
                      'y': y_hat_2d[:,1],
                      'z': y_hat_2d[:,2]
                      }).to_csv(f, sep=' ', index=False, header=False, float_format="%.10f")
    print("✅ x_hat saved to x_vectors.out (with atom labels)")
    print("✅ y_hat saved to y_vectors.out (with atom labels)")
    X, Y, E_A, E_B = compute_surfaces(params, E_X)

    # -- Plotting
    if ask_yes_no("Show 3D surface plot now?"):
        fig_w = get_numeric("Figure width (inches)", default=DEFAULT_FIGSIZE[0])
        fig_h = get_numeric("Figure height (inches)", default=DEFAULT_FIGSIZE[1])
        fig, ax = plot_surfaces(X, Y, E_A, E_B, fig_w, fig_h)
        plt.show()

    if ask_yes_no("Save the 3D plot as image?"):
        outpath = safe_save_path("Image filename", "conical_intersection.png")
        fig_w = get_numeric("Figure width (inches)", default=DEFAULT_FIGSIZE[0])
        fig_h = get_numeric("Figure height (inches)", default=DEFAULT_FIGSIZE[1])
        dpi = get_numeric("DPI", default=DEFAULT_DPI, type_cast=int)
        fig, ax = plot_surfaces(X, Y, E_A, E_B, fig_w, fig_h)
        fig.savefig(outpath, dpi=dpi, bbox_inches='tight')
        print(f"✅ Saved static image as '{outpath}'")

    # -- Animation
    if ask_yes_no("Create a rotation animation?"):
        fig_w = get_numeric("Animation figure width (inches)", default=DEFAULT_FIGSIZE[0])
        fig_h = get_numeric("Animation figure height (inches)", default=DEFAULT_FIGSIZE[1])
        if ask_yes_no("Save animation as MP4?"):
            mp4_path = safe_save_path("MP4 filename", "conical_intersection_rotation.mp4")
            anim_dpi = get_numeric("DPI for MP4", default=DEFAULT_ANIM_DPI, type_cast=int)
            animate_surfaces(X, Y, E_A, E_B, fig_w, fig_h, anim_dpi, DEFAULT_ANIM_FPS, mp4_path, writer='ffmpeg')
        if ask_yes_no("Save animation as GIF?"):
            gif_path = safe_save_path("GIF filename", "conical_intersection_rotation.gif")
            anim_fps = get_numeric("FPS for GIF", default=DEFAULT_ANIM_FPS, type_cast=int)
            animate_surfaces(X, Y, E_A, E_B, fig_w, fig_h, DEFAULT_ANIM_DPI, anim_fps, gif_path, writer='pillow')
    print("✅ Done! Thank you for using ConeZen.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting gracefully.")
        sys.exit(0)
