# Omega-Scan — Charte d'architecture technique complète

Ce document est normatif. Toute règle qu'il contient prime sur une préférence individuelle ou une facilité ponctuelle de développement. Une dérogation doit être proposée comme modification tracée de cette charte (voir §12), jamais faite silencieusement dans le code.

## 0. Portée et généalogie

La suite `omega-` prévoit 4 outils d'administration système en terminal. `omega-fire` (pare-feu/fail2ban/monitoring) est le premier, en v3.0, terminé. `omega-stress` (test de charge HTTP) est le deuxième, terminé, et sert de gabarit de référence pour toute la suite. `omega-scan` est le troisième : scanner de posture de sécurité web, déjà fonctionnel en v1 (architecture à plat, interface Rich) au moment où cette charte est rédigée — décision prise le 2026-08-26 de le faire migrer vers le gabarit d'`omega-stress` plutôt que de laisser divergentes trois architectures dans la même suite, à l'approche de l'interface unificatrice prévue une fois les 4 outils terminés.

Cette charte est **directement dérivée de celle d'omega-stress** (`STRESS/omega-stress/ARCHITECTURE.md`), elle-même alignée sur omega-fire — même patron à 9 paquets racine, même Dependency Rule, même split CQRS, même pipeline `executor/planner/steps/guards/hooks`. Elle en reprend la lettre partout où le domaine du scan ne justifie pas un écart, et documente chaque écart ci-dessous, daté.

**Ce qui est repris à l'identique** : les 9 paquets racine (`app/`, `application/`, `core/`, `domain/`, `infrastructure/`, `interfaces/`, `plugins/`, `ports/`, `shared/`), la Dependency Rule, le split `commands/`/`queries/`, la hiérarchie d'exceptions par couche, le principe « toute action importante passe par le pipeline », le catalogue de thèmes partagé, les deux adaptateurs `interfaces/tui/` (Textual) et `interfaces/cli/` à parité stricte.

**Ce qui est adapté au domaine du scan de sécurité passif** — chaque écart est justifié et daté :

| Écart | Raison | Date |
|---|---|---|
| Le mot `scan` reste utilisé normalement dans tout le code (`run_scan`, `domain/scans/`, `ScanRun`…) | La règle omega-stress §6 qui bannit ce mot est propre à omega-stress, où elle évite une confusion avec son concept interne de « pré-check ». Chez omega-scan, « scan » **est** le nom du domaine métier lui-même — l'interdire serait absurde. Chaque outil de la suite garde le vocabulaire de son propre domaine. | 2026-08-26 |
| Pas de `core/capability_registry.py` pour une capacité système locale (CPU/RAM/fd) | Omega-scan ne génère pas de charge locale à surveiller pour goulot d'étranglement : il émet des requêtes HTTP ponctuelles et légères. Seule la capacité **terminal** (couleur, taille, emoji) est pertinente ici. `core/capability.py` et `domain/terminal/` suffisent ; pas de `infrastructure/probe/` système. | 2026-08-26 |
| `application/pipeline/guards/authorization_guard.py` porte sur l'**autorisation de la cible**, pas sur une charge | Reprend le même nom et le même rôle que chez omega-stress (cible confirmée ou épinglée avant action), mais la légitimité ici est « ai-je le droit d'observer ce service » plutôt que « ai-je le droit de le charger ». Sémantique proche, guard identique dans sa position pipeline. | 2026-08-26 |
| Pas de `guards/threshold_guard.py` ni `pipeline/abort.py` | Un scan ne s'arrête jamais en cours sur dépassement de seuil : il n'y a pas de charge cumulative à surveiller. Un prober qui échoue (timeout, TLS KO) est catégorisé en erreur partielle et le scan continue sur ce qui est testable (`domain/scans/` gère les verdicts `completed`/`partial`/`failed`, pas un arrêt automatique). | 2026-08-26 |
| `guards/precheck_guard.py` absent | Le pré-check n'a pas de sens ici : un scan **est** déjà l'action la plus légère de la suite, il n'y a rien de plus risqué en amont à valider avant de le déclencher (contrairement à un test de charge Haut/Maximum chez omega-stress). | 2026-08-26 |
| `ports/` éclaté en 5 probers (`connectivity_prober`, `http_prober`, `tls_prober`, `path_prober`, `methods_prober`) plutôt qu'un unique port comme `load_runner` | Le scan a 5 sous-collectes réseau indépendantes et déjà séparées dans le code v1 (`collectors/*.py`) ; un port unique masquerait cette séparation testable module par module, alors qu'omega-stress n'a qu'une seule famille de charge à générer. | 2026-08-26 |
| `infrastructure/storage/sqlite/` et l'historique/comparaison de scans **n'existaient pas en v1** | Ajout délibéré lors de la migration (voir `docs/decisions/` et le plan de migration) : la comparaison de scans dans le temps était déjà notée comme évolution future dans les documents de conception d'origine (`SCAN/dev/document-unique-projet.md` §20), jamais implémentée faute de socle Clean Architecture pour l'accueillir proprement. | 2026-08-26 |
| `domain/checks/` compte 8 sous-paquets (les 6 catégories v1 + `cors/` + `tls_depth/`, nouveaux) | Upgrade fonctionnelle actée avec l'utilisateur lors de la migration : nouvelles règles passives (CORS, Cache-Control, security.txt, profondeur TLS), toujours sans scan actif — le hors-périmètre v1 (§13 du README) reste inchangé. | 2026-08-26 |
| `plugins/` présent mais **vide** | Même raison que chez omega-stress : aucun axe d'extension identifié, structure posée pour cohérence de suite. | 2026-08-26 |

