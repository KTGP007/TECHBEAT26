import os
import subprocess
import venv

VENV_NAME = "TECHBEATS26"

def clear_terminal():
    subprocess.run("cls", shell=True)  # For Windows

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    DARK_PURPLE = '\033[0;35m' 
    PURPLE = '\033[35m'
    ORANGE = '\033[33m'

REMOVE_DEPENDENCIES = [
    "scikit-learn",
    "seaborn"
]

REQUIREMENTS = [
    "matplotlib",
    "numpy",
    "pandas"
]

def run(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass


clear_terminal()

print(f""""
{colors.GREEN+" COEP's AI & DS Dept. -AI Model Building challenge"+colors.RESET}"""+
f"""\n"""+ colors.CYAN+""" _________________ _____  _______ __________
/_  __/ __/ ___/ // / _ )/ __/ _ /_  __/ __/
 / / / _// /__/ _  / _  / _// __ |/ / _\ \  
/_/ /___/\___/_//_/____/___/_/ |_/_/ /___/  

=========================================
TECHBEATS26 AI CONTEST RULES
========================================
"""

+ colors.RESET+
f'1. Do {colors.RED+"NOT"+colors.RESET} use {colors.YELLOW+"scikit-learn"+colors.RESET} or any {colors.YELLOW+"ML libraries."+ colors.RESET}\n'
f'2. Only Python standard {colors.GREEN+"logic, numpy, and pandas allowed."+colors.RESET}\n'
f'3. {colors.RED+"Do not copy code"+colors.RESET} from other participants.\n'
f'4. Organizers may ask participants to {colors.DARK_PURPLE+"explain their code."+colors.RESET}\n'
f'5. Violation of rules may lead to {colors.RED+"disqualification."+colors.RESET}\n'
f'6. If setup fails please contact the {colors.ORANGE+"contest organizers."+colors.RESET}\n'
f'Press {colors.GREEN+"ENTER"+colors.RESET} to accept the rules and continue setup.'
+ colors.RESET
)

input()

# ---------------------------------------------
# 1. CREATE VIRTUAL ENVIRONMENT
# ---------------------------------------------
if not os.path.exists(VENV_NAME):
    print("[1/5] Creating virtual environment...")
    venv.EnvBuilder(with_pip=True).create(VENV_NAME)
    print(colors.GREEN+"✅ Virtual environment created\n"+colors.RESET)
else:
    print(colors.GREEN+"[1/5] Virtual environment already exists ✅\n"+colors.RESET)

python_path = os.path.join(VENV_NAME, "Scripts", "python.exe")

# ---------------------------------------------
# 2. UPGRADE PIP
# ---------------------------------------------
print("[2/5] Upgrading pip...")
run(f'"{python_path}" -m pip install --upgrade pip')
print(colors.GREEN+"✅ pip upgraded\n"+colors.RESET)

# ---------------------------------------------
# 3. REMOVE RESTRICTED LIBRARIES
# ---------------------------------------------
print("[3/5] Removing restricted libraries...")
for pkg in REMOVE_DEPENDENCIES:
    run(f'"{python_path}" -m pip uninstall -y {pkg}')
    print(colors.YELLOW+f"✅ Removed {pkg} (if installed)"+colors.RESET)

# ---------------------------------------------
# 4. INSTALL REQUIRED LIBRARIES
# ---------------------------------------------
print("[4/5] Installing required libraries...")
for pkg in REQUIREMENTS:
    run(f'"{python_path}" -m pip install {pkg}')
    print(colors.GREEN+f"✅ Installed {pkg}"+colors.RESET)

# ---------------------------------------------
# 5. CREATE CONTEST FILES
# ---------------------------------------------
print(colors.GREEN+"[5/5] Creating contest files...\n"+colors.RESET)

files = {
    "model.py": """# ==========================================
# TECHBEATS26 - MODEL FILE !!! DO NOT REMOVE X_VALUES, Y_VALUES, m, c, data.graph(m,c)
# ==========================================
import data 
m,c = None,None
X_VALUES = data.X_VALUES
Y_VALUES = data.Y_VALUES


# ==========================================
# CODE HERE
# ==========================================


data.graph(m,c)
""",
    "data.py": """# ==========================================
# TECHBEATS26 - DATA FILE !!! DO NOT DELETE ANYTHING HERE !!!
# ==========================================
import matplotlib.pyplot as plt
import numpy as np

Y_VALUES = [7, 11, 15, 19, 18, 22, 26, 30, 34, 33, 37, 41, 45, 49, 48, 52, 56, 60, 64, 63, 67, 71, 75, 79, 78, 82, 86, 90, 94, 93, 97, 101, 105, 109, 108, 112, 116, 120, 124, 123, 127, 131, 135, 139, 138, 142, 146, 150, 154, 153, 157, 161, 165, 169, 168, 172, 176, 180, 184, 183, 187, 191, 195, 199, 198, 202, 206, 210, 214, 213, 217, 221, 225, 229, 228, 232, 236, 240, 244, 243, 247, 251, 255, 259, 258, 262, 266, 270, 274, 273, 277, 281, 285, 289, 288, 292, 296, 300, 304, 303, 307, 311, 315, 319, 318, 322, 326, 330, 334, 333, 337, 341, 345, 349, 348, 352, 356, 360, 364, 363, 367, 371, 375, 379, 378, 382, 386, 390, 394, 393, 397, 401, 405, 409, 408, 412, 416, 420, 424, 423, 427, 431, 435, 439, 438, 442, 446, 450, 454, 453, 457, 461, 465, 469, 468, 472, 476, 480, 484, 483, 487, 491, 495, 499, 498, 502, 506, 510, 514, 513, 517, 521, 525, 529, 528, 532, 536, 540, 544, 543, 547, 551, 555, 559, 558, 562, 566, 570, 574, 573, 577, 581, 585, 589, 588, 592, 596, 600, 604, 603]
X_VALUES = list(range(1,201))
x = 6
y = 120

class colors:
    RED = '\033[91m'
    RESET = '\033[0m'

# graphs value expects m and c
def graph (m=None, c=None):

    plt.figure(figsize=(10, 6))
    plt.scatter(X_VALUES, Y_VALUES, color='blue', label='Actual Data Points')
    if m is None or c is None:
        print(colors.RED+"Warning: m: slope and c: y-intercept are not given. Showing trend only (ignoring regression line and estimates)."+colors.RESET)
    else:
        try:
            target_x = x
            target_y = y
            estimated_y = m * target_x + c
            estimated_x = (target_y - c) / m
            line_x = np.linspace(min(X_VALUES) - 5, max(X_VALUES) + 5, 100)
            line_y = m * line_x + c
            plt.plot(line_x, line_y, color='red',
                     label=f'Regression Line: y = {m}x + {c}')
            plt.scatter(target_x, estimated_y, color='black',
                        s=100, zorder=5,
                        label=f'Est. Y at X={target_x}')
            plt.scatter(estimated_x, target_y, color='cyan',
                        s=100, zorder=5,
                        label=f'Est. X at Y={target_y}')
        except Exception as e:
            print(colors.RED+f"Regression plotting skipped due to error: {e}"+colors.RESET)
    plt.title("Linear Regression Visualization")
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()"""
}

for name, content in files.items():
    if not os.path.exists(name):
        with open(name, "w") as f:
            f.write(content)
        print(colors.GREEN+f"✅ Created {name}"+colors.RESET)
    else:
        print(colors.GREEN+f"✅ {name} already exists"+colors.RESET)

print(colors.GREEN+"\n🎉 SETUP COMPLETE\n"+colors.RESET)
print(colors.DARK_PURPLE+"""  _________  ____  ___    __   __  _________ __  __
 / ___/ __ \/ __ \/ _ \  / /  / / / / ___/ //_/ / /
/ (_ / /_/ / /_/ / // / / /__/ /_/ / /__/ ,<   /_/ 
\___/\____/\____/____/ /____/\____/\___/_/|_| (_)"""+colors.RESET)

print("\nStudents work ONLY in:")
print(colors.GREEN+" - model.py"+colors.RESET)

# ---------------------------------------------
# 6. Activate Environment
# ---------------------------------------------

activate_bat = os.path.join(VENV_NAME, "Scripts", "activate.bat")
activate_ps1 = os.path.join(VENV_NAME, "Scripts", "Activate.ps1")

def detect_shell():
    if "PSModulePath" in os.environ:
        return "powershell"
    elif os.environ.get("COMSPEC", "").lower().endswith("cmd.exe"):
        return "cmd"
    else:
        return "unknown"

shell_type = detect_shell()

print(f"\nDetected shell: {shell_type}")

try:
    if shell_type == "powershell":
        subprocess.run(
            ["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", activate_ps1],
            check=False
        )

    elif shell_type == "cmd":
        subprocess.run(
            ["cmd", "/k", activate_bat],
            check=False
        )

    else:
        print("⚠ Unknown shell. Attempting CMD fallback...")
        subprocess.run(
            ["cmd", "/k", activate_bat],
            check=False
        )

except Exception as e:
    print(colors.RED+"❌ Failed to activate environment:"+colors.RESET, e)


User_venv = f"{VENV_NAME}\\Scripts\\activate"

print("\nif Enviroment Activation Process fails then, run this here")
print(colors.GREEN+User_venv+colors.RESET)


clear_terminal()
