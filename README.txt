================================================================================
                              OMEGA-SCAN
              Scanner de posture de securite web
                elaboré par kraynux pour Omega-server
                https://kraynux.snake-mackarel.ts.net
================================================================================

Omega-scan est un outil en ligne de commande qui analyse l'hygiene de
configuration visible de vos services HTTP/HTTPS. Il observe, collecte des
faits, applique des regles interpretatives et produit des rapports
actionnables, sans jamais effectuer d'attaque active.


1. VISION ET PERIMETRE
================================================================================

Omega-scan est un scanner de posture de securite web, destine a un
usage d'administration systeme : verifier rapidement l'hygiene de
configuration visible d'un service HTTP/HTTPS sur localhost, LAN, ou une
cible externe (y compris derriere un tunnel comme Tailscale funnel).

Ce que fait Omega-scan :
  - Collecte des faits observables (headers, cookies, methodes HTTP, TLS,
    chemins sensibles)
  - Applique des regles interpretatives declaratives sur ces faits
  - Produit des findings homogenes, justifies et actionnables
  - Restitue le resultat en console (Rich) et via trois exports (JSON,
    texte, HTML)
  - Detecte les faux positifs (catch-all, chemins proteges par auth)
  - S'adapte au contexte (proxy/tunnel, multi-vhost, SNI)

Ce qu'Omega-scan ne fait PAS :
  - Scanner de vulnerabilites actives (pas de SQLi/XSS/RCE)
  - Scanner de CVE
  - Outil de bruteforce ou de fuzzing massif
  - Crawler profond
  - Outil multi-cibles parallele agressif
  - Dashboard web
  - Authentification cote scanner
  - Comparaison historique entre scans (prevu en evolution future)


2. INSTALLATION
================================================================================

Prerequis :
  - Python 3.10+
  - Connexion Internet (pour les dependances et les scans externes)

Installation rapide :
    mkdir -p ~/SCANNER/
    cd ~/SCANNER/
    
- deposer le dossier "omega-scan" dans le dossier SCANNER et ensuite :
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
- render le script de départ executable :
    chmod +x omega-scan.sh


Dependances :
  - rich           : interface console (couleurs, tableaux, progressions)
  - httpx          : client HTTP/HTTPS moderne
  - jinja2         : templating pour l'export HTML
  - pytest         : framework de tests
  - pytest-httpserver : serveur HTTP factice pour les tests
  - trustme        : generation de certificats TLS de test


3. UTILISATION
================================================================================

Mode interactif (recommande) :

    ./omega-scan.sh

Parcours guide :
  1. Accueil
  2. Saisie de la cible (IPv4, IPv6, hostname ou URL complete)
  3. Choix du profil (quick, standard, extended, local-lab)
  4. Confirmation avant lancement
  5. Scan avec barre de progression en temps reel
  6. Resume (note globale, ventilation par statut/severite)
  7. Actions (detail par categorie, export, relancer, retour)

Mode non-interactif (scripts / CI) :

    ./omega-scan.sh --target example.org --profile standard
    ./omega-scan.sh --target 192.168.1.10 --profile local-lab

Options d'affichage :

    --help, -h        Affiche l'aide complete
    --plain, -p       Mode texte simple (sans Rich, compatible tous terminaux)
    --no-color        Desactive les couleurs
    --no-emoji        Desactive les emojis
    --no-live         Desactive les animations Live
    --target, -t URL  Cible directe (mode non-interactif)
    --profile NAME    Profil : quick, standard, extended, local-lab

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

+----------------------+----------+-----------+-----------+-------------+
| Parametre            | quick    | standard  | extended  | local-lab   |
+----------------------+----------+-----------+-----------+-------------+
| Usage                | Verif.   | Complet   | Approf.   | localhost   |
|                      | rapide   | (defaut)  |           | / LAN       |
| Timeout connect/read | 3s / 6s  | 3s / 6s   | 5s / 10s  | 3s / 6s     |
| Methodes HTTP        | OPTIONS  | OPTIONS,  | OPTIONS,  | OPTIONS,    |
|                      |          | TRACE     | TRACE,    | TRACE       |
|                      |          |           | PUT,      |             |
|                      |          |           | DELETE,   |             |
|                      |          |           | PATCH     |             |
| Path probing         | Non      | Oui       | Oui       | Oui         |
|                      |          | (~20)     | (complet) | (~20)       |
| TLS                  | Non      | Oui       | Oui       | Oui         |
|                      |          |           | (detaille)|(tolerant)   |
| Catch-all            | -        | Oui       | Oui       | Oui         |
| Politique HSTS       | Non      | Standard  | Strict    | Tolerante   |
|                      | evaluee  |           |           |             |
+----------------------+----------+-----------+-----------+-------------+

Quand utiliser quel profil :
  - quick      : Verification eclair avant mise en production
  - standard   : Audit complet d'un service en production (recommande)
  - extended   : Audit approfondi incluant les methodes HTTP risquees
  - local-lab  : Scan de localhost/LAN sans penaliser les regles pensees
                 pour le public (HSTS notamment)


5. ARCHITECTURE
================================================================================

