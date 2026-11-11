<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan.png" alt="Omega-Scan" width="512">
</div>

# 🔍 OMEGA-SCAN

**Scanner de posture de sécurité web**

> Élaboré par [kraynux](https://github.com/kraynux) pour [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Page officiel : [OMEGA-SCAN](https://kraynux.snake-mackarel.ts.net/omega-scan/) &nbsp; Apercu : [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-scan/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 Interface et rapports exportés disponibles en **17 langues** — voir [Langues de l'interface](#langues-de-linterface).  
**Langues :**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](docs/translation/en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](docs/translation/es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](docs/translation/pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](docs/translation/it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](docs/translation/de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](docs/translation/nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](docs/translation/pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](docs/translation/ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](docs/translation/zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](docs/translation/vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](docs/translation/th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](docs/translation/id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](docs/translation/ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](docs/translation/ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](docs/translation/hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](docs/translation/ar/README.md)

---

**Omega-scan** est un outil TUI + CLI qui analyse l'hygiène de configuration visible de vos services HTTP/HTTPS. Il observe, collecte des faits, applique des règles interprétatives et produit des rapports actionnables, sans jamais effectuer d'attaque active. Outil de la suite `omega-`, structuré en Clean Architecture — voir `ARCHITECTURE.md` pour le détail technique complet.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-scan/D.png" width="24%" />
</p>

## 1. Vision et périmètre

Omega-scan est un scanner de posture de sécurité web, destiné à un usage d'administration système : vérifier rapidement l'hygiène de configuration visible d'un service HTTP/HTTPS sur localhost, LAN, ou une cible externe, y compris derrière un tunnel comme Tailscale Funnel.

### Ce que fait Omega-scan

- Collecte des faits observables : headers, cookies, méthodes HTTP, TLS, chemins sensibles, en-têtes CORS.
- Applique des règles interprétatives déclaratives sur ces faits.
- Produit des findings homogènes, justifiés et actionnables.
- Restitue le résultat en TUI (Textual) ou en CLI scriptable, et via trois exports : JSON, texte, HTML.
- Détecte les faux positifs, notamment les comportements catch-all et les chemins protégés par authentification.
- S'adapte au contexte : proxy, tunnel, multi-vhost, SNI.
- Exige une confirmation d'autorisation explicite avant tout scan d'une cible non déjà épinglée-autorisée.
- Conserve un historique persistant des scans par cible, rejouable et comparable dans le temps.

### Ce qu'Omega-scan ne fait pas

- Scanner de vulnérabilités actives, pas de SQLi, XSS ou RCE.
- Scanner de CVE.
- Outil de bruteforce ou de fuzzing massif.
- Crawler profond.
- Outil multi-cibles parallèle agressif.
- Dashboard web.
- Authentification côté scanner.

## 2. Installation

### Prérequis

- Python 3.10+
- Connexion Internet, pour les dépendances et les scans externes

### Installation

L'archive officielle est fournie au format `.tar.gz`. Vérifiez son intégrité avant installation :

```bash
sha256sum omega-scan.tar.gz
```

### Méthode 1 — script d'installation

```bash
[ -d omega-scan ] && echo "ℹ️ Déjà extrait ici, étape ignorée." || tar -xzf omega-scan.tar.gz
[ -d ~/omega-scan ] && echo "ℹ️ ~/omega-scan existe déjà, déplacement ignoré." || mv omega-scan ~/
cd ~/omega-scan/
chmod +x install.sh
./install.sh
```

### Méthode 2 — installation complète résiliente



```bash
( [ -d omega-scan ] || tar -xzf omega-scan.tar.gz ) && \
( [ -d ~/omega-scan ] || mv omega-scan ~/ ) && \
cd ~/omega-scan && chmod +x install.sh && ./install.sh
```

`install.sh` :

1. Crée l'environnement virtuel `.venv` s'il n'existe pas déjà.
2. Installe les dépendances (`pip install -e .`, `pyproject.toml` reste l'unique source de vérité).
3. Rend `omega-scan.sh` et `install.sh` exécutables.
4. Ajoute l'alias `scan` à `~/.bashrc` et `~/.zshrc` (sans doublon si déjà présent).

### Dépendances

Déclarées dans `pyproject.toml` (plus de `requirements.txt`) :
- `textual` : interface TUI, thèmes, adaptation automatique au terminal
- `httpx` : client HTTP/HTTPS moderne
- `jinja2` : templating pour l'export HTML
- Dépendances de développement (`pip install -e ".[dev]"`) : `pytest`, `pytest-asyncio`, `pytest-httpserver`, `trustme`, `ruff`, `mypy`, `import-linter`

## 3. Utilisation

### Mode interactif (TUI)

Recommandé pour l'usage quotidien — lancé sans argument :

```bash
./omega-scan.sh
```

Parcours : écran de démarrage (se ferme sur une touche ou un clic) → menu principal → saisie de la cible et choix du profil (avec confirmation d'autorisation si la cible n'est pas déjà épinglée) → scan (jauge de progression et détail des opérations réseau affichés en direct) → résultats (note globale, findings filtrables par catégorie, détail au clic sur une ligne) → export/historique/comparaison depuis le menu principal. L'adaptation au terminal (couleurs, taille, dégradation structurelle) est automatique, plus besoin de flags d'affichage manuels.

#### Raccourcis clavier

| Touche | Action |
|---|---|
| `↑` / `↓` | Naviguer entre les éléments d'un écran |
| `Tab` / `Maj+Tab` | Naviguer entre les champs d'un formulaire |
| `Échap` | Retour à l'écran précédent (confirmation de sortie sur l'accueil) |
| `t` | Thème suivant (appliqué immédiatement, sans confirmation) |
| `r` | Rafraîchir la détection du terminal |
| `a` | Afficher l'aide |
| `q` | Quitter (avec confirmation) |

