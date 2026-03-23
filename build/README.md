# SEO Page Generation System

Génère des pages HTML statiques à partir de templates et de specs.

## Structure

- **`templates/seo-base.html`** — Base HTML avec placeholders `{{VAR}}`
- **`page-specs.json`** — Config pays, types de pages, liens internes
- **`generate.py`** — Script de build

## Internal linking

```bash
# Strengthen internal links (8–12 per page, connect by category/country/rate)
python build/strengthen-internal-links.py

# Validate no broken links
python build/validate-links.py
```

## Usage

```bash
# Lister les pages qui seraient générées
python build/generate.py --list

# Générer toutes les pages hourly-after-tax-country
python build/generate.py

# Spécifier le répertoire de sortie
python build/generate.py --output-dir ./output
```

## Page variables

| Variable | Description |
|----------|-------------|
| `hourly` / `yearly` | Taux horaire ou salaire annuel |
| `country` | Clé pays (kenya, nigeria, philippines, south-africa) |
| `after_tax` | true/false |
| `currency`, `symbol` | Définis par pays |

## Ajouter une nouvelle page

1. Éditer `page-specs.json` :
   - Ajouter un pays dans `countries` si nécessaire
   - Définir `calculatorPage` pour les liens internes

2. Éditer `generate.py` :
   - Ajouter la page dans la liste `pages` (ligne ~250) :
     ```python
     (1500, "shilling", "kenya"),  # KES 1,500/hr Kenya
     ```

3. Lancer `python build/generate.py`

## Sections template

- H1
- key_result
- calculator_block
- summary
- explanation
- examples
- faq
- related_calculations
- disclaimer

## Contenu varié (anti-duplication)

- FAQs avec variantes par pays
- Liens internes injectés depuis `relatedLinks`
- Explications générées à partir des specs pays
