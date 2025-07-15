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
# This script is distributed under the GNU General Public License v3.0 (GPL-3.0).
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
#
# ==============================================================================

import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter



# ==============================================================================
# 📢 About / Info
# ==============================================================================

def print_about():
    term_width = shutil.get_terminal_size().columns

    lines = [
        "="*60,
        "Conical Intersection Branching Plane Visualization",
        "="*60,
        "🔬  This Python script generates a 3D model of the potential",
        "     energy surfaces near a conical intersection using the",
        "     branching plane method.",
        "",
        "✏️  Author: Kalpa Dihingia",
        "🏛️  Institute: Banaras Hindu University (BHU)",
        "",
        "📄  How to use:",
        "   1️⃣ Prepare input files:",
        "      - Gradient file for state A and B (e.g., gradientA.out, gradientB.out)",
        "      - Non-adiabatic coupling (NAC) vector file (e.g., NAC.out)",
        "",
        "   2️⃣ Run: python3 ci_branching_plane.py",
        "   3️⃣ Provide inputs when prompted:",
        "      - Energy gap between states (in Hartree)",
        "      - Energy of the intersection point",
        "   4️⃣ Choose to save static plots and/or rotation animations.",
        "",
        "💡  Theory implemented based on:",
        "     Ignacio Fdez. Galván et al., J. Chem. Theory Comput. 2016.",
        "",
        "🔗  License: Open-source under the MIT License",
        "🗂️  Please cite the relevant paper if you use this tool in your work.",
        "="*60,
        "✅  Done! Thank you for using the script.",
        "="*60
    ]

    for line in lines:
        print(line.center(term_width))


print_about()
# ==============================================================================
# 🔑 Utility: Yes/No prompt
# ==============================================================================
def ask_yes_no(prompt):
    """Reusable yes/no input validator"""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ['y', 'yes', 'n', 'no']:
            return answer in ['y', 'yes']
        print("❌ Invalid input. Please enter 'y' or 'yes', 'n' or 'no'.")

# ==============================================================================
# 📂 Input: Load NAC and gradient vectors
# ==============================================================================

def extract_nac():
    while True:
        nac_file = input("Enter the NAC vector file name (e.g., NAC.out): ").strip()
        if not os.path.isfile(nac_file):
            print(f"File '{nac_file}' not found. Please try again.")
            continue
        break
    nac_list = []
    with open(nac_file, "r") as f2:
        lines = f2.readlines()
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            nac_list.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return np.array(nac_list)

def grad_A_cal(grad_fileA):
    grad_A_list = []
    with open(grad_fileA, "r") as f1:
        lines = f1.readlines()
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            grad_A_list.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return np.array(grad_A_list)

def grad_B_cal(grad_fileB):
    grad_B_list = []
    with open(grad_fileB, "r") as f1:
        lines = f1.readlines()
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            grad_B_list.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return np.array(grad_B_list)

# ============================END OF LOADING THE VECTORS==================================================

# Collect gradient file names with check

while True:
    grad_file_nameA = input("Enter the gradient file name for State A (e.g., gradientA.out): ").strip()
    if not os.path.isfile(grad_file_nameA):
        print(f"❌ File '{grad_file_nameA}' not found. Please try again.")
        continue
    break

while True:
    grad_file_nameB = input("Enter the gradient file name for State B (e.g., gradientB.out): ").strip()
    if not os.path.isfile(grad_file_nameB):
        print(f"❌ File '{grad_file_nameB}' not found. Please try again.")
        continue
    break

# Load vectors
h = extract_nac()
grad_A = grad_A_cal(grad_file_nameA)
grad_B = grad_B_cal(grad_file_nameB)

print("\n Loaded Gradient A:\n", grad_A)
print("\n Loaded Gradient B:\n", grad_B)

# Branching plane vectors
g_ab = 0.5*(grad_B - grad_A)                  # This is gAB [4]

#linear combination of gradients
s_ab=0.5*(grad_B + grad_A)

g_ab=g_ab.flatten()
h_ab=h.flatten()
s_ab=s_ab.flatten()

# ==============================================================================
# ⚙️  Branching plane vector calculations
# ==============================================================================

# Example core logic follows — same as your calculations — here you’d have:
# - energy gap input
# - orthogonalization
# - grid generation
# - energy surfaces (E_A, E_B)

# Keep your robust try/except for numeric input, e.g.:


while True:
    try:
        energy_gap=float(input("Enter the energy gap between the two states(hartree) "))
        break
    except ValueError:
        print("Invalid input! Please enter a numeric value for energy gap.")

# correction of the nonadiabatic coupling vector 
h_ab=h_ab*energy_gap

angle_gh=np.arccos( np.dot(g_ab,h_ab)/(np.linalg.norm(g_ab)*np.linalg.norm(h_ab)))
print("Initial angle between g and h vectors", angle_gh)

print("magnitute of g or |g|=",np.linalg.norm(g_ab))   # this can also be written as np.sqrt(np.dot(g_ab,g_ab))
#print("|g|^2", np.dot(g_ab,g_ab))
#print("|h|^2", np.dot(h_ab,h_ab))

