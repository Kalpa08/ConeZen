# 🌀 ConeZen
Copyright (C) 2025 Kalpa Dihingia

**ConeZen** is an open-source Python tool for visualising the branching plane topology near a conical intersection (CI).

It uses nonadiabatic coupling (NAC) and gradient data from the **SHARC–OpenMolcas** interface to generate clear 3D plots and rotating animations.  
Ideal for computational chemists who want reproducible, publication-ready CI topology plots.

---

## 📌 Features
- Visualise CI branching planes in 3D.
- Generate static plots and smooth rotation animations (GIF/MP4).
- Tested with NAC and gradient data from SHARC–OpenMolcas.
- Fully open-source under GPLv3.
- Citation required for published work.

---

## ⚡ How to use

1. **Optimise** the CI geometry with SHARC–ORCA.
2. **Calculate** gradients & NACs with SHARC–OpenMolcas.
3. **Extract** `NAC.out`, `gradientA.out`, `gradientB.out`.
4. **Run:** `python3 ci_plot.py` and follow prompts.

See `example_input/` for a working demo.

---

## ✏️ Citation

If you use **ConeZen** for published research, please cite:
- **Kalpa Dihingia**, *ConeZen: Visualiser for conical intersection branching planes* (Zenodo, DOI: TBD)
- The related scientific paper once published

```bibtex
@software{kalpa_conezen_2025,
  author  = {Kalpa Dihingia},
  title   = {ConeZen: Visualiser for conical intersection branching planes},
  year    = 2025,
  publisher = {Zenodo},
  version = {v1.0},
  doi     = {10.xxxx/zenodo.xxxxx}
}
