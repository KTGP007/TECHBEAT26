# 🎓 TECHBEAT26 — Complete Student Guide

> **COEP AI & DS Dept. — AI Model Building Challenge 2026**
> Script: `v2.py` | Language: Python

---

## 📖 Table of Contents

1. [What is this Script?](#1--what-is-this-script)
2. [Prerequisites — What You Need Before Starting](#2--prerequisites)
3. [Setting Up VS Code (First Time)](#3--setting-up-vs-code)
4. [Opening the Project Folder](#4--opening-the-project-folder)
5. [Understanding the Terminal](#5--understanding-the-terminal)
6. [Running the Script (`v2.py`)](#6--running-the-script)
7. [What Happens When You Run It — Step by Step](#7--what-happens-when-you-run-it)
8. [After Setup — Writing Your Code](#8--after-setup--writing-your-code)
9. [Running Your Solution](#9--running-your-solution)
10. [Useful Commands Cheat Sheet](#10--useful-commands-cheat-sheet)
11. [Troubleshooting Common Errors](#11--troubleshooting)
12. [Script Code Explanation (For Curious Students)](#12--code-explanation)

---

## 1. 🤔 What is this Script?

`v2.py` is the **official contest setup script** for TECHBEAT26. It does the following automatically:

| Step | What It Does |
|------|-------------|
| 🎨 Shows animated welcome screen | Greeting based on time of day |
| 📋 Displays contest rules | 7 rules you must follow |
| 🏆 Explains the 3 rounds | R1.1, R1.2, and R2 |
| 🐍 Creates a virtual environment | Named `TECHBEATS26` |
| 📦 Installs required libraries | numpy, pandas, matplotlib, scikit-learn |
| 🚫 Removes banned libraries | tensorflow, keras, torch, etc. |
| 📝 Generates your starter files | `model.py` and `data.py` |

**You run this ONCE at the start of the contest.** After that, you only work on `model.py`.

---

## 2. ✅ Prerequisites

Before you begin, make sure you have:

| Requirement | How to Check |
|-------------|-------------|
| **Python 3.8+** installed | Open terminal → type `python --version` |
| **VS Code** installed | Search "Visual Studio Code" in Start Menu |
| **The script file** `v2.py` | Should be given by the organizers |

### Installing Python (if not installed)

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3 for Windows
3. **⚠️ IMPORTANT:** During installation, check ✅ **"Add Python to PATH"**
4. Click "Install Now"
5. Verify by opening Command Prompt and typing:
   ```
   python --version
   ```
   You should see something like `Python 3.12.x`

### Installing VS Code (if not installed)

1. Go to [code.visualstudio.com](https://code.visualstudio.com/)
2. Download the Windows installer
3. Install with default settings
4. **Recommended:** Install the **Python extension** (see next section)

---

## 3. 🛠️ Setting Up VS Code

### Step 1: Install the Python Extension

1. Open VS Code
2. Click the **Extensions** icon on the left sidebar (it looks like 4 squares)
   - Or press `Ctrl + Shift + X`
3. Search for **"Python"**
4. Click **Install** on the one by **Microsoft** (it will be the first result)

### Step 2: Choose Your Python Interpreter

1. Press `Ctrl + Shift + P` (opens the Command Palette)
2. Type **"Python: Select Interpreter"**
3. Select your installed Python version (e.g., `Python 3.12.x`)

---

## 4. 📂 Opening the Project Folder

### Method 1: From VS Code

1. Open VS Code
2. Go to **File → Open Folder**
3. Navigate to the folder where `v2.py` is saved
4. Click **Select Folder**

### Method 2: From File Explorer

1. Navigate to the folder containing `v2.py` in File Explorer
2. Right-click in the folder
3. Select **"Open with Code"** (if available)

### Method 3: From Terminal

```powershell
cd C:\path\to\your\folder
code .
```

> [!IMPORTANT]
> **Always open the FOLDER, not just the file.** This ensures the terminal starts in the correct directory.

---

## 5. 💻 Understanding the Terminal

The terminal is a text-based window where you type commands to run programs.

### Opening the Terminal in VS Code

- Press `` Ctrl + ` `` (backtick key, usually below `Esc`)
- Or go to **Terminal → New Terminal** from the menu bar

### Types of Terminal

| Terminal | Icon/Label | When to Use |
|----------|-----------|-------------|
| **PowerShell** | `PS C:\..>` | Default on Windows, works fine |
| **Command Prompt** | `C:\..>` | Also works |

### Essential Terminal Commands

| Command | What It Does | Example |
|---------|-------------|---------|
| `cd folder_name` | Go inside a folder | `cd Desktop` |
| `cd ..` | Go back one folder | `cd ..` |
| `dir` | List files in current folder | `dir` |
| `cls` | Clear the screen | `cls` |
| `python file.py` | Run a Python script | `python v2.py` |

> [!TIP]
> You can type the **first few letters** of a file name and press **Tab** to auto-complete it.

---

## 6. 🚀 Running the Script

### Step-by-Step

1. **Open VS Code** with the project folder (see Section 4)
2. **Open the Terminal** (press `` Ctrl + ` ``)
3. **Verify you're in the right folder.** The terminal should show the path where `v2.py` is located. Type:
   ```powershell
   dir
   ```
   You should see `v2.py` in the list.

4. **Run the script:**
   ```powershell
   python v2.py
   ```

5. **Follow the on-screen instructions** — just press **Enter** when prompted.

> [!CAUTION]
> **Do NOT close the terminal** while the script is running. It needs time to create the virtual environment and install packages.

---

## 7. 📺 What Happens When You Run It

The script goes through several animated screens:

### Screen 1 — Greeting 👋
- Shows a time-based greeting (Good Morning / Afternoon / Evening / Night)
- Displays system info (Python version, OS, time)
- **Action:** Press `Enter` to continue

### Screen 2 — Contest Rules 📋
- Shows the TECHBEATS banner animation
- Displays 7 rules:
  1. Individual participation only
  2. Use Python only
  3. No copying code
  4. Don't modify the dataset
  5. Code must run successfully
  6. Be ready for viva
  7. Rule violations → disqualification
- **Action:** Press `Enter` to continue

### Screen 3 — Round Structure 🏆
- Shows all 3 rounds:

| Round | Description | Notes |
|-------|------------|-------|
| **R1.1** | Data Cleaning | Clean a noisy dataset |
| **R1.2** | sklearn Linear Regression | Use scikit-learn |
| **R2** | Manual Linear Regression | ⚠️ sklearn NOT allowed |
| **R3** | Viva | Oral explanation of your code |

- **Action:** Press `Enter` to accept rules and begin setup

### Setup Phase ⚙️ (Automatic — just watch!)
- **Step 1/5:** Creates virtual environment (`TECHBEATS26`)
- **Step 2/5:** Upgrades pip
- **Step 3/5:** Removes restricted libraries (tensorflow, keras, torch, etc.)
- **Step 4/5:** Installs required packages (numpy, pandas, matplotlib, scikit-learn)

### Round Selection 🎯
- You choose which round to attempt: **1**, **2**, or **3**
- Confirm with **Y**

### Step 5/5 — Files Created 📝
- `model.py` — **Your working file** (write your code here)
- `data.py` — **Data file** (DO NOT EDIT THIS!)

### Final Screen ✅
- Shows a summary of everything that was set up
- Displays "GOOD LUCK!" animation
- Activates the virtual environment automatically

---

## 8. ✍️ After Setup — Writing Your Code

### What files were created?

| File | Purpose | Can You Edit? |
|------|---------|--------------|
| `model.py` | Your solution goes here | ✅ YES — write your code here |
| `data.py` | Contains the dataset & grading logic | ❌ NO — do not touch this! |

### Opening `model.py`

1. In VS Code, click on `model.py` in the **Explorer panel** (left sidebar)
2. Or press `Ctrl + P` and type `model.py`

### What's inside `model.py`?

Depending on the round you chose:

**Round 1.1 (Data Cleaning):**
```python
import data
RAW = data.RAW        # The noisy dataset
cleaned = []          # Put your cleaned data here

# YOUR CODE HERE — clean the data!

data.graph(cleaned)   # DO NOT REMOVE — this grades your work
```

**Round 1.2 (sklearn Linear Regression):**
```python
import data
import numpy as np
from sklearn.linear_model import LinearRegression
m, c = None, None     # Store slope (m) and intercept (c)

# YOUR CODE HERE — train a model!

data.graph(m, c)      # DO NOT REMOVE — this grades your work
```

**Round 2 (Manual Linear Regression):**
```python
import data
m, c = None, None
X_VALUES = data.X_VALUES
Y_VALUES = data.Y_VALUES

# YOUR CODE HERE — calculate m and c WITHOUT sklearn!

data.graph(m, c)      # DO NOT REMOVE — this grades your work
```

> [!WARNING]
> **Never delete the `data.graph(...)` line at the bottom!** This is what checks and grades your solution.

---

## 9. ▶️ Running Your Solution

After writing your code in `model.py`:

### Method 1: From Terminal
```powershell
python model.py
```

### Method 2: Using the Test Command (Recommended)
```powershell
python v2.py --test
```
This does 3 things automatically:
1. ✅ Checks if `data.py` is untampered
2. 🔄 Restores `data.py` if it was modified
3. ▶️ Runs your `model.py`

### Other Useful Flags

| Command | What It Does |
|---------|-------------|
| `python v2.py --guard` | Check if `data.py` is intact |
| `python v2.py --restore` | Restore `data.py` to original if tampered |
| `python v2.py --test` | Guard + Restore + Run model.py |

### Understanding the Output

When you run your code, you'll see a **results panel**:

- ✔ **PERFECT** — Your solution is correct! 🎉
- ≈ **ACCEPTABLE** — Close, but needs improvement
- ✘ **INCORRECT** — Check your logic
- 🚨 **CHEAT DETECTED** — You used a banned library in Round 2

A **matplotlib graph** will also pop up showing your results visually.

---

## 10. 📋 Useful Commands Cheat Sheet

| What You Want To Do | Command |
|---------------------|---------|
| Run the setup script | `python v2.py` |
| Run your solution | `python model.py` |
| Test with integrity check | `python v2.py --test` |
| Check if data.py is intact | `python v2.py --guard` |
| Restore data.py | `python v2.py --restore` |
| Check Python version | `python --version` |
| List files in folder | `dir` |
| Clear terminal | `cls` |
| Open new terminal | `` Ctrl + ` `` |
| Open Command Palette | `Ctrl + Shift + P` |
| Quick file search | `Ctrl + P` |
| Save file | `Ctrl + S` |
| Undo | `Ctrl + Z` |
| Run selection in terminal | Select code → `Shift + Enter` |

---

## 11. 🔧 Troubleshooting

### ❌ `'python' is not recognized as an internal or external command`

**Problem:** Python is not in your system PATH.

**Fix:**
1. Reinstall Python from [python.org](https://www.python.org/downloads/)
2. **Check ✅ "Add Python to PATH"** during installation
3. Restart VS Code after installing

**Alternative:** Try using `python3` instead of `python`:
```powershell
python3 v2.py
```

---

### ❌ `ModuleNotFoundError: No module named 'venv'`

**Fix:** Install the full Python distribution (not a minimal one). Re-download from python.org.

---

### ❌ Terminal shows wrong directory

**Fix:** Make sure you opened the **folder** in VS Code, not just the file. Go to **File → Open Folder** and select the folder containing `v2.py`.

---

### ❌ `PermissionError` or `Access Denied`

**Fix:** Try running VS Code as Administrator:
1. Right-click VS Code in Start Menu
2. Select "Run as administrator"

---

### ❌ Weird characters showing (like `[92m` instead of green text)

**Problem:** Your terminal doesn't support ANSI colors.

**Fix:** Use the **VS Code integrated terminal** instead of the old Command Prompt. The VS Code terminal handles colors correctly.

---

### ❌ `data.py has been modified or corrupted`

**Fix:** Run the restore command:
```powershell
python v2.py --restore
```

---

### ❌ Graph window doesn't appear

**Fix:** Make sure `matplotlib` is installed. Run:
```powershell
pip install matplotlib
```
Or re-run the setup script: `python v2.py`

---

## 12. 🔍 Code Explanation (What Each Section of `v2.py` Does)

For students who want to understand the script's inner workings:

### High-Level Architecture

```
v2.py
├── CONFIG              → Virtual env name, allowed/banned packages
├── ANSI STYLES (class S) → Color codes for terminal animations
├── TEXT EFFECTS         → typewrite(), matrix_drop(), gradient_bar()
├── BOXES & PANELS       → fancy_box(), info_panel(), step_ok/fail()
├── ASCII ART            → TECHBEATS banner, greeting text art
├── SCREENS              → screen_greeting(), screen_rules(), screen_rounds()
├── SETUP LOGIC          → venv creation, pip install/uninstall
├── FILE TEMPLATES       → model.py & data.py content for each round
├── INTEGRITY GUARD      → SHA-256 hash check on data.py
└── MAIN                 → Orchestrates everything in sequence
```

### Key Components Explained

| Section | Lines | Purpose |
|---------|-------|---------|
| **Config** | 30–47 | Defines the venv name, packages to remove, and packages to install |
| **Class S** | 54–76 | ANSI escape codes for colored/styled terminal output |
| **Text Effects** | 131–228 | Fancy animations: typewrite, matrix rain, progress bars, spinners |
| **Screens** | 463–560 | The 3 interactive screens (greeting, rules, rounds) |
| **Backup** | 566–585 | Moves existing `model.py`/`data.py` to a `previous_attempts/` folder |
| **Round Selection** | 592–611 | Menu for choosing Round 1.1, 1.2, or 2 |
| **File Templates** | 618–1101 | The actual Python code that gets written into `model.py` and `data.py` |
| **Integrity Guard** | 1167–1226 | Uses SHA-256 hashing to detect if a student tampered with `data.py` |
| **Main Flow** | 1232–1359 | Command-line argument parsing + the full setup sequence |

### Anti-Cheat System

The script has a built-in anti-cheat mechanism:
- **data.py** contains a unique seed generated from your computer's MAC address + hostname
- This means every student gets a **unique dataset** — you can't copy answers from others
- In **Round 2**, the `data.py` file secretly scans your `model.py` for banned terms like `sklearn`, `polyfit`, `scipy`, etc.
- If detected → 🚨 **CHEAT DETECTED** is shown instead of your grade

### Hidden Feature: Skip Setup

If you've already run the setup before and just want to switch rounds, you can type **`s`** (lowercase) at any "Press ENTER" prompt to skip the setup and go directly to round selection.

---

## 🏁 Quick Start Summary

```
1. Open VS Code
2. Open the folder containing v2.py  (File → Open Folder)
3. Open Terminal                      (Ctrl + `)
4. Run:  python v2.py
5. Follow the screens → Press Enter → Pick your round
6. Open model.py → Write your solution
7. Run:  python model.py
8. Check your grade → Fix if needed → Repeat step 7
9. Call the organizer when you're done!
```

---

> **Good luck! 🍀 May the best coder win!**
>
> — TECHBEAT26 Organizing Team