Aucune extraction en paquet partagé (`omega-shared`) n'est faite à ce stade : le catalogue de thèmes est un point commun de fait (voir §8), pas le code d'architecture lui-même — cohérent avec la position déjà prise par omega-stress vis-à-vis d'omega-fire.

---

## 1. Contexte et objectif

Omega-Scan est une application locale TUI + CLI de scan de posture de sécurité web (headers, cookies, méthodes HTTP, TLS, chemins sensibles, fuites d'information), écrite en Python, structurée selon **Clean Architecture** et **Ports & Adapters**, alignée sur le gabarit de suite `omega-`. C'est un scanner d'observation passive : il ne teste jamais activement une vulnérabilité (pas de SQLi/XSS/RCE/CVE/fuzzing — voir README §13, inchangé par cette migration).

Objectif architectural principal : garder un **cœur métier stable, testable et indépendant** des détails techniques comme `httpx`, `sqlite3`, `Textual` ou le format d'export.

Règle directrice : **les dépendances de code pointent toujours vers l'intérieur**. Aucune couche interne ne doit connaître une couche plus externe.

## 2. Arborescence du projet

```text
omega-scan/
├── pyproject.toml
├── README.md
├── ARCHITECTURE.md
├── LICENCE
├── .gitignore
├── src/
│   └── omega_scan/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app/
│       │   ├── bootstrap.py
│       │   ├── dependency_container.py
│       │   └── lifecycle.py
│       ├── core/
│       │   ├── capability.py
│       │   ├── constants.py
│       │   ├── enums.py
│       │   ├── exceptions.py
│       │   ├── models.py
│       │   ├── results.py
│       │   └── audit.py
│       ├── domain/
│       │   ├── errors.py
│       │   ├── targets/
│       │   │   ├── models.py
│       │   │   ├── service.py
│       │   │   ├── validation.py
│       │   │   └── exceptions.py
│       │   ├── profiles/
│       │   │   ├── models.py
│       │   │   └── policies.py
│       │   ├── scans/
│       │   │   ├── models.py
│       │   │   ├── service.py
│       │   │   └── exceptions.py
│       │   ├── findings/
│       │   │   ├── models.py
│       │   │   └── evidence.py
│       │   ├── checks/
│       │   │   ├── transport/{service.py,policies.py}
│       │   │   ├── headers/{service.py,policies.py}
│       │   │   ├── cookies/{service.py,policies.py}
│       │   │   ├── methods/{service.py,policies.py}
│       │   │   ├── exposure/{service.py,policies.py}
│       │   │   ├── information_leaks/{service.py,policies.py}
│       │   │   ├── cors/{service.py,policies.py}
│       │   │   └── tls_depth/{service.py,policies.py}
│       │   ├── reports/
│       │   │   ├── models.py
│       │   │   ├── service.py
│       │   │   └── comparison.py
│       │   ├── terminal/
│       │   │   ├── models.py
│       │   │   ├── policies.py
│       │   │   └── service.py
│       │   └── theme/
│       │       ├── models.py
│       │       ├── policies.py
│       │       └── service.py
│       ├── application/
│       │   ├── exceptions.py
│       │   ├── commands/
│       │   │   ├── pin_target.py
│       │   │   ├── unpin_target.py
│       │   │   ├── confirm_target_authorization.py
│       │   │   ├── run_scan.py
│       │   │   ├── replay_scan.py
│       │   │   ├── export_scan_report.py
│       │   │   ├── select_theme.py
│       │   │   └── select_render_profile.py
│       │   ├── queries/
│       │   │   ├── list_targets.py
│       │   │   ├── list_scan_history.py
│       │   │   ├── get_scan_details.py
│       │   │   ├── compare_scans.py
│       │   │   ├── list_profiles.py
│       │   │   └── detect_terminal.py
│       │   ├── dto/
│       │   │   └── mappers.py
│       │   ├── pipeline/
│       │   │   ├── executor.py
│       │   │   ├── steps.py
│       │   │   ├── guards/
│       │   │   │   ├── authorization_guard.py
│       │   │   │   └── capability_guard.py
│       │   │   └── hooks/
│       │   │       ├── audit_hook.py
│       │   │       └── notification_hook.py
│       │   └── services/
│       │       ├── scan_history_service.py
│       │       ├── scan_replayer.py
│       │       ├── scan_comparison_service.py
│       │       └── theme_selection_service.py
│       ├── ports/
│       │   ├── target_repository.py
│       │   ├── scan_repository.py
│       │   ├── connectivity_prober.py
│       │   ├── http_prober.py
│       │   ├── tls_prober.py
│       │   ├── path_prober.py
│       │   ├── methods_prober.py
│       │   ├── report_exporter.py
│       │   ├── terminal_detector.py
│       │   ├── settings_store.py
│       │   └── scan_progress_notifier.py
│       ├── infrastructure/
│       │   ├── exceptions.py
│       │   ├── config/
│       │   │   ├── defaults.py
│       │   │   ├── loader.py
│       │   │   ├── env.py
│       │   │   └── paths.py
│       │   ├── resources/
│       │   │   ├── admin_paths.txt
│       │   │   ├── backup_suffixes.txt
│       │   │   ├── expected_headers.txt
│       │   │   ├── sensitive_paths.txt
│       │   │   └── method_policy.json
│       │   ├── storage/
│       │   │   ├── sqlite/
│       │   │   │   ├── connection.py
│       │   │   │   ├── schema.py
│       │   │   │   ├── migrations.py
│       │   │   │   ├── target_repository.py
│       │   │   │   └── scan_repository.py
│       │   │   └── files/
│       │   │       └── json_settings_store.py
│       │   ├── network/
│       │   │   ├── httpx_connectivity_prober.py
│       │   │   ├── httpx_http_prober.py
│       │   │   ├── httpx_tls_prober.py
│       │   │   ├── httpx_path_prober.py
│       │   │   └── httpx_methods_prober.py
│       │   ├── exporters/
│       │   │   ├── json_exporter.py
│       │   │   ├── text_exporter.py
│       │   │   ├── html_exporter.py
│       │   │   ├── html_theme_resolver.py
│       │   │   └── templates/
│       │   │       └── report.html.jinja
│       │   ├── terminal/
│       │   │   ├── raw_capabilities.py
│       │   │   ├── detector.py
│       │   │   └── fallback_resolver.py
│       │   └── logging/
│       │       ├── app_logger.py
│       │       ├── audit_logger.py
│       │       └── config.py
│       ├── interfaces/
│       │   ├── exceptions.py
│       │   ├── tui/
│       │   │   ├── app.py
│       │   │   ├── controllers/
│       │   │   ├── screens/
│       │   │   ├── widgets/
│       │   │   ├── presenters/
│       │   │   ├── rendering/
│       │   │   └── styles/
│       │   └── cli/
│       │       ├── main.py
│       │       ├── commands/
│       │       └── formatters/
│       ├── plugins/
│       │   ├── loader.py
│       │   ├── manager.py
│       │   ├── exceptions.py
│       │   ├── builtin/        # vide
│       │   └── external/       # vide
│       └── shared/
│           ├── clock.py
│           ├── ids.py
│           └── typing.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
└── var/
    ├── db/app.db
    ├── settings.json
    └── exports/
```

### Détails de `src/omega_scan/`

#### `app/`
Assemble et démarre l'application, injection de dépendances, cycle de vie. **Jamais de logique métier.** `bootstrap.py` câble ports ↔ adaptateurs concrets. `dependency_container.py` : conteneur DI explicite, pas de framework tiers. `lifecycle.py` : ouverture/fermeture SQLite, flush des settings.

#### `core/`
Langage transverse. **Pas d'appels système, pas de SQL, pas de rendu.** `capability.py` : modèle générique de capacité (`AVAILABLE`/`DEGRADED`/`MISSING`/`DISQUALIFIED`), utilisé uniquement pour la capacité terminal ici (pas de capacité système locale, voir §0). `enums.py` : `ScanProfileName` (quick/standard/extended/local-lab), `RenderProfile` (complete/standard/reduced/mono), `ScanVerdict` (completed/partial/failed), `CapabilityStatus`. `results.py` : `Result[T, E]` générique. `audit.py` : forme générique d'un événement d'audit (horodatage, cible, action, décision d'autorisation, issue).

