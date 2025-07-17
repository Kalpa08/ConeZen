# conezen/logic.py

import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- CONSTANTS ---
DEFAULT_DPI = 300
DEFAULT_FIGSIZE = (10, 8)
DEFAULT_ANIM_DPI = 200
DEFAULT_ANIM_FPS = 20
R_GRID = np.linspace(0, 0.001, 500)
THETA_GRID = np.linspace(0, 2 * np.pi, 500)
DEFAULT_EX = 0  # hartree energy at crossing point

# --- DATA LOADING ---
def load_vector_file(path: Path):
    """Load 3D vector data (skipping header) from file."""
    data = []
    skipped = 0
    with path.open() as f:
        lines = f.readlines()[1:]
        for i, line in enumerate(lines, start=2):
            parts = line.strip().split()
            if len(parts) < 3:
                skipped += 1
                continue
            try:
                data.append([float(x) for x in parts[:3]])
            except ValueError:
                skipped += 1
    return np.array(data), skipped

def extract_atom_symbols(xyz_file: Path):
    """Extract atom symbols from an xyz file path."""
    atom_list = []
    with xyz_file.open(encoding="utf-8") as f:
        lines = f.readlines()[2:]
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 4:
                atom_list.append(parts[0])
    return atom_list

# --- CORE CALCULATIONS ---
def get_branching_plane_vectors(grad_A, grad_B, h):
    """Compute the branching plane vectors and related quantities."""
    g_ab = 0.5 * (grad_B - grad_A)
    s_ab = 0.5 * (grad_B + grad_A)
    g_ab = g_ab.flatten()
    s_ab = s_ab.flatten()
    h_ab = h.flatten()
    
    # Scaling h_ab to g_ab before orthogonalization
    h_ab = h_ab * (np.linalg.norm(g_ab) / np.linalg.norm(h_ab))

    numerator = 2 * np.dot(g_ab, h_ab)
    denominator = np.dot(g_ab, g_ab) - np.dot(h_ab, h_ab)
    beta_rad = 0.5 * np.arctan2(numerator, denominator)
    cosb, sinb = np.cos(beta_rad), np.sin(beta_rad)

    g_tilde = g_ab * cosb + h_ab * sinb
    h_tilde = h_ab * cosb - g_ab * sinb
    g2, h2 = np.dot(g_tilde, g_tilde), np.dot(h_tilde, h_tilde)
    x_hat = g_tilde / np.sqrt(g2)
    y_hat = h_tilde / np.sqrt(h2)
    
    del_gh = np.sqrt(0.5 * (g2 + h2))
    delta_gh = (g2 - h2) / (g2 + h2)
    s_x = np.dot(s_ab, x_hat) / del_gh
    s_y = np.dot(s_ab, y_hat) / del_gh
    sigma = np.sqrt(s_x ** 2 + s_y ** 2)
    theta_s_rad = np.arctan2(s_y, s_x)
    
    return {
        'x_hat': x_hat, 'y_hat': y_hat, 'del_gh': del_gh,
        'delta_gh': delta_gh, 'sigma': sigma, 'theta_s_rad': theta_s_rad
    }

def compute_surfaces(params, E_X):
    """Compute grid and energy surfaces."""
    R, Theta = np.meshgrid(R_GRID, THETA_GRID)
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    delta_gh, del_gh, sigma, theta_s_rad = params['delta_gh'], params['del_gh'], params['sigma'], params['theta_s_rad']
    
    part1 = del_gh * R * (sigma * np.cos(Theta - theta_s_rad))
    sqrt_term = 1 + delta_gh * np.cos(2 * Theta)
    # Avoid math error for negative values in the square root
    sqrt_term_safe = np.maximum(sqrt_term, 0) 
    
    part2 = del_gh * R * np.sqrt(sqrt_term_safe)
    
    E_A = (E_X + part1 + part2) * 27.2114
    E_B = (E_X + part1 - part2) * 27.2114
    
    # Return a flag if the sqrt term had negative values
    had_neg_sqrt = np.any(sqrt_term < 0)
    
    return X, Y, E_A, E_B, had_neg_sqrt

# --- PLOTTING & ANIMATION ---
def plot_surfaces(X, Y, E_A, E_B, fig_width, fig_height, elev=28, azim=-133, title=None):
    """Plot the two energy surfaces."""
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, E_A, cmap='viridis', edgecolor='none', alpha=0.8, antialiased=True)
    ax.plot_surface(X, Y, E_B, cmap='plasma', edgecolor='none', alpha=0.9, antialiased=True)
    ax.set_xlabel('g', fontsize=12, labelpad=15)
    ax.set_ylabel('h', fontsize=12, labelpad=15)
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
    ax.set_xlabel("g̃ (a.u.)")
    ax.set_ylabel("h̃ (a.u.)")
    ax.set_zlabel("Energy (eV)")
    
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
