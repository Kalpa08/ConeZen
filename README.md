# 🌀 ConeZen

<p align="center">
  <img src="logo6.svg" alt="ConeZen Logo" width="300"/>
</p>

<h1 align="center">ConeZen</h1>

<p align="center"><i>Visualiser for Conical Intersection Branching Planes</i></p>

---

## Overview

**ConeZen** is an open-source Python tool for visualizing the branching plane topology near a conical intersection (CI).  
It processes nonadiabatic coupling (NAC) and gradient data from **SHARC–OpenMolcas** (sharc manual(https://github.com/Kalpa08/conezen/edit/main/README_backup.md))to generate high-quality, publication-ready 3D plots and animations for computational chemistry applications.

---

## ✨ Features

- 📈 3D visualization of CI branching planes  
- 🎞️ Static and animated (GIF/MP4) output  
- ⚙️ SHARC–OpenMolcas support for gradients and NACs  
- 🖼️ Ready for publication: customizable, high-resolution figures  
- 🔓 GPLv3 licensed and free to use (citation required)

---

## 🚀 Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/Kalpa08/conezen.git
cd conezen
pip install -r requirements.txt
````
---

## 📦 Dependencies

```bash
numpy
matplotlib
pandas
```
1. **Prepare input files:**
   - Optimize CI geometry with **SHARC–ORCA**
   - Generate gradients and NACs with **SHARC–OpenMolcas**
   - Collect the following files:
     - `gradientA.out`
     - `gradientB.out`
     - `NAC.out`
     - *(Optional)* Your `.xyz` geometry file

2. **Run the visualizer:**

   ```bash
   python3 ci_branching_plane.py
```

📂 **Example data:**  
See [`example_input/`](example_input/) for sample files and [`example_output/`](example_output/) for typical results.

---

## 📁 Repository Structure

```bash
conezen/
├── ci_branching_plane.py     # Main visualizer script
├── requirements.txt          # Python dependencies
│
├── example_input/            # Example NAC and gradient files
├── example_output/           # Example plots and animations
│
├── LICENSE                   # GPL-3.0 license text
├── CITATION.cff              # Citation metadata
├── .zenodo.json              # Zenodo metadata for DOI
├── ACKNOWLEDGMENTS.md        # Acknowledgments
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Code of Conduct
├── RELEASE_NOTES.md          # Version history
└── README.md                 # Main documentation
```
---
## ✏️ Citation

If you use **ConeZen** for published research, please cite:
- **Kalpajyoti Dihingia**, *ConeZen: Visualiser for conical intersection branching planes* (Zenodo, DOI: TBD)
- The related scientific paper once published

```bibtex
@software{conezen,
  author  = {Kalpajyoti Dihingia},
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