omega-scan/
 |-- main.py                    Point d'entree, parsing CLI
 |-- omega-scan.sh              Script de lancement (activation venv)
 |-- requirements.txt           Dependances figees
 |
 |-- config/                    Configuration et constantes
 |   |-- defaults.py            Timeouts, user-agent, throttling
 |   |-- profiles.py            Profils quick/standard/extended/local-lab
 |   +-- paths.py               Listes de chemins admin/sensibles
 |
 |-- core/                      Socle d'execution
 |   |-- pipeline.py            Orchestration du scan complet
 |   |-- target_parser.py       Normalisation des cibles
 |   |-- context.py             Contexte de scan (meta, erreurs)
 |   |-- errors.py              Classification des erreurs
 |   |-- logger.py              Journalisation technique
 |   +-- serialization.py       Conversion JSON centralisee
 |
 |-- models/                    Objets metier (donnees, pas de logique)
 |   |-- target.py              Cible canonique
 |   |-- finding.py             Finding (regle + preuve + interpretation)
 |   |-- scan_result.py         Resultat complet du scan
 |   |-- summary.py             Resume calcule
 |   +-- evidence.py            Preuve attachee a un finding
 |
 |-- collectors/                Font du reseau, ne jugent jamais
 |   |-- connectivity.py        Pre-scan DNS/HTTP/HTTPS
 |   |-- http_probe.py          Collecte HTTP/HTTPS principale
 |   |-- tls_probe.py           Collecte TLS, certificat, SNI
 |   |-- path_probe.py          Path probing + detection catch-all
 |   +-- methods_probe.py       Test des methodes HTTP
 |
 |-- normalizers/               Nettoient et homogeneisent
 |   |-- headers.py             content_profile, proxy_suspected
 |   |-- cookies.py             Normalisation des cookies
 |   +-- redirects.py           Chaine de redirections
 |
 |-- checks/                    Jugent a partir des preuves, pas de reseau
 |   |-- base.py                Infrastructure des checks
 |   |-- transport.py           TRN-* (HTTPS, HSTS, redirections)
 |   |-- headers.py             HDR-* (CSP, nosniff, referrer, framing)
 |   |-- methods.py             MTH-* (OPTIONS, TRACE, PUT, DELETE...)
 |   |-- exposure.py            EXR-* (chemins admin, fichiers sensibles)
 |   +-- information_leaks.py   INF-* (bannieres, stack traces, robots)
 |
 |-- exporters/                 Lisent scan_result, ne recalculent rien
 |   |-- json_exporter.py       Export JSON source de verite
 |   |-- text_exporter.py       Rapport humain compact
 |   +-- html_exporter.py       Rapport web (Jinja2 + CSS inline)
 |
 |-- ui/                        Affiche, pas de logique metier
 |   |-- app.py                 Application console interactive
 |   |-- screens.py             Ecrans (accueil, fin de scan)
 |   |-- prompts.py             Saisies et menus
 |   |-- tables.py              Tableaux de findings
 |   |-- panels.py              Panneaux d'information
 |   |-- progress.py            Barre de progression
 |   +-- compat.py              Detection et compatibilite terminaux
 |
 |-- reports/                   Dossier de sortie des exports
 |
 +-- tests/                     Tests unitaires et d'integration

Regles de conception :
  - collectors/   : fait du reseau, ne juge jamais
  - normalizers/  : nettoie et homogeneise, ne juge jamais
  - checks/       : juge a partir des preuves, ne fait jamais de reseau
  - ui/           : affiche, ne contient aucune logique metier
  - exporters/    : lisent scan_result, ne recalculent rien


6. TAXONOMIE DES REGLES
================================================================================

Transport (TRN-*) :
  TRN-HTTP-001    HTTP accessible sans redirection HTTPS      WARN
  TRN-HTTPS-001   HTTPS non accessible                        FAIL
  TRN-HSTS-001    Header HSTS absent                          FAIL
  TRN-HSTS-002    HSTS max-age faible (< 1 an)                WARN

Headers (HDR-*) :
  HDR-CSP-001     CSP absente sur page HTML                   FAIL
  HDR-CSP-002     CSP trop permissive                         WARN
  HDR-NOSNIFF-001 X-Content-Type-Options absent               WARN
  HDR-SERVER-001  Banniere Server exposee                     WARN

Methodes HTTP (MTH-*) :
  MTH-OPTIONS-001 Methode OPTIONS activee                     INFO
  MTH-TRACE-001   Methode TRACE activee                       WARN
  MTH-PUT-001     Methode PUT activee                         WARN
  MTH-DELETE-001  Methode DELETE activee                      WARN
  MTH-PATCH-001   Methode PATCH activee                       WARN
  MTH-CONNECT-001 Methode CONNECT activee                     WARN

Exposition (EXR-*) :
  EXR-ADMIN-001   Chemin admin accessible sans auth           WARN
  EXR-SENSITIVE-001 Fichier sensible accessible (.env, .git)  FAIL

