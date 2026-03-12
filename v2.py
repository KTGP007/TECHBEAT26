#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║  TECHBEAT26 — Contest Setup                              ║
║  COEP AI & DS Dept. — AI Model Building Challenge 2026   ║
║  v1.py  (final build)                                    ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import subprocess
import venv
import shutil
import random
import platform
from datetime import datetime

# ─── UTF-8 on Windows ───────────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


# ══════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════

VENV_NAME = "TECHBEATS26"

REMOVE_DEPENDENCIES = ["seaborn"]

REQUIREMENTS = [
    "numpy",
    "pandas",
    "matplotlib",
    "scikit-learn",
]
class S:
    """ANSI style codes."""
    # Foreground
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"
    # Decorations
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    UNDER   = "\033[4m"
    BLINK   = "\033[5m"
    RESET   = "\033[0m"
    # Cursor helpers
    HIDE    = "\033[?25l"
    SHOW    = "\033[?25h"
    UP      = "\033[1A"
    CLEAR_LINE = "\033[2K"

ROUND_LABELS = {
    "1": f"Round 1: {S.GREEN}1.1{S.RESET} — Data Cleaning (Noisy Dataset)",
    "2": f"Round 1: {S.GREEN}1.2{S.RESET} — sklearn Linear Regression",
    "3": "Round 2 — Manual Linear Regression (sklearn not allowed here)",
}


# ══════════════════════════════════════════════════════
#  ANSI COLORS & STYLES
# ══════════════════════════════════════════════════════


# Palette used for cycling effects
PALETTE = [S.CYAN, S.GREEN, S.YELLOW, S.MAGENTA, S.BLUE, S.RED]

# Decorative characters
SPARKS   = ["✦", "✧", "★", "☆", "✶", "✴", "❖", "◈", "⟡", "⋆"]
BLOCKS   = ["░", "▒", "▓", "█"]
SPINNERS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
DOTS     = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]


# ══════════════════════════════════════════════════════
#  LOW-LEVEL UTILITIES
# ══════════════════════════════════════════════════════

def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)


def move_up(n=1):
    sys.stdout.write(f"\033[{n}A")


