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

Conical intersections (CIs) are regions of electronic state degeneracy that act as efficient funnels for non-radiative decay, governing the outcomes of many photochemical processes, from the photostability of DNA to the mechanism of vision `[@Yarkony2001` , `@Nelson2020]`. They act as highly efficient funnels for ultrafast, non-radiative transitions between potential energy surfaces (PESs). A complete mechanistic understanding requires characterizing the topography of the PESs in the two-dimensional "branching plane" where the degeneracy is lifted [@Galvan2016]. However, interpreting the raw numerical data (state gradients and coupling vectors) produced by quantum chemistry software is a significant challenge.

We present **ConeZen** , an open-source Python package designed to bridge this gap. ConeZen automates the entire workflow from parsing the output of quantum chemistry packages (e.g., SHARC-OpenMolcas [@Galvan2019]) to the generation of quantitative topological descriptors and intuitive 3D visualizations. By providing a user-friendly command-line interface (CLI) and a flexible API, ConeZen allows researchers to rapidly characterize and visualize CI topographies, facilitating a deeper understanding of nonadiabatic reaction dynamics.

# Statement of need

The study of nonadiabatic dynamics is central to modern computational photochemistry. While powerful software packages like SHARC-OpenMolcas can compute the essential vectors—state gradients and nonadiabatic couplings (NACs)—that describe a CI, they often lack integrated tools for visualizing the resulting PES topography. This forces researchers to engage in manual, often complex and error-prone, post-processing to extract meaningful chemical insight from the raw data. This gap creates a significant barrier to entry for newcomers and slows the pace of research for experienced practitioners.

ConeZen addresses this critical need by providing a standardized, reproducible, and easy-to-use tool for CI analysis. It processes the raw vector data to generate quantitative metrics that are essential for classifying the intersection's character. By calculating the slope, asymmetry, and tilt of the intersecting surfaces, ConeZen allows for an unambiguous classification of a CI as peaked, sloped, bifurcating, or single-path `[@Galvan2022; @Cuellar-Zuquin2023]`. This classification is directly linked to the predicted reaction dynamics, indicating whether a decay process will be highly efficient (peaked) or whether it might lead to a mixture of products (bifurcating). By automating this analysis, ConeZen lowers the barrier to entry, enhances research productivity, and promotes reproducibility in the field of computational photochemistry.

# Implementation

ConeZen is a lightweight package written in Python 3. It is built on a minimal stack of robust and widely used scientific libraries: NumPy for numerical operations [@harris2020array], Pandas for data handling [@mckinney-proc-scipy-2010], and Matplotlib for 2D and 3D plotting [@Hunter:2007].

The core of the package is an implementation of the first-order analytical model described by Fdez. Galván et al. `@Galvan2016`,. The a;hprotj, proceeds as follow:
  - **Input Processing:** The tool takes the gradient difference vector $$g^{AB}$$ and the nonadiabatic coupling vector $$h^{AB}$$ as primary inputs
  - **Orthonormalization:**  It performs a scaling and rotation procedure to transform these two vectors into an orthonormal basis,$$\hat{x}$$ , $$\hat{y}$$ which defines the branching plane.
  - **Parameter Calculation:** Using this basis, ConeZen computes the key topological descriptors:
      - Pitch or pitch ($\delta_{gh}$)
      - Asymmetry ($\Delta_{gh}$)
      - The relative Tilt and tilt heading $$\sigma$$, $$\theta_s$$ respectively

The energy surfaces $$E(r, \theta)$$ of the two intersecting states are computed using the analytical expression:

$$
E(r, \theta) = E_{X} + \delta_{gh} \cdot r \left( \sigma \cos(\theta - \theta_s) \pm \sqrt{1 + \Delta_{gh} cos(2 \theta )} \right )
$$

where 
    - $$E_{X}$$ is the energy at the intersection point.
    - $$r$$ and $$\theta$$ are polar coordinates 

# Acknowledgements

The authors acknowledge support from Banaras Hindu University (BHU) and the Science and Engineering Research Board (SERB), India.

# References



