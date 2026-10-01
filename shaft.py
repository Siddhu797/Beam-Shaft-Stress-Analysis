import numpy as np
import matplotlib.pyplot as plt
import os
import math

# ============================================================
# SHAFT STRESS ANALYSIS + SOLID/HOLLOW COMPARISON
# ============================================================

print("====================================================")
print("       SHAFT STRESS ANALYSIS CALCULATOR")
print("====================================================")

# ============================================================
# MATERIAL DATABASE
# ============================================================

materials = {
    1: {
        "name": "Structural Steel",
        "E": 200000,
        "yield": 250,
        "nu": 0.30,
        "density": 7850
    },

    2: {
        "name": "AISI 4140 Steel",
        "E": 205000,
        "yield": 655,
        "nu": 0.29,
        "density": 7850
    },

    3: {
        "name": "Aluminium 6061-T6",
        "E": 68900,
        "yield": 276,
        "nu": 0.33,
        "density": 2700
    },

    4: {
        "name": "Aluminium 7075-T6",
        "E": 71700,
        "yield": 503,
        "nu": 0.33,
        "density": 2810
    },

    5: {
        "name": "Stainless Steel 304",
        "E": 193000,
        "yield": 215,
        "nu": 0.29,
        "density": 8000
    }
}

# ============================================================
# SHAFT TYPE
# ============================================================

print("\nShaft Type")
print("----------")
print("1. Solid Shaft")
print("2. Hollow Shaft")

try:
    shaft_type = int(input("Select shaft type (1-2): "))
except ValueError:
    print("\nERROR: Enter 1 or 2.")
    exit()

if shaft_type not in [1, 2]:
    print("\nERROR: Invalid shaft type.")
    exit()

# ============================================================
# INPUT
# ============================================================

try:

    outer_diameter = float(
        input("\nEnter outer diameter (mm): ")
    )

    if shaft_type == 2:

        inner_diameter = float(
            input("Enter inner diameter (mm): ")
        )

    else:

        inner_diameter = 0

    length = float(
        input("Enter shaft length (mm): ")
    )

    torque = float(
        input("Enter applied torque (N-mm): ")
    )

    bending_moment = float(
        input("Enter bending moment (N-mm): ")
    )

    print("\nMaterial Selection")
    print("------------------")

    for number, material_data in materials.items():

        print(
            f"{number}. "
            f"{material_data['name']}"
        )

    material_choice = int(
        input("\nSelect material (1-5): ")
    )

except ValueError:

    print("\nERROR: Please enter numerical values only.")
    exit()

# ============================================================
# VALIDATION
# ============================================================

if outer_diameter <= 0:

    print("\nERROR: Outer diameter must be greater than zero.")
    exit()

if shaft_type == 2:

    if inner_diameter <= 0:

        print("\nERROR: Inner diameter must be greater than zero.")
        exit()

    if inner_diameter >= outer_diameter:

        print(
            "\nERROR: Inner diameter must be smaller "
            "than outer diameter."
        )
        exit()

if length <= 0:

    print("\nERROR: Shaft length must be greater than zero.")
    exit()

if torque < 0:

    print("\nERROR: Torque cannot be negative.")
    exit()

if bending_moment < 0:

    print("\nERROR: Bending moment cannot be negative.")
    exit()

if material_choice not in materials:

    print("\nERROR: Invalid material selection.")
    exit()

# ============================================================
# MATERIAL PROPERTIES
# ============================================================

material = materials[material_choice]

material_name = material["name"]

E = material["E"]

yield_strength = material["yield"]

nu = material["nu"]

density = material["density"]

# Shear modulus
G = E / (2 * (1 + nu))

# ============================================================
# SELECTED SHAFT CROSS-SECTION
# ============================================================

D = outer_diameter
d = inner_diameter

area = (
    math.pi / 4
    * (D**2 - d**2)
)

I = (
    math.pi / 64
    * (D**4 - d**4)
)

J = (
    math.pi / 32
    * (D**4 - d**4)
)

# ============================================================
# SELECTED SHAFT CALCULATIONS
# ============================================================