Fuites d'information (INF-*) :
  INF-BANNER-001  Bannieres serveur exposees                  WARN
  INF-ERROR-001   Messages d'erreur detailles                 WARN
  INF-STACK-001   Stack trace expose                          FAIL
  INF-ROBOTS-001  Fichier robots.txt present                  OK (info)
  INF-HEADER-001  Headers techniques bavards                  WARN


7. POLITIQUE DE CONFIANCE
================================================================================

+----------+-------------------------------------------------------------+
| Niveau   | Definition                                                  |
+----------+-------------------------------------------------------------+
| certain  | Preuve directe, non ambigue, lue telle quelle dans la       |
|          | reponse (header present/absent, code HTTP brut).            |
| high     | Preuve claire mais contexte indirect (methodes via OPTIONS, |
|          | cookie observe).                                            |
| medium   | Constat possiblement influence par un intermediaire (proxy, |
|          | WAF, tunnel).                                               |
| low      | Detection indirecte, contenu ambigu, ou situation           |
|          | catch_all_suspected.                                        |
+----------+-------------------------------------------------------------+

Degradations automatiques :
  - catch_all_suspected = true  => confiance plafonnee a low
  - proxy_suspected = true      => confiance plafonnee a medium
  - observed_access_state ambiguous => confiance plafonnee a low


8. DETECTION DE FAUX POSITIFS
================================================================================

Comportement catch-all :
  Avant de tester les chemins sensibles, Omega-scan genere un chemin
  aleatoire improbable. Si le serveur repond 200 OK dessus, la cible est
  marquee catch_all_suspected = true et tous les findings d'exposition
  sont degrades en confidence = low.

Authentification vs absence :
  Un chemin protege (401/403, redirection vers login) n'est ni marque
  comme absent ni comme expose. Il est marque N/A avec la note "chemin
  protege, presence non confirmable sans authentification".

Proxy / tunnel :
  Si des headers X-Forwarded-*, Via ou Forwarded sont detectes,
  proxy_suspected passe a true et les findings concernes (bannieres, TLS)
  voient leur confiance plafonnee a medium.


9. COMPATIBILITE TERMINAUX
================================================================================

Omega-scan detecte automatiquement les capacites du terminal et adapte
son affichage :

  Terminal           Couleurs  Emojis  Live    Mode recommande
  ------------------ --------- ------- ------- -------------------------
  Ghostty            24-bit    oui     oui     defaut
  Alacritty          24-bit    oui     oui     defaut
  WezTerm            24-bit    oui     oui     defaut
  Kitty              24-bit    oui     oui     defaut
  Konsole            256       oui     oui     defaut
  GNOME Terminal     256       oui     oui     defaut
  Terminator         256       oui     oui     defaut
  xfce4-terminal     256       oui     oui     defaut
  urxvt              256       non     oui     --no-emoji
  xterm              16        non     oui     --no-emoji --no-color
  Linux TTY          16        non     non     --plain
  SSH (moderne)      oui       partiel partiel --no-emoji
  SSH (ancien)       partiel   non     non     --plain


10. EXPORTS
================================================================================

Les rapports sont generes dans le dossier reports/ :

JSON - Source de verite :
  Structure complete : meta, target, connectivity, http, tls, findings,
  summary, errors. Strictement JSON-serializable, aucun objet Python brut.

Texte - Rapport humain compact :
  Lisible hors terminal, pas de codes ANSI, structure hierarchisee.

HTML - Rapport web lisible :
  Rapport autonome avec CSS inline, consultable dans n'importe quel
  navigateur. Partageable et archivable.


11. TESTS
================================================================================

    source .venv/bin/activate
    pytest tests/ -v

Tests couverts :
  - Parsing de cible (IPv4, IPv6, hostname, URL, ports, chemins)
  - Checks transport (HTTPS, HSTS, redirections)
  - Checks headers (CSP, nosniff, referrer, framing)
  - Checks methodes HTTP
  - Exporteurs (JSON, texte, HTML)
  - Detection catch-all
  - Categorisation des echecs reseau
  - Pipeline complet bout-en-bout


12. CRITERES DE REUSSITE DE LA V1
================================================================================

  - La cible est correctement interpretee, y compris derriere un proxy
  - Le scan termine proprement meme en cas d'echec partiel
  - Aucun finding d'exposition sans verification du comportement catch-all
  - Aucun chemin protege par auth confondu avec une absence
  - Le JSON exporte est propre, sans objets non serialisables
  - L'HTML et le texte sont consultables sans friction
  - Le resume permet de comprendre l'etat du service en moins de 10s
  - La suite de tests couvre le parsing, les regles principales, et au
    moins un scenario d'integration bout-en-bout


13. HORS PERIMETRE (rappel definitif)
================================================================================

  - Scan de CVE
  - Detection active de SQLi/XSS/RCE
  - Authentification complexe cote scanner
  - Crawling profond
  - Fuzzing
  - Bruteforce massif de chemins
  - Scan multi-cibles simultane
  - Parallelisme agressif
  - Dashboard web
  - Comparaison historique entre scans


================================================================================
  Omega-scan -- Observer, collecter, interpreter, rapporter.
  Un scanner de posture, pas un outil d'attaque.
================================================================================