def run_silent(cmd):
    try:
        subprocess.run(
            cmd, shell=True, check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


# ══════════════════════════════════════════════════════
#  TEXT EFFECTS
# ══════════════════════════════════════════════════════

def typewrite(text, delay=0.018, color=""):
    """Classic typewriter with optional color."""
    for ch in text:
        sys.stdout.write(color + ch + S.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def typewrite_fast(text, color=""):
    """Instant styled print (no animation)."""
    print(color + text + S.RESET)


def sweep_reveal(text, color=S.CYAN, chunk=4, delay=0.003):
    """Reveal text left-to-right in chunks — looks like a scanner."""
    for j in range(0, len(text), chunk):
        sys.stdout.write(f"\r{S.BOLD}{color}{text[:j+chunk]}{S.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def matrix_drop(width=60, rows=6, delay=0.03):
    """Quick Matrix-style digit rain effect for transitions."""
    chars = "01アイウエオカキクケコサシスセソ"
    sys.stdout.write(S.HIDE)
    for _ in range(rows):
        line = "  "
        for __ in range(width):
            ch = random.choice(chars)
            shade = random.choice([S.GREEN, S.DIM + S.GREEN, S.CYAN])
            line += shade + ch + S.RESET
        print(line)
        time.sleep(delay)
    sys.stdout.write(S.SHOW)


def sparkle_line(width=30, color=S.YELLOW):
    """Print a decorative sparkle border."""
    line = "  " + " ".join(random.choice(SPARKS) for _ in range(width))
    print(color + S.BOLD + line + S.RESET)


def gradient_bar(filled, total, width=35):
    """Colored progress bar with gradient fill."""
    ratio = filled / total if total else 1
    done = int(width * ratio)
    bar = ""
    for i in range(width):
        if i < done:
            stage = i / width
            if stage < 0.33:
                bar += S.RED + "█"
            elif stage < 0.66:
                bar += S.YELLOW + "█"
            else:
                bar += S.GREEN + "█"
        else:
            bar += S.GRAY + "░"
    pct = int(100 * ratio)
    return f"{bar}{S.RESET}  {S.BOLD}{pct:>3}%{S.RESET}"


def spinner_wait(label, action, *args, **kwargs):
    """Run *action* with a braille-dot spinner shown while waiting."""
    import threading
    result = [None]
    error = [None]

    def _run():
        try:
            result[0] = action(*args, **kwargs)
        except Exception as e:
            error[0] = e

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    i = 0
    sys.stdout.write(S.HIDE)
    while t.is_alive():
        sp = DOTS[i % len(DOTS)]
        sys.stdout.write(f"\r  {S.CYAN}{sp}{S.RESET}  {label}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(S.SHOW)
    sys.stdout.write(f"\r{S.CLEAR_LINE}")
    if error[0]:
        raise error[0]
    return result[0]


# ══════════════════════════════════════════════════════
#  BOXES & PANELS
# ══════════════════════════════════════════════════════

def fancy_box(lines, color=S.CYAN, pad=2):
    """Draw a Unicode double-line box around text."""
    inner = max(len(l) for l in lines) + pad * 2
    print(f"  {color}╔{'═' * inner}╗{S.RESET}")
    for line in lines:
        gap = inner - len(line) - pad
        print(f"  {color}║{S.RESET}{' ' * pad}{S.BOLD}{line}{S.RESET}{' ' * gap}{color}║{S.RESET}")
    print(f"  {color}╚{'═' * inner}╝{S.RESET}")


def info_panel():
    """System information strip."""
    now = datetime.now().strftime("%d %b %Y  %H:%M:%S")
    py = platform.python_version()
    os_name = platform.system() + " " + platform.release()
    print()
    print(f"  {S.DIM}┌─ System ──────────────────────────────────────────────────────────────┐{S.RESET}")
    print(f"  {S.DIM}│{S.RESET}  🐍 Python {S.BOLD}{py}{S.RESET}   │   🖥️  {os_name}   │   🕐 {now}  {S.DIM}│{S.RESET}")
    print(f"  {S.DIM}└───────────────────────────────────────────────────────────────────────┘{S.RESET}")
    print()


def step_ok(n, total, label):
    print(f"  {S.GREEN}✔{S.RESET}  Step {S.BOLD}{n}/{total}{S.RESET}  {label}")

def step_fail(n, total, label):
    print(f"  {S.RED}✘{S.RESET}  Step {S.BOLD}{n}/{total}{S.RESET}  {label}")


# ══════════════════════════════════════════════════════
#  ASCII ART — TECHBEATS BANNER
# ══════════════════════════════════════════════════════

TECHBEATS = r"""
 _________________ _____  _______ __________
/_  __/ __/ ___/ // / _ )/ __/ _ /_  __/ __/
 / / / _// /__/ _  / _  / _// __ |/ / _\ \  
/_/ /___/\___/_//_/____/___/_/ |_/_/ /___/  
"""

TAGLINE = "    COEP AI & DS Dept.  ─  AI Model Building Challenge 2026  "


def animate_banner():
    """Reveal TECHBEATS with color cycling + underline sweep."""
    lines = [l for l in TECHBEATS.splitlines() if l.strip()]

    # Phase 1 — line-by-line reveal
    for i, line in enumerate(lines):
        c = PALETTE[i % len(PALETTE)]
        print(c + S.BOLD + line + S.RESET)
        time.sleep(0.10)

    # Phase 2 — color cycle pulse (8 frames)
    for frame in range(10):
        move_up(len(lines))
        for i, line in enumerate(lines):
            c = PALETTE[(i + frame) % len(PALETTE)]
            print(c + S.BOLD + line + S.RESET)
        time.sleep(0.07)

    # Underline sweep
    bar_w = max(len(l) for l in lines)
    sweep = ""
    for i in range(bar_w):
        sweep += "═"
        sys.stdout.write(f"\r{S.CYAN}{S.BOLD}{sweep}{S.RESET}")
        sys.stdout.flush()
        time.sleep(0.008)
    print()


def static_banner():
    """Non-animated banner for subsequent screens."""
    lines = [l for l in TECHBEATS.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        c = PALETTE[i % len(PALETTE)]
        print(c + S.BOLD + line + S.RESET)
    bar_w = max(len(l) for l in lines)
    print(S.CYAN + S.BOLD + "═" * bar_w + S.RESET)


# ══════════════════════════════════════════════════════
#  GREETINGS — TIME-AWARE
# ══════════════════════════════════════════════════════

GREET_MORNING = r"""
   ██████╗  ██████╗  ██████╗ ██████╗
  ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗
  ██║  ███╗██║   ██║██║   ██║██║  ██║
  ██║   ██║██║   ██║██║   ██║██║  ██║
  ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝
   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝
  ███╗   ███╗ ██████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗ ██╗
  ████╗ ████║██╔═══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝ ██║
  ██╔████╔██║██║   ██║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗██║
  ██║╚██╔╝██║██║   ██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║╚═╝
  ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝██╗
  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝
"""

GREET_AFTERNOON = r"""
   ██████╗  ██████╗  ██████╗ ██████╗
  ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗
  ██║  ███╗██║   ██║██║   ██║██║  ██║
  ██║   ██║██║   ██║██║   ██║██║  ██║
  ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝
   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝
   █████╗ ███████╗████████╗███████╗██████╗ ███╗   ██╗ ██████╗  ██████╗ ███╗   ██╗██╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██╔═══██╗██╔═══██╗████╗  ██║██║
  ███████║█████╗     ██║   █████╗  ██████╔╝██╔██╗ ██║██║   ██║██║   ██║██╔██╗ ██║██║
  ██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██║   ██║██║╚██╗██║╚═╝
  ██║  ██║██║        ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║ ╚████║██╗
  ╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝
"""

GREET_EVENING = r"""
   ██████╗  ██████╗  ██████╗ ██████╗
  ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗
  ██║  ███╗██║   ██║██║   ██║██║  ██║
  ██║   ██║██║   ██║██║   ██║██║  ██║
  ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝
   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝
  ███████╗██╗   ██╗███████╗███╗   ██╗██╗███╗   ██╗ ██████╗ ██╗
  ██╔════╝██║   ██║██╔════╝████╗  ██║██║████╗  ██║██╔════╝ ██║
  █████╗  ██║   ██║█████╗  ██╔██╗ ██║██║██╔██╗ ██║██║  ███╗██║
  ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║██║╚██╗██║██║   ██║╚═╝
  ███████╗ ╚████╔╝ ███████╗██║ ╚████║██║██║ ╚████║╚██████╔╝██╗
  ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝
"""

GREET_NIGHT = r"""
   ██████╗  ██████╗  ██████╗ ██████╗
  ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗
  ██║  ███╗██║   ██║██║   ██║██║  ██║
  ██║   ██║██║   ██║██║   ██║██║  ██║
  ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝
   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝
  ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗██╗
  ████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝██║
  ██╔██╗ ██║██║██║  ███╗███████║   ██║   ██║
  ██║╚██╗██║██║██║   ██║██╔══██║   ██║   ╚═╝
  ██║ ╚████║██║╚██████╔╝██║  ██║   ██║   ██╗
  ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝
"""

GOOD_LUCK = r"""
   ██████╗  ██████╗  ██████╗ ██████╗     ██╗     ██╗   ██╗ ██████╗██╗  ██╗██╗
  ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗    ██║     ██║   ██║██╔════╝██║ ██╔╝██║
  ██║  ███╗██║   ██║██║   ██║██║  ██║    ██║     ██║   ██║██║     █████╔╝ ██║
  ██║   ██║██║   ██║██║   ██║██║  ██║    ██║     ██║   ██║██║     ██╔═██╗ ╚═╝
  ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝    ███████╗╚██████╔╝╚██████╗██║  ██╗██╗
   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝
"""

# Map hour ranges → art + accent color
GREET_MAP = {
    "morning":   (GREET_MORNING,   S.YELLOW,  "☀️"),
    "afternoon": (GREET_AFTERNOON, S.GREEN,   "🌤️"),
    "evening":   (GREET_EVENING,   S.MAGENTA, "🌆"),
    "night":     (GREET_NIGHT,     S.CYAN,    "🌙"),
}


def _period():
    h = datetime.now().hour
    if 5 <= h < 12:  return "morning"
    if 12 <= h < 17: return "afternoon"
    if 17 <= h < 21: return "evening"
    return "night"


def animate_greeting():
    """Time-based greeting with sparkle borders + sweep reveal."""
    period = _period()
    art, color, emoji = GREET_MAP[period]
    lines = [l for l in art.splitlines() if l.strip()]

    sparkle_line(35, color)
    time.sleep(0.1)

    for line in lines:
        sweep_reveal(line, color=color, chunk=5, delay=0.003)
        time.sleep(0.03)

    sparkle_line(35, color)
    print()
    typewrite(f"  {emoji}  It's a beautiful {period}! Welcome to TECHBEAT26.", delay=0.015, color=color)


def animate_good_luck():
    """GOOD LUCK with color cycling."""
    lines = [l for l in GOOD_LUCK.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        c = PALETTE[i % len(PALETTE)]
        print(c + S.BOLD + line + S.RESET)
        time.sleep(0.08)
    # pulse
    for frame in range(8):
        move_up(len(lines))
        for i, line in enumerate(lines):
            c = PALETTE[(i + frame) % len(PALETTE)]
            print(c + S.BOLD + line + S.RESET)
        time.sleep(0.08)


# ══════════════════════════════════════════════════════
#  PROGRESS BAR (ENHANCED)
# ══════════════════════════════════════════════════════

def progress_bar(label, items, action):
    """Animated gradient progress bar with item labels."""
    total = len(items)
    print()
    for i, item in enumerate(items, 1):
        action(item)
        bar = gradient_bar(i, total)
        sys.stdout.write(
            f"\r  {S.CYAN}{label}{S.RESET}  {bar}  {S.DIM}{item:<20}{S.RESET}"
        )
        sys.stdout.flush()
    print()


# ══════════════════════════════════════════════════════
#  SCREENS
# ══════════════════════════════════════════════════════

def screen_greeting():
    """Screen 1: Animated greeting + system info."""
    clear()
    print()
    animate_greeting()
    info_panel()
    input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to continue...")


def screen_rules():
    """Screen 2: Contest rules with animated banner."""
    clear()
    animate_banner()
    print()
    typewrite(TAGLINE, delay=0.012, color=S.YELLOW)
    print()

    typewrite("  📋  General Rules", delay=0.025, color=S.CYAN + S.BOLD)
    time.sleep(0.15)

    rules = [
        (S.GREEN,   "1.", "Participation is individual only."),
        (S.GREEN,   "2.", "Use Python for all coding tasks."),
        (S.RED,     "3.", "Do NOT copy code from other participants."),
        (S.RED,     "4.", "Dataset provided by organizers must NOT be modified."),
        (S.WHITE,   "5.", "Code must run successfully when tested."),
        (S.MAGENTA, "6.", "You may be asked to explain your code during viva."),
        (S.RED,     "7.", "Violation of rules → disqualification."),
    ]
    for color, num, text in rules:
        time.sleep(0.06)
        print(f"      {S.BOLD}{num}{S.RESET}  {color}{text}{S.RESET}")

    print()
    input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to continue...")


def screen_rounds():
    """Screen 3: Round structure with matrix transition."""
    clear()
    matrix_drop(50, 4, 0.025)
    print()
    static_banner()
    print()

    typewrite("  🏆  Round Structure", delay=0.025, color=S.CYAN + S.BOLD)
    time.sleep(0.15)

    structure = [
        (S.GREEN + S.BOLD, "  Round 1  (Choose One):"),
        (S.WHITE,          "    R1.1  Data Cleaning — fix a noisy dataset"),
        (S.WHITE,          "    R1.2  Linear Regression using scikit-learn"),
        ("", ""),
        (S.GREEN + S.BOLD, "  Round 2:"),
        (S.WHITE,          "    Manual Linear Regression implementation"),
        (S.RED,            "    ⚠  scikit-learn NOT allowed"),
        ("", ""),
        (S.GREEN + S.BOLD, "  Round 3:"),
        (S.WHITE,          "    Viva for participants who complete R1 & R2"),
    ]
    for color, text in structure:
        if not text:
            print()
            continue
        typewrite(f"    {text}", delay=0.010, color=color)
        time.sleep(0.02)

    print()
    input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to accept rules and begin setup...")


def screen_setup_banner():
    """Reusable banner for setup screens."""
    clear()
    static_banner()
    print()
    typewrite(TAGLINE, delay=0.012, color=S.YELLOW)
    print(S.DIM + "  " + "─" * 60 + S.RESET)


# ══════════════════════════════════════════════════════
#  BACKUP
# ══════════════════════════════════════════════════════

def backup_existing_files():
    files = ["model.py", "data.py"]
    existing = [f for f in files if os.path.exists(f)]
    if not existing:
        return None

    base = os.path.join(os.getcwd(), "previous_attempts")
    os.makedirs(base, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(base, ts)
    os.makedirs(dest)

    for f in existing:
        shutil.move(os.path.join(os.getcwd(), f), dest)

    print(f"\n  {S.YELLOW}📦 Backed up existing files:{S.RESET}")
    for f in existing:
        print(f"      {S.DIM}→ previous_attempts/{ts}/{f}{S.RESET}")
    print()
    return dest


# ══════════════════════════════════════════════════════
#  ROUND SELECTION
# ══════════════════════════════════════════════════════

def select_round():
    while True:
        print(S.CYAN + S.BOLD + "\n  ╭─ Select Round Template ─╮\n" + S.RESET)
        for key, label in ROUND_LABELS.items():
            print(f"    {S.BOLD}{S.YELLOW}{key}{S.RESET}  →  {label}")
        print()

        choice = input(f"  {S.BOLD}Enter choice [1/2/3]: {S.RESET}").strip()

        if choice not in ROUND_LABELS:
            print(f"  {S.RED}✘ Invalid choice — try again.{S.RESET}")
            continue

        print(f"\n  Selected: {S.GREEN}{S.BOLD}{ROUND_LABELS[choice]}{S.RESET}")
        confirm = input(f"  Confirm? ({S.GREEN}Y{S.RESET}/{S.RED}N{S.RESET}): ").strip().lower()

        if confirm == "y":
            return choice

        print(f"\n  {S.YELLOW}↻ Selection cleared — choose again.{S.RESET}")


# ══════════════════════════════════════════════════════
#  FILE TEMPLATES
# ══════════════════════════════════════════════════════

MODEL_R11 = """\
# ==========================================
# TECHBEAT26 - R1.1  Data Cleaning Round
# ==========================================

import data

# Your task:
# data.RAW contains a noisy dataset.
# Clean it and store the result in `cleaned`.

cleaned = None

# Write cleaning logic here


"""

DATA_R11 = """\
# ==========================================
# NOISY DATASET  (organizer fills this)
# ==========================================

RAW = []

"""

MODEL_R12 = """\
# ==========================================
# TECHBEAT26 - R1.2  sklearn Linear Regression
# ==========================================

import data
import numpy as np
from sklearn.linear_model import LinearRegression

# Your task:
# Use data.X and data.Y to train a model.
# Print the R2 score and plot predictions.

X = np.array(data.X).reshape(-1, 1)
Y = np.array(data.Y)

model = LinearRegression()

# Train and evaluate here


"""

DATA_R12 = """\
# ==========================================
# CLEAN DATASET  (organizer fills this)
# ==========================================

X = []
Y = []

"""

MODEL_R2 = """\
# ==========================================
# TECHBEAT26 - R2 Manual Linear Regression
# ==========================================
# DO NOT REMOVE: X_VALUES, Y_VALUES, m, c, or data.graph(m,c)
# ==========================================

import data

m, c = None, None

X_VALUES = data.X_VALUES
Y_VALUES = data.Y_VALUES


# ==========================================
# CODE HERE
# ==========================================


data.graph(m, c)
"""

DATA_R2 = """\
# ==========================================
# TECHBEAT26 - DATA FILE
# DO NOT DELETE ANYTHING FROM HERE
# ==========================================

import matplotlib.pyplot as plt
import numpy as np

Y_VALUES = [7, 11, 15, 19, 18, 22, 26, 30, 34, 33, 37, 41, 45, 49, 48, 52, 56, 60, 64, 63, 67, 71, 75, 79, 78, 82, 86, 90, 94, 93, 97, 101, 105, 109, 108, 112, 116, 120, 124, 123, 127, 131, 135, 139, 138, 142, 146, 150, 154, 153, 157, 161, 165, 169, 168, 172, 176, 180, 184, 183, 187, 191, 195, 199, 198, 202, 206, 210, 214, 213, 217, 221, 225, 229, 228, 232, 236, 240, 244, 243, 247, 251, 255, 259, 258, 262, 266, 270, 274, 273, 277, 281, 285, 289, 288, 292, 296, 300, 304, 303, 307, 311, 315, 319, 318, 322, 326, 330, 334, 333, 337, 341, 345, 349, 348, 352, 356, 360, 364, 363, 367, 371, 375, 379, 378, 382, 386, 390, 394, 393, 397, 401, 405, 409, 408, 412, 416, 420, 424, 423, 427, 431, 435, 439, 438, 442, 446, 450, 454, 453, 457, 461, 465, 469, 468, 472, 476, 480, 484, 483, 487, 491, 495, 499, 498, 502, 506, 510, 514, 513, 517, 521, 525, 529, 528, 532, 536, 540, 544, 543, 547, 551, 555, 559, 558, 562, 566, 570, 574, 573, 577, 581, 585, 589, 588, 592, 596, 600, 604, 603]
X_VALUES = list(range(1, 201))

x = 6
y = 120


class colors:
    RED   = '\\033[91m'
    GREEN = '\\033[92m'
    RESET = '\\033[0m'


def graph(m=None, c=None):

    plt.figure(figsize=(10, 6))
    plt.scatter(X_VALUES, Y_VALUES, color='blue', label='Actual Data Points')

    if m is None or c is None:
        print(colors.RED + "Warning: m and c not set. Showing data only." + colors.RESET)
    else:
        try:
            estimated_y = m * x + c
            estimated_x = (y - c) / m
            line_x = np.linspace(min(X_VALUES) - 5, max(X_VALUES) + 5, 100)
            line_y = m * line_x + c
            plt.plot(line_x, line_y, color='red',
                     label=f'Regression Line: y = {m}x + {c}')
            plt.scatter(x, estimated_y, color='black',
                        s=100, zorder=5,
                        label=f'Est. Y at X={x}')
            plt.scatter(estimated_x, y, color='cyan',
                        s=100, zorder=5,
                        label=f'Est. X at Y={y}')
            print(colors.GREEN + f"[OK] y = {m:.4f}x + {c:.4f}" + colors.RESET)
        except Exception as e:
            print(colors.RED + f"Plotting error: {e}" + colors.RESET)

    plt.title("Linear Regression Visualization")
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
"""

TEMPLATES = {
    "1": (MODEL_R11, DATA_R11),
    "2": (MODEL_R12, DATA_R12),
    "3": (MODEL_R2,  DATA_R2),
}


def create_files(choice):
    model_src, data_src = TEMPLATES[choice]
    with open("model.py", "w", encoding="utf-8") as f:
        f.write(model_src)
    with open("data.py", "w", encoding="utf-8") as f:
        f.write(data_src)


# ══════════════════════════════════════════════════════
#  COUNTDOWN
# ══════════════════════════════════════════════════════

def countdown(seconds=3, label="Starting setup"):
    """Visual countdown before setup begins."""
    print()
    for i in range(seconds, 0, -1):
        c = [S.RED, S.YELLOW, S.GREEN][min(seconds - i, 2)]
        sys.stdout.write(f"\r  {c}{S.BOLD}  {label} in {i}...{S.RESET}  ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write(f"\r  {S.GREEN}{S.BOLD}  🚀 GO!{S.RESET}                              \n")
    time.sleep(0.3)


# ══════════════════════════════════════════════════════
#  FINAL SUMMARY
# ══════════════════════════════════════════════════════

def final_summary(choice, backup_dir, elapsed):
    """Premium finish screen."""
    clear()
    print()

    summary_lines = [
        "TECHBEAT26  ─  Setup Complete ✓",
        "",
        f"Round    :  {ROUND_LABELS[choice]}",
        f"Env      :  {VENV_NAME}/",
        f"Files    :  model.py   data.py",
        f"Time     :  {elapsed:.1f}s",
    ]
    if backup_dir:
        summary_lines.append(f"Backup   :  {os.path.relpath(backup_dir)}")

    fancy_box(summary_lines, color=S.GREEN)
    print()

    animate_good_luck()

    print()
    print(f"  {S.DIM}{'─' * 55}{S.RESET}")
    print(f"  {S.BOLD}Next steps:{S.RESET}")
    print(f"    1. Open {S.CYAN}model.py{S.RESET} and write your solution")
    print(f"    2. Run:  {S.GREEN}python model.py{S.RESET}")
    print(f"    3. Call the organizer when done")
    print(f"  {S.DIM}{'─' * 55}{S.RESET}")
    print()


# ══════════════════════════════════════════════════════
#  ─────────────── M A I N ───────────────
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    start_time = time.time()

    # ── Screen 1: Greeting ──────────────────────────
    screen_greeting()

    # ── Screen 2: Rules ─────────────────────────────
    screen_rules()

    # ── Screen 3: Round structure ───────────────────
    screen_rounds()

    # ── Countdown ───────────────────────────────────
    clear()
    static_banner()
    countdown(3, "Initializing environment")

    # ── Setup Phase ─────────────────────────────────
    screen_setup_banner()
    TOTAL = 5
    print()

    # Step 1 — Virtual environment
    if not os.path.exists(VENV_NAME):
        spinner_wait(
            "Creating virtual environment...",
            lambda: venv.EnvBuilder(with_pip=True).create(VENV_NAME),
        )
        step_ok(1, TOTAL, "Virtual environment created")
    else:
        step_ok(1, TOTAL, "Virtual environment already exists")

    python_path = os.path.join(VENV_NAME, "Scripts", "python.exe")

    # Step 2 — Upgrade pip
    ok = spinner_wait(
        "Upgrading pip...",
        run_silent, f'"{python_path}" -m pip install --upgrade pip',
    )
    if ok:
        step_ok(2, TOTAL, "pip upgraded")
    else:
        step_fail(2, TOTAL, "pip upgrade failed")

    # Step 3 — Remove restricted libs
    progress_bar(
        f"Step 3/{TOTAL}  Removing restricted libs ",
        REMOVE_DEPENDENCIES,
        lambda pkg: run_silent(f'"{python_path}" -m pip uninstall -y {pkg}'),
    )
    step_ok(3, TOTAL, "Restricted libraries removed")

    # Step 4 — Install packages
    progress_bar(
        f"Step 4/{TOTAL}  Installing packages      ",
        REQUIREMENTS,
        lambda pkg: run_silent(f'"{python_path}" -m pip install {pkg}'),
    )
    step_ok(4, TOTAL, "Required libraries installed")

    # Step 5 — Prepare contest files
    print()
    backup_dir = backup_existing_files()
    clear()
    screen_setup_banner()
    choice = select_round()
    create_files(choice)
    step_ok(5, TOTAL, "Contest files created")

    elapsed = time.time() - start_time

    # ── Final Summary ───────────────────────────────
    final_summary(choice, backup_dir, elapsed)

    # ── Activate environment ────────────────────────
    activate_bat = os.path.join(VENV_NAME, "Scripts", "activate.bat")
    activate_ps1 = os.path.join(VENV_NAME, "Scripts", "Activate.ps1")

    shell = "powershell" if "PSModulePath" in os.environ else "cmd"
    print(f"  Detected shell: {S.CYAN}{shell}{S.RESET}")

    try:
        if shell == "powershell":
            subprocess.run(
                ["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", activate_ps1],
                check=False,
            )
        else:
            subprocess.run(["cmd", "/k", activate_bat], check=False)
    except Exception as e:
        print(S.RED + "  Environment activation failed: " + S.RESET + str(e))
        print(f"\n  Run manually: {S.GREEN}{VENV_NAME}\\Scripts\\activate{S.RESET}")
