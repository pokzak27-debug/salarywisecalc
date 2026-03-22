#!/usr/bin/env python3
"""Add Related Calculations section below results on all pages."""

import os
import re

HOURLY_RATES = [12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 45, 50, 60, 70, 80]
HOURLY_AFTER_TAX = [25, 30, 35, 40, 50]
SALARY_AFTER_TAX = ["70000", "80000", "90000", "100k", "120k"]


def slug_hourly(r):
    return f"{r}-dollar-an-hour-is-how-much-a-year.html"


def slug_hourly_at(r):
    return f"{r}-an-hour-after-tax.html"


def slug_salary_at(s):
    return f"{s}-salary-after-tax.html"


def related_block(links):
    """links: list of (href, text)"""
    items = "\n          ".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    return f'''      <div class="related-calculations">
        <h3>Related Calculations</h3>
        <ul>
          {items}
        </ul>
      </div>
'''


def get_links_index():
    return [
        ("hourly-to-salary.html", "Hourly to Salary"),
        ("salary-to-hourly.html", "Salary to Hourly"),
        ("15-dollar-an-hour-is-how-much-a-year.html", "$15 an hour"),
        ("20-dollar-an-hour-is-how-much-a-year.html", "$20 an hour"),
        ("25-dollar-an-hour-is-how-much-a-year.html", "$25 an hour"),
        ("70000-salary-after-tax.html", "$70k after tax"),
    ]


def get_links_hourly_page(rate):
    idx = HOURLY_RATES.index(rate) if rate in HOURLY_RATES else 10
    nearby = []
    for i in range(max(0, idx - 2), min(len(HOURLY_RATES), idx + 5)):
        if HOURLY_RATES[i] != rate:
            nearby.append((slug_hourly(HOURLY_RATES[i]), f"${HOURLY_RATES[i]} an hour"))
    links = nearby[:4]
    if rate in HOURLY_AFTER_TAX:
        links.append((slug_hourly_at(rate), f"${rate}/hr after tax"))
    links.extend([
        ("index.html", "Salary Calculator"),
        ("hourly-to-salary.html", "Hourly to Salary"),
    ])
    return links[:6]


def get_links_hourly_after_tax(rate):
    nearby = [(slug_hourly_at(r), f"${r}/hr after tax") for r in HOURLY_AFTER_TAX if r != rate]
    links = nearby[:3]
    links.extend([
        (slug_hourly(rate), f"${rate}/hr gross"),
        ("index.html", "Salary Calculator"),
        ("25-an-hour-after-tax.html", "$25/hr after tax") if rate != 25 else ("30-an-hour-after-tax.html", "$30/hr after tax"),
    ])
    return links[:6]


def get_links_salary_after_tax(sal):
    # sal is like "70000" or "100k"
    others = [("70000", "$70k"), ("80000", "$80k"), ("90000", "$90k"), ("100k", "$100k"), ("120k", "$120k")]
    links = [(slug_salary_at(s), t) for s, t in others if s != sal][:3]
    links.extend([
        ("salary-to-hourly.html", "Salary to Hourly"),
        ("index.html", "Salary Calculator"),
        ("25-an-hour-after-tax.html", "$25/hr after tax"),
    ])
    return links[:6]


def get_links_hourly_to_salary():
    return [
        ("salary-to-hourly.html", "Salary to Hourly"),
        ("15-dollar-an-hour-is-how-much-a-year.html", "$15 an hour"),
        ("20-dollar-an-hour-is-how-much-a-year.html", "$20 an hour"),
        ("25-dollar-an-hour-is-how-much-a-year.html", "$25 an hour"),
        ("70000-salary-after-tax.html", "$70k after tax"),
        ("index.html", "Salary Calculator"),
    ]


def get_links_salary_to_hourly():
    return [
        ("hourly-to-salary.html", "Hourly to Salary"),
        ("70000-salary-after-tax.html", "$70k after tax"),
        ("80000-salary-after-tax.html", "$80k after tax"),
        ("100k-salary-after-tax.html", "$100k after tax"),
        ("25-dollar-an-hour-is-how-much-a-year.html", "$25 an hour"),
        ("index.html", "Salary Calculator"),
    ]


def get_links_simple():
    return [
        ("index.html", "Salary Calculator"),
        ("hourly-to-salary.html", "Hourly to Salary"),
        ("salary-to-hourly.html", "Salary to Hourly"),
        ("25-dollar-an-hour-is-how-much-a-year.html", "$25 an hour"),
        ("70000-salary-after-tax.html", "$70k after tax"),
    ]


def add_section(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if 'class="related-calculations"' in html:
        return False

    name = os.path.basename(path)

    # Determine link set
    if name == "index.html":
        links = get_links_index()
    elif name == "hourly-to-salary.html":
        links = get_links_hourly_to_salary()
    elif name == "salary-to-hourly.html":
        links = get_links_salary_to_hourly()
    elif name in ("about.html", "contact.html", "terms.html", "privacy-policy.html"):
        links = get_links_simple()
    elif "-an-hour-after-tax.html" in name:
        rate = int(re.match(r"(\d+)-an-hour-after-tax", name).group(1))
        links = get_links_hourly_after_tax(rate)
    elif "-salary-after-tax.html" in name:
        sal = re.match(r"(\d+k|\d+)-salary-after-tax", name).group(1)
        links = get_links_salary_after_tax(sal)
    elif "-dollar-an-hour-is-how-much-a-year.html" in name:
        rate = int(re.match(r"(\d+)-dollar-an-hour", name).group(1))
        links = get_links_hourly_page(rate)
    else:
        links = get_links_simple()

    block = related_block(links)

    # Insert after results
    if '<div class="results-box">' in html:
        # Index: after results-box, before hero-calculator closing
        old = '      </div>\n    </div>\n\n    <div class="internal-links">'
        if old in html:
            html = html.replace(old, '      </div>\n' + block + '    </div>\n\n    <div class="internal-links">')
    elif '<div class="results-section">' in html:
        # Calculator-card pages: after results-section, before calculator-card closing
        old = '      </div>\n    </div>\n\n    <section class="page-content'
        if old in html:
            html = html.replace(old, '      </div>\n' + block + '    </div>\n\n    <section class="page-content')
    elif 'page-content' in html and ('about' in name or 'contact' in name or 'terms' in name or 'privacy' in name):
        # Simple pages: after section, before ad-end or footer
        old = '    </section>\n    <div class="ad-slot ad-slot-end">'
        if old in html:
            html = html.replace(old, '    </section>\n' + block + '    <div class="ad-slot ad-slot-end">')
        else:
            old2 = '    </section>\n  </main>'
            if old2 in html:
                html = html.replace(old2, '    </section>\n' + block + '  </main>')

    if 'related-calculations' in html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    count = 0
    for name in sorted(os.listdir(".")):
        if name.endswith(".html"):
            if add_section(name):
                count += 1
                print(f"Updated {name}")
    print(f"\nDone. Updated {count} files.")


if __name__ == "__main__":
    main()
