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
    echo "  pip install -r requirements.txt"
    exit 1
fi

# 2. Vérification robuste : tester si un paquet clé (rich) est bien importable
# C'est beaucoup plus fiable que de vérifier l'existence d'un dossier
if ! "$VENV_DIR/bin/python" -c "import rich" 2>/dev/null; then
    echo "⚠️  Le venv semble incomplet, réinstallation des dépendances..."
    "$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
fi

# 3. Activer le venv et lancer l'application
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
exec python "$SCRIPT_DIR/main.py" "$@"
