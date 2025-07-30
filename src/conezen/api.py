# conezen/api.py

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from . import logic

class ConeZenAPI:
    """
    Provides a programmatic API for ConeZen's core functionalities.

    This class encapsulates the workflow of loading data, calculating
    branching plane parameters, computing potential energy surfaces,
    and generating visualizations.

    Usage:
        >>> from conezen import ConeZenAPI
        >>> # Initialize the API
        >>> cz = ConeZenAPI()
        >>> # Load data from files (or from numpy arrays)
        >>> cz.load_data_from_files(
        ...     grad_a_path='gradientA.out',
        ...     grad_b_path='gradientB.out',
        ...     nac_path='NAC.out'
        ... )
        >>> # Perform the core calculations
        >>> cz.calculate_parameters()
        >>> cz.compute_surfaces(E_X=0.0)
        >>> # Get results
        >>> params = cz.get_parameters()
        >>> print(f"Calculated sigma (σ): {params['sigma']:.6f}")
        >>> # Generate and show a plot
        >>> fig, ax = cz.plot()
        >>> plt.show()
    """
    def __init__(self):
        """Initializes the ConeZenAPI object."""
        self.grad_A = None
        self.grad_B = None
        self.h = None
        self.parameters = {}
        self.surfaces = {}

    def load_data_from_files(self, grad_a_path: str, grad_b_path: str, nac_path: str):
        """
        Loads gradient and NAC data from files.

        Args:
            grad_a_path (str): Path to the gradient file for State A.
            grad_b_path (str): Path to the gradient file for State B.
            nac_path (str): Path to the NAC vector file.
        """
        print("Loading data from files...")
        self.grad_A, _ = logic.load_vector_file(Path(grad_a_path))
        self.grad_B, _ = logic.load_vector_file(Path(grad_b_path))
        self.h, _ = logic.load_vector_file(Path(nac_path))
        print(f"Data loaded successfully. Found {self.grad_A.shape[0]} atoms.")

    def load_data_from_arrays(self, grad_a: np.ndarray, grad_b: np.ndarray, h: np.ndarray):
        """
        Loads gradient and NAC data directly from NumPy arrays.

        Args:
            grad_a (np.ndarray): Gradient of State A (N x 3 array).
            grad_b (np.ndarray): Gradient of State B (N x 3 array).
            h (np.ndarray): NAC vector (N x 3 array).
        """
        if not (grad_a.shape == grad_b.shape == h.shape and grad_a.ndim == 2 and grad_a.shape[1] == 3):
            raise ValueError("All input arrays must be of shape (N, 3).")
        self.grad_A = grad_a
        self.grad_B = grad_b
        self.h = h
        print(f"Data loaded successfully from arrays for {self.grad_A.shape[0]} atoms.")

    def calculate_parameters(self):
        """
        Calculates the branching plane vectors and key CI quantities.
        Requires data to be loaded first.
        """
        if self.grad_A is None or self.grad_B is None or self.h is None:
            raise RuntimeError("Data not loaded. Call load_data_from_files() or load_data_from_arrays() first.")
        
        print("Calculating branching plane parameters...")
        self.parameters = logic.get_branching_plane_vectors(self.grad_A, self.grad_B, self.h)
        print("Calculation complete.")

    def compute_surfaces(self, E_X: float = 0.0):
        """
        Computes the potential energy surfaces (PES).
        Requires parameters to be calculated first.

        Args:
            E_X (float, optional): Energy of the intersection point in Hartree. Defaults to 0.0.
        """
        if not self.parameters:
            raise RuntimeError("Parameters not calculated. Call calculate_parameters() first.")

        print(f"Computing surfaces with E_X = {E_X} Hartree...")
        X, Y, E_A, E_B, had_neg_sqrt = logic.compute_surfaces(self.parameters, E_X)
        self.surfaces = {'X': X, 'Y': Y, 'E_A': E_A, 'E_B': E_B}
        if had_neg_sqrt:
            print("⚠️  Warning: Some negative values in sqrt term were clamped to zero.")
        print("Surface computation complete.")

    def get_parameters(self) -> dict:
        """
        Returns the dictionary of calculated branching plane parameters.

        Returns:
            dict: A dictionary containing 'x_hat', 'y_hat', 'del_gh', 'delta_gh', 'sigma', and 'theta_s_rad'.
        """
        if not self.parameters:
            print("Warning: Parameters have not been calculated yet.")
        return self.parameters

    def get_vectors(self) -> dict:
        """
        Returns the orthonormal branching plane vectors x_hat and y_hat reshaped to (N, 3).

        Returns:
            dict: A dictionary with 'x_hat' and 'y_hat' as (N, 3) numpy arrays.
        """
        if not self.parameters:
            raise RuntimeError("Parameters not calculated. Call calculate_parameters() first.")
        
        N = self.grad_A.shape[0]
        return {
            'x_hat': self.parameters['x_hat'].reshape(N, 3),
            'y_hat': self.parameters['y_hat'].reshape(N, 3)
        }

    def plot(self, **kwargs):
        """
        Generates a 3D static plot of the energy surfaces.
        Surfaces must be computed first.

        Args:
            **kwargs: Additional keyword arguments passed to `logic.plot_surfaces()`
                      (e.g., `fig_width`, `fig_height`, `elev`, `azim`).

        Returns:
            A tuple of (matplotlib.figure.Figure, matplotlib.axes.Axes).
        """
        if not self.surfaces:
            raise RuntimeError("Surfaces not computed. Call compute_surfaces() first.")
        
        fig_w = kwargs.pop('fig_width', logic.DEFAULT_FIGSIZE[0])
        fig_h = kwargs.pop('fig_height', logic.DEFAULT_FIGSIZE[1])
        
        return logic.plot_surfaces(
            self.surfaces['X'], self.surfaces['Y'],
            self.surfaces['E_A'], self.surfaces['E_B'],
            fig_width=fig_w, fig_height=fig_h, **kwargs
        )
    
    def animate(self, outpath: str, **kwargs):
        """
        Generates a 3D rotation animation of the energy surfaces.
        Surfaces must be computed first.

        Args:
            outpath (str): The output file path (e.g., 'animation.mp4' or 'animation.gif').
            **kwargs: Additional keyword arguments passed to `logic.animate_surfaces()`
                      (e.g., `anim_dpi`, `anim_fps`, `writer`).
        """
        if not self.surfaces:
            raise RuntimeError("Surfaces not computed. Call compute_surfaces() first.")

        # Determine writer from file extension if not provided explicitly
        if 'writer' not in kwargs:
            kwargs['writer'] = 'ffmpeg' if outpath.lower().endswith('.mp4') else 'pillow'

        logic.animate_surfaces(
            self.surfaces['X'], self.surfaces['Y'],
            self.surfaces['E_A'], self.surfaces['E_B'],
            fig_width=kwargs.pop('fig_width', logic.DEFAULT_FIGSIZE[0]),
            fig_height=kwargs.pop('fig_height', logic.DEFAULT_FIGSIZE[1]),
            anim_dpi=kwargs.pop('anim_dpi', logic.DEFAULT_ANIM_DPI),
            anim_fps=kwargs.pop('anim_fps', logic.DEFAULT_ANIM_FPS),
            outpath=outpath,
            **kwargs
        )