print("magnitude of h or |h|=",np.linalg.norm(h_ab))
print("dot product (g_ab.h_ab)", np.dot(g_ab,h_ab))

# Calculate beta to orthogonalize g_ab and h_ab_original [9, 13]

numerator=2*np.dot(g_ab,h_ab)
denominator=np.dot(g_ab,g_ab)-np.dot(h_ab,h_ab)
#print("numerator")
#print(numerator)
#print("denominator")
#print(denominator)

# Use arctan2 for robust angle calculation
beta_rad=0.5*np.arctan2(numerator,denominator)
beta=np.degrees(beta_rad)
print("beta (degrees):",beta)

cos_beta=np.cos(beta_rad)
sin_beta=np.sin(beta_rad)
g_tilde=g_ab*cos_beta+h_ab*sin_beta
h_tilde=h_ab*cos_beta-g_ab*sin_beta
#print("g_tilde")
#print(g_tilde)
#print("h_tilde")
#print(h_tilde)

dot_g_h_tilde = np.dot(g_tilde, h_tilde)
print("Dot product of g_tilde and h_tilde:", dot_g_h_tilde)

g2=np.dot(g_tilde, g_tilde)   # ||g_tilde||^2
h2=np.dot(h_tilde, h_tilde)   # ||h_tilde||^2

#compute unit vectors
x_hat=g_tilde/np.sqrt(g2)
y_hat=h_tilde/np.sqrt(h2)


#print("x_hat ")
#print(x_hat)
#print("y_hat ")
#print(y_hat)
print("|x_hat|",np.dot(x_hat,x_hat) )
print("|y_hat|",np.dot(y_hat,y_hat) )
print("x_hat . y_hat", np.dot(x_hat,y_hat))

del_gh=np.sqrt(0.5*(g2+h2))
print("δ_gh =", del_gh)

delta_gh=(g2-h2)/(g2+h2)
print("Δ_gh =", delta_gh)

# Example grid in x,y
#x = np.linspace(0, 0.001, 500)
#y = np.linspace(0, 0.001, 500)
#X, Y = np.meshgrid(x, y)
#r=np.sqrt(X**2 + Y**2)
r = np.linspace(0, 0.001, 500)            # radius from 0 to small value
theta = np.linspace(0, 2 * np.pi, 500)    # full circle
R, Theta = np.meshgrid(r, theta)
X = R * np.cos(Theta)
Y = R * np.sin(Theta)


# s_x and s_y
s_x=np.dot(s_ab,x_hat)/del_gh
s_y=np.dot(s_ab,y_hat)/del_gh

sigma=np.sqrt(np.dot(s_x,s_x) + np.dot(s_y,s_y))  # Equation 48
theta_rad= np.arctan2(Y,X)                       # Equation 52
theta_rad = Theta
theta=np.degrees(theta_rad)
theta_s_rad=np.arctan2(s_y,s_x)                        # Equation 52
theta_s=np.degrees(theta_s_rad)

# Energy gap (Eq. 46)
gap_part1 = 2 * del_gh 
gap_part2 = np.sqrt((X**2 + Y**2) + delta_gh*(X**2 - Y**2))
gap=gap_part1*gap_part2

print("value of sigma (σ)", sigma)
#print("value of theta (θ)", theta)
print("value of theta_s (θ_s)", theta_s)
#print("value of r = np.sqrt(X**2 + Y**2", r)

# Average energy (Eq. 50)
while True:
    try:
        E_X = float(input("Enter the energy of the intersection point (hartree)")) #-244.227552099400  # use your intersection point energy here
        break
    except ValueError:
        print("Invalid Input! Please enter a numeric value for energy.")

# In polar coordinates
part1=del_gh*R*(sigma*(np.cos(theta_rad-theta_s_rad)))
part2=del_gh*R*np.sqrt(1+delta_gh*np.cos(2*theta_rad))
# Test that the term under the square root is always >= 0
term = 1 + delta_gh * np.cos(2 * theta_rad)
print("Min of sqrt term:", np.min(term))
print("Any negative values?", np.any(term < 0))
E_A=E_X + part1 + part2
E_B=E_X + part1 - part2

#print("\nShape of E_A:", E_A.shape) # Should match your X,Y meshgrid shape
#print("First few values of E_A:\n", E_A[:2,:2]) # Print a small part to check
#print("\nShape of E_B:", E_B.shape)
#print("First few values of E_B:\n", E_B[:2,:2])



# --------------------------
# 3D Plot with cleaner styling and no sidebars
# --------------------------

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Use vibrant, contrasting colormaps
surf1 = ax.plot_surface(
    X, Y, E_A,
    cmap='viridis',       # Try 'cool', 'turbo', or 'plasma' for vibrant surfaces
    edgecolor='none',
    alpha=0.8,
    antialiased=True
)
surf2 = ax.plot_surface(
    X, Y, E_B,
    cmap='plasma',     # Warm contrasting color
    edgecolor='none',
    alpha=0.9,
    antialiased=True
)

# No colorbars for a clean look

# Improved axis labels and styling
ax.set_xlabel('X direction', fontsize=12, labelpad=15)
ax.set_ylabel('Y direction', fontsize=12, labelpad=15)
ax.set_zlabel('Energy', fontsize=12, labelpad=15)


