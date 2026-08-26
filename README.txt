================================================================================
                              OMEGA-SCAN
              Scanner de posture de securite web
                elabore par kraynux pour Omega-server
                https://kraynux.snake-mackarel.ts.net
================================================================================

Omega-scan est un outil TUI + CLI qui analyse l'hygiene de configuration
visible de vos services HTTP/HTTPS. Il observe, collecte des faits, applique
des regles interpretatives et produit des rapports actionnables, sans jamais
effectuer d'attaque active. Troisieme outil de la suite omega- (apres
omega-fire et omega-stress), structure en Clean Architecture -- voir
ARCHITECTURE.md pour le detail technique complet.


1. VISION ET PERIMETRE
================================================================================

Omega-scan est un scanner de posture de securite web, destine a un
usage d'administration systeme : verifier rapidement l'hygiene de
configuration visible d'un service HTTP/HTTPS sur localhost, LAN, ou une
cible externe (y compris derriere un tunnel comme Tailscale funnel).

Ce que fait Omega-scan :
  - Collecte des faits observables (headers, cookies, methodes HTTP, TLS,
    chemins sensibles, en-tetes CORS)
  - Applique des regles interpretatives declaratives sur ces faits
  - Produit des findings homogenes, justifies et actionnables
  - Restitue le resultat en TUI (Textual) ou en CLI scriptable, et via trois
    exports (JSON, texte, HTML)
  - Detecte les faux positifs (catch-all, chemins proteges par auth)
  - S'adapte au contexte (proxy/tunnel, multi-vhost, SNI)
  - Exige une confirmation d'autorisation explicite avant tout scan d'une
    cible non deja epinglee-autorisee
  - Conserve un historique persistant des scans par cible, rejouable et
    comparable dans le temps

Ce qu'Omega-scan ne fait PAS :
  - Scanner de vulnerabilites actives (pas de SQLi/XSS/RCE)
  - Scanner de CVE
  - Outil de bruteforce ou de fuzzing massif
  - Crawler profond
  - Outil multi-cibles parallele agressif
  - Dashboard web
  - Authentification cote scanner


2. INSTALLATION
================================================================================

Prerequis :
  - Python 3.10+
  - Connexion Internet, pour les dependances et les scans externes

Installation :

L'archive officielle est fournie au format .tar.gz. Verifiez son
integrite avant installation :

  sha256sum omega-scan.tar.gz

Methode 1 -- script d'installation :

  [ -d omega-scan ] && echo "Deja extrait ici, etape ignoree." || tar -xzf omega-scan.tar.gz
  [ -d ~/omega-scan ] && echo "~/omega-scan existe deja, deplacement ignore." || mv omega-scan ~/
  cd ~/omega-scan/
  chmod +x install.sh
  ./install.sh

