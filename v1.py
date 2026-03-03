import os
import subprocess
import venv

VENV_NAME = "TECHBEAT26"

# ---------------------------------------------
# DEPENDENCIES (Minimal)
# ---------------------------------------------
REMOVE_DEPENDENCIES = [
    "matplotlib",
    "scikit-learn",
    "seaborn"
]

REQUIREMENTS = [
    "numpy",
    "pandas"
]

def run(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        pass

print("\n=== TECHBEAT26 AI CONTEST SETUP ===\n")

# ---------------------------------------------
# 1. CREATE VIRTUAL ENVIRONMENT
# ---------------------------------------------
if not os.path.exists(VENV_NAME):
    print("[1/5] Creating virtual environment...")
    venv.EnvBuilder(with_pip=True).create(VENV_NAME)
    print("✅ Virtual environment created\n")
else:
    print("[1/5] Virtual environment already exists ✅\n")

python_path = os.path.join(VENV_NAME, "Scripts", "python.exe")

# ---------------------------------------------
# 2. UPGRADE PIP
# ---------------------------------------------
print("[2/5] Upgrading pip...")
run(f'"{python_path}" -m pip install --upgrade pip')
print("✅ pip upgraded\n")

# ---------------------------------------------
# 3. REMOVE RESTRICTED LIBRARIES
# ---------------------------------------------
print("[3/5] Removing restricted libraries...")
for pkg in REMOVE_DEPENDENCIES:
    run(f'"{python_path}" -m pip uninstall -y {pkg}')
    print(f"✅ Removed {pkg} (if installed)")

# ---------------------------------------------
# 4. INSTALL REQUIRED LIBRARIES
# ---------------------------------------------
print("[4/5] Installing required libraries...")
for pkg in REQUIREMENTS:
    run(f'"{python_path}" -m pip install {pkg}')
    print(f"✅ Installed {pkg}")

# ---------------------------------------------
# 5. CREATE CONTEST FILES
# ---------------------------------------------
print("[5/5] Creating contest files...\n")

files = {

    "model.py": """# ==========================================
# TECHBEAT26 - MODEL FILE
# ==========================================

def train_model():
    
    # ==========================================
    # ADD YOUR CODE HERE
    # ==========================================
    
    pass
""",

    "data.py": """# ==========================================
# TECHBEAT26 - DATA FILE
# ==========================================

# ==========================================
# INSERT 200 X VALUES BELOW
# ==========================================
X_VALUES = [
    # ADD YOUR 200 X VALUES HERE
]

# ==========================================
# INSERT 200 Y VALUES BELOW
# ==========================================
Y_VALUES = [
    # ADD YOUR 200 Y VALUES HERE
]
""",

    "main.py": """from model import train_model

if __name__ == "__main__":
    train_model()
"""
}

for name, content in files.items():
    if not os.path.exists(name):
        with open(name, "w") as f:
            f.write(content)
        print(f"✅ Created {name}")
    else:
        print(f"✅ {name} already exists")

print("\n🎉 SETUP COMPLETE\n")
print(f"Activate environment:")
# ---------------------------------------------
# 6. Activte Enviroment
# ---------------------------------------------

activate_cmd = os.path.join(VENV_NAME, "Scripts", "activate")

# Run activation command (Windows CMD)
subprocess.call(activate_cmd, shell=True)

print("\nif Enviroment Activation Process failed then, run this here")
print(f"   {VENV_NAME}\\Scripts\\activate")


print("\nStudents work ONLY in:")
print(" - model.py")