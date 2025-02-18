[![codecov](https://codecov.io/gh/sarajahedazad/Elastoplasticity/graph/badge.svg?token=lwDXua5AOA)](https://codecov.io/gh/sarajahedazad/Elastoplasticity)

---
### Table of contents
* [What is Newton's Method?](#nm)
* [Requirements](#requirements)
* [Codes](#codes)
* [Conda environment, install, and testing](#install)
* [An alternative way to test the implemented Newton's method without installing the package ](#alter)
* [References](#references)

---
# Elastoplasticty

This repository provides an implementation of [Newton's method](https://en.wikipedia.org/wiki/Newton%27s_method) (also known as the Newton–Raphson method) for finding roots (zeros) of functions or systems of equations. Newton's method is an iterative algorithm commonly used in numerical analysis and scientific computing.

## What is Newton's Method? <a name="nm"></a>

Newton's method is designed to find solutions to the equation $F(x) = 0$. It uses the first-order Taylor expansion to generate iterative approximations of the root. For a single variable, each iteration is:


$x_{k+1} = x_k - \frac{F(x_k)}{F'(x_k)}$


For multiple variables, the concept extends using the Jacobian matrix $J(x)$:

$x_{k+1} = x_k - J(x_k)^{-1} F(x_k)$

By iterating this process, we often converge quickly (quadratically, near the root) to a solution, given a good initial guess and certain regularity conditions on $F$.

Stopping criteria: Maximum number of iterations is reached, or the found solution is smaller than a predefined absolute tolerance, or the absolute differnece between $x_{k+1}$ and $x_{k}$ is smaller than a predefined relative tolerance.

---
### Requirements

`numpy library`  
`sympy library`     

---

### Codes
The file `newton_solver.py` (located in the `src/newtonsolver` folder) contains several functions that implement Newton's method. The primary function that users call to find the root of an expression is `solve`.

**Function `solve`**  
*Inputs:*  
**F**: expression of a function defined in sympy. Should be a `sympy.Matrix`.    
example: `F = sympy.Matrix([ x[0]**3- 4 *x[0], x[0]**2- 1 ])`     
**J**: Jacobian of F. Should be a `sympy.Matrix`.    
example: `J = F.jacobian(x)`     
**x**: A tuple containing symbols used to define the expression F in sympy. Should be as `tuple[sympy.Symbol, ...]`.     
example: `x = sympy.symbols(f'x:{n}')` in which n is the number of variables (according to F, n is 2 here).     
**x0**: a numpy arrasy as the initial guess for x.     
example: `x = np.array([ 1.5, 2.2 ])`   
**max_iter**: maximum number of iteration allowed to run the Newton's algorithm, default = 50  
**abs_tol**: absolute tolerance, default = $10^{-9}$  
**rel_tol**: relative tolerance, default = $10^{-9}$    
**verbose**: whether to print out the debug information at each iteration or not, default = False

*Outputs:*  
**root**: the solution for the expression F, based on the initial guess of x0.

`Error`: if no root is found after maximum number of iterations, an error will be raised.

---

### Conda environment, install, and testing <a name="install"></a>
_This section is copied and pasted from [Lejeune's Lab Graduate Course Materials: Bisection Method](https://github.com/Lejeune-Lab-Graduate-Course-Materials/bisection-method.git)_

To install this package, please begin by setting up a conda environment (mamba also works):
```bash
conda create --name newton-solver-env python=3.12
```
Once the environment has been created, activate it:

```bash
conda activate elastoplasticity-env
```
Double check that python is version 3.12 in the environment:
```bash
python --version
```
Ensure that pip is using the most up to date version of setuptools:
```bash
pip install --upgrade pip setuptools wheel
```
Create an editable install of the bisection method code (note: you must be in the correct directory):
```bash
pip install -e .
```
Test that the code is working with pytest:
```bash
pytest -v --cov=elastoplasticity --cov-report term-missing
```
Code coverage should be 100%. Now you are prepared to write your own code based on this method and/or run the tutorial. 


If you are using VSCode to run this code, don't forget to set VSCode virtual environment to bisection-method-env.

If you would like the open `tutorial_elastoplasticity.ipynb` located in the `tutorials` folder as a Jupyter notebook in the browser, you might need to install Jupyter notebook in your conda environment as well:
```bash
pip install jupyter
```
```bash
cd tutorials/
```
```bash
jupyter notebook tutorial_elastoplasticity.ipynb
```
### An alternative way to test the implemented Newton's method without installing the package <a name="alter"></a>
- Step 1: Download the `elasto_plasity.py` file from the folder `src/elastoplasticiy`([here](https://github.com/sarajahedazad/Elastoplasticity/tree/main/src/elastoplasticity)). Place it in the same folder as your working directory.
- Step 2: Create a python file in that folder and write your example in that file. You can import the `elastoplasticity` with the following line:
`import elasto_plasticity as ep`
- Step 3: Run your code an enjoy!
Here is an example that demonstrates how you can test `elasto_plasticity.py` file (it should be in the same folder as the python file that you intend to run):

```
import numpy as np
import sympy
import elasto_plasticity as ep

E, H, Y= 1000, 111, 10
Y0 = Y
ep_iso = ep.ElastoPlasticIsoHard( E, H, Y0)
ep_k = ep.ElastoPlasticKinematicHard( E, H, Y)
sigma0 = 0
epsilon_arr = np.concatenate( (np.linspace(0, 0.02, 100), np.linspace(0.02, 0, 100), np.linspace(0, -0.02, 100), np.linspace(-0.02, 0, 100), np.linspace(0, 0.04, 200), np.linspace(0.04, 0, 200)))

ep.plot_total_applied_strain( epsilon_arr )
ep_iso.plot_stress_strain_curve(epsilon_arr, sigma0)
ep_k.plot_stress_strain_curve(epsilon_arr, sigma0)
```
---
### References
* [Lejeune Lab Graduate Course Materials: Bisection-Method](https://github.com/Lejeune-Lab-Graduate-Course-Materials/bisection-method/tree/main) 
* chatGPT: was used for completing the documentation. The introduction and [What is Newton's Method?](#nm) sections are written by the GenAI. Also, was used to generate epsilon arrays.
