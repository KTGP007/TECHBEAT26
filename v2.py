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
import argparse  
import hashlib   
import urllib.request

# ─── UTF-8 on Windows ───────────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


# ══════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════

VENV_NAME = "TECHBEATS26"

REMOVE_DEPENDENCIES = [
    "seaborn",
    "scipy",
    "statsmodels",
    "tensorflow",
    "keras",
    "torch",
]

REQUIREMENTS = [
    "numpy",
    "pandas",
    "matplotlib",
    "scikit-learn",
]

class SkipToRound(Exception):
    """Hidden shortcut: raised when user types 's' at any prompt to skip setup."""
    pass


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
    # "1": "Round 1.1",
    # "2": "Round 1.2",
    # "3": "Round 2"
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
    
    # Hide the cursor for a cleaner animation
    sys.stdout.write(S.HIDE)
    
    try:
        for _ in range(rows):
            line = "  "
            for __ in range(width):
                ch = random.choice(chars)
                # Randomly pick between Green, Dim Green, and Cyan
                shade = random.choice([S.GREEN, S.DIM + S.GREEN, S.CYAN])
                line += shade + ch + S.RESET
            print(line)
            time.sleep(delay)
    finally:
        # ALWAYS ensure the cursor comes back, even if interrupted
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
    resp = input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to continue...")
    if resp.strip().lower() == "s":
        raise SkipToRound()


# ══════════════════════════════════════════════════════
#  GUIDE DOWNLOAD
# ══════════════════════════════════════════════════════

GUIDE_URLS = {
    "1": (
        "English",
        "https://raw.githubusercontent.com/KTGP007/TECHBEAT26/main/TECHBEAT26_Student_Guide.pdf",
        "TECHBEAT26_Student_Guide.pdf",
    ),
    "2": (
        "हिंदी (Hindi)",
        "https://raw.githubusercontent.com/KTGP007/TECHBEAT26/main/TECHBEAT26_Student_Guide_Hindi.pdf",
        "TECHBEAT26_Student_Guide_Hindi.pdf",
    ),
    "3": (
        "मराठी (Marathi)",
        "https://raw.githubusercontent.com/KTGP007/TECHBEAT26/main/TECHBEAT26_Student_Guide_Marathi.pdf",
        "TECHBEAT26_Student_Guide_Marathi.pdf",
    ),
}


def screen_guide():
    """Optional screen: offer to download the student guide."""
    clear()
    static_banner()
    print()
    print(f"  {S.CYAN}{S.BOLD}📘  Student Guide{S.RESET}")
    print(f"  {S.DIM}{'─' * 50}{S.RESET}")
    print(f"  A step-by-step guide for VS Code & Terminal is available.")
    print()

    resp = input(f"  Would you like to download the guide? ({S.GREEN}Y{S.RESET}/{S.RED}N{S.RESET}): ").strip().lower()

    if resp == "s":
        raise SkipToRound()

    if resp != "y":
        print(f"\n  {S.DIM}Skipping guide download.{S.RESET}")
        time.sleep(0.5)
        return

    print()
    print(f"  {S.BOLD}Choose language:{S.RESET}")
    print(f"    {S.YELLOW}{S.BOLD}1{S.RESET}  →  English")
    print(f"    {S.YELLOW}{S.BOLD}2{S.RESET}  →  हिंदी (Hindi)")
    print(f"    {S.YELLOW}{S.BOLD}3{S.RESET}  →  मराठी (Marathi)")
    print()

    choice = input(f"  {S.BOLD}Enter choice [1/2/3]: {S.RESET}").strip()

    if choice not in GUIDE_URLS:
        print(f"  {S.RED}✘ Invalid choice — skipping guide.{S.RESET}")
        time.sleep(0.5)
        return

    lang, url, filename = GUIDE_URLS[choice]
    print()

    try:
        spinner_wait(
            f"Downloading {lang} guide...",
            lambda: urllib.request.urlretrieve(url, filename),
        )
        print(f"  {S.GREEN}✔{S.RESET}  Guide saved as {S.CYAN}{S.BOLD}{filename}{S.RESET}")
        print(f"  {S.DIM}Open it in VS Code or any text editor to read.{S.RESET}")
    except Exception as e:
        print(f"  {S.RED}✘ Download failed:{S.RESET} {e}")
        print(f"  {S.DIM}You can download it manually from GitHub later.{S.RESET}")

    print()
    resp = input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to continue...")
    if resp.strip().lower() == "s":
        raise SkipToRound()


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
    resp = input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to continue...")
    if resp.strip().lower() == "s":
        raise SkipToRound()


