#!/bin/bash
# ============================================================
# Omega-scan — Script de lancement
# Active automatiquement l'environnement virtuel Python
# ============================================================

set -e

# Déterminer le répertoire où se trouve ce script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# 1. Vérifier que le venv existe
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Environnement virtuel introuvable : $VENV_DIR"
    echo ""
    echo "Créez-le avec :"
    echo "  cd $SCRIPT_DIR"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -e ."
    exit 1
fi

# 2. Vérification robuste : tester si le paquet est bien installé (mode editable)
# C'est beaucoup plus fiable que de vérifier l'existence d'un dossier
if ! "$VENV_DIR/bin/python" -c "import omega_scan" 2>/dev/null; then
    echo "⚠️  Le venv semble incomplet, réinstallation..."
    "$VENV_DIR/bin/pip" install -q -e "$SCRIPT_DIR"
fi

# 3. Ancrer le repertoire runtime (base SQLite, settings, logs, exports) sur
# l'emplacement du script, jamais sur le repertoire courant du shell appelant
# (sans ca, lancer ./omega-scan.sh depuis des repertoires differents utilise
# des bases SQLite differentes a chaque fois : historique/cibles epinglees
# qui semblent "disparaitre" alors qu'ils sont juste ecrits ailleurs)
export OMEGA_SCAN_VAR_DIR="${OMEGA_SCAN_VAR_DIR:-$SCRIPT_DIR/var}"

# 4. Activer le venv et lancer l'application (script console declare dans pyproject.toml)
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
exec omega-scan "$@"
