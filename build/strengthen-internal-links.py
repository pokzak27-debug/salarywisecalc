#!/usr/bin/env python3
"""
Strengthen internal linking across all SEO pages.
- Ensure 10+ internal links per page
- Every page: 1 hub (salary-guides), 1 country, 1 after-tax
- Natural anchor text
- Validate: no broken links
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def get_existing_html():
    existing = set()
    for p in PROJECT_ROOT.glob("*.html"):
        existing.add(p.name)
    return existing

EXISTING = get_existing_html()

# REQUIRED: every page must link to these
HUB = ("salary-guides.html", "browse all salary guides")
COUNTRY = ("salary-calculator-usa.html", "USA salary calculator")
AFTER_TAX = ("60000-salary-after-tax.html", "$60k take-home estimate")
REQUIRED = [HUB, COUNTRY, AFTER_TAX]

def _get_existing_hourly_rates():
    rates = []
    for f in EXISTING:
        m = re.match(r"(\d+)-dollar-an-hour-is-how-much-a-year\.html", f)
        if m:
            rates.append(int(m.group(1)))
    return sorted(set(rates))

HOURLY_YEARLY = _get_existing_hourly_rates()
HOURLY_AFTER_TAX_USD = [20, 25, 30, 35, 40, 50]

def _get_existing_salary_after_tax():
    amts = []
    for f in EXISTING:
        m = re.match(r"(\d+k|\d+)-salary-after-tax\.html", f)
        if m and "australia" not in f:
            amts.append(m.group(1))
    def _key(x):
        return int(x.replace('k',''))*1000 if x.endswith('k') else int(x)
    return sorted(amts, key=_key)

def _get_existing_year_monthly():
    amts = []
    for f in EXISTING:
        m = re.match(r"(\d+)-a-year-is-how-much-a-month\.html", f)
        if m:
            amts.append(int(m.group(1)))
    return sorted(amts)

SALARY_AFTER_TAX = _get_existing_salary_after_tax()
YEARLY_MONTHLY_AMTS = _get_existing_year_monthly()

def _get_existing_monthly_rates():
    result = []
    for f in EXISTING:
        m = re.match(r"(\d+)-an-hour-monthly-pay\.html", f)
        if m:
            result.append(int(m.group(1)))
    return sorted(result)

def _get_existing_biweekly_rates():
    result = []
    for f in EXISTING:
        m = re.match(r"(\d+)-an-hour-biweekly-pay\.html", f)
        if m:
            result.append(int(m.group(1)))
    return sorted(result)

MONTHLY_RATES = _get_existing_monthly_rates()
BIWEEKLY_RATES = _get_existing_biweekly_rates()

COUNTRY_HOURLY = {
    "kenya": ("1000-shilling-per-hour-after-tax-kenya.html", "KES 1,000/hr Kenya"),
    "nigeria": ("5000-naira-per-hour-after-tax-nigeria.html", "₦5,000/hr Nigeria"),
    "philippines": ("200-peso-per-hour-after-tax-philippines.html", "₱200/hr Philippines"),
    "south-africa": ("200-rand-an-hour-after-tax-south-africa.html", "R200/hr South Africa"),
}

COUNTRY_CALC = {
    "usa": "salary-calculator-usa.html",
    "uk": "salary-calculator-uk.html",
    "canada": "salary-calculator-canada.html",
    "australia": "salary-calculator-australia.html",
    "kenya": "salary-calculator-kenya.html",
    "nigeria": "salary-calculator-nigeria.html",
    "philippines": "salary-calculator-philippines.html",
    "south-africa": "salary-calculator-south-africa.html",
}

def filter_existing(links):
    """Return only (href, text) where href exists."""
    return [(h, t) for h, t in links if h in EXISTING]

def ensure_required(links, min_total=10):
    """Add required links if missing, dedupe, ensure min_total."""
    seen = set()
    result = []
    for h, t in links:
        if h not in seen and h in EXISTING:
            seen.add(h)
            result.append((h, t))
    for h, t in REQUIRED:
        if h not in seen and h in EXISTING:
            seen.add(h)
            result.append((h, t))
    while len(result) < min_total:
        extra = [
            ("index.html", "free salary calculator"),
            ("salary-after-tax-usa.html", "take-home calculator"),
            ("hourly-to-salary.html", "hourly to yearly converter"),
            ("salary-to-hourly.html", "salary to hourly converter"),
            ("gross-vs-net-salary.html", "gross vs net pay"),
            ("weekly-vs-biweekly-vs-monthly-pay.html", "pay frequency guide"),
            ("sitemap.html", "view all calculators"),
        ]
        added = False
        for h, t in extra:
            if h not in seen and h in EXISTING and len(result) < min_total:
                result.append((h, t))
                seen.add(h)
                added = True
        if not added:
            break
    return result

def nearby_rates(rate, rates, n=4):
    idx = rates.index(rate) if rate in rates else 0
    start = max(0, idx - n)
    end = min(len(rates), idx + n + 1)
    return [r for r in rates[start:end] if r != rate][:8]

def links_hourly_yearly(rate):
    nearby = nearby_rates(rate, HOURLY_YEARLY, 3)
    links = [(f"{r}-dollar-an-hour-is-how-much-a-year.html", f"${r}/hr yearly") for r in nearby]
    if f"{rate}-an-hour-monthly-pay.html" in EXISTING:
        links.append((f"{rate}-an-hour-monthly-pay.html", f"${rate}/hr monthly pay"))
    if f"{rate}-an-hour-biweekly-pay.html" in EXISTING:
        links.append((f"{rate}-an-hour-biweekly-pay.html", f"${rate}/hr biweekly"))
    if f"{rate}-an-hour-after-tax.html" in EXISTING:
        links.append((f"{rate}-an-hour-after-tax.html", f"see ${rate}/hr take-home"))
    sal = rate * 2080
    for s in SALARY_AFTER_TAX:
        val = int(s.replace("k","")) * 1000 if "k" in s else int(s)
        if abs(val - sal) < 25000:
            links.append((f"{s}-salary-after-tax.html", f"${val//1000}k take-home"))
            break
    links.extend([
        ("index.html", "free salary calculator"),
        ("hourly-to-salary.html", "convert hourly to yearly"),
        ("salary-to-hourly.html", "salary to hourly converter"),
    ])
    return ensure_required(filter_existing(links), 10)

def links_hourly_after_tax(rate):
    links = []
    for r in nearby_rates(rate, HOURLY_AFTER_TAX_USD, 2):
        if f"{r}-an-hour-after-tax.html" in EXISTING:
            links.append((f"{r}-an-hour-after-tax.html", f"${r}/hr take-home"))
    if f"{rate}-dollar-an-hour-is-how-much-a-year.html" in EXISTING:
        links.append((f"{rate}-dollar-an-hour-is-how-much-a-year.html", f"${rate}/hr gross yearly"))
    if f"{rate}-an-hour-monthly-pay.html" in EXISTING:
        links.append((f"{rate}-an-hour-monthly-pay.html", f"${rate}/hr monthly"))
    if f"{rate}-an-hour-biweekly-pay.html" in EXISTING:
        links.append((f"{rate}-an-hour-biweekly-pay.html", f"${rate}/hr biweekly"))
    sal = rate * 2080
    for s in SALARY_AFTER_TAX:
        val = int(s.replace("k","")) * 1000 if "k" in s else int(s)
        if abs(val - sal) < 25000:
            links.append((f"{s}-salary-after-tax.html", f"${val//1000}k take-home"))
            break
    links.extend([
        ("index.html", "free salary calculator"),
        ("salary-after-tax-usa.html", "take-home calculator"),
        ("hourly-to-salary.html", "convert hourly to yearly"),
    ])
    return ensure_required(filter_existing(links), 10)

def _salary_amt(s):
    return int(s.replace("k","")) * 1000 if s.endswith("k") else int(s)

def links_salary_after_tax(amount_str):
    links = []
    amt = _salary_amt(amount_str)
    nearby = sorted(
        [s for s in SALARY_AFTER_TAX if s != amount_str and abs(_salary_amt(s) - amt) < 45000],
        key=lambda x: abs(_salary_amt(x) - amt)
    )[:6]
    for s in nearby:
        href = f"{s}-salary-after-tax.html"
        if href in EXISTING:
            txt = f"${int(s.replace('k',''))}k" if s.endswith("k") else f"${int(s):,}"
            links.append((href, f"{txt} take-home"))
    hr = amt / 2080
    for r in HOURLY_YEARLY:
        if abs(r - hr) < 3:
            if f"{r}-dollar-an-hour-is-how-much-a-year.html" in EXISTING:
                links.append((f"{r}-dollar-an-hour-is-how-much-a-year.html", f"${r}/hr yearly"))
            if f"{r}-an-hour-after-tax.html" in EXISTING:
                links.append((f"{r}-an-hour-after-tax.html", f"${r}/hr take-home"))
            break
    for y in YEARLY_MONTHLY_AMTS:
        if abs(y - amt) < 15000 and f"{y}-a-year-is-how-much-a-month.html" in EXISTING:
            links.append((f"{y}-a-year-is-how-much-a-month.html", f"${y:,}/year monthly"))
            break
    links.extend([
        ("salary-after-tax-usa.html", "take-home calculator"),
        ("index.html", "free salary calculator"),
    ])
    return ensure_required(filter_existing(links), 10)

def links_monthly_pay(rate):
    links = []
    if f"{rate}-dollar-an-hour-is-how-much-a-year.html" in EXISTING:
        links.append((f"{rate}-dollar-an-hour-is-how-much-a-year.html", f"${rate}/hr yearly"))
    if f"{rate}-an-hour-biweekly-pay.html" in EXISTING:
        links.append((f"{rate}-an-hour-biweekly-pay.html", f"${rate}/hr biweekly"))
    for r in nearby_rates(rate, MONTHLY_RATES, 2):
        if f"{r}-an-hour-monthly-pay.html" in EXISTING and r != rate:
            links.append((f"{r}-an-hour-monthly-pay.html", f"${r}/hr monthly"))
    if f"{rate}-an-hour-after-tax.html" in EXISTING:
        links.append((f"{rate}-an-hour-after-tax.html", f"${rate}/hr take-home"))
    links.extend([
        ("60000-a-year-is-how-much-a-month.html", "$60k yearly to monthly"),
        ("50000-a-year-is-how-much-a-month.html", "$50k monthly"),
        ("weekly-vs-biweekly-vs-monthly-pay.html", "pay frequency guide"),
        ("index.html", "free salary calculator"),
    ])
    return ensure_required(filter_existing(links), 10)

def links_biweekly_pay(rate):
    links = []
    if f"{rate}-dollar-an-hour-is-how-much-a-year.html" in EXISTING:
        links.append((f"{rate}-dollar-an-hour-is-how-much-a-year.html", f"${rate}/hr yearly"))
    if f"{rate}-an-hour-monthly-pay.html" in EXISTING:
        links.append((f"{rate}-an-hour-monthly-pay.html", f"${rate}/hr monthly"))
    for r in nearby_rates(rate, BIWEEKLY_RATES, 2):
        if f"{r}-an-hour-biweekly-pay.html" in EXISTING and r != rate:
            links.append((f"{r}-an-hour-biweekly-pay.html", f"${r}/hr biweekly"))
    if f"{rate}-an-hour-after-tax.html" in EXISTING:
        links.append((f"{rate}-an-hour-after-tax.html", f"${rate}/hr take-home"))
    links.extend([
        ("60000-a-year-is-how-much-a-month.html", "$60k monthly"),
        ("weekly-vs-biweekly-vs-monthly-pay.html", "pay frequency guide"),
        ("index.html", "free salary calculator"),
    ])
    return ensure_required(filter_existing(links), 10)

def links_country_hourly(country_key):
    links = []
    calc = COUNTRY_CALC.get(country_key)
    if calc and calc in EXISTING:
        links.append((calc, f"Salary Calculator {country_key.title()}"))
    for ck, (href, txt) in COUNTRY_HOURLY.items():
        if ck != country_key and href in EXISTING:
            links.append((href, txt))
    links.extend([
        ("index.html", "free salary calculator"),
        ("hourly-to-salary.html", "convert hourly to yearly"),
        ("60000-salary-after-tax.html", "$60k take-home"),
        ("60000-a-year-is-how-much-a-month.html", "$60k monthly"),
        ("gross-vs-net-salary.html", "gross vs net pay"),
    ])
    return ensure_required(filter_existing(links), 10)

def links_salary_calculator_country(slug):
    links = []
    ck = slug.replace("-", "_").replace(" ", "_")
    hourly_href = next((h for k, (h, _) in COUNTRY_HOURLY.items() if k.replace("_", "-") in slug or slug in k), None)
    if hourly_href and hourly_href in EXISTING:
        links.append((hourly_href, "hourly take-home in this country"))
    for k, calc in COUNTRY_CALC.items():
        k_slug = k.replace("_", "-")
        if k_slug != slug and calc in EXISTING:
            links.append((calc, f"{k.replace('_', ' ').title()} salary calculator"))
    links.extend([
        ("index.html", "free salary calculator"),
        ("salary-after-tax-usa.html", "take-home calculator"),
        ("gross-vs-net-salary.html", "gross vs net pay"),
    ])
    return ensure_required(filter_existing(links), 10)

def links_generic():
    return ensure_required(filter_existing([
        ("index.html", "free salary calculator"),
        ("hourly-to-salary.html", "convert hourly to yearly"),
        ("salary-to-hourly.html", "salary to hourly converter"),
        ("25-dollar-an-hour-is-how-much-a-year.html", "$25/hr yearly"),
        ("30-dollar-an-hour-is-how-much-a-year.html", "$30/hr yearly"),
        ("60000-salary-after-tax.html", "$60k take-home"),
        ("gross-vs-net-salary.html", "gross vs net pay"),
        ("weekly-vs-biweekly-vs-monthly-pay.html", "pay frequency guide"),
        ("salary-after-tax-usa.html", "take-home calculator"),
        ("compare-salary-offers-guide.html", "compare job offers"),
        ("salary-budgeting-guide.html", "salary budgeting guide"),
        ("cost-of-living-salary-guide.html", "cost of living by city"),
        ("sitemap.html", "view all calculators"),
    ]), 10)

def get_links_for_page(filename):
    if filename in ("index.html", "build/templates/seo-base.html"):
        return None  # Skip - index has its own curated link structure

    # Hourly yearly
    m = re.match(r"(\d+)-dollar-an-hour-is-how-much-a-year\.html", filename)
    if m:
        return links_hourly_yearly(int(m.group(1)))

    # Hourly after tax USD
    m = re.match(r"(\d+)-an-hour-after-tax\.html", filename)
    if m and "usa" not in filename and "jamaica" not in filename and "uk" not in filename and "ireland" not in filename and "canada" not in filename and "singapore" not in filename and "barbados" not in filename and "trinidad" not in filename and "bahamas" not in filename:
        return links_hourly_after_tax(int(m.group(1)))

    # Salary after tax
    m = re.match(r"(\d+k|\d+)-salary-after-tax\.html", filename)
    if m and "australia" not in filename:
        return links_salary_after_tax(m.group(1))

    # Monthly pay
    m = re.match(r"(\d+)-an-hour-monthly-pay\.html", filename)
    if m:
        return links_monthly_pay(int(m.group(1)))

    # Biweekly pay
    m = re.match(r"(\d+)-an-hour-biweekly-pay\.html", filename)
    if m:
        return links_biweekly_pay(int(m.group(1)))

    # Country hourly
    for ck, (href, _) in COUNTRY_HOURLY.items():
        if filename == href:
            return links_country_hourly(ck)

    # Salary calculator country
    m = re.match(r"salary-calculator-(.+)\.html", filename)
    if m:
        slug = m.group(1)
        return links_salary_calculator_country(slug)

    # Yearly to monthly
    m = re.match(r"(\d+)-a-year-is-how-much-a-month\.html", filename)
    if m:
        amt = int(m.group(1))
        links = []
        for y in YEARLY_MONTHLY_AMTS:
            if y != amt and abs(y - amt) < 25000 and f"{y}-a-year-is-how-much-a-month.html" in EXISTING:
                links.append((f"{y}-a-year-is-how-much-a-month.html", f"${y:,}/year monthly"))
        for r in [20, 25, 30]:
            if f"{r}-an-hour-monthly-pay.html" in EXISTING:
                links.append((f"{r}-an-hour-monthly-pay.html", f"${r}/hr monthly"))
        links.extend([
            ("index.html", "free salary calculator"),
            ("60000-salary-after-tax.html", "$60k take-home"),
            ("salary-budgeting-guide.html", "salary budgeting guide"),
            ("weekly-vs-biweekly-vs-monthly-pay.html", "pay frequency guide"),
        ])
        return ensure_required(filter_existing(links), 10)

    return links_generic()

def make_related_block(links):
    if not links:
        return None
    items = "\n          ".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    return f'''      <div class="related-calculations">
        <h3>Related Calculations</h3>
        <ul>
          {items}
        </ul>
      </div>'''

def make_internal_links_block(links):
    if not links:
        return None
    items = "\n          ".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    return f'''      <div class="internal-links">
        <p>Related pages:</p>
        <ul>
          {items}
        </ul>
      </div>'''

def update_page(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    links = get_links_for_page(filepath.name)
    if not links:
        return False, "skip"

    # Replace related-calculations
    related_new = make_related_block(links)
    internal_new = make_internal_links_block(links)

    # Pattern: <div class="related-calculations"> ... </div>
    related_pat = re.compile(
        r'<div class="related-calculations">\s*<h3>Related Calculations</h3>\s*<ul>.*?</ul>\s*</div>',
        re.DOTALL
    )
    if related_pat.search(html):
        html = related_pat.sub(related_new, html, count=1)

    # Replace internal-links section (same links, avoid duplicates/broken)
    internal_pat = re.compile(
        r'<div class="internal-links">\s*<p>[^<]*</p>\s*<ul>.*?</ul>\s*</div>',
        re.DOTALL
    )
    if internal_pat.search(html) and internal_new:
        html = internal_pat.sub(internal_new, html, count=1)
    elif 'class="internal-links"' not in html and internal_new:
        # Add before disclaimer
        if '<p class="disclaimer">' in html:
            html = html.replace('<p class="disclaimer">', internal_new + '\n\n      <p class="disclaimer">', 1)

    # Add related before disclaimer if neither section exists
    if 'related-calculations' not in html and 'internal-links' not in html and '<p class="disclaimer">' in html:
        html = html.replace('<p class="disclaimer">', related_new + '\n\n      <p class="disclaimer">', 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return True, len(links)

def main():
    updated = 0
    for path in sorted(PROJECT_ROOT.glob("*.html")):
        ok, msg = update_page(path)
        if ok:
            updated += 1
            print(f"Updated {path.name} ({msg} links)")
    print(f"\nDone. Updated {updated} pages.")

if __name__ == "__main__":
    main()