Methode 2 -- installation complete resiliente (copier-coller, relancable
sans erreur, chaque etape ignore ce qui a deja ete fait) :

  ( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
  ( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
  cd ~/omega-scan && chmod +x install.sh && ./install.sh

install.sh :
  1. Cree l'environnement virtuel .venv s'il n'existe pas deja.
  2. Installe les dependances (pip install -e ., pyproject.toml reste
     l'unique source de verite).
  3. Rend omega-scan.sh et install.sh executables.
  4. Ajoute l'alias "scan" a ~/.bashrc et ~/.zshrc (sans doublon si deja
     present).

Dependances (declarees dans pyproject.toml, plus de requirements.txt) :
  - textual   : interface TUI, themes, adaptation automatique au terminal
  - httpx     : client HTTP/HTTPS moderne
  - jinja2    : templating pour l'export HTML
  - Dependances de developpement (pip install -e ".[dev]") : pytest,
    pytest-asyncio, pytest-httpserver, trustme, ruff, mypy, import-linter


3. UTILISATION
================================================================================

Mode interactif (TUI) -- recommande pour l'usage quotidien, lance sans
argument :

  ./omega-scan.sh

Parcours : ecran de demarrage (se ferme sur une touche ou un clic) -> menu
principal -> saisie de la cible et choix du profil (avec confirmation
d'autorisation si la cible n'est pas deja epinglee) -> scan (jauge de
progression et detail des operations reseau affiches en direct) ->
resultats (note globale, findings filtrables par categorie, detail au clic
sur une ligne) -> export/historique/comparaison depuis le menu principal.
L'adaptation au terminal (couleurs, taille, degradation structurelle) est
automatique, plus besoin de flags d'affichage manuels.

Raccourcis clavier :

  Haut / Bas       Naviguer entre les elements d'un ecran
  Tab / Maj+Tab    Naviguer entre les champs d'un formulaire
  Echap            Retour a l'ecran precedent (confirmation sur l'accueil)
  t                Theme suivant (applique immediatement, sans confirmation)
  r                Rafraichir la detection du terminal
  a                Afficher l'aide
  q                Quitter (avec confirmation)

Mode scriptable (CLI) -- toute sous-commande declenche le mode CLI (texte
simple, ou JSON avec --json) :

  # Scanner une cible (--authorize requis si la cible n'est pas deja epinglee)
  ./omega-scan.sh scan example.org --profile standard --authorize
  ./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

  # Historique
  ./omega-scan.sh history list --host example.org
  ./omega-scan.sh history show scan-30577411758e
  ./omega-scan.sh history compare scan-aaa scan-bbb
  ./omega-scan.sh history replay scan-30577411758e

  # Export
  ./omega-scan.sh export scan-30577411758e --format html --output rapport.html

  # Cibles epinglees-autorisees (dispense de --authorize sur les scans suivants)
  ./omega-scan.sh targets pin example.org --note "accord client 2026-08"
  ./omega-scan.sh targets unpin example.org
  ./omega-scan.sh targets list

Garde d'autorisation de cible :
  Aucun scan ne demarre sans confirmation explicite d'autorisation sur la
  cible (case a cocher en TUI, --authorize en CLI), sauf cible deja
  epinglee. Verifiee cote application (guard dedie dans le pipeline), pas
  seulement cote interface.

Formats de cible acceptes :

  192.168.1.10                IPv4
  192.168.1.10:8080           IPv4 avec port
  ::1                         IPv6
  [2001:db8::10]:8443         IPv6 avec crochets et port
  example.org                 Hostname
  intranet.lan:8080/admin     Hostname avec port et chemin
  http://example.org          URL HTTP
  https://example.org/admin   URL HTTPS


4. PROFILS DE SCAN
================================================================================

  Parametre       | quick    | standard | extended | local-lab
  ----------------|----------|----------|----------|----------
  Usage           | rapide   | complet  | approfondi | localhost/LAN
  Timeout co/lect | 3s / 6s  | 3s / 6s  | 5s / 10s | 3s / 6s
  Methodes HTTP   | OPTIONS  | +TRACE   | +PUT/DELETE/PATCH | OPTIONS,TRACE
  Path probing    | non      | oui (~20)| oui (complet) | oui (~20)
  TLS             | non      | oui      | oui (detaille) | oui (tolerant)
  Sonde CORS      | non      | oui      | oui      | oui
  Catch-all       | -        | oui      | oui      | oui
  Politique HSTS  | non evaluee | standard | stricte | tolerante

Quand utiliser quel profil :
  - quick      : verification eclair avant mise en production
  - standard   : audit complet d'un service en production, recommande
  - extended   : audit approfondi incluant les methodes HTTP risquees
  - local-lab  : scan de localhost ou LAN sans penaliser les regles pensees
                 pour le public (HSTS notamment)


5. ARCHITECTURE
================================================================================

Omega-scan est structure en Clean Architecture (domain / application /
infrastructure / interfaces / ports / core / app / plugins / shared),
alignee sur le gabarit de la suite omega- (voir omega-stress). Le detail
complet (arborescence, regles de dependance, chaines fonctionnelles,
hierarchie d'exceptions, taxonomie de nommage) vit dans ARCHITECTURE.md,
document normatif de reference.

Vue d'ensemble tres courte :

  src/omega_scan/
  |-- domain/          Logique metier pure (cibles, profils, scans, checks,
  |                    reports, themes...)
  |-- application/     Cas d'usage (commands/queries), pipeline
  |                    d'execution, gardes
  |-- ports/           Contrats attendus par l'application (probers,
  |                    repositories, exporters...)
  |-- infrastructure/  Implementations concretes (httpx, SQLite -- Textual
  |                    n'est PAS ici)
  |-- interfaces/      tui/ (Textual) et cli/ (scriptable), a parite
  |                    fonctionnelle stricte
  |-- app/             Assemblage (DependencyContainer, bootstrap, cycle
  |                    de vie)
  |-- core/, shared/   Vocabulaire transverse, utilitaires non metier
  +-- plugins/         Structure posee, vide (aucun axe d'extension
                        confirme)

Regles de conception inchangees depuis la v1 :
  - domain/checks/            : juge a partir des preuves, ne fait jamais
                                 de reseau
  - infrastructure/network/   : fait du reseau, ne juge jamais
  - interfaces/                : affiche, ne contient aucune logique metier
  - infrastructure/exporters/ : lisent le resultat de scan, ne recalculent
                                 rien


6. TAXONOMIE DES REGLES
================================================================================

Transport, TRN-* :
  - TRN-HTTP-001  : HTTP accessible sans redirection HTTPS (WARN)
  - TRN-HTTPS-001 : HTTPS non accessible (FAIL)
  - TRN-HSTS-001  : header HSTS absent (FAIL)
  - TRN-HSTS-002  : HSTS max-age faible, inferieur a 1 an (WARN)

Profondeur TLS, TLS-* :
  - TLS-VERSION-001 : protocole TLS obsolete (< TLSv1.2) (FAIL)
  - TLS-CIPHER-001  : suite cryptographique manifestement faible (RC4,
                      DES, NULL, EXPORT, MD5) (WARN)

Headers, HDR-* :
  - HDR-CSP-001     : CSP absente sur page HTML (FAIL)
  - HDR-CSP-002     : CSP trop permissive (WARN)
  - HDR-NOSNIFF-001 : X-Content-Type-Options absent (WARN)
  - HDR-SERVER-001  : banniere Server exposee (WARN)
  - HDR-CACHE-001   : Cache-Control absent ou permissif sur une page HTML
                      (WARN)

Cookies, COO-* :
  - COO-SECURE-001    : cookie sur reponse HTTPS sans attribut Secure (WARN)
  - COO-HTTPONLY-001  : cookie sans attribut HttpOnly (WARN)
  - COO-SAMESITE-001  : SameSite absent, ou None sans Secure (WARN)

CORS, COR-* :
  - COR-WILDCARD-CREDENTIALS-001 : Access-Control-Allow-Origin: * combine
                                    a Access-Control-Allow-Credentials:
                                    true (FAIL)
  - COR-REFLECTED-ORIGIN-001     : origine arbitraire refletee telle
                                    quelle (WARN)

Methodes HTTP, MTH-* :
  - MTH-OPTIONS-001 : methode OPTIONS activee (INFO)
  - MTH-TRACE-001   : methode TRACE activee (WARN)
  - MTH-PUT-001     : methode PUT activee (WARN)
  - MTH-DELETE-001  : methode DELETE activee (WARN)
  - MTH-PATCH-001   : methode PATCH activee (WARN)
  - MTH-CONNECT-001 : methode CONNECT activee (WARN)

Exposition, EXR-* :
  - EXR-ADMIN-001     : chemin admin accessible sans auth (WARN)
  - EXR-SENSITIVE-001 : fichier sensible accessible, .env/.git (FAIL)

Fuites d'information, INF-* :
  - INF-BANNER-001      : bannieres serveur exposees (WARN)
  - INF-ERROR-001       : messages d'erreur detailles (WARN)
  - INF-STACK-001       : stack trace exposee (FAIL)
  - INF-ROBOTS-001      : fichier robots.txt present (OK, info)
  - INF-HEADER-001      : headers techniques bavards (WARN)
  - INF-SECURITYTXT-001 : fichier /.well-known/security.txt present
                          (OK, info)


7. POLITIQUE DE CONFIANCE
================================================================================

  Niveau  | Definition
  --------|-----------------------------------------------------------
  certain | Preuve directe, non ambigue (header present/absent, code brut)
  high    | Preuve claire mais contexte indirect (OPTIONS, cookie observe)
  medium  | Constat possiblement influence par un intermediaire (proxy/WAF)
  low     | Detection indirecte, ou situation catch_all_suspected

Degradations automatiques :
  - catch_all_suspected = true      : confiance plafonnee a low
  - proxy_suspected = true          : confiance plafonnee a medium
  - observed_access_state=ambiguous : confiance plafonnee a low


8. DETECTION DE FAUX POSITIFS
================================================================================

Comportement catch-all :
  Avant de tester les chemins sensibles, Omega-scan genere un chemin
  aleatoire improbable. Si le serveur repond 200 OK dessus, la cible est
  marquee catch_all_suspected = true et tous les findings d'exposition
  sont degrades en confidence = low.

Authentification vs absence :
  Un chemin protege (401, 403, ou redirection vers login) n'est ni marque
  comme absent ni comme expose. Il est marque N/A avec la note :
  "chemin protege, presence non confirmable sans authentification".

Proxy / tunnel :
  Si des headers X-Forwarded-*, Via ou Forwarded sont detectes,
  proxy_suspected passe a true et les findings concernes (bannieres, TLS)
  voient leur confiance plafonnee a medium.


9. COMPATIBILITE TERMINAUX
================================================================================

Le TUI (Textual) detecte automatiquement les capacites du terminal
(couleur, taille) et adapte sa feuille de style structurelle en
consequence (complete/standard/reduced/mono) -- plus de flags manuels
(--no-emoji, --no-color, --plain) comme en v1. Le mode CLI reste toujours
en texte simple (ou --json), independant du terminal.


10. EXPORTS
================================================================================

Les rapports sont generes dans var/exports/ par defaut (chemin runtime,
voir ARCHITECTURE.md), ou au chemin indique (--output en CLI, boite de
dialogue en TUI).

  - JSON  : structure complete du scan (ScanRun), strictement
            JSON-serializable -- source de verite
  - Texte : rapport humain compact, lisible hors terminal, sans codes ANSI
  - HTML  : rapport autonome avec CSS inline, consultable dans n'importe
            quel navigateur, partageable et archivable


11. HISTORIQUE ET COMPARAISON
================================================================================

Chaque scan est persiste (SQLite, var/db/app.db) : historique consultable
par cible, detail d'un run passe, comparaison entre deux scans (findings
apparus / resolus / inchanges / changes), et rejeu d'un scan sur la meme
cible sans ressaisie -- absents de la v1, ajoutes lors de la migration
vers Clean Architecture.


12. TESTS
================================================================================

  source .venv/bin/activate
  pytest tests/ -v

Structure :
  - tests/unit/        : domaine et application, sans I/O reelle
  - tests/integration/ : SQLite/fichiers reels, serveur HTTP factice
                          (pytest-httpserver)
  - tests/e2e/          : CLI et TUI de bout en bout (Textual.testing)


13. HORS PERIMETRE
================================================================================

  - Scan de CVE
  - Detection active de SQLi, XSS, RCE
  - Authentification complexe cote scanner
  - Crawling profond
  - Fuzzing
  - Bruteforce massif de chemins
  - Scan multi-cibles simultane
  - Parallelisme agressif
  - Dashboard web

================================================================================
  Omega-scan -- Observer, collecter, interpreter, rapporter.
  Un scanner de posture, pas un outil d'attaque.
================================================================================
