#!/usr/bin/env python3
"""Splash do MEGA CODE Portable: corvo em pixel art + "MEGA CODE 4" (só stdlib).

Lê assets/raven.pix (grade de caracteres) e imprime com meio-blocos truecolor.
Chamado por tools/splash.sh. Não escreve nada em disco.
"""
import os
import sys

PAL = {
    "K": (22, 22, 30), "G": (72, 80, 108), "H": (130, 140, 175), "L": (62, 70, 102),
    "R": (255, 35, 35), "Y": (150, 0, 0), "B": (95, 95, 105),
    "T": (125, 90, 55), "D": (80, 58, 36),
}

FONT = {
    "M": ["█   █", "██ ██", "█ █ █", "█   █", "█   █"],
    "E": ["█████", "█    ", "████ ", "█    ", "█████"],
    "G": [" ████", "█    ", "█  ██", "█   █", " ████"],
    "A": [" ███ ", "█   █", "█████", "█   █", "█   █"],
    "C": [" ████", "█    ", "█    ", "█    ", " ████"],
    "O": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "D": ["████ ", "█   █", "█   █", "█   █", "████ "],
    "4": ["█   █", "█   █", "█████", "    █", "    █"],
}

ESC = "\x1b["
RESET = ESC + "0m"


def word(s):
    return [" ".join(FONT[c][r] for c in s) for r in range(5)]


def fg(c):
    return f"{ESC}38;2;{c[0]};{c[1]};{c[2]}m"


def bg(c):
    return f"{ESC}48;2;{c[0]};{c[1]};{c[2]}m"


def cell(top, bot):
    if top is None and bot is None:
        return " "
    if bot is None:
        return f"{fg(top)}▀{RESET}"
    if top is None:
        return f"{fg(bot)}▄{RESET}"
    return f"{fg(top)}{bg(bot)}▀{RESET}"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    pix = os.environ.get("RAVEN_PIX", os.path.join(here, "..", "assets", "raven.pix"))
    with open(pix, encoding="utf-8") as f:
        grid = [ln.rstrip("\n") for ln in f if ln.strip()]
    w = max(len(r) for r in grid)
    if len(grid) % 2:
        grid.append("." * w)
    grid = [r.ljust(w, ".") for r in grid]

    code4 = [f"{a}   {b}" for a, b in zip(word("CODE"), word("4"))]
    title = word("MEGA") + [""] + code4
    rows = len(grid) // 2
    off = (rows - len(title)) // 2 - 1

    out = []
    for r in range(rows):
        top, bot = grid[2 * r], grid[2 * r + 1]
        left = "".join(
            cell(PAL.get(top[x]), PAL.get(bot[x])) for x in range(w)
        )
        t = r - off
        if 0 <= t < len(title) and title[t]:
            k = t / max(1, len(title) - 1)
            c = (255 - int(70 * k), 40 - int(30 * k), 40 - int(30 * k))
            right = f"{ESC}1m{fg(c)}{title[t]}{RESET}"
        elif t == len(title) + 1:
            right = f"{fg((200, 200, 215))}Portable AI Coding Agent{RESET}"
        elif t == len(title) + 2:
            right = f"{ESC}2m{fg((160, 160, 175))}plug in. launch. code.{RESET}"
        else:
            right = ""
        out.append("  " + left + "   " + right)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # splash é enfeite: nunca pode impedir o launcher de abrir
