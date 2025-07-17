# 🌀 ConeZen

<p align="center">
  <img src="logo6.svg" alt="ConeZen Logo" width="300"/>
</p>

<h1 align="center">ConeZen</h1>

<p align="center"><i>Visualiser for Conical Intersection Branching Planes</i></p>

---
## ConeZen 🌀: Conical Intersection Branching Plane Visualization

**ConeZen** is a lightweight, open-source Python package designed to characterize and visualize the branching plane topology at a conical intersection (CI). The shape and orientation of a CI's potential energy surfaces dictate the pathways for ultrafast, non-radiative electronic transitions, which are fundamental to processes like vision, photosynthesis, and DNA photostability.

Using output from standard quantum chemistry programs (tested on SHARC-OpenMolcas), ConeZen computes key topological descriptors and renders intuitive 3D potential energy surfaces. This allows researchers to move from raw numerical data to an intuitive, quantitative understanding of the CI landscape, helping to predict the outcomes of photochemical reactions.
- Note: ConeZen was tested with the gradients and NAC obtained from SHARC-OpenMolcas interface. (see [SHARC Manual](https://sharc-md.org/?page_id=1454))
---

## ✨ Key Features

- **Automated Analysis**  
Computes key CI descriptors:  
 - the average slope or pitch ( $\delta{gh}$ )  
 - the cone ellipticity or asymmetry ($\Delta{gh}$)  
 - the overall tilt magnitude and direction ($\sigma$), $\theta_s$.   
This saves researchers from tedious manual calculations and allows for rapid classification of CIs as peaked, sloped, single-path, or bifurcating.   

- **High-Quality Visualization**  
Generates publication-ready 3D surface plots using Matplotlib. The plots are fully customizable and can be exported in various high-resolution formats (PNG, PDF, SVG) for direct inclusion in presentations and publications.  
- **Animations**  
Creates animated GIFs or MP4s showing a 360° rotation of the 3D surface. These are especially useful for presentations and for gaining a more intuitive feel for the three-dimensional structure of the potential energy surfaces around the degeneracy.  

- **Dual Interface**  
Offers both an easy-to-use interactive Command-Line Interface (CLI) and an importable Python library (API). This provides flexibility for both quick, interactive analyses and more complex, scripted workflows or integration into larger computational chemistry pipelines.   

- **Minimal Dependencies**  
- Built on a small, robust stack of standard scientific libraries (NumPy, Pandas, Matplotlib), making installation straightforward and avoiding dependency conflicts.  

---

## 🚀 Installation

ConeZen is distributed on the Python Package Index (PyPI). It is highly recommended to install ConeZen in a dedicated Python virtual environment to avoid conflicts with other packages.

Clone this repository and install dependencies:

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv conezen_env
source conezen_env/bin/activate  # On Windows, use `conezen_env\Scripts\activate`

# Install ConeZen
pip install conezen

````
For creating MP4 animations, you will also need to have FFmpeg installed and available in your system's PATH.

---
## Usage
ConeZen can be run in two ways: through the command line or as a Python library.

## 1. Command-Line Interface (CLI)
The easiest way to use ConeZen is to run it from your terminal. Running conezen initiates a user-friendly, step-by-step process. The tool will first request the file paths for the gradients of the two electronic states, the nonadiabatic coupling vector, and the molecular geometry. It then interactively prompts for plotting and saving options.

```
conezen
```
The interactive session will look like this:

```bash
============================================================
    ConeZen: Conical Intersection Branching Plane Visualization
============================================================
...
Enter the gradient file name for State A (default: gradientA.out):
Enter the gradient file name for State B (default: gradientB.out):
Enter the NAC vector file name (default: NAC.out):
Enter the xyz file name for atom labels (default: orca.xyz):
Enter the energy of the intersection point (Hartree) (default: 0):
...
✅ Key quantities calculated.
Save branching plane key quantities to a file? [y/n]: y
Enter filename for parameters (default: ci_parameters.txt):
...
Show 3D surface plot now? [y/n]: y

```

## 2. Python API
You can also import ConeZen into your own Python scripts or a Jupyter Notebook for more advanced workflows. This gives you direct access to the underlying data structures and plotting functions for custom analysis.

Here is a basic example with detailed comments:

```python
import numpy as np
import matplotlib.pyplot as plt
import conezen as cz

# 1. Load your data.
# In a real case, you would load these from your quantum chemistry output files
# using a function like `numpy.loadtxt`. The vectors should be flattened
# into 1D arrays before being passed to ConeZen.
grad_A = np.random.rand(90)
grad_B = np.random.rand(90)
h_ab = np.random.rand(90)
E_X = -105.5  # Energy of the CI point in Hartree

# 2. Compute the branching plane vectors and topological parameters.
# This function returns a dictionary containing the calculated quantities.
params = cz.get_branching_plane_vectors(grad_A, grad_B, h_ab)

# The `params` dictionary contains: 'x_hat', 'y_hat', 'del_gh',
# 'delta_gh', 'sigma', and 'theta_s_rad'.
print(f"Asymmetry (Δ_gh): {params['delta_gh']:.4f}")
print(f"Tilt (σ): {params['sigma']:.4f}")

# 3. Compute the potential energy surfaces for plotting.
# This function generates the mesh grid and calculates the energy of the
# upper (E_A) and lower (E_B) surfaces at each point.
X, Y, E_A, E_B, _ = cz.compute_surfaces(params, E_X)

# 4. Plot the surfaces using the built-in plotting function.
fig, ax = cz.plot_surfaces(X, Y, E_A, E_B, title="My Conical Intersection")
plt.show()

# You can also save the figure to a file for publications.
# fig.savefig("my_intersection.pdf", dpi=300, bbox_inches='tight')
```

## Input File Format

ConeZen expects simple text files for the gradients, nonadiabatic coupling (NAC) vectors, and geometry. The format is designed for easy generation from post-processing scripts and is directly compatible with output from programs like SHARC-OpenMolcas.

-Gradient and NAC Files (```gradientA.out```, ```gradientB.out```, ```NAC.out```):
	-The first line is treated as a header and is skipped.
	-Subsequent lines should contain the Cartesian vector components (x, y, z) for each atom, typically in units of Hartree/Bohr.
	-The script reads the first three numeric values on each line. Any additional text (like atom symbols) is ignored.
- Geometry File (.xyz):
	- A standard XYZ file format is expected. This is used to correctly label the atoms in the output vector files.
	- The first two lines (number of atoms and a comment line) are skipped as per the standard.
Example gradientA.out:
```
7 3 ! m1 1 s1 3 ms1 0
 1.538527244911E-002  2.700614793356E-002 -1.774304949876E-002
 4.842665117426E-004 -6.611115362176E-005 -1.307997738720E-003
 6.585259497396E-004 -9.263239120174E-004  3.094972603908E-004
 ...
 ```
Example orca.xyz:	
```
7
Coordinates from ORCA-job orca
 C   -1.67927099317952     -0.08967085472111      1.37125703628325
 H   -1.55677664790204     -0.76202298903129      0.52236315843451
 ...
```
### Output
The CLI tool can generate several useful output files in your working directory:
- ci_parameters.txt: A text file containing the calculated topological quantities ($\delta{gh}$,$\Delta{gh}$, $\sigma$, $\theta_s$). This provides a quick human-readable summary of the CI's characters.
- x_vectors.out, y_vectors.out:  The orthonormal branching plane vectors ( $\x{hat}$ and {\y{hat}}}.
- conical_intersection.png: A high-resolution image of the 3D plot. The plot is saved with a transparent background and tight bounding box, making it easy to incorporate into other documents.

# Citing ConeZen

If you use ConeZen in your research, please cite the accompanying paper. Your citation allows us to track the software's impact and helps support its continued development.

```
Kalpajyoti Dihingia & Biswajit Maiti, ConeZen: A Python Package for Visualizing Conical Intersection Branching Planes, J. Open Source Softw. (2025).

Zenodo DOI: [Zenodo DOI will go here]
```
```bibtex
@software{conezen,
  author  = {Kalpajyoti Dihingia and Biswajit Maiti},
  title   = {ConeZen: Visualiser for conical intersection branching planes},
  year    = 2025,
  publisher = {Zenodo},
  version = {v1.0},
  doi     = {10.xxxx/zenodo.xxxxx}
}
```

---

## ⚖️ License

Distributed under the **GNU GPL v3.0**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Developed at **Banaras Hindu University (BHU)**

- Based on:  
  > Ignacio Fdez. Galván, Mickaël G. Delcey, Thomas Bondo Pedersen, Francesco Aquilante, and Roland Lindh,  
  > "Analytical State-Average Complete-Active-Space Self-Consistent Field Nonadiabatic Coupling Vectors: Implementation with Density-Fitted Two-Electron Integrals",  
  > *J. Chem. Theory Comput.* 2016, **12(8)**, 3636–3653. DOI: [10.1021/acs.jctc.6b00384](https://doi.org/10.1021/acs.jctc.6b00384)

For full metadata and citation, see [`CITATION.cff`](CITATION.cff) and [`.zenodo.json`](.zenodo.json).

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting issues or pull requests.