bending_stress = (
    bending_moment
    * (D / 2)
    / I
)

torsional_stress = (
    torque
    * (D / 2)
    / J
)

von_mises_stress = math.sqrt(
    bending_stress**2
    +
    3 * torsional_stress**2
)

angle_twist_rad = (
    torque
    * length
    /
    (G * J)
)

angle_twist_deg = (
    angle_twist_rad
    * 180
    / math.pi
)

volume_mm3 = area * length

volume_m3 = volume_mm3 * 1e-9

mass_kg = density * volume_m3

factor_of_safety = (
    yield_strength
    /
    von_mises_stress
)

if factor_of_safety >= 1:

    structural_status = "SAFE"

else:

    structural_status = "UNSAFE"

# ============================================================
# SELECTED SHAFT RESULTS
# ============================================================

print("\n====================================================")
print("                  SHAFT ANALYSIS")
print("====================================================")

if shaft_type == 1:

    print("Shaft Type          : Solid")

else:

    print("Shaft Type          : Hollow")

print(f"Outer Diameter      : {D:.2f} mm")

if shaft_type == 2:

    print(f"Inner Diameter      : {d:.2f} mm")

print(f"Shaft Length        : {length:.2f} mm")

print(f"\nMaterial            : {material_name}")

print(f"Young's Modulus     : {E:.0f} MPa")

print(f"Shear Modulus       : {G:.0f} MPa")

print(f"Yield Strength      : {yield_strength:.0f} MPa")

print(f"Density             : {density:.0f} kg/m^3")

print(f"\nCross-sectional Area: {area:.2f} mm^2")

print(f"Area Moment (I)     : {I:.2f} mm^4")

print(f"Polar Moment (J)    : {J:.2f} mm^4")

print(f"Volume              : {volume_mm3:.2f} mm^3")

print(f"Mass                : {mass_kg:.3f} kg")

print(f"\nBending Stress      : {bending_stress:.2f} MPa")

print(
    f"Torsional Shear     : "
    f"{torsional_stress:.2f} MPa"
)

print(
    f"Von Mises Stress    : "
    f"{von_mises_stress:.2f} MPa"
)

print(
    f"Angle of Twist      : "
    f"{angle_twist_deg:.4f} degrees"
)

print(
    f"Factor of Safety    : "
    f"{factor_of_safety:.2f}"
)

print(
    f"Structural Status   : "
    f"{structural_status}"
)

# ============================================================
# SOLID SHAFT REFERENCE CALCULATION
# ============================================================

solid_diameter = D
solid_inner_diameter = 0

solid_area = (
    math.pi / 4
    * solid_diameter**2
)

solid_I = (
    math.pi / 64
    * solid_diameter**4
)

solid_J = (
    math.pi / 32
    * solid_diameter**4
)

solid_bending_stress = (
    bending_moment
    * (solid_diameter / 2)
    / solid_I
)

solid_torsional_stress = (
    torque
    * (solid_diameter / 2)
    / solid_J
)

solid_von_mises = math.sqrt(
    solid_bending_stress**2
    +
    3 * solid_torsional_stress**2
)

solid_angle_rad = (
    torque
    * length
    /
    (G * solid_J)
)

solid_angle_deg = (
    solid_angle_rad
    * 180
    / math.pi
)

solid_volume_mm3 = (
    solid_area
    * length
)

solid_volume_m3 = (
    solid_volume_mm3
    * 1e-9
)

solid_mass = (
    density
    * solid_volume_m3
)

solid_fos = (
    yield_strength
    /
    solid_von_mises
)

# ============================================================
# MASS REDUCTION
# ============================================================

if solid_mass > 0:

    mass_reduction = (
        (solid_mass - mass_kg)
        /
        solid_mass
        * 100
    )

else:

    mass_reduction = 0

# ============================================================
# SOLID VS HOLLOW COMPARISON
# ============================================================

print("\n====================================================")
print("        SOLID vs HOLLOW SHAFT COMPARISON")
print("====================================================")

print(
    f"{'Parameter':<25}"
    f"{'Solid':>15}"
    f"{'Selected':>15}"
)

