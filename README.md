# Beam & Shaft Stress Analysis Calculator

A Python-based mechanical engineering analysis tool for evaluating the structural behaviour of beams and shafts under specified loading and material conditions.

## Project Overview

This project contains two independent engineering analysis modules:

1. **Beam Analysis**
2. **Shaft Analysis**

The program performs analytical calculations and generates engineering plots automatically using Python.

---

## 1. Beam Analysis

The beam module evaluates a simply supported beam subjected to a concentrated load.

### Calculations

- Support reactions
- Shear force
- Bending moment
- Bending stress
- Maximum deflection
- Deflection position
- Factor of Safety
- Structural status

### Generated Graphs

- Shear Force Diagram
- Bending Moment Diagram
- Beam Deflection Curve

### Example Input

| Parameter | Value |
|---|---:|
| Material | AISI 4140 Steel |
| Beam Length | 1000 mm |
| Beam Width | 50 mm |
| Beam Height | 40 mm |
| Applied Load | 500 N |
| Load Position | 500 mm |

---

## 2. Shaft Analysis

The shaft module evaluates the structural response of a circular shaft subjected to bending and torsional loading.

The program supports both solid and hollow shaft configurations.

### Calculations

- Cross-sectional area
- Area moment of inertia
- Polar moment of inertia
- Volume
- Mass
- Bending stress
- Torsional shear stress
- Von Mises stress
- Angle of twist
- Factor of Safety
- Structural status

### Generated Graphs

- Shaft Stress Distribution
- Solid vs Hollow Shaft Comparison

---

## 3. Solid vs Hollow Shaft Analysis

The program compares a solid shaft with a selected hollow shaft having the same outer diameter.

The comparison includes:

- Mass
- Bending stress
- Torsional shear stress
- Von Mises stress
- Factor of Safety
- Mass reduction

### Example Result

For the tested shaft configuration:

| Parameter | Solid Shaft | Hollow Shaft |
|---|---:|---:|
| Outer Diameter | 40 mm | 40 mm |
| Inner Diameter | 0 mm | 30 mm |
| Mass | 9.865 kg | 4.316 kg |
| Bending Stress | 31.83 MPa | 46.56 MPa |
| Torsional Shear | 7.96 MPa | 11.64 MPa |
| Von Mises Stress | 34.69 MPa | 50.74 MPa |
| Factor of Safety | 18.88 | 12.91 |

The tested hollow-shaft configuration produced a calculated mass reduction of **56.25%** while maintaining a calculated Factor of Safety above unity for the specified loading conditions.

---

## 4. Software and Technologies

- Python 3
- NumPy
- Matplotlib

---

## 5. Project Structure

```text
Pyth/
│
├── beam.py
├── shaft.py
│
├── results/
│   ├── beam_deflection.png
│   ├── bending_moment_diagram.png
│   ├── shear_force_diagram.png
│   ├── shaft_stress_distribution.png
│   └── solid_vs_hollow_comparison.png
│
├── Screenshots/
│
└── README.md