#!/usr/bin/env bash
# Splash do MEGA CODE Portable: corvo + MEGA CODE 4 antes de abrir o TUI.
# Uso (start.sh):  source "$ROOT_DIR/tools/splash.sh"; show_splash
# Variáveis: SPLASH_DELAY (segundos, padrão 2), NO_SPLASH=1 desativa.

show_splash() {
    [ -n "${NO_SPLASH:-}" ] && return 0
    [ -t 1 ] || return 0                       # só em terminal interativo
    command -v python3 >/dev/null 2>&1 || return 0
    local dir; dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    [ -f "$dir/splash.py" ] && [ -f "$dir/../assets/raven.pix" ] || return 0
    clear
    printf '\n'
    python3 "$dir/splash.py" 2>/dev/null || return 0
    printf '\n'
    sleep "${SPLASH_DELAY:-2}"
}
