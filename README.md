# OMEGA-SCAN

**Scanner de posture de sécurité web**

Élaboré par kraynux pour Omega-server
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)
Page officiel :
[OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) 
Apercu :
[Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)

---

Omega-scan est un outil en ligne de commande qui analyse l'hygiène de configuration visible de vos services HTTP/HTTPS. Il observe, collecte des faits, applique des règles interprétatives et produit des rapports actionnables, sans jamais effectuer d'attaque active.

## 1. Vision et périmètre

Omega-scan est un scanner de posture de sécurité web, destiné à un usage d'administration système : vérifier rapidement l'hygiène de configuration visible d'un service HTTP/HTTPS sur localhost, LAN, ou une cible externe, y compris derrière un tunnel comme Tailscale Funnel.

### Ce que fait Omega-scan

- Collecte des faits observables : headers, cookies, méthodes HTTP, TLS, chemins sensibles.
- Applique des règles interprétatives déclaratives sur ces faits.
- Produit des findings homogènes, justifiés et actionnables.
- Restitue le résultat en console avec Rich et via trois exports : JSON, texte, HTML.
- Détecte les faux positifs, notamment les comportements catch-all et les chemins protégés par authentification.
- S'adapte au contexte : proxy, tunnel, multi-vhost, SNI.

### Ce qu'Omega-scan ne fait pas

- Scanner de vulnérabilités actives, pas de SQLi, XSS ou RCE.
- Scanner de CVE.
- Outil de bruteforce ou de fuzzing massif.
- Crawler profond.
- Outil multi-cibles parallèle agressif.
- Dashboard web.
- Authentification côté scanner.
- Comparaison historique entre scans, prévue en évolution future.

## 2. Installation

### Prérequis

- Python 3.10+
- Connexion Internet, pour les dépendances et les scans externes

### Installation rapide

```# 1. Création du dossier parent et on s'y place
mkdir -p ~/SCANNER/
cd ~/SCANNER/

# [Déposer le dossier "omega-scan" dans le dossier SCANNER]

# 2. On entre dans le projet
cd omega-scan/

# 3. Création du venv AU BON ENDROIT
python -m venv .venv

# 4. Activation et installation des dépendances
source .venv/bin/activate
pip install -r requirements.txt

# 5. Rendre le script de départ exécutable
chmod +x omega-scan.sh
  
```

### Dépendances

- `rich` : interface console, couleurs, tableaux, progressions
- `httpx` : client HTTP/HTTPS moderne
- `jinja2` : templating pour l'export HTML
- `pytest` : framework de tests
- `pytest-httpserver` : serveur HTTP factice pour les tests
- `trustme` : génération de certificats TLS de test

## 3. Utilisation

### Mode interactif

Recommandé pour l'usage quotidien :

```bash
./omega-scan.sh
```

### Parcours guidé

1. Accueil
2. Saisie de la cible, IPv4, IPv6, hostname ou URL complète
3. Choix du profil : `quick`, `standard`, `extended`, `local-lab`
4. Confirmation avant lancement
5. Scan avec barre de progression en temps réel
6. Résumé, note globale et ventilation par statut et sévérité
7. Actions : détail par catégorie, export, relancer, retour

### Mode non interactif

Pour scripts ou CI :

```bash
./omega-scan.sh --target example.org --profile standard
./omega-scan.sh --target 192.168.1.10 --profile local-lab
```

### Options d'affichage

- `--help`, `-h` : affiche l'aide complète
- `--plain`, `-p` : mode texte simple, sans Rich, compatible tous terminaux
- `--no-color` : désactive les couleurs
- `--no-emoji` : désactive les emojis
- `--no-live` : désactive les animations Live
- `--target`, `-t URL` : cible directe, mode non interactif
- `--profile NAME` : profil parmi `quick`, `standard`, `extended`, `local-lab`

### Formats de cible acceptés

```text
192.168.1.10                IPv4
192.168.1.10:8080           IPv4 avec port
::1                         IPv6
[2001:db8::10]:8443         IPv6 avec crochets et port
example.org                 Hostname
intranet.lan:8080/admin     Hostname avec port et chemin
http://example.org          URL HTTP
https://example.org/admin   URL HTTPS
```

## 4. Profils de scan

| Paramètre | `quick` | `standard` | `extended` | `local-lab` |
|---|---|---|---|---|
| Usage | Vérif. rapide | Complet (défaut) | Approfondi | localhost / LAN |
| Timeout connect/read | 3s / 6s | 3s / 6s | 5s / 10s | 3s / 6s |
| Méthodes HTTP | OPTIONS | OPTIONS, TRACE | OPTIONS, TRACE, PUT, DELETE, PATCH | OPTIONS, TRACE |
| Path probing | Non | Oui (~20) | Oui (complet) | Oui (~20) |
| TLS | Non | Oui | Oui (détaillé) | Oui (tolérant) |
| Catch-all | - | Oui | Oui | Oui |
| Politique HSTS | Non évaluée | Standard | Strict | Tolérante |

### Quand utiliser quel profil

