
<p align="center">
  <img src="logo6.svg" alt="ConeZen Logo" width="300"/>
</p>

<h1 align="center">ConeZen</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3.0"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python Version"></a>
  <a href="https://doi.org/10.5281/zenodo.16161336"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.16161336.svg" alt="DOI"></a>
</p>

<p align="center"><i>Visualiser for Conical Intersection Branching Planes</i></p>



---
## Conical Intersection Branching Plane Visualization

**ConeZen** is a lightweight, open-source Python package designed to characterize and visualize the branching plane topology at a conical intersection (CI). The shape and orientation of a CI's potential energy surfaces dictate the pathways for ultrafast, non-radiative electronic transitions, which are fundamental to processes like vision, photosynthesis, and DNA photostability.

Using output from standard quantum chemistry programs (tested on SHARC-OpenMolcas), **ConeZen** computes key topological descriptors and renders intuitive 3D potential energy surfaces. This allows researchers to move from raw numerical data to an intuitive, quantitative understanding of the CI landscape, helping to predict the outcomes of photochemical reactions.
- 📝Note: ConeZen was tested with the gradients and NAC obtained from SHARC-OpenMolcas interface. The automated extraction feature is specifically designed for the QM.out file generated by this interface. (see [SHARC Manual](https://sharc-md.org/?page_id=1454))
---

## ✨ Key Features

- **Automated Analysis**
  -  **Direct QM Output Parsing**  Automatically extracts the required gradients and nonadiabatic coupling (NAC) vectors directly from sharc-molcas QM.out files. Just specify the file and the states of interest (e.g., S1, T2), and ConeZen handles the rest.
  - **Topological Analysis**  Computes key CI descriptors from the vector data:  
 	- The strength or pitch ( $\delta_{gh}$ )  
 	- The asymmetry ( $$\Delta_{gh}$$ )  
 	- The relative tilt and tilt heading $$\sigma$$ , $\theta_s$ respectively.   
This saves researchers from tedious manual calculations and allows for rapid classification of CIs as peaked, sloped, single-path, or bifurcating.   

- **High-Quality Visualization**  
Generates publication-ready 3D surface plots using Matplotlib. The plots are fully customizable and can be exported in various high-resolution formats (PNG, PDF, SVG) for direct inclusion in presentations and publications.  
- **Animations**  
Creates animated GIFs or MP4s showing a 360° rotation of the 3D surface. These are especially useful for presentations and for gaining a more intuitive feel for the three-dimensional structure of the potential energy surfaces around the degeneracy.  

- **Dual Interface**  
Offers both an easy-to-use interactive Command-Line Interface (CLI) and an importable Python library (API). This provides flexibility for both quick, interactive analyses and more complex, scripted workflows or integration into larger computational chemistry pipelines.   

- **Minimal Dependencies**  
Built on a small, robust stack of standard scientific libraries (NumPy, Pandas, Matplotlib), making installation straightforward and avoiding dependency conflicts.  

---

## 🚀 Installation

Follow these steps to install **ConeZen** from the source code.

### 1. Clone the Repository

First, clone the repository to your local machine and navigate into the directory.
```
git clone https://github.com/Kalpa08/ConeZen.git
cd ConeZen
```
### 2. Create a Conda Environment

It's recommended to create a dedicated environment to manage dependencies. The following commands will create and activate a new environment named 
```conezen_env``` with ```Python 3.11```.

```bash
# Create and activate a virtual environment (optional but recommended)
conda create --name conezen_env python=3.11
conda activate conezen_env 
```
### 3. Install the Package

Finally, install **ConeZen** and all its required dependencies using pip. The ```.``` tells pip to install the package located in the current directory.

```
# Install ConeZen
pip install build
pip install .

````
That's it! **ConeZen** is now installed in your environment and ready to use.

### System Dependencies (Required for Animations)

To create and save animations as MP4 files, you must have FFmpeg installed and accessible in your system's PATH.

- **Windows:** Download the binaries from the official [FFmpeg site](https://ffmpeg.org/download.html) and add the bin folder to your system's PATH.

- **macOS:** Install using [Homebrew](https://brew.sh/):

```Bash

brew install ffmpeg
```
**Linux (Ubuntu/Debian):** Install using the package manager:

```Bash
sudo apt-get install ffmpeg
```


---
## 🧪 Usage
**ConeZen** can be run in two ways: through the command line or as a Python library.

### 1. Command-Line Interface (CLI)
The easiest way to use ConeZen is to run it from your terminal. Running conezen initiates a user-friendly, step-by-step process. The tool will first request the file paths for the gradients of the two electronic states, the nonadiabatic coupling vector, and the molecular geometry. It then interactively prompts for plotting and saving options.

```
conezen
```
The interactive session will look like this:

### New Automated Extraction Workflow:

This is the recommended and easiest workflow.

```
============================================================
    ConeZen: Conical Intersection Branching Plane Visualization
============================================================
...
(Do you want to automatically extract gradients and NACs from a QM output file? (only for sharc-molcas output QM.out file) [y/n]: y
Enter the source QM file name (default: QM.out):
Enter the total number of singlet states (default: 20): 5
Enter the total number of triplet states (default: 20): 5
Enter the lower state (e.g., S2): s2
Enter the upper state (e.g., S3): s3
✅ Successfully extracted and saved 'S2_gradient.out'
✅ Successfully extracted and saved 'S3_gradient.out'
✅ Automatically extracted and saved 'NAC_S2_S3.out'
Enter the energy of the intersection point (Hartree) (default: 0):
...
✅ Key quantities calculated.
Save branching plane key quantities to a file? [y/n]: y
Enter filename for parameters (default: ci_parameters.txt):
...
Show 3D surface plot now? [y/n]: y
```
### Manual Input Workflow:

If you choose not to use the automated extractor or have your gradient/NAC files prepared separately, you can provide them manually.

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

### 2. Python API
You can also import ConeZen into your own Python scripts or a Jupyter Notebook for more advanced workflows. This gives you direct access to the underlying data structures and plotting functions for custom analysis.

Here is a basic example with detailed comments:

```python
import numpy as np
import matplotlib.pyplot as plt
import conezen as cz
from pathlib import Path
from conezen.logic import load_vector_file


#  1 Use the specialized load_vector_file function.
#    This function skips the non-numeric header in your files.
#    Do NOT use np.loadtxt.
grad_A_data, _ = load_vector_file(Path('gradientA.out'))
grad_B_data, _ = load_vector_file(Path('gradientB.out'))
h_ab_data, _ =  load_vector_file(Path('NAC.out'))

# 2. Flatten the arrays to the required 1D shape.
grad_A = grad_A_data.flatten()
grad_B = grad_B_data.flatten()
h_ab = h_ab_data.flatten()

E_X = 0  # Energy of the CI point in Hartree

# 3. Compute the branching plane vectors and topological parameters.
# This function returns a dictionary containing the calculated quantities.
params = cz.get_branching_plane_vectors(grad_A, grad_B, h_ab)

# The `params` dictionary contains: 'x_hat', 'y_hat', 'del_gh',
# 'delta_gh', 'sigma', and 'theta_s_rad'.
print(f"Asymmetry (Δ_gh): {params['delta_gh']:.4f}")
print(f"Pitch (δ_gh): {params['del_gh']:.4f}")
print(f"Tilt (σ): {params['sigma']:.4f}")
print(f"theta_s (θs): {np.degrees(params['theta_s_rad']):.4f}")


# 4. Compute the potential energy surfaces for plotting.
# This function generates the mesh grid and calculates the energy of the
# upper (E_A) and lower (E_B) surfaces at each point.
X, Y, E_A, E_B, _ = cz.compute_surfaces(params, E_X)

# 5. Plot the surfaces using the built-in plotting function.
fig, ax = cz.plot_surfaces(X, Y, E_A, E_B, fig_width=8, fig_height=6, title="My Conical Intersection")
plt.show()

# You can also save the figure to a file for publications.
#fig.savefig("my_intersection.pdf", dpi=300, bbox_inches='tight')
```

## 📄 Input File Format

ConeZen can now work directly with QM.out files from SHARC-OpenMolcas, but it also supports manually prepared text files.
- Source Quantum Chemistry File (`QM.out`):
	-  This is the primary input for the new automated workflow.
 	-  ConeZen searches this file for the specific headers corresponding to the requested electronic states (e.g., m1 1 s1 3 ms1 0 for the S2 gradient) to extract gradient and NAC vectors. 

- Gradient and NAC Files (```gradientA.out```, ```gradientB.out```, ```NAC.out```):
	- These files are generated automatically when using the extraction workflow or can be provided manually.
 	- The first line is treated as a header and is skipped.
	- Subsequent lines should contain the Cartesian vector components (x, y, z) for each atom.
	- The script reads the first three numeric values on each line. Any additional text (like atom symbols) is ignored.
- Geometry File (```.xyz```):
	- A standard XYZ file format is used to add atom labels to the output vector files.
	- The first two lines (number of atoms and a comment line) are skipped as per the standard.

Example ```gradientA.out```:
```
7 3 ! m1 1 s1 3 ms1 0
 1.538527244911E-002  2.700614793356E-002 -1.774304949876E-002
 4.842665117426E-004 -6.611115362176E-005 -1.307997738720E-003
 6.585259497396E-004 -9.263239120174E-004  3.094972603908E-004
 ...
 ```
Example ```NAC.out```:
```
7 3 ! m1 1 s1 3 ms1 0   m2 1 s2 4 ms2 0
-1.577934889249E+002  4.936445290015E+001 -6.162157991488E+001 
-5.923796065802E+000  1.911233859294E+000 -2.389064178526E+000 
 2.196082257074E+001  4.671921146048E+001 -2.720461218524E+001
 ...
 ```
Example ```orca.xyz```:	
```
7
Coordinates from ORCA-job orca
 C   -1.67927099317952     -0.08967085472111      1.37125703628325
 H   -1.55677664790204     -0.76202298903129      0.52236315843451
 ...
```
## 📤 Output
The CLI tool can generate several useful output files in your working directory:
- ```S2_gradient.out```, ```NAC_S2_S3.out```, etc.: The gradient and NAC files automatically extracted from the source QM.out file.
- ```ci_parameters.txt```: A text file containing the calculated topological quantities ($\delta_{gh}$, $$\Delta_{gh}$$ , σ , $\theta_s$). This provides a quick human-readable summary of the CI's characters.
- ```x_vectors.out```, ```y_vectors.out```:  The orthonormal branching plane vectors $\hat{x}$ and $\hat{y}$.
- ```conical_intersection.png```: A high-resolution image of the 3D plot. The plot is saved with a transparent background and tight bounding box, making it easy to incorporate into other documents.

## 🧾 Citing ConeZen

If you use ConeZen in your research, please cite the accompanying paper. Your citation allows us to track the software's impact and helps support its continued development.



```bibtex
@software{conezen,
  author  = {Kalpajyoti Dihingia and Biswajit Maiti},
  title   = {ConeZen: Visualiser for conical intersection branching planes},
  year    = 2025,
  publisher = {Zenodo},
  version = {v0.1.4},
  doi     = 10.5281/zenodo.16161336
}
```

---

## ⚖️ License

Distributed under the **GNU GPL v3.0**. See the [LICENSE](LICENSE) file for details.

---
## 🙏 Acknowledgments

- Developed at *Banaras Hindu University, Varanasi, India*.
- Based on the theoretical framework described in:
  	```J. Chem. Theory Comput. 2016, 12(8), 3636–3653. DOI: 10.1021/acs.jctc.6b00384```
---

For full metadata and citation, see [`CITATION.cff`](CITATION.cff) and [`.zenodo.json`](.zenodo.json).

---

## 🤝 Contributions

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting issues or pull requests.
