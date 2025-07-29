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

Conical intersections (CIs) are regions of electronic state degeneracy that act as efficient funnels for non-radiative decay, governing the outcomes of many photochemical processes, from the photostability of DNA to the mechanism of vision. They act as highly efficient funnels for ultrafast, non-radiative transitions between potential energy surfaces (PESs). A complete mechanistic understanding requires characterizing the topography of the PESs in the two-dimensional "branching plane" where the degeneracy is lifted [@Galvan2016]. However, interpreting the raw numerical data (state gradients and coupling vectors) produced by quantum chemistry software is a significant challenge.

We present **ConeZen** , an open-source Python package designed to bridge this gap. ConeZen automates the entire workflow from parsing the output of quantum chemistry packages (e.g., SHARC-OpenMolcas) to the generation of quantitative topological descriptors and intuitive 3D visualizations. By providing a user-friendly command-line interface (CLI) and a flexible API, ConeZen allows researchers to rapidly characterize and visualize CI topographies, facilitating a deeper understanding of nonadiabatic reaction dynamics.

# Statement of need

The study of nonadiabatic dynamics is central to modern computational photochemistry. While powerful software packages like SHARC-OpenMolcas can compute the essential vectors—state gradients and nonadiabatic couplings (NACs)—that describe a CI, they often lack integrated tools for visualizing the resulting PES topography. This forces researchers to engage in manual, often complex and error-prone, post-processing to extract meaningful chemical insight from the raw data. This gap creates a significant barrier to entry for newcomers and slows the pace of research for experienced practitioners.

ConeZen addresses this critical need by providing a standardized, reproducible, and easy-to-use tool for CI analysis. It processes the raw vector data to generate quantitative metrics that are essential for classifying the intersection's character. By calculating the slope, asymmetry, and tilt of the intersecting surfaces, ConeZen allows for an unambiguous classification of a CI as peaked, sloped, bifurcating, or single-path. This classification is directly linked to the predicted reaction dynamics, indicating whether a decay process will be highly efficient (peaked) or whether it might lead to a mixture of products (bifurcating). By automating this analysis, ConeZen lowers the barrier to entry, enhances research productivity, and promotes reproducibility in the field of computational photochemistry.



# Acknowledgements

The authors acknowledge support from Banaras Hindu University (BHU) and the Science and Engineering Research Board (SERB), India.

# References



