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
*
# **Elasto-Plasticity and Hardening Models**

## **Introduction**
Elasto-plasticity describes the behavior of materials that undergo **both elastic and plastic deformation** when subjected to loading. 

- **Elastic deformation**: The material returns to its original shape when the load is removed.
- **Plastic deformation**: The material undergoes **permanent deformation** once the stress exceeds a certain limit, called the **yield stress**.

To model plastic behavior, two common hardening rules are used: **Isotropic Hardening** and **Kinematic Hardening**.

---

## **Isotropic Hardening**
### **Concept**
In **isotropic hardening**, the yield surface **expands uniformly** in all directions as plastic deformation occurs. This means that after yielding, the material becomes stronger, and a higher stress is required to continue plastic flow.

### **Characteristics**
- Yield surface grows **symmetrically**.
- Hardening affects material strength **equally in all directions**.
- Suitable for materials undergoing **monotonic loading** (continuous loading in one direction).
- Does **not** capture the **Bauschinger effect** (which describes how materials soften when load direction is reversed).

### **Mathematical Representation**
If $Y_0$ is the initial yield stress and $H$ is the hardening modulus, then the **new yield stress** $Y$ after plastic strain $\varepsilon_p$ follows:

$$
Y = Y_0 + H \varepsilon_p
$$

Where:
- $Y_0$ is the initial yield stress.
- $H$ is the hardening modulus (determines how much the yield surface expands).
- $\varepsilon_p$ is the accumulated plastic strain.

---

## **Kinematic Hardening**
### **Concept**
In **kinematic hardening**, the yield surface **translates (shifts) in stress space** without changing size. This allows the material to model cyclic loading and capture the **Bauschinger effect**.

### **Characteristics**
- Yield surface **moves** instead of expanding.
- Captures **cyclic plasticity** and **ratcheting effects**.
- Useful for **reversed and cyclic loading** (e.g., fatigue analysis).
- More realistic for metals and alloys subjected to **alternating stress cycles**.

### **Mathematical Representation**
The evolution of the **back stress** $X$, which defines the translation of the yield surface, is governed by:

$$
dX = C d\varepsilon_p
$$

Where:
- $X$ is the back stress (shifts the yield surface).
- $C$ is a kinematic hardening parameter.
- $d\varepsilon_p$ is the plastic strain increment.

---

## **Comparison: Isotropic vs. Kinematic Hardening**

| Feature               | Isotropic Hardening | Kinematic Hardening |
|-----------------------|--------------------|---------------------|
| Yield Surface Change | Expands uniformly  | Translates (shifts) |
| Captures Bauschinger Effect? | ❌ No | ✅ Yes |
| Best for Monotonic Loading? | ✅ Yes | ❌ No |
| Best for Cyclic Loading? | ❌ No | ✅ Yes |
| Yield Stress Increase? | **Yes** (hardening in all directions) | **No** (only shifts) |

---

## **Applications**
### **Isotropic Hardening**
✅ Used for **monotonic loading** problems, such as:
- Metal forming
- Pressing and forging
- Simple tensile/compression tests

### **Kinematic Hardening**
✅ Used for **cyclic loading** problems, such as:
- Fatigue analysis
- Springback in sheet metal forming
- Structural analysis of materials under **alternating loads**

---

## **Example: Stress-Strain Response**
Below is a comparison of how stress-strain behavior differs under **isotropic** and **kinematic hardening**.

- **Isotropic Hardening** → The material hardens in all directions, requiring more stress for continued plastic flow.
- **Kinematic Hardening** → The material softens when the load is reversed, modeling real cyclic behavior.

📌 **Check out the implementation in this repository!** 🚀
*
---

## **References**
- J. Lubliner, *Plasticity Theory*, 2006.
- T. Belytschko, *Nonlinear Finite Elements for Continua and Structures*, 2014.
- Simo & Hughes, *Computational Inelasticity*, 1998.

---

### Conda environment, install, and testing <a name="install"></a>
_This section is copied and pasted from [Lejeune's Lab Graduate Course Materials: Bisection Method](https://github.com/Lejeune-Lab-Graduate-Course-Materials/bisection-method.git)_

To install this package, please begin by setting up a conda environment (mamba also works):
```bash
conda create --name elastoplasticity-env python=3.12
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