### Langues de l'interface

L'interface est disponible en 17 langues : français, anglais, espagnol, portugais (Brésil), italien, allemand, néerlandais, polonais, russe, chinois simplifié, vietnamien, thaï, indonésien, japonais, coréen, hindi et arabe. Le choix se fait dans les Réglages (« Langue / Language ») et s'applique après un redémarrage de l'interface ; la variable `OMEGA_SCAN_LANG` (par exemple `OMEGA_SCAN_LANG=en ./omega-scan.sh`) force une langue le temps d'une session. Lancé depuis omega-suite, omega-scan prend la langue de la suite. Sur une console texte Linux (TTY), les langues à écriture non latine s'affichent en anglais pour la session. La ligne de commande reste en français.

### Contact et support

L'aide (touche `a`) propose un écran **Contact et support** : *Payer un café* (page PayPal du développeur), *Contacter le support* (adresse mail et formulaire de contact du site, affichés en clair), *Se déclarer utilisateur (anonyme)* et *Vérifier les mises à jour*. La déclaration est volontaire, désactivée par défaut et envoyée une seule fois : elle sert seulement à compter les utilisateurs et, si on le souhaite, leur continent ou leur pays (listes fermées, jamais de texte libre). Elle envoie une clé tirée au hasard, le nom du logiciel (`omega-scan`) et sa version ; jamais de nom, de nom de machine, de réglage, de cible ni de résultat. L'adresse IP n'est pas enregistrée dans les déclarations, mais passe, comme toute visite, par les contrôles de sécurité et le journal du serveur de réception. Retrait à tout moment depuis le même écran (*Ne plus me déclarer*). La vérification des mises à jour lit seulement la liste des versions publiées sur le site, et jamais sans clic.

### Mode scriptable (CLI)

Toute sous-commande déclenche le mode CLI (texte simple, ou JSON avec `--json`) :

```bash
# Scanner une cible (--authorize requis si la cible n'est pas déjà épinglée)
./omega-scan.sh scan example.org --profile standard --authorize
./omega-scan.sh scan 192.168.1.10 --profile local-lab --authorize --json

# Historique
./omega-scan.sh history list --host example.org
./omega-scan.sh history show scan-30577411758e
./omega-scan.sh history compare scan-aaa scan-bbb
./omega-scan.sh history replay scan-30577411758e

# Export
./omega-scan.sh export scan-30577411758e --format html --output rapport.html

# Cibles épinglées-autorisées (dispense de --authorize sur les scans suivants)
./omega-scan.sh targets pin example.org --note "accord client 2026-08"
./omega-scan.sh targets unpin example.org
./omega-scan.sh targets list
```

### Garde d'autorisation de cible

Aucun scan ne démarre sans confirmation explicite d'autorisation sur la cible (case à cocher en TUI, `--authorize` en CLI), sauf cible déjà épinglée. Vérifiée côté application (`application/pipeline/guards/authorization_guard.py`), pas seulement côté interface.

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
| Sonde CORS | Non | Oui | Oui | Oui |
| Catch-all | - | Oui | Oui | Oui |
| Politique HSTS | Non évaluée | Standard | Strict | Tolérante |

### Quand utiliser quel profil

- `quick` : vérification éclair avant mise en production
- `standard` : audit complet d'un service en production, recommandé
- `extended` : audit approfondi incluant les méthodes HTTP risquées
- `local-lab` : scan de localhost ou LAN sans pénaliser les règles pensées pour le public, HSTS notamment

## 5. Architecture

Omega-scan est structuré en **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alignée sur le gabarit de la suite `omega-` (voir `omega-stress`). Le détail complet — arborescence, règles de dépendance, chaînes fonctionnelles, hiérarchie d'exceptions, taxonomie de nommage — vit dans **`ARCHITECTURE.md`**, document normatif de référence.

Vue d'ensemble très courte :