- `quick` : vérification éclair avant mise en production
- `standard` : audit complet d'un service en production, recommandé
- `extended` : audit approfondi incluant les méthodes HTTP risquées
- `local-lab` : scan de localhost ou LAN sans pénaliser les règles pensées pour le public, HSTS notamment

## 5. Architecture

```text
omega-scan/
|-- main.py                    Point d'entrée, parsing CLI
|-- omega-scan.sh              Script de lancement, activation venv
|-- requirements.txt           Dépendances figées
|
|-- config/                    Configuration et constantes
|   |-- defaults.py            Timeouts, user-agent, throttling
|   |-- profiles.py            Profils quick/standard/extended/local-lab
|   +-- paths.py               Listes de chemins admin/sensibles
|
|-- core/                      Socle d'exécution
|   |-- pipeline.py            Orchestration du scan complet
|   |-- target_parser.py       Normalisation des cibles
|   |-- context.py             Contexte de scan, meta, erreurs
|   |-- errors.py              Classification des erreurs
|   |-- logger.py              Journalisation technique
|   +-- serialization.py       Conversion JSON centralisée
|
|-- models/                    Objets métier, données sans logique
|   |-- target.py              Cible canonique
|   |-- finding.py             Finding, règle + preuve + interprétation
|   |-- scan_result.py         Résultat complet du scan
|   |-- summary.py             Résumé calculé
|   +-- evidence.py            Preuve attachée à un finding
|
|-- collectors/                Font du réseau, ne jugent jamais
|   |-- connectivity.py        Pré-scan DNS/HTTP/HTTPS
|   |-- http_probe.py          Collecte HTTP/HTTPS principale
|   |-- tls_probe.py           Collecte TLS, certificat, SNI
|   |-- path_probe.py          Path probing + détection catch-all
|   +-- methods_probe.py       Test des méthodes HTTP
|
|-- normalizers/               Nettoient et homogénéisent
|   |-- headers.py             content_profile, proxy_suspected
|   |-- cookies.py             Normalisation des cookies
|   +-- redirects.py           Chaîne de redirections
|
|-- checks/                    Jugent à partir des preuves, pas de réseau
|   |-- base.py                Infrastructure des checks
|   |-- transport.py           TRN-* : HTTPS, HSTS, redirections
|   |-- headers.py             HDR-* : CSP, nosniff, referrer, framing
|   |-- methods.py             MTH-* : OPTIONS, TRACE, PUT, DELETE...
|   |-- exposure.py            EXR-* : chemins admin, fichiers sensibles
|   +-- information_leaks.py   INF-* : bannières, stack traces, robots
|
|-- exporters/                 Lisent scan_result, ne recalculent rien
|   |-- json_exporter.py       Export JSON source de vérité
|   |-- text_exporter.py       Rapport humain compact
|   +-- html_exporter.py       Rapport web, Jinja2 + CSS inline
|
|-- ui/                        Affiche, pas de logique métier
|   |-- app.py                 Application console interactive
|   |-- screens.py             Écrans, accueil, fin de scan
|   |-- prompts.py             Saisies et menus
|   |-- tables.py              Tableaux de findings
|   |-- panels.py              Panneaux d'information
|   |-- progress.py            Barre de progression
|   +-- compat.py              Détection et compatibilité terminaux
|
|-- reports/                   Dossier de sortie des exports
|
+-- tests/                     Tests unitaires et d'intégration
```

### Règles de conception

- `collectors/` : fait du réseau, ne juge jamais
- `normalizers/` : nettoie et homogénéise, ne juge jamais
- `checks/` : juge à partir des preuves, ne fait jamais de réseau
- `ui/` : affiche, ne contient aucune logique métier
- `exporters/` : lisent `scan_result`, ne recalculent rien

## 6. Taxonomie des règles

### Transport, `TRN-*`

- `TRN-HTTP-001` : HTTP accessible sans redirection HTTPS, `WARN`
- `TRN-HTTPS-001` : HTTPS non accessible, `FAIL`
- `TRN-HSTS-001` : header HSTS absent, `FAIL`
- `TRN-HSTS-002` : HSTS `max-age` faible, inférieur à 1 an, `WARN`

### Headers, `HDR-*`

- `HDR-CSP-001` : CSP absente sur page HTML, `FAIL`
- `HDR-CSP-002` : CSP trop permissive, `WARN`
- `HDR-NOSNIFF-001` : `X-Content-Type-Options` absent, `WARN`
- `HDR-SERVER-001` : bannière `Server` exposée, `WARN`

### Méthodes HTTP, `MTH-*`

- `MTH-OPTIONS-001` : méthode OPTIONS activée, `INFO`
- `MTH-TRACE-001` : méthode TRACE activée, `WARN`
- `MTH-PUT-001` : méthode PUT activée, `WARN`
- `MTH-DELETE-001` : méthode DELETE activée, `WARN`
- `MTH-PATCH-001` : méthode PATCH activée, `WARN`
- `MTH-CONNECT-001` : méthode CONNECT activée, `WARN`

### Exposition, `EXR-*`

