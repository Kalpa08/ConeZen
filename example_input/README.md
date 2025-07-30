# Example: Reproducing Results from JCTC 2016, 12, 3636

This directory contains the necessary input files to reproduce the results for the bifurcating sloped conical intersection presented in *J. Chem. Theory Comput. 2016, 12 (8), 3636–3653* with the help of **ConeZen**.

## How to Reproduce

This example uses the manual parameter input workflow of ConeZen, where you provide the final branching plane vectors and the calculated CI parameters directly.

1.  **Start ConeZen** from your terminal:
    ```bash
    conezen
    ```

2.  When prompted, choose the **manual parameter input** workflow:
    * Answer **no** (`n`) to "Do you want to automatically extract...".
    * Answer **no** (`n`) to "Do you have the raw gradient and non-adiabatic coupling vectors...".

3.  **Provide the input files** located in this directory:
    * For the `x_hat` vector file, enter: `x_vector.out`
    * For the `y_hat` vector file, enter: `y_vector.out`

4.  **Enter the conical intersection parameters** when prompted:
    * `del_gh (δ_gh)`: **0.0949**
    * `delta_gh (Δ_gh)`: **0.5320**
    * `sigma (σ)`: **0.9550**
    * `theta_s (θ_s) in degrees`: **0**
    * `Energy of the intersection point, E_X (Hartree)`: **0**

5.  Follow the remaining prompts to visualize and save the results. The output should match the peaked single path topography described in the paper.