```text
src/omega_scan/
├── domain/          Logique métier pure (cibles, profils, scans, checks, reports, thèmes...)
├── application/     Cas d'usage (commands/queries), pipeline d'exécution, gardes
├── ports/           Contrats attendus par l'application (probers, repositories, exporters...)
├── infrastructure/  Implémentations concrètes (httpx, SQLite, Textual n'est PAS ici)
├── interfaces/      tui/ (Textual) et cli/ (scriptable), à parité fonctionnelle stricte
├── app/             Assemblage (DependencyContainer, bootstrap, cycle de vie)
├── core/, shared/   Vocabulaire transverse, utilitaires non métier
└── plugins/         Structure posée, vide (aucun axe d'extension confirmé)
```

Règles de conception inchangées depuis la v1 :
- `domain/checks/` : juge à partir des preuves, ne fait jamais de réseau.
- `infrastructure/network/` : fait du réseau, ne juge jamais.
- `interfaces/` : affiche, ne contient aucune logique métier.
- `infrastructure/exporters/` : lisent le résultat de scan, ne recalculent rien.

## 6. Taxonomie des règles

### Transport, `TRN-*`

- `TRN-HTTP-001` : HTTP accessible sans redirection HTTPS, `WARN`
- `TRN-HTTPS-001` : HTTPS non accessible, `FAIL`
- `TRN-HSTS-001` : header HSTS absent, `FAIL`
- `TRN-HSTS-002` : HSTS `max-age` faible, inférieur à 1 an, `WARN`

### Profondeur TLS, `TLS-*`

- `TLS-VERSION-001` : protocole TLS obsolète (< TLSv1.2), `FAIL`
- `TLS-CIPHER-001` : suite cryptographique manifestement faible (RC4, DES, NULL, EXPORT, MD5), `WARN`

### Headers, `HDR-*`

- `HDR-CSP-001` : CSP absente sur page HTML, `FAIL`
- `HDR-CSP-002` : CSP trop permissive, `WARN`
- `HDR-NOSNIFF-001` : `X-Content-Type-Options` absent, `WARN`
- `HDR-SERVER-001` : bannière `Server` exposée, `WARN`
- `HDR-CACHE-001` : `Cache-Control` absent ou permissif sur une page HTML, `WARN`

### Cookies, `COO-*`

- `COO-SECURE-001` : cookie sur réponse HTTPS sans attribut `Secure`, `WARN`
- `COO-HTTPONLY-001` : cookie sans attribut `HttpOnly`, `WARN`
- `COO-SAMESITE-001` : `SameSite` absent, ou `None` sans `Secure`, `WARN`

### CORS, `COR-*`

- `COR-WILDCARD-CREDENTIALS-001` : `Access-Control-Allow-Origin: *` combiné à `Access-Control-Allow-Credentials: true`, `FAIL`
- `COR-REFLECTED-ORIGIN-001` : origine arbitraire reflétée telle quelle dans `Access-Control-Allow-Origin`, `WARN`

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
- `INF-SECURITYTXT-001` : fichier `/.well-known/security.txt` présent, `OK` info

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

Le TUI (Textual) détecte automatiquement les capacités du terminal (couleur, taille) et adapte sa feuille de style structurelle en conséquence (`complete`/`standard`/`reduced`/`mono`) — plus de flags manuels (`--no-emoji`, `--no-color`, `--plain`) comme en v1. Le mode CLI reste toujours en texte simple (ou `--json`), indépendant du terminal.

## 10. Exports

Les rapports texte et HTML s'écrivent dans la langue choisie dans les Réglages (« Langue des exports », par défaut celle de l'interface) ; le JSON reste une donnée, non traduite. Les rapports sont générés dans `var/exports/` par défaut (chemin runtime, voir `ARCHITECTURE.md`), ou au chemin indiqué (`--output` en CLI, boîte de dialogue en TUI).

### JSON, source de vérité

Structure complète du scan (`ScanRun`), strictement JSON-serializable.

### Texte, rapport humain compact

Lisible hors terminal, sans codes ANSI, avec structure hiérarchisée.

### HTML, rapport web lisible

Rapport autonome avec CSS inline, consultable dans n'importe quel navigateur, partageable et archivable.

## 11. Historique et comparaison

Chaque scan est persisté (SQLite, `var/db/app.db`) : historique consultable par cible, détail d'un run passé, comparaison entre deux scans (findings apparus / résolus / inchangés / changés), et rejeu d'un scan sur la même cible sans ressaisie — absents de la v1, ajoutés lors de la migration vers Clean Architecture.

## 12. Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

Structure : `tests/unit/` (domaine et application, sans I/O réelle), `tests/integration/` (SQLite/fichiers réels, serveur HTTP factice `pytest-httpserver`), `tests/e2e/` (CLI et TUI de bout en bout, `Textual.testing`).

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

---

> Omega-scan — Observer, collecter, interpréter, rapporter.  
> Un scanner de posture, pas un outil d'attaque.
