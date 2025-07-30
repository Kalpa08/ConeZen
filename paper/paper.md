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

Conical intersections (CIs) are fundamental mechanistic features that govern the outcomes of virtually all photochemical and photophysical processes in polyatomic molecules. Once considered theoretical curiosities, they are now recognized as ubiquitous and essential for explaining non-radiative dynamics, a paradigm shift that has established them as the "new conventional wisdom" in photochemistry.[@Yarkony2001] The functional role of a CI is dictated by its local topography, enabling it to serve starkly different purposes. In DNA, CIs provide an ultrafast deactivation funnel that dissipates the energy from UV radiation, ensuring the remarkable photostability of our genetic material.[@Sobolewski2006],[@barbatti2010relaxation] In contrast, the CI in the retinal chromophore acts as a highly efficient chemical switch, channeling photo-energy into the specific isomerization that initiates vision.[@polli2010conical]

Despite their importance, a significant bottleneck exists in translating the raw numerical data—state energy gradients and nonadiabatic coupling vectors—produced by quantum chemistry software into mechanistic insight. We present `ConeZen`, an open-source Python package designed to bridge this gap. ConeZen automates the entire analytical workflow, from parsing the output of quantum chemistry packages like SHARC-OpenMolcas [@Mai_sharc2018],[@Galvan2019]  to generating quantitative topological descriptors and intuitive 3D visualizations. By providing a user-friendly command-line interface (CLI) and a flexible API, `ConeZen` empowers researchers to rapidly characterize and visualize CI topographies, facilitating a deeper understanding of nonadiabatic reaction dynamics.

# Statement of need

The study of nonadiabatic dynamics is central to modern computational photochemistry. While powerful software packages such as SHARC-OpenMolcas can compute the essential vectors that describe a CI, they often lack integrated tools for analyzing and visualizing the resulting potential energy surface (PES) topography. This deficiency forces researchers into manual, often complex and error-prone, post-processing to extract meaningful chemical insight from raw data. This "analysis gap" creates a significant barrier to entry for newcomers and slows the pace of research for experienced practitioners.

`ConeZen` addresses this critical need by providing a standardized, reproducible, and easy-to-use tool for CI analysis. It processes the raw vector data to generate quantitative metrics essential for classifying the intersection's character, implementing the robust methodology developed by Fdez. Galván et al. [@Galvan2016],[@Boeije2023] By calculating the slope, asymmetry, and tilt of the intersecting surfaces, `ConeZen` allows for an unambiguous classification of a CI's topography:[@Fdez.Galvan2022]
(a) **Peaked vs. Sloped:** This describes the upper PES. A peaked CI acts as a highly efficient funnel for decay and is often associated with photoreactivity, whereas a sloped CI has an exit ramp that often favors a return to the reactant geometry, promoting photostability.
(b) **Bifurcating vs. Single-Path:** This describes the lower PES, which dictates the reaction outcome. A bifurcating CI features two distinct exit valleys that can lead to a mixture of photoproducts, while a single-path CI has one well-defined channel that favors a single outcome.

This classification is directly linked to predicted reaction dynamics, providing immediate mechanistic insight. By automating this analysis and coupling it with rigorous 3D visualization, `ConeZen` lowers the barrier to entry, enhances research productivity, and promotes reproducibility in the field of computational photochemistry.

# Acknowledgements

The authors acknowledge support from Banaras Hindu University (BHU) and the Science and Engineering Research Board (SERB), India.

# References



