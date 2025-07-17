---
title: 'ConeZen: A Python Package for Visualizing Conical Intersection Branching Planes'
tags:
  - Python
  - computational chemistry
  - photochemistry
  - conical intersection
  - nonadiabatic dynamics
  - data visualization
authors:
  - name: Kalpajyoti Dihingia
    orcid: 0009-0006-1147-609X
    affiliation: 1
  - name: Biswajit Maiti
    orcid: 0000-0002-5018-5889
    affiliation: 1
affiliations:
  - name: Department of Chemistry, Banaras Hindu University, Varanasi, Uttar Pradesh, India
    index: 1
date: 2025-07-17
bibliography: paper.bib
---

# Summary

Conical intersections (CIs) are regions of electronic state degeneracy that act as efficient funnels for non-radiative decay, governing the outcomes of many photochemical processes \cite{Yarkony2001, Nelson2020}. Understanding the mechanism requires characterization of the potential energy surfaces (PES) in the branching plane around the CI.

We present **ConeZen**, an open-source Python package that computes and visualizes the two-dimensional PES near a conical intersection. ConeZen is available on the Python Package Index (PyPI) and provides a command-line interface for user-friendly operation. It automates the entire workflow from input parsing (e.g., from SHARC/OpenMolcas) to 3D visualization, helping researchers understand CI topographies without manual post-processing.

# Statement of need

Nonadiabatic transitions via CIs are central to excited-state molecular dynamics \cite{Boggio-Pasqua2015}. While quantum chemistry software such as SHARC-OpenMolcas \cite{Mai2016} can compute the state gradients and nonadiabatic coupling (NAC) vectors required to describe a CI, these tools do not offer a direct way to visualize the topography or interpret the physical implications.

ConeZen bridges this gap by processing vector data and rendering meaningful visualizations and quantitative metrics. These include slope, asymmetry, and cone tilts that are essential for determining if a CI is peaked, sloped, bifurcating, or single-path \cite{Galvan2022, Cuellar-Zuquin2023}.

The program serves a broad range of theoretical chemists by standardizing CI visualization with minimal user effort, enabling reproducibility, and lowering the entry barrier for new researchers.

# Implementation

ConeZen is written in Python 3 and built on standard scientific libraries including **NumPy** \cite{harris2020array}, **Pandas** \cite{mckinney-proc-scipy-2010}, and **Matplotlib** \cite{Hunter:2007}.

The package implements the first-order analytical model described by Fdez. Galván et al. \cite{Galvan2016}, which uses two input vectors: the gradient difference vector \(\mathbf{g}_{AB}\) and the nonadiabatic coupling vector \(\mathbf{h}_{AB}\). These are orthogonalized and normalized to generate a local basis \(\hat{x}, \hat{y}\) for the branching plane.

Using this basis, ConeZen computes several topological descriptors:

- **Pitch** ($\delta_{gh}$): average energetic slope.
- **Asymmetry** ($\Delta_{gh}$): ellipticity of the cone.
- **Tilt** $$\sigma$$ and **tilt heading** $$\theta_s$$ : define the slope of the average PES.

The energy surfaces $$ (E(r, \theta)) $$ of the two intersecting states are computed using the analytical expression:

$$
E(r, \theta) = E_{X} + \delta_{gh} \cdot r \left( \sigma \cos(\theta - \theta_s) \pm \sqrt{1 + \Delta_{gh} cos(2 \theta )} \right )
$$

where $$ \E_{X} $$ is the energy at the intersection point.

# Example

We demonstrate the application of ConeZen using a benchmark CI from a model system. The necessary gradients and NAC vectors were calculated at the SA-CASSCF level using SHARC–OpenMolcas and provided as input to ConeZen.

The resulting output included a 3D surface plot of the two PES and tabulated parameters identifying the CI as *sloped bifurcating*, consistent with earlier reports.

> **Figure 1**: 3D plot of potential energy surfaces for a conical intersection in *[Molecule Name]*. The double-cone structure is evident.

# Acknowledgements

This work was developed at Banaras Hindu University (BHU). The authors thank Prof. Biswajit Maiti for valuable discussions and scientific guidance.

# References

