#!/usr/bin/env bash
# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
# ==============================================================================
# Script d'installation - OMEGA-SCAN TUI/CLI
# À lancer depuis le dossier extrait de l'archive : cd omega-scan && ./install.sh
# Résilient : peut être relancé sans erreur si une étape a déjà été faite.
# Contrairement à omega-fire.sh, aucune étape ne nécessite les privilèges
# root (pas de groupe dédié, pas de setgid) : Omega-Scan s'exécute
# entièrement en utilisateur normal, ses fichiers runtime (var/) lui
# appartiennent donc déjà nativement.
# ==============================================================================

set -e

# Couleurs (mêmes conventions que omega-fire.sh)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
ok()   { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; }
tip()  { echo -e "${WHITE}💡 $1${NC}"; }

echo -e "${WHITE}    ░▒▓███████████████████████████████████████████████▓▒░${NC}"
echo -e "${WHITE}    ░ Ω M E G A - SCAN — I N S T A L L A T I O N ░${NC}"
echo -e "${WHITE}    ░▒▓███████████████████████████████████████████████▓▒░${NC}"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# -------------------------------------------------------------------------
# 1. Environnement virtuel Python
# -------------------------------------------------------------------------
if [ -d ".venv" ]; then
    info ".venv existe déjà, création ignorée."
else
    if ! python3 -m venv .venv 2>/tmp/omega-scan-venv-err.log; then
        err "Échec de la création de l'environnement virtuel."
        warn "Sur Debian/Ubuntu (et dérivées), le module venv n'est pas toujours inclus avec python3 de base."
        tip "Installez-le puis relancez ce script : sudo apt install python3-venv"
        cat /tmp/omega-scan-venv-err.log >&2
        rm -f /tmp/omega-scan-venv-err.log
        exit 1
    fi
    rm -f /tmp/omega-scan-venv-err.log
    ok "Environnement virtuel créé (.venv)."
fi

# -------------------------------------------------------------------------
# 2. Dépendances — pyproject.toml reste l'unique source de verite (pas de
#    requirements.txt separe a maintenir en double). omega-lib n'est pas
#    publiee sur PyPI : l'archive distribuable la vendore dans
#    vendor/omega-lib/ (voir build-release.sh des autres outils de la
#    suite) — installee ICI, avant omega-scan lui-meme, pour que pip la
#    trouve deja satisfaite dans le venv et ne tente jamais de la chercher
#    sur PyPI. Absente en clone de developpement (omega-lib vient alors du
#    monorepo local ~/DEV/LIB/omega-lib, deja installee a part) : etape
#    silencieusement ignoree si vendor/omega-lib/ n'existe pas.
# -------------------------------------------------------------------------
source .venv/bin/activate
pip install -q --upgrade pip
if [ -d "$SCRIPT_DIR/vendor/omega-lib" ]; then
    pip install -q -e "$SCRIPT_DIR/vendor/omega-lib"
    ok "Dépendance vendorée omega-lib installée."
fi
pip install -q -e .
ok "Dépendances installées."

# -------------------------------------------------------------------------
# 3. Scripts exécutables
# -------------------------------------------------------------------------
chmod +x omega-scan.sh
chmod +x "$SCRIPT_DIR/install.sh"
ok "Scripts rendus exécutables."

# -------------------------------------------------------------------------
# 4. Alias (optionnel) — bash et zsh, quel que soit celui réellement utilisé.
#    Pas de sudo ici : Omega-Scan ne requiert aucun privilège root.
# -------------------------------------------------------------------------
ALIAS_LINE="alias scan=\"${SCRIPT_DIR}/omega-scan.sh\""

for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    rc_name="$(basename "$rc")"
    if grep -qxF "$ALIAS_LINE" "$rc" 2>/dev/null; then
        info "Alias déjà présent dans $rc_name."
    elif echo "$ALIAS_LINE" >> "$rc" 2>/dev/null; then
        ok "Alias ajouté à $rc_name."
    else
        warn "Impossible d'ajouter l'alias à $rc_name."
    fi
done

echo ""
ok "Installation terminée."
tip "Lancez Omega-Scan avec : ${SCRIPT_DIR}/omega-scan.sh (ou 'scan' dans un nouveau terminal si l'alias vient d'être ajouté)."