#### `domain/` (par sous-domaine)
Logique métier pure. **Jamais de httpx, sqlite, Textual/Rich.**
- `targets/` — `Target`, `PinnedTarget`, règles d'autorisation (`UnauthorizedTargetError`).
- `profiles/` — les 4 profils de scan prédéfinis (`quick`/`standard`/`extended`/`local-lab`), lecture seule (pas de CRUD utilisateur, contrairement aux profils de charge d'omega-stress).
- `scans/` — `ScanRun`, transitions de statut (`completed`/`partial`/`failed`), `scan_id` stable par cible (voir `shared/ids.py`).
- `findings/` — `Finding`, `Evidence`, catégories et taxonomie de règles (`TRN-*`, `HDR-*`, `MTH-*`, `EXR-*`, `INF-*`, nouveaux `COR-*`, `TLS-*`).
- `checks/<catégorie>/` — `service.py` juge à partir des preuves collectées ; `policies.py` porte la table de règles (seuils, listes attendues, sévérités). **Toute table de bornage vit ici, jamais dans `infrastructure/` ni `interfaces/`.**
- `reports/` — `service.py` construit le contenu logique du résumé (note A–F, ventilation par statut/sévérité) ; `comparison.py` calcule le diff entre deux `ScanRun` (findings apparus/disparus/inchangés).
- `terminal/` — capacité terminal → profil de rendu, porté à l'identique du gabarit omega-stress.
- `theme/` — catalogue de thèmes **partagé** avec omega-stress (voir §8).

#### `application/`
Orchestre les cas d'usage. **Jamais de rendu, jamais d'I/O directe (toujours via un port).**
- `commands/` — action qui change un état (`run_scan`, `pin_target`, `confirm_target_authorization`…).
- `queries/` — lecture sans effet de bord (`list_scan_history`, `compare_scans`, `get_scan_details`…).
- `pipeline/` — voir §4. Tout scan passe par ici.
- `services/` — orchestration transversale (`scan_comparison_service`, `scan_replayer`).

#### `ports/`
Contrats attendus par le cœur applicatif. Cinq probers distincts (voir §0) plutôt qu'un port unique, reflétant les 5 collectes réseau indépendantes déjà présentes en v1.

#### `infrastructure/`
Implémente la technique réelle. `storage/sqlite/` — seul endroit où `sqlite3` est importé, **nouveau** (historique + cibles épinglées, absent en v1). `network/` — seul endroit où `httpx` est importé. `exporters/` — seul endroit où `jinja2` est importé. `resources/` — listes de chemins et politique de méthodes, chargées mais jamais interprétées ici (l'interprétation est une règle de `domain/checks/*/policies.py`).

#### `interfaces/`
`tui/` — Textual, seul endroit où il est importé ; interface principale. `cli/` — scriptable, sans Textual, parité stricte avec le TUI (aucune règle métier qui existerait dans l'un sans exister dans l'autre).

#### `plugins/` et `shared/`
Identiques dans leur rôle à omega-stress (voir sa charte §2) : `plugins/` vide en l'absence d'axe d'extension confirmé, `shared/` strictement non métier (`clock.py`, `ids.py` — génère un `scan_id` stable par cible, `typing.py`).

---

## 3. Règles de dépendance strictes

- `domain/` ne dépend d'aucune autre couche.
- `application/` peut dépendre de `domain/`, `core/` et `ports/`, **jamais d'un adaptateur concret d'infrastructure**.
- `infrastructure/` implémente les contrats de `ports/` et peut utiliser `domain/`/`core/` si nécessaire.
- `interfaces/` appelle `application/` (commands/queries) et affiche le résultat, **sans logique métier**.
- `shared/` ne contient jamais de logique métier déguisée.
- `plugins/` n'impose jamais sa logique au domaine.
- `app/` assemble et ne décide rien du métier.
- Pas d'import `textual` en dehors de `interfaces/tui/`. Pas d'import `sqlite3`/`httpx`/`jinja2` en dehors de `infrastructure/` (fichiers uniques désignés en §2).

**Violation = défaut d'architecture bloquant, pas un détail de style.**

## 4. Chaînes fonctionnelles obligatoires

### Capacité terminal
1. Détection technique : `infrastructure/terminal/raw_capabilities.py`.
2. Décision de profil de rendu : `domain/terminal/service.py`.
3. Projection visuelle : `interfaces/tui/rendering/render_profile_resolver.py`.

### Exécution d'un scan
Tout scan **doit passer par** `application/pipeline/`, dans l'ordre :
1. `guards/authorization_guard.py` — cible confirmée ou déjà épinglée-autorisée, sinon refus immédiat (`UnauthorizedTargetError`). Vérifié pipeline-side, pas seulement côté UI (voir §7).
2. `guards/capability_guard.py` — capacité terminal suffisante pour le rendu demandé.
3. `steps.py` — orchestre les 5 probers dans l'ordre déjà éprouvé en v1 : connectivité → HTTP/HTTPS → TLS → path probing → méthodes HTTP.
4. `steps.py` — applique les 8 familles de checks (`domain/checks/*/service.py`) sur les preuves collectées.
5. `domain/reports/service.py` — calcule le résumé et le verdict.
6. `hooks/audit_hook.py` — trace la tentative de scan et la décision d'autorisation (voir §7), avant ou après exécution selon l'issue.

**Aucun appel réseau direct ne doit contourner un port `*_prober`.**

### Historique et comparaison
1. `infrastructure/storage/sqlite/scan_repository.py` persiste chaque `ScanRun` (résultat complet, pas seulement le résumé).
2. `application/queries/list_scan_history.py` / `get_scan_details.py` exposent la lecture.
3. `domain/reports/comparison.py`, orchestré par `application/services/scan_comparison_service.py`, calcule le diff entre deux runs d'une même cible.
4. `application/commands/replay_scan.py` relance un scan sur une cible déjà connue, sans resaisie.

### Exports
1. `domain/reports/` construit le contenu logique (résumé, findings, verdict).
2. `infrastructure/exporters/` écrit le format concret (JSON, texte, HTML).
3. `interfaces/` propose le format et le chemin à l'utilisateur.

## 5. Gestion des exceptions inter-couches

### 5.1 Deux catégories d'échecs
- **Échec métier attendu** (cible non autorisée, profil invalide, prober indisponible de façon prévisible) : `Result[T, DomainError]` via `core/results.py`, pas une exception Python.
- **Échec technique inattendu** : exception Python classique, traduite à chaque frontière de couche, jusqu'au filet de sécurité en présentation (§5.4).

### 5.2 Hiérarchie d'exceptions

| Couche | Racine | Sous-types |
|---|---|---|
| `core/exceptions.py` | `OmegaScanError` | `ConfigurationError` |
| `domain/errors.py` | `DomainError` | `ValidationError`, `UnauthorizedTargetError`, `TargetParseError`, `IncompatibleTerminalError` (+ exceptions spécifiques par sous-domaine) |
| `application/exceptions.py` | `ApplicationError` | `UseCaseExecutionError`, `CapabilityUnavailableError`, `PermissionDeniedError`, `PartialExecutionError`, `ProberFailureError` |
| `infrastructure/exceptions.py` | `InfrastructureError` | `StorageError`, `ParseError`, `AdapterConfigurationError` |
| `interfaces/exceptions.py` | `InterfaceError` | `UserInputError`, `RenderError` |
| `plugins/exceptions.py` | `PluginError` | `PluginLoadError`, `PluginActivationError` |

`ProberFailureError` vit dans `application/exceptions.py` et non `infrastructure/exceptions.py` malgré son nom : c'est le type technique qu'`application/pipeline/steps.py` doit connaître par son nom pour marquer un module en `partial`, et la Dependency Rule interdit à `application/` d'importer `infrastructure/` (même raisonnement que `RunnerFailureError` chez omega-stress, voir sa charte §5.2).

### 5.3 Frontière infrastructure : traduction obligatoire
Aucune exception spécifique à une techno ne franchit la frontière d'un port sans traduction — `sqlite3.Error` → `StorageError` ; `httpx.ConnectError`/timeout → `ProberFailureError` (le module concerné passe en `partial`, le scan continue). Cette traduction est la responsabilité de l'adaptateur.

### 5.4 Filet de sécurité en présentation
`interfaces/` ne traite que des `DomainError`/`ApplicationError` déjà traduites. Point d'arrêt unique dans `interfaces/tui/app.py` et `interfaces/cli/main.py` : toute exception non prévue y est interceptée, journalisée, affichée comme erreur générique.

## 6. Convention de nommage du code

Vocabulaire produit = vocabulaire code ici : « scan », « cible », « profil », « finding », « historique », « comparaison », « export ». Contrairement à omega-stress, le mot `scan` n'est pas banni (voir §0). Seule règle de collecte pytest à respecter : aucun fichier hors de `tests/` ne s'appelle `test_*.py`.

Un port et son adaptateur peuvent partager le même nom de fichier dans des dossiers différents (`ports/scan_repository.py` / `infrastructure/storage/sqlite/scan_repository.py`) ; la classe concrète est préfixée par sa techno (`SqliteScanRepository`, pas `ScanRepository`).

## 7. Règle d'autorisation de cible

Aucun scan ne démarre sans confirmation explicite d'autorisation sur la cible, sauf cible déjà épinglée avec autorisation déjà confirmée. Vérifiée côté `application/pipeline/guards/authorization_guard.py`, pas seulement côté UI : l'UI peut désactiver le bouton de lancement, le guard refuse quand même un scan non confirmé, indépendamment de l'écran ou de la commande CLI appelante. Chaque décision (confirmée, refusée, déjà épinglée) est tracée par `hooks/audit_hook.py`.

## 8. Système de thèmes et de rendu — catalogue partagé de la suite

Catalogue **identique** à celui d'omega-stress (source d'autorité : `Projet/themes.txt` côté omega-stress) : 10 thèmes TUI, 5 thèmes export. Vit dans `domain/theme/policies.py`. Décision de thème (couleur, choix manuel) et profil de rendu (structure, décidé automatiquement depuis la capacité terminal) restent deux décisions indépendantes, jamais mélangées dans un même fichier — même règle qu'omega-stress §8.

## 9. Règles de test

- Tout objet de `domain/` et `core/` est testable sans mock.
- Tout command/query de `application/` est testable en injectant de faux ports, sans SQLite réel, sans Textual, sans réseau.
- Le pipeline est testable guard par guard.
- Un test e2e TUI est le seul niveau où `interfaces/tui/` est exercée de bout en bout ; un test e2e CLI, le seul niveau pour `interfaces/cli/`.
- `pyproject.toml` restreint la découverte pytest à `testpaths = ["tests"]`.

## 10. Anti-patterns interdits

- Importer `textual` hors de `interfaces/tui/`, ou `sqlite3`/`httpx`/`jinja2` hors des fichiers uniques désignés en §2.
- Mettre une table de règles/seuils dans `infrastructure/` ou `interfaces/` plutôt que dans le `policies.py` du sous-domaine concerné.
- Laisser un écran (`interfaces/tui/screens/`) juger un finding ou décider d'une autorisation.
- Écrire dans une commande CLI une règle qui n'existe pas déjà, à l'identique, dans un command/query appelé aussi par le TUI.
- Lancer un scan sans passer par `application/pipeline/`.
- Faire dépendre un command/query d'une classe concrète d'infrastructure plutôt que d'un port.
- Peupler `plugins/builtin`/`plugins/external` sans axe d'extension confirmé.
- Introduire un test actif (SQLi/XSS/RCE/CVE/fuzzing) dans `domain/checks/` — hors périmètre définitif de l'outil (voir README).

## 11. Vérification continue

- `ruff` + `mypy` en CI sur chaque commit.
- Un contrôle d'imports (`import-linter`) fait échouer la CI si `domain`/`core` importent une couche externe, ou si `application` importe `infrastructure`/`interfaces`.
- Toute PR ajoutant un fichier dans `infrastructure/` avec une valeur numérique de seuil/sévérité est refusée en revue et redirigée vers le `policies.py` du sous-domaine concerné.

## 12. Évolution de cette charte

Cette charte peut être modifiée, jamais contournée silencieusement. Toute dérogation proposée doit : (1) être documentée ici avec sa justification, (2) indiquer explicitement quelle règle elle assouplit, (3) être datée.