def screen_rounds():
    """Screen 3: Round structure with matrix transition."""
    clear()
    matrix_drop(50, 4, 0.025)
    print()
    static_banner()
    print()

    typewrite("  🏆  Round Structure", delay=0.025, color=S.CYAN + S.BOLD)
    time.sleep(0.15)

    # structure = [
    #     (S.GREEN + S.BOLD, "  Round 1  (Choose One):"),
    #     (S.WHITE,          "    R1.1  DCR ROUND"),
    #     (S.WHITE,          "    R1.2  SL-ROUND"),
    #     ("", ""),
    #     (S.GREEN + S.BOLD, "  Round 2:"),
    #     (S.WHITE,          "    MANUAL ROUND"),
    #     # (S.RED,            "    ⚠  scikit-learn NOT allowed"),
    #     ("", ""),
    #     (S.GREEN + S.BOLD, "  Round 3:"),
    #     (S.WHITE,          "    VIVA ROUND"),
    # ]
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
    resp = input(f"  Press {S.GREEN}{S.BOLD}ENTER{S.RESET} to accept rules and begin setup...")
    if resp.strip().lower() == "s":
        raise SkipToRound()


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

RAW = data.RAW

# Your task:
# data.RAW contains a noisy 1D dataset (list).
# Clean it, ensure all items are valid numbers if not possible remove it.
# and store the final valid numbers in the `cleaned` list.
# IMP: cleaned list must be between between 0 and 100, values must be float

cleaned = []


# ==========================================
# CODE HERE
# ==========================================


# ==========================================
# DO NOT REMOVE THIS LINE:
data.graph(cleaned)
"""


DATA_R11 = """\
# ==========================================
# TECHBEAT26 - DATA FILE (R1.1)
# DO NOT DELETE ANYTHING FROM HERE
# ==========================================

import matplotlib.pyplot as plt
import random
import hashlib
import uuid
import socket

class colors:
    RED   = '\\033[91m'
    GREEN = '\\033[92m'
    CYAN  = '\\033[96m'
    YELLOW= '\\033[93m'
    RESET = '\\033[0m'

try:
    def anti_cheeky_func():
        mac = str(uuid.getnode())   
        host = socket.gethostname()           
        raw = mac + host
        h = hashlib.sha256(raw.encode()).hexdigest()
        return int(h, 16) % (10**8)

    seed = anti_cheeky_func()
    random.seed(seed)
    
    RAW = []
    garbage_pool = [None, "N/A", "NaN", "", "Error", "  ", "null", "Missing"]
    outlier_pool = [999, -50, 10000, -999, 5000, -10]
    
    # Generate exactly 25 items
    for _ in range(25):
        choice = random.choices(
            ['clean_int', 'clean_float', 'str_int', 'str_float', 'outlier', 'garbage'],
            weights=[35, 15, 15, 10, 10, 15], 
            k=1
        )[0]
        
        if choice == 'clean_int':
            RAW.append(random.randint(5, 95))
        elif choice == 'clean_float':
            RAW.append(round(random.uniform(5.0, 95.0), 1))
        elif choice == 'str_int':
            val = random.randint(5, 95)
            RAW.append(f" {val} " if random.choice([True, False]) else str(val))
        elif choice == 'str_float':
            val = round(random.uniform(5.0, 95.0), 1)
            RAW.append(str(val))
        elif choice == 'outlier':
            RAW.append(random.choice(outlier_pool))
        elif choice == 'garbage':
            RAW.append(random.choice(garbage_pool))
            
except Exception as e:
    RAW = [
        12, 15, "18", 22.5, None, " 24 ", "N/A", 27, 
        999, -50, "30", "NaN", 33, "", "40.5", 42, 
        "Error", 45, 10000, 48, "  ", 50, 55, " 60 ", None
    ]

def _get_expected():
    total = 0
    count = 0
    for item in RAW:
        try:
            val = float(item)
            if 0 <= val <= 100:
                total += val
                count += 1
        except (ValueError, TypeError):
            pass
    return total, count