# Remove background panes for a modern feel
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Light grid for reference
ax.grid(True, linestyle='--', alpha=0.3)

# FIXED view angles


ax.view_init(elev=45, azim=210)
plt.tight_layout()


# --------------------------
# Ask user whether to save figure
# --------------------------


if ask_yes_no("\nDo you want to save the plot as an image file? [y/yes/n]: "):
    filename = input("Enter the filename (e.g., 'conical_intersection.png'): ").strip()
    if filename == '':
        filename = 'conical_intersection.png'
    # Ask user for figure aspect ratio
    while True:
        try:
            width_str = input("Enter figure width in inches (default: 10): ").strip()
            height_str =input("Enter figure height in inches (default: 8): ").strip()
            fig_width = float(width_str) if width_str != '' else 10
            fig_height = float(height_str) if height_str != '' else 8
            break
        except ValueError:
            print("Invalid Input! Please enter a numeric value for energy.")

    while True:
        try:
            dpi_str = input("Enter DPI (default: 300): ").strip()
            dpi_val = float(dpi_str) if dpi_str != '' else 300
            break
        except ValueError:
            print("Invalid input! Please enter an integer for DPI.")
    # Re-apply your chosen view before saving
    ax.view_init(elev=45, azim=210)
    # Recreate figure with new size
    fig.set_size_inches(fig_width, fig_height)
    plt.savefig(filename, dpi=dpi_val, bbox_inches='tight')
    print(f"✅ Saved static image as '{filename}' with size {fig_width}x{fig_height} inches, DPI={dpi_val}")
else:
    print("Figure was not saved.")

plt.show()

# -----------------------------------------------------
# Animate rotation (FuncAnimation does everything!)
# -----------------------------------------------------

if ask_yes_no("\nDo you want to create a rotation animation? [y/yes/n]: "):
    print("🎥 Generating rotation animation...")

    # Ask user for figure aspect ratio
    while True:
        try:
            width_str = input("Enter figure width in inches (default: 10): ").strip()
            height_str = input("Enter figure height in inches (default: 8): ").strip()
            fig_width = float(width_str) if width_str != '' else 10
            fig_height = float(height_str) if height_str != '' else 8
            break
        except ValueError:
            print("Invalid Input! Please enter a numeric value for energy.")

    fig_anim = plt.figure(figsize=(10, 8))
    ax_anim = fig_anim.add_subplot(111, projection="3d")

    surf1_anim = ax_anim.plot_surface(
        X, Y, E_A, cmap="viridis", alpha=0.8, edgecolor='none')
    surf2_anim = ax_anim.plot_surface(
        X, Y, E_B, cmap="plasma", alpha=0.8, edgecolor='none')

    ax_anim.set_xlabel("X displacement")
    ax_anim.set_ylabel("Y displacement")
    ax_anim.set_zlabel("Energy")
    ax_anim.set_title("CI Surfaces (Rotating)")

    ax_anim.xaxis.pane.fill = False
    ax_anim.yaxis.pane.fill = False
    ax_anim.zaxis.pane.fill = False
    ax_anim.grid(True, linestyle='--', alpha=0.3)

    def update_rotation(frame):
        ax_anim.view_init(elev=30, azim=frame)
        return fig_anim,

    anim_rot = FuncAnimation(
        fig_anim, update_rotation,
        frames=np.arange(0, 360, 2),
        interval=60
    )

    if ask_yes_no("\nDo you want to save the animation as MP4? [y/yes/n]:"):
        mp4_filename = input("Enter MP4 filename (default: conical_intersection_rotation.mp4): ").strip()
        if mp4_filename == '':
            mp4_filename = "conical_intersection_rotation.mp4"
        #dpi_str = input("Enter DPI for MP4 (default: 200): ").strip()
        while True:
            try:
                dpi_str = input("Enter DPI for MP4 (default: 200): ").strip()
                dpi_val = int(dpi_str) if dpi_str != '' else 200
                break
            except ValueError:
                print("❌ Invalid input! Please enter an integer for DPI.")
        anim_rot.save("conical_intersection_rotation.mp4", writer="ffmpeg", dpi=200)
        print("✅ Saved MP4")

    if ask_yes_no("\nDo you want to save the animation as GIF? [y/yes/n]:"): 
        gif_filename = input("Enter GIF filename (default: conical_intersection_rotation.gif): ").strip()
        if gif_filename == '':
            gif_filename = "conical_intersection_rotation.gif"
        while True:
            try:
                fps_str = input("Enter FPS for GIF (default: 20): ").strip()
                fps_val = int(fps_str) if fps_str != '' else 20
                break
            except ValueError:
                print("Invalid input! Please enter an integer for FPS.")
        anim_rot.save("conical_intersection_rotation.gif", writer=PillowWriter(fps=fps_val))
        print(f"Saved GIF as '{gif_filename}' with FPS={fps_val}")
else:
    print("Rotation animation was not created.")



# Next plan is to generate KEYSTROKES.TXT file, so that one can keep the record of the input for the reproducibility.

