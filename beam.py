import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# BEAM STRESS ANALYSIS CALCULATOR
# ============================================================

print("====================================================")
print("          BEAM STRESS ANALYSIS CALCULATOR")
print("====================================================")

# ============================================================
# MATERIAL DATABASE
# ============================================================

materials = {
    1: {
        "name": "Structural Steel",
        "E": 200000,
        "yield": 250
    },
    2: {
        "name": "AISI 4140 Steel",
        "E": 205000,
        "yield": 655
    },
    3: {
        "name": "Aluminium 6061-T6",
        "E": 68900,
        "yield": 276
    },
    4: {
        "name": "Aluminium 7075-T6",
        "E": 71700,
        "yield": 503
    },
    5: {
        "name": "Stainless Steel 304",
        "E": 193000,
        "yield": 215
    }
}

print("\nAvailable Materials")
print("-------------------")

for number, material in materials.items():
    print(
        f"{number}. {material['name']} "
        f"(E = {material['E']} MPa, "
        f"Yield = {material['yield']} MPa)"
    )

# ============================================================
# INPUTS
# ============================================================

try:

    length = float(input("\nEnter beam length (mm): "))
    width = float(input("Enter beam width (mm): "))
    height = float(input("Enter beam height (mm): "))

    load = float(input("Enter point load (N): "))

    load_position = float(
        input("Enter load position from left support (mm): ")
    )

    material_choice = int(
        input("Select material (1-5): ")
    )

except ValueError:

    print("\nERROR: Please enter numerical values only.")
    exit()

# ============================================================
# INPUT VALIDATION
# ============================================================

if length <= 0:
    print("\nERROR: Beam length must be greater than zero.")
    exit()

if width <= 0 or height <= 0:
    print("\nERROR: Beam dimensions must be greater than zero.")
    exit()

if load <= 0:
    print("\nERROR: Load must be greater than zero.")
    exit()

if load_position <= 0 or load_position >= length:
    print(
        "\nERROR: Load position must be between "
        "the two supports."
    )
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

# ============================================================
# BEAM GEOMETRY
# ============================================================

I = (width * height**3) / 12

c = height / 2

# Distance from load to supports

a = load_position
b = length - load_position

# ============================================================
# SUPPORT REACTIONS
# ============================================================

reaction_A = (load * b) / length
reaction_B = (load * a) / length

# ============================================================
# POSITION ARRAY
# ============================================================

x = np.linspace(0, length, 500)

# ============================================================
# SHEAR FORCE
# ============================================================

shear_force = np.where(
    x < load_position,
    reaction_A,
    reaction_A - load
)

# ============================================================
# BENDING MOMENT
# ============================================================

bending_moment = np.where(
    x <= load_position,
    reaction_A * x,
    reaction_B * (length - x)
)

# Maximum bending moment occurs at load position

M_max = reaction_A * a

# ============================================================
# BENDING STRESS
# ============================================================

stress = (M_max * c) / I

# ============================================================
# FACTOR OF SAFETY
# ============================================================

factor_of_safety = yield_strength / stress

# ============================================================
# DEFLECTION
# ============================================================

deflection = np.zeros_like(x)

# Left side of load

left = x <= a

deflection[left] = (
    load * b * x[left]
    /
    (6 * length * E * I)
    *
    (
        length**2
        - b**2
        - x[left]**2
    )
)

# Right side of load

right = x >= a

deflection[right] = (
    load * a * (length - x[right])
    /
    (6 * length * E * I)
    *
    (
        length**2
        - a**2
        - (length - x[right])**2
    )
)

# ============================================================
# MAXIMUM DEFLECTION
# ============================================================

max_deflection_index = np.argmax(
    np.abs(deflection)
)

max_deflection = abs(
    deflection[max_deflection_index]
)

max_deflection_position = (
    x[max_deflection_index]
)

# ============================================================
# RESULTS
# ============================================================

print("\n====================================================")
print("                  ANALYSIS RESULTS")
print("====================================================")

print(f"Material            : {material_name}")

print(f"Young's Modulus     : {E:.0f} MPa")
print(f"Yield Strength      : {yield_strength:.0f} MPa")

print(f"\nReaction at A       : {reaction_A:.2f} N")
print(f"Reaction at B       : {reaction_B:.2f} N")

print(f"\nSecond Moment (I)   : {I:.2f} mm^4")

print(f"Maximum Moment      : {M_max:.2f} N-mm")

print(f"Bending Stress      : {stress:.2f} MPa")

print(
    f"Maximum Deflection  : "
    f"{max_deflection:.4f} mm"
)

print(
    f"Deflection Position : "
    f"{max_deflection_position:.2f} mm"
)

print(f"Factor of Safety    : {factor_of_safety:.2f}")

if factor_of_safety >= 1:

    print("Structural Status   : SAFE")

else:

    print("Structural Status   : UNSAFE")

# ============================================================
# RESULTS FOLDER
# ============================================================

os.makedirs("results", exist_ok=True)

# ============================================================
# SHEAR FORCE DIAGRAM
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    x,
    shear_force,
    linewidth=2
)

plt.axhline(
    0,
    linewidth=1
)

plt.axvline(
    load_position,
    linestyle="--",
    linewidth=1
)

plt.scatter(
    [load_position],
    [reaction_A - load],
    s=50
)

plt.text(
    load_position + length * 0.02,
    reaction_A + 10,
    f"Load = {load:.0f} N"
)

plt.xlabel("Beam Position (mm)")
plt.ylabel("Shear Force (N)")
plt.title("Shear Force Diagram")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "results/shear_force_diagram.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# BENDING MOMENT DIAGRAM
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    x,
    bending_moment,
    linewidth=2
)

plt.axhline(
    0,
    linewidth=1
)

plt.axvline(
    load_position,
    linestyle="--",
    linewidth=1
)

plt.scatter(
    [load_position],
    [M_max],
    s=50
)

plt.text(
    load_position + length * 0.02,
    M_max,
    f"{M_max:.0f} N-mm"
)

plt.xlabel("Beam Position (mm)")
plt.ylabel("Bending Moment (N-mm)")
plt.title("Bending Moment Diagram")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "results/bending_moment_diagram.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# DEFLECTION CURVE
# ============================================================

plt.figure(figsize=(9, 5))

plt.plot(
    x,
    deflection,
    linewidth=2
)

plt.axhline(
    0,
    linewidth=1
)

plt.scatter(
    [max_deflection_position],
    [deflection[max_deflection_index]],
    s=60
)

plt.text(
    max_deflection_position + length * 0.02,
    deflection[max_deflection_index],
    f"{max_deflection:.4f} mm"
)

plt.xlabel("Beam Position (mm)")
plt.ylabel("Deflection (mm)")
plt.title("Beam Deflection Curve")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "results/beam_deflection.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n====================================================")
print("Analysis complete.")
print("Graphs saved in the 'results' folder.")
print("====================================================")