- `EXR-ADMIN-001` : chemin admin accessible sans auth, `WARN`
- `EXR-SENSITIVE-001` : fichier sensible accessible, `.env`, `.git`, `FAIL`

### Fuites d'information, `INF-*`

- `INF-BANNER-001` : bannières serveur exposées, `WARN`
- `INF-ERROR-001` : messages d'erreur détaillés, `WARN`
- `INF-STACK-001` : stack trace exposée, `FAIL`
- `INF-ROBOTS-001` : fichier `robots.txt` présent, `OK` info
- `INF-HEADER-001` : headers techniques bavards, `WARN`

## 7. Politique de confiance

| Niveau | Définition |
|---|---|
| `certain` | Preuve directe, non ambiguë, lue telle quelle dans la réponse, header présent ou absent, code HTTP brut. |
| `high` | Preuve claire mais contexte indirect, méthodes via OPTIONS, cookie observé. |
| `medium` | Constat possiblement influencé par un intermédiaire, proxy, WAF, tunnel. |
| `low` | Détection indirecte, contenu ambigu, ou situation `catch_all_suspected`. |

### Dégradations automatiques

- `catch_all_suspected = true` : confiance plafonnée à `low`
- `proxy_suspected = true` : confiance plafonnée à `medium`
- `observed_access_state = ambiguous` : confiance plafonnée à `low`

## 8. Détection de faux positifs

### Comportement catch-all

Avant de tester les chemins sensibles, Omega-scan génère un chemin aléatoire improbable. Si le serveur répond `200 OK` dessus, la cible est marquée `catch_all_suspected = true` et tous les findings d'exposition sont dégradés en `confidence = low`.

### Authentification vs absence

Un chemin protégé, `401`, `403`, ou redirection vers login, n'est ni marqué comme absent ni comme exposé. Il est marqué `N/A` avec la note : « chemin protégé, présence non confirmable sans authentification ».

### Proxy / tunnel

Si des headers `X-Forwarded-*`, `Via` ou `Forwarded` sont détectés, `proxy_suspected` passe à `true` et les findings concernés, bannières, TLS, voient leur confiance plafonnée à `medium`.

## 9. Compatibilité terminaux

Omega-scan détecte automatiquement les capacités du terminal et adapte son affichage.

| Terminal | Couleurs | Emojis | Live | Mode recommandé |
|---|---|---|---|---|
| Ghostty | 24-bit | oui | oui | défaut |
| Alacritty | 24-bit | oui | oui | défaut |
| WezTerm | 24-bit | oui | oui | défaut |
| Kitty | 24-bit | oui | oui | défaut |
| Konsole | 256 | oui | oui | défaut |
| GNOME Terminal | 256 | oui | oui | défaut |
| Terminator | 256 | oui | oui | défaut |
| xfce4-terminal | 256 | oui | oui | défaut |
| urxvt | 256 | non | oui | `--no-emoji` |
| xterm | 16 | non | oui | `--no-emoji --no-color` |
| Linux TTY | 16 | non | non | `--plain` |
| SSH moderne | oui | partiel | partiel | `--no-emoji` |
| SSH ancien | partiel | non | non | `--plain` |

## 10. Exports

Les rapports sont générés dans le dossier `reports/`.

### JSON, source de vérité

Structure complète : `meta`, `target`, `connectivity`, `http`, `tls`, `findings`, `summary`, `errors`. Strictement JSON-serializable, sans objet Python brut.

### Texte, rapport humain compact

Lisible hors terminal, sans codes ANSI, avec structure hiérarchisée.

### HTML, rapport web lisible

Rapport autonome avec CSS inline, consultable dans n'importe quel navigateur, partageable et archivable.

## 11. Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

### Tests couverts

- Parsing de cible, IPv4, IPv6, hostname, URL, ports, chemins
- Checks transport, HTTPS, HSTS, redirections
- Checks headers, CSP, nosniff, referrer, framing
- Checks méthodes HTTP
- Exporteurs, JSON, texte, HTML
- Détection catch-all
- Catégorisation des échecs réseau
- Pipeline complet bout-en-bout

## 12. Critères de réussite de la v1

- La cible est correctement interprétée, y compris derrière un proxy
- Le scan termine proprement même en cas d'échec partiel
- Aucun finding d'exposition sans vérification du comportement catch-all
- Aucun chemin protégé par auth confondu avec une absence
- Le JSON exporté est propre, sans objets non sérialisables
- L'HTML et le texte sont consultables sans friction
- Le résumé permet de comprendre l'état du service en moins de 10 secondes
- La suite de tests couvre le parsing, les règles principales, et au moins un scénario d'intégration bout-en-bout

## 13. Hors périmètre

- Scan de CVE
- Détection active de SQLi, XSS, RCE
- Authentification complexe côté scanner
- Crawling profond
- Fuzzing
- Bruteforce massif de chemins
- Scan multi-cibles simultané
- Parallélisme agressif
- Dashboard web
- Comparaison historique entre scans

---

> Omega-scan — Observer, collecter, interpréter, rapporter.  
> Un scanner de posture, pas un outil d'attaque.
