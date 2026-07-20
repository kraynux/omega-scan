# Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)

"""
Point d'entrée principal d'Omega-scan.
Gère le parsing des arguments CLI et lance l'application.
"""

import sys
import os


def parse_args():
    """
    Parse les arguments de ligne de commande.
    Retourne un dict avec les options détectées.
    """
    args = {
        "plain": False,
        "no_color": False,
        "no_emoji": False,
        "no_live": False,
        "target": None,
        "profile": "standard",
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ("--help", "-h"):
            print("""
╔══════════════════════════════════════════════════════════════╗
║  Omega-scan — Scanner de posture de sécurité web             ║
╚══════════════════════════════════════════════════════════════╝

Usage: omega-scan [options]

Options d'affichage :
  --plain, -p        Mode texte simple (sans Rich, compatible tous terminaux)
  --no-color         Désactive les couleurs (pour terminaux sans couleur)
  --no-emoji         Désactive les emojis (pour terminaux sans support emoji)
  --no-live          Désactive les animations Live (pour SSH/TTY)

Options de scan :
  --target, -t URL   Cible directe (mode non-interactif)
  --profile NAME     Profil : quick, standard, extended, local-lab

Options générales :
  --help, -h         Affiche cette aide

Exemples :
  omega-scan                              # Mode interactif
  omega-scan --no-emoji                   # Sans emojis (urxvt, xterm)
  omega-scan --plain                      # Mode texte pur (TTY, SSH ancien)
  omega-scan --target example.org         # Scan direct
  omega-scan --target 192.168.1.10 --profile quick
""")
            sys.exit(0)
        
        elif arg in ("--plain", "-p"):
            args["plain"] = True
        
        elif arg == "--no-color":
            args["no_color"] = True
        
        elif arg == "--no-emoji":
            args["no_emoji"] = True
        
        elif arg == "--no-live":
            args["no_live"] = True
        
        elif arg in ("--target", "-t"):
            if i + 1 < len(sys.argv):
                args["target"] = sys.argv[i + 1]
                i += 1
            else:
                print("Erreur : --target nécessite une URL en argument", file=sys.stderr)
                sys.exit(1)
        
        elif arg == "--profile":
            if i + 1 < len(sys.argv):
                args["profile"] = sys.argv[i + 1]
                i += 1
            else:
                print("Erreur : --profile nécessite un nom de profil", file=sys.stderr)
                sys.exit(1)
        
        else:
            print(f"Option inconnue : {arg}", file=sys.stderr)
            print("Utilisez --help pour voir les options disponibles.", file=sys.stderr)
            sys.exit(1)
        
        i += 1
    
    return args

if __name__ == "__main__":
    # 1. Parser les arguments
    cli_args = parse_args()
    
    # 2. Appliquer les variables d'environnement pour Rich
    if cli_args["no_color"] or cli_args["plain"]:
        os.environ["NO_COLOR"] = "1"
    
    # 3. Initialiser la console Rich pour gérer les interruptions proprement
    from rich.console import Console
    console = Console()
    
    # 4. Lancer l'application
    try:
        from ui.app import main
        main(cli_args=cli_args)
    except KeyboardInterrupt:
        # On utilise console.print() au lieu de print() pour que le markup Rich fonctionne
        console.print("\n\n[bold yellow]⚠ Interruption par l'utilisateur[/bold yellow]\n")
        sys.exit(0)