print("-" * 55)

print(
    f"{'Outer Diameter (mm)':<25}"
    f"{solid_diameter:>15.2f}"
    f"{D:>15.2f}"
)

print(
    f"{'Inner Diameter (mm)':<25}"
    f"{0:>15.2f}"
    f"{d:>15.2f}"
)

print(
    f"{'Mass (kg)':<25}"
    f"{solid_mass:>15.3f}"
    f"{mass_kg:>15.3f}"
)

print(
    f"{'Bending Stress (MPa)':<25}"
    f"{solid_bending_stress:>15.2f}"
    f"{bending_stress:>15.2f}"
)

print(
    f"{'Torsional Shear (MPa)':<25}"
    f"{solid_torsional_stress:>15.2f}"
    f"{torsional_stress:>15.2f}"
)

print(
    f"{'Von Mises (MPa)':<25}"
    f"{solid_von_mises:>15.2f}"
    f"{von_mises_stress:>15.2f}"
)

print(
    f"{'Angle of Twist (deg)':<25}"
    f"{solid_angle_deg:>15.4f}"
    f"{angle_twist_deg:>15.4f}"
)

print(
    f"{'Factor of Safety':<25}"
    f"{solid_fos:>15.2f}"
    f"{factor_of_safety:>15.2f}"
)

print("-" * 55)

if shaft_type == 2:

    print(
        f"{'Mass Reduction':<25}"
        f"{'---':>15}"
        f"{mass_reduction:>14.2f}%"
    )

else:

    print(
        "Mass Reduction      : "
        "Selected shaft is the solid reference."
    )

# ============================================================
# RESULTS FOLDER
# ============================================================

os.makedirs("results", exist_ok=True)

# ============================================================
# STRESS DISTRIBUTION
# ============================================================

outer_radius = D / 2

if shaft_type == 1:

    r = np.linspace(
        0,
        outer_radius,
        300
    )

else:

    inner_radius = d / 2

    r = np.linspace(
        inner_radius,
        outer_radius,
        300
    )

bending_distribution = (
    bending_stress
    * r
    / outer_radius
)

shear_distribution = (
    torsional_stress
    * r
    / outer_radius
)

von_mises_distribution = np.sqrt(
    bending_distribution**2
    +
    3 * shear_distribution**2
)

# ============================================================
# STRESS DISTRIBUTION PLOT
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    r,
    bending_distribution,
    linewidth=2,
    label="Bending Stress"
)

plt.plot(
    r,
    shear_distribution,
    linewidth=2,
    label="Torsional Shear Stress"
)

plt.plot(
    r,
    von_mises_distribution,
    linewidth=2,
    label="Von Mises Stress"
)

plt.xlabel(
    "Radial Position (mm)"
)

plt.ylabel(
    "Stress (MPa)"
)

plt.title(
    "Shaft Stress Distribution"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/shaft_stress_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# SOLID VS HOLLOW COMPARISON GRAPH
# ============================================================

if shaft_type == 2:

    labels = [
        "Mass (kg)",
        "Von Mises (MPa)",
        "FoS"
    ]

    solid_values = [
        solid_mass,
        solid_von_mises,
        solid_fos
    ]

    hollow_values = [
        mass_kg,
        von_mises_stress,
        factor_of_safety
    ]

    x = np.arange(
        len(labels)
    )

    width = 0.35

    plt.figure(
        figsize=(9, 5)
    )

    plt.bar(
        x - width / 2,
        solid_values,
        width,
        label="Solid Shaft"
    )

    plt.bar(
        x + width / 2,
        hollow_values,
        width,
        label="Hollow Shaft"
    )

    plt.xticks(
        x,
        labels
    )

    plt.ylabel(
        "Value"
    )

    plt.title(
        "Solid vs Hollow Shaft Comparison"
    )

    plt.grid(
        axis="y"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "results/solid_vs_hollow_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

# ============================================================
# COMPLETION
# ============================================================

print("\n====================================================")
print("Shaft analysis complete.")
print("Graphs saved in the 'results' folder.")
print("====================================================")