def graph(cleaned=None):
    if cleaned is None or not isinstance(cleaned, list):
        print(colors.RED + "✘ [ERROR] Please pass a valid list to data.graph(cleaned)" + colors.RESET)
        return

    original_len = len(RAW)
    cleaned_len = len(cleaned)
    expected_sum, expected_count = _get_expected()
    
    try:
        cleaned_sum = sum(cleaned)
        if abs(cleaned_sum - expected_sum) < 0.01 and cleaned_len == expected_count:
            grade = colors.GREEN + "✔ PERFECT (Data is clean)" + colors.RESET
        else:
            grade = colors.RED + "✘ INCORRECT (Check your filtering logic)" + colors.RESET
            
    except Exception as e:
        cleaned_sum = f"ERROR"
        grade = colors.RED + "✘ FAILED (List contains non-numeric strings)" + colors.RESET

    print(colors.CYAN + "\\n╭── Data Cleaning Results ──────────────────────╮" + colors.RESET)
    print(f"  Original length : {original_len}")
    print(f"  Cleaned length  : {cleaned_len}")
    if type(cleaned_sum) != str:
        print(f"  Cleaned Sum     : {cleaned_sum:.1f}")
    else:
        print(f"  Cleaned Sum     : {cleaned_sum}")
    print(f"  Status          : {grade}")
    print(colors.CYAN + "╰───────────────────────────────────────────────╯" + colors.RESET)
    print(f"\\nCleaned Data Array:\\n{cleaned}\\n")

    labels = ['Original (Noisy)', 'Cleaned']
    counts = [original_len, cleaned_len]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, counts, color=['#ff6666', '#66b3ff'], edgecolor='black')
    
    plt.title('TECHBEAT26: Data Cleaning Progression', fontweight='bold')
    plt.ylabel('Total Data Points')
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), 
                 ha='center', va='bottom', fontweight='bold', fontsize=12)

    plt.ylim(0, max(counts) + 5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
"""

MODEL_R12 = """\
# ==========================================
# TECHBEAT26 - R1.2 sklearn Linear Regression
# ==========================================

import data
import numpy as np
from sklearn.linear_model import LinearRegression
m,c = None,None


# STEPS
# 1. Take X and Y data
# 2. Prepare it for the model
# 3. Create linear regression model
# 4. Train the model on data
# 5. Get slope and intercept
# 6. Check how good the model is
# 7. Plot the graph


# =============
# CODE HERE
# =============

# ==========================================
# Do not remove this
data.graph(m,c)
"""

DATA_R12 = """\
# ==========================================
# TECHBEAT26 - DATA FILE (R2)
# DO NOT DELETE ANYTHING FROM HERE
# ==========================================

import matplotlib.pyplot as plt
import numpy as np
import random
import hashlib
import uuid
import socket
import os

class colors:
    RED   = '\\033[91m'
    GREEN = '\\033[92m'
    CYAN  = '\\033[96m'
    YELLOW= '\\033[93m'
    RESET = '\\033[0m'

# Target variables for prediction
x = 6
y = 120

try:
    def anti_cheeky_func():
        mac = str(uuid.getnode())      
        host = socket.gethostname()           
        raw = mac + host
        h = hashlib.sha256(raw.encode()).hexdigest()
        return int(h, 16) % (10**8)

    seed = anti_cheeky_func()
    random.seed(seed)
    np.random.seed(seed)
    
    X_VALUES = list(range(1, 201))
    Y_VALUES = []
    
    for xi in X_VALUES:
        noise = random.randint(-2, 2)
        yi = 3 * xi + 5 + noise
        Y_VALUES.append(yi)
        
except Exception as e:
    X_VALUES = list(range(1, 201))
    Y_VALUES = [3 * xi + 5 for xi in X_VALUES]

def _get_expected():
    m, c = np.polyfit(X_VALUES, Y_VALUES, 1)
    return m, c

def _check_for_cheats():
    # Secretly reads the student's model.py to find banned shortcuts
    banned_terms = ["polyfit", "lstsq", "sklearn", "scipy", "statsmodels", "linregress"]
    if not os.path.exists("model.py"):
        return False
        
    try:
        with open("model.py", "r", encoding="utf-8") as f:
            for line in f:
                # Ignore comments so we don't trigger on the header instructions
                clean_line = line.split("#")[0] 
                for term in banned_terms:
                    if term in clean_line:
                        return term # Return the exact word they used to cheat
    except Exception:
        pass
    return False

def graph(m=None, c=None):
    expected_m, expected_c = _get_expected()
    cheat_used = _check_for_cheats()
    
    print(colors.CYAN + "╭── Manual Linear Regression Results ───────────╮" + colors.RESET)
    
    # Check if they haven't calculated anything yet
    if m is None or c is None:
        print(f"  {colors.YELLOW}⚠ m and/or c are missing! Showing raw data only.{colors.RESET}")
        print(colors.CYAN + "╰───────────────────────────────────────────────╯" + colors.RESET)
    else:
        # Only try to grade them if m and c actually exist
        try:
            m_val = float(m)
            c_val = float(c)
            
            print(f"  Student Slope (m) : {m_val:.4f}")
            print(f"  Student Intcp (c) : {c_val:.4f}")
            
            # Grading Logic overrides if a cheat is detected
            if cheat_used:
                grade = colors.RED + f"🚨 CHEAT DETECTED (Banned term: {cheat_used})" + colors.RESET
            elif abs(m_val - expected_m) < 0.01 and abs(c_val - expected_c) < 0.01:
                grade = colors.GREEN + "✔ PERFECT (Exact OLS match)" + colors.RESET
            elif abs(m_val - 3.0) <= 0.5 and abs(c_val - 5.0) <= 2.0:
                grade = colors.YELLOW + "≈ ACCEPTABLE (Close, but check math)" + colors.RESET
            else:
                grade = colors.RED + "✘ INCORRECT (Math is off)" + colors.RESET
                
            print(f"  Status            : {grade}")
        except Exception as e:
            print(f"  {colors.RED}✘ [ERROR] m and c must be numeric values!{colors.RESET}")
        
        print(colors.CYAN + "╰───────────────────────────────────────────────╯" + colors.RESET)

    # Draw the graph (This now runs regardless of m/c values!)
    plt.figure(figsize=(10, 6))
    plt.scatter(X_VALUES, Y_VALUES, color='blue', label='Actual Data Points', alpha=0.4)

    try:
        # Only attempt to draw the line and estimations if m and c are valid numbers
        if m is not None and c is not None and not cheat_used:
            line_x = np.array([min(X_VALUES) - 5, max(X_VALUES) + 5])
            line_y = m * line_x + c
            plt.plot(line_x, line_y, color='red', linewidth=2, label=f'Regression Line: y = {m:.2f}x + {c:.2f}')
            
            estimated_y = m * x + c
            estimated_x = (y - c) / m if m != 0 else 0
            
            plt.scatter(x, estimated_y, color='black', s=100, zorder=5, label=f'Est. Y at X={x} ({estimated_y:.1f})')
            plt.scatter(estimated_x, y, color='magenta', s=100, zorder=5, label=f'Est. X at Y={y} ({estimated_x:.1f})')
            
    except Exception as e:
        pass # Ignore plotting errors if m or c were weird data types

    plt.title("TECHBEAT26: Manual Linear Regression", fontweight='bold')
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
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

# =============
# CODE HERE
# =============


# DO NOT REMOVE THIS LINE
data.graph(m, c)
"""

DATA_R2 = """\
# ==========================================
# TECHBEAT26 - DATA FILE (R2)
# DO NOT DELETE ANYTHING FROM HERE
# ==========================================

import matplotlib.pyplot as plt
import numpy as np
import random
import hashlib
import uuid
import socket
import os

class colors:
    RED   = '\\033[91m'
    GREEN = '\\033[92m'
    CYAN  = '\\033[96m'
    YELLOW= '\\033[93m'
    RESET = '\\033[0m'

# Target variables for prediction
x = 6
y = 120

try:
    def anti_cheeky_func():
        mac = str(uuid.getnode())      
        host = socket.gethostname()           
        raw = mac + host
        h = hashlib.sha256(raw.encode()).hexdigest()
        return int(h, 16) % (10**8)

    seed = anti_cheeky_func()
    random.seed(seed)
    np.random.seed(seed)
    
    X_VALUES = list(range(1, 201))
    Y_VALUES = []
    
    for xi in X_VALUES:
        noise = random.randint(-2, 2)
        yi = 3 * xi + 5 + noise
        Y_VALUES.append(yi)
        
except Exception as e:
    X_VALUES = list(range(1, 201))
    Y_VALUES = [3 * xi + 5 for xi in X_VALUES]

def _get_expected():
    m, c = np.polyfit(X_VALUES, Y_VALUES, 1)
    return m, c

def _check_for_cheats():
    # Secretly reads the student's model.py to find banned shortcuts
    banned_terms = ["polyfit", "lstsq", "sklearn", "scipy", "statsmodels", "linregress"]
    if not os.path.exists("model.py"):
        return False
        
    try:
        with open("model.py", "r", encoding="utf-8") as f:
            for line in f:
                # Ignore comments so we don't trigger on the header instructions
                clean_line = line.split("#")[0] 
                for term in banned_terms:
                    if term in clean_line:
                        return term # Return the exact word they used to cheat
    except Exception:
        pass
    return False

def graph(m=None, c=None):
    expected_m, expected_c = _get_expected()
    cheat_used = _check_for_cheats()
    
    print(colors.CYAN + "╭── Manual Linear Regression Results ───────────╮" + colors.RESET)
    
    # Check if they haven't calculated anything yet
    if m is None or c is None:
        print(f"  {colors.YELLOW}⚠ m and/or c are missing! Showing raw data only.{colors.RESET}")
        print(colors.CYAN + "╰───────────────────────────────────────────────╯" + colors.RESET)
    else:
        # Only try to grade them if m and c actually exist
        try:
            m_val = float(m)
            c_val = float(c)
            
            print(f"  Student Slope (m) : {m_val:.4f}")
            print(f"  Student Intcp (c) : {c_val:.4f}")
            
            # Grading Logic overrides if a cheat is detected
            if cheat_used:
                grade = colors.RED + f"🚨 CHEAT DETECTED (Banned term: {cheat_used})" + colors.RESET
            elif abs(m_val - expected_m) < 0.01 and abs(c_val - expected_c) < 0.01:
                grade = colors.GREEN + "✔ PERFECT (Exact OLS match)" + colors.RESET
            elif abs(m_val - 3.0) <= 0.5 and abs(c_val - 5.0) <= 2.0:
                grade = colors.YELLOW + "≈ ACCEPTABLE (Close, but check math)" + colors.RESET
            else:
                grade = colors.RED + "✘ INCORRECT (Math is off)" + colors.RESET
                
            print(f"  Status            : {grade}")
        except Exception as e:
            print(f"  {colors.RED}✘ [ERROR] m and c must be numeric values!{colors.RESET}")
        
        print(colors.CYAN + "╰───────────────────────────────────────────────╯" + colors.RESET)

    # Draw the graph (This now runs regardless of m/c values!)
    plt.figure(figsize=(10, 6))
    plt.scatter(X_VALUES, Y_VALUES, color='blue', label='Actual Data Points', alpha=0.4)

    try:
        # Only attempt to draw the line and estimations if m and c are valid numbers
        if m is not None and c is not None and not cheat_used:
            line_x = np.array([min(X_VALUES) - 5, max(X_VALUES) + 5])
            line_y = m * line_x + c
            plt.plot(line_x, line_y, color='red', linewidth=2, label=f'Regression Line: y = {m:.2f}x + {c:.2f}')
            
            estimated_y = m * x + c
            estimated_x = (y - c) / m if m != 0 else 0
            
            plt.scatter(x, estimated_y, color='black', s=100, zorder=5, label=f'Est. Y at X={x} ({estimated_y:.1f})')
            plt.scatter(estimated_x, y, color='magenta', s=100, zorder=5, label=f'Est. X at Y={y} ({estimated_x:.1f})')
            
    except Exception as e:
        pass # Ignore plotting errors if m or c were weird data types

    plt.title("TECHBEAT26: Manual Linear Regression", fontweight='bold')
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
#  INTEGRITY GUARD
# ══════════════════════════════════════════════════════

def check_data_integrity(auto_restore=False):
    """Verifies that data.py matches one of the valid templates, and optionally restores it."""
    
    def normalize_text(raw_text):
        clean_lines = [line.rstrip() for line in raw_text.splitlines() if line.strip()]
        return "\n".join(clean_lines).encode('utf-8')

    valid_templates = {
        hashlib.sha256(normalize_text(DATA_R11)).hexdigest(): ("Round 1.1 (Data Cleaning)", DATA_R11),
        hashlib.sha256(normalize_text(DATA_R12)).hexdigest(): ("Round 1.2 (sklearn)", DATA_R12),
        hashlib.sha256(normalize_text(DATA_R2)).hexdigest():  ("Round 2 (Manual)", DATA_R2),
    }

    def guess_expected_template():
        if os.path.exists("model.py"):
            with open("model.py", "r", encoding="utf-8") as f:
                content = f.read()
                if "R1.1" in content: return DATA_R11, "Round 1.1"
                if "R1.2" in content: return DATA_R12, "Round 1.2"
                if "R2" in content:   return DATA_R2, "Round 2"
        return None, None

    actual_hash = None
    if os.path.exists("data.py"):
        with open("data.py", "r", encoding="utf-8") as f:
            actual_text = f.read()
        actual_bytes = normalize_text(actual_text)
        actual_hash = hashlib.sha256(actual_bytes).hexdigest()

    print(f"\n  {S.CYAN}Running TECHBEAT26 Integrity Guard...{S.RESET}")

    if actual_hash in valid_templates:
        round_name, _ = valid_templates[actual_hash]
        print(f"  {S.GREEN}✔ [OK] data.py integrity verified for {round_name}. No tampering detected.{S.RESET}\n")
        return True  # <-- Changed: Return peacefully instead of sys.exit(0)
    else:
        if not os.path.exists("data.py"):
            state_msg = f"{S.YELLOW}⚠ [MISSING] data.py not found.{S.RESET}"
        else:
            state_msg = f"{S.YELLOW}⚠ [TAMPERED] data.py modified.{S.RESET}"

        if auto_restore:
            print(f"  {state_msg} Restoring original file...")
            expected_data, round_name = guess_expected_template()
            
            if expected_data:
                with open("data.py", "w", encoding="utf-8") as f:
                    f.write(expected_data)
                print(f"  {S.GREEN}✔ [RESTORED] data.py has been reset to its pristine {round_name} state.{S.RESET}\n")
                return True # <-- Changed: Return peacefully instead of sys.exit(0)
            else:
                print(f"  {S.RED}✘ [FAIL] Cannot determine which round to restore. model.py is missing or altered.{S.RESET}")
                sys.exit(1)
        else:
            if not os.path.exists("data.py"):
                print(f"  {S.RED}✘ [FAIL] data.py is missing!{S.RESET}")
            else:
                print(f"  {S.RED}✘ [FAIL] WARNING: data.py has been modified or corrupted!{S.RESET}")
            print(f"  {S.DIM}Tip: Run `python v2.py --restore` to fix.{S.RESET}\n")
            sys.exit(1)

# ══════════════════════════════════════════════════════
#  ─────────────── M A I N ───────────────
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TECHBEAT26 Setup and Guard")
    parser.add_argument("--guard" or "g", action="store_true", help="Run integrity test on data.py")
    parser.add_argument("--restore"or "r", action="store_true", help="Restore data.py to original state if tampered")
    parser.add_argument("--test"or "t", action="store_true", help="Guard, restore if needed, and run model.py")
    
    args, unknown = parser.parse_known_args() 

    # Handle the command line flags12
    if args.guard or args.restore or args.test:
        # If --test is used, we want auto-restore to be True
        should_restore = args.restore or args.test
        
        # This will either return True (success/restored) or sys.exit(1) on failure
        check_data_integrity(auto_restore=should_restore)
        
        # If they used --test, run their model.py code now
        if args.test:
            if os.path.exists("model.py"):
                print(f"  {S.CYAN}▶ Executing model.py...{S.RESET}\n")
                print(f"{S.DIM}{'─' * 60}{S.RESET}")
                # Use sys.executable to ensure it runs with the current python interpreter
                subprocess.run([sys.executable, "model.py"])
                print(f"{S.DIM}{'─' * 60}{S.RESET}\n")
                print(f"  {S.GREEN}✔ Run complete.{S.RESET}\n")
            else:
                print(f"  {S.RED}✘ [FAIL] Cannot run test: model.py is missing!{S.RESET}\n")
                
        # Exit cleanly so the setup GUI screens don't run
        sys.exit(0)
    start_time = time.time()

    try:
        # ── Screen 1: Greeting ──────────────────────────
        screen_greeting()

        # ── Screen 1.5: Guide Download ──────────────────
        screen_guide()

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

    except SkipToRound:
        # Hidden shortcut: user typed 's' — skip setup, jump to round selection
        clear()
        print(f"\n  {S.YELLOW}⚡ Setup skipped — jumping to round selection...{S.RESET}\n")
        time.sleep(0.5)

    # Step 5 — Prepare contest files
    print()
    backup_dir = backup_existing_files()
    clear()
    screen_setup_banner()
    choice = select_round()
    create_files(choice)

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
