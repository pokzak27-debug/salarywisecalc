#!/usr/bin/env python3
"""
SalaryWiseCalc - SEO page generator
Generates static HTML from templates + page specs.
Usage: python build/generate.py [--type hourly-after-tax-country] [--list]
"""

import json
import os
import re
import argparse
from pathlib import Path

BUILD_DIR = Path(__file__).parent
PROJECT_ROOT = BUILD_DIR.parent
TEMPLATES_DIR = BUILD_DIR / "templates"
SPECS_FILE = BUILD_DIR / "page-specs.json"

HOURS_PER_WEEK = 40
WEEKS_PER_YEAR = 52

def yearly_from_hourly(hourly):
    return hourly * HOURS_PER_WEEK * WEEKS_PER_YEAR

def monthly_from_yearly(yearly):
    return yearly / 12

def weekly_from_yearly(yearly):
    return yearly / WEEKS_PER_YEAR

def fmt_num(n, symbol=""):
    if n is None or (isinstance(n, float) and (n != n or n < 0)):
        return "—"
    s = f"{int(round(n)):,}"
    return f"{symbol}{s}" if symbol else s

def load_specs():
    with open(SPECS_FILE, encoding="utf-8") as f:
        return json.load(f)

def render(template, vars_dict):
    out = template
    for k, v in vars_dict.items():
        placeholder = "{{" + k + "}}"
        out = out.replace(placeholder, str(v) if v is not None else "")
    return out

def build_hourly_after_tax_country(specs, rate, unit, country_key):
    """Build one hourly-after-tax country page."""
    country = specs["countries"][country_key]
    symbol = country["symbol"]
    name = country["name"]
    slug = f"{rate}-{unit}-per-hour-after-tax-{country['slug']}.html"

    gross_yearly = yearly_from_hourly(rate)
    gross_monthly = gross_yearly / 12
    gross_weekly = gross_yearly / 52

    # Net estimate (simplified; real values come from country-specific logic)
    net_rate = 0.69  # placeholder - override per country in config
    if country_key == "kenya":
        net_rate = 0.692  # ~1.44M from 2.08M
    elif country_key == "nigeria":
        net_rate = 0.719  # ~7.48M from 10.4M
    elif country_key == "philippines":
        net_rate = 0.877  # ~365k from 416k

    net_yearly = gross_yearly * net_rate
    net_monthly = net_yearly / 12
    net_weekly = net_yearly / 52

    rate_display = f"{symbol}{rate:,}" if "," not in str(rate) else f"{symbol}{rate}"

    # FAQ with slight variation per page (avoid duplication)
    faq_variants = {
        "how_much": f"At 40 hrs/week full-time, about {fmt_num(net_yearly, symbol)} per year after {' '.join(country['deductions'])}.",
        "monthly": f"Roughly {fmt_num(net_monthly, symbol)} per month after statutory deductions. Monthly pay is standard in {name}.",
        "weekly": f"About {fmt_num(net_weekly, symbol)} per week after {' '.join(country['deductions'][:2])}, assuming 40 hours per week.",
        "good_pay": f"{fmt_num(gross_yearly, symbol)} gross (~{fmt_num(net_yearly, symbol)} net) is above median for many professional roles. Cost of living varies by city.",
        "reduces": f"Income tax, {' '.join(country['deductions'])}, and pension contributions.",
        "part_time": f"Yes. Multiply {rate_display} by your weekly hours, then by 52 for annual gross. Tax and contributions are lower at lower income.",
    }

    faq_items = [
        (f"How much is {rate_display} per hour after tax in {name}?", faq_variants["how_much"]),
        (f"What is {rate_display} per hour monthly after tax in {name}?", faq_variants["monthly"]),
        (f"How much is {rate_display} per hour weekly after tax?", faq_variants["weekly"]),
        (f"Is {rate_display} per hour good pay in {name}?", faq_variants["good_pay"]),
        (f"What reduces {rate_display} per hour take-home in {name}?", faq_variants["reduces"]),
        (f"Can I use this for part-time at {rate_display} per hour?", faq_variants["part_time"]),
    ]

    # Add country-specific FAQ if available
    if country_key == "kenya":
        faq_items.insert(2, (f"Does SHIF affect {rate_display} per hour take-home in Kenya?",
            "Yes. SHIF (Social Health Insurance Fund) is 2.75% of gross. NSSF and Housing Levy (1.5% of net) also apply."))
    elif country_key == "nigeria":
        faq_items.insert(2, (f"Does pension affect {rate_display} per hour take-home in Nigeria?",
            "Yes. Pension is 8% employee contribution (employer adds 10%). It reduces take-home but builds retirement savings."))

    faq_html = "\n".join(
        f'        <div class="faq-item">\n          <h3>{q}</h3>\n          <p>{a}</p>\n        </div>'
        for q, a in faq_items
    )

    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]
    }
    faq_jsonld_str = f'  <script type="application/ld+json">\n  {json.dumps(faq_jsonld)}</script>'

    related = specs["relatedLinks"]["core"][:4]
    related += specs["relatedLinks"]["guides"][:4]
    related += [
        {"href": country["calculatorPage"], "text": f"Salary Calculator {name}"},
    ]
    related_html = "\n".join(f'          <li><a href="{r["href"]}">{r["text"]}</a></li>' for r in related)

    table_class = f"{country_key[:2]}-gross-table" if len(country_key) >= 2 else "gross-table"

    base = (TEMPLATES_DIR / "seo-base.html").read_text(encoding="utf-8")

    extra_styles = f"""  <style>
    .key-result {{ background: var(--color-bg-alt, #f8f9fa); border-left: 4px solid var(--color-accent, #2563eb); padding: 1rem 1.25rem; margin: 1rem 0; border-radius: 0 6px 6px 0; }}
    .key-result .amount {{ font-size: 1.5rem; font-weight: 700; }}
    .summary-block {{ margin: 1.25rem 0; padding: 1rem; border: 1px solid var(--color-border, #e0e0e0); border-radius: 6px; font-size: 0.95rem; }}
    .{table_class} {{ width: 100%; max-width: 480px; border-collapse: collapse; margin: 0.75rem 0; font-size: 0.9rem; }}
    .{table_class} th, .{table_class} td {{ padding: 0.4rem 0.6rem; text-align: left; border-bottom: 1px solid var(--color-border, #e0e0e0); }}
    .{table_class} th {{ font-weight: 600; }}
  </style>
"""

    calculator_block = f'''    <div class="calculator-card" data-calculator="hourly-to-salary" data-currency-symbol="{symbol}">
      <h2>{rate_display} per Hour After Tax Calculator</h2>
      <p class="subtitle">Enter any hourly rate to see gross annual (formula is the same). Tax and net use an illustrative formula—for {name} take-home at {rate_display}/hr see the key result above (~{fmt_num(net_yearly, symbol)}). Assumes 40 hrs/week. Use for <a href="weekly-vs-biweekly-vs-monthly-pay.html">budgeting</a> and cost-of-living planning.</p>
      <div class="form-group">
        <label for="hourly">Hourly rate ({symbol.strip()})</label>
        <input type="number" id="hourly" data-input="hourly" inputmode="decimal" value="{rate}" min="0" step="10">
      </div>
      <div class="ad-slot ad-slot-in-calculator">
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="2222222222" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
      <div class="results-section">
        <h3>Results</h3>
        <div class="result-item">
          <span class="label">Gross annual</span>
          <span class="value" data-output="gross-yearly">{fmt_num(gross_yearly, symbol)}</span>
        </div>
        <p class="subtitle" style="margin-top:0.5rem;font-size:0.85rem;">For {name} net at {rate_display}/hr, see key result above (~{fmt_num(net_yearly, symbol)}).</p>
        <div class="result-item">
          <span class="label">Est. deductions (approx.)</span>
          <span class="value" data-output="tax-estimate">—</span>
        </div>
        <div class="result-item highlight">
          <span class="label">Net annual (approx.)</span>
          <span class="value" data-output="net-yearly">—</span>
        </div>
      </div>
    </div>'''

    key_result = f'''    <div class="key-result">
      <p><span class="amount">~{fmt_num(net_yearly, symbol)}</span> take-home per year ({', '.join(country['deductions'])}, 40 hrs/week). Monthly ≈ {fmt_num(net_monthly, symbol)}. Weekly ≈ {fmt_num(net_weekly, symbol)}.</p>
    </div>'''

    intro = f'''      <p>At {rate_display} per hour working full-time (40 hours per week) in {name}, you earn <strong>{fmt_num(gross_yearly, symbol)} gross</strong> per year and roughly <strong>{fmt_num(net_yearly, symbol)}</strong> take-home after {' '.join(country['deductions'])}. Your actual take-home varies by relief and allowances. Use the calculator below to adjust your rate. Plan your budget using our <a href="weekly-vs-biweekly-vs-monthly-pay.html">pay frequency</a> and <a href="60000-a-year-is-how-much-a-month.html">monthly budgeting</a> guides.</p>'''

    summary = f'''    <div class="summary-block">
      <p><strong>Quick summary:</strong> {rate_display}/hr = {fmt_num(gross_yearly, symbol)}/yr gross. After {' '.join(country['deductions'])}, take-home ≈ {fmt_num(net_yearly, symbol)}/yr. Use our <a href="index.html">Salary Calculator</a>, <a href="hourly-to-salary.html">Hourly to Salary</a>, and <a href="{country['calculatorPage']}">Salary Calculator {name}</a> for conversions. For budgeting, see <a href="60000-a-year-is-how-much-a-month.html">$60k monthly</a> and <a href="50000-a-year-is-how-much-a-month.html">$50k monthly</a>.</p>
    </div>'''

    explanation = f'''
      <h2>{rate_display} per Hour After Tax: Quick Answer</h2>
      <p>{rate_display} per hour at 40 hours per week for 52 weeks = {fmt_num(gross_yearly, symbol)} gross per year. {name} applies {' '.join(country['deductions'])}. At current rates, that leaves roughly {fmt_num(net_yearly, symbol)} take-home. That's about {fmt_num(net_monthly, symbol)} per month or {fmt_num(net_weekly, symbol)} per week. See <a href="gross-vs-net-salary.html">Gross vs net salary</a> for why gross and take-home differ. Use our <a href="index.html">Salary Calculator</a> and <a href="{country['calculatorPage']}">Salary Calculator {name}</a> for conversions.</p>

      <h2>Annual, Monthly, and Weekly Estimates</h2>
      <p>At {rate_display}/hr full-time, gross pay breaks down as follows. Employers typically pay monthly. Divide net annual (~{fmt_num(net_yearly, symbol)}) by 12 for monthly, by 52 for weekly. See <a href="weekly-vs-biweekly-vs-monthly-pay.html">Weekly vs biweekly vs monthly pay</a> for how pay frequency affects budgeting.</p>

      <table class="{table_class}">
        <thead>
          <tr><th>Gross period</th><th>Est. gross pay</th></tr>
        </thead>
        <tbody>
          <tr><td>Annual</td><td>{fmt_num(gross_yearly, symbol)}</td></tr>
          <tr><td>Monthly</td><td>{fmt_num(gross_monthly, symbol)}</td></tr>
          <tr><td>Weekly</td><td>{fmt_num(gross_weekly, symbol)}</td></tr>
        </tbody>
      </table>

      <p><strong>Example (full-time):</strong> You work 40 hrs/week at {rate_display}/hr. Gross = {fmt_num(gross_yearly, symbol)}/yr. After {' '.join(country['deductions'][:2])}, net ≈ {fmt_num(net_yearly, symbol)}/yr, or {fmt_num(net_monthly, symbol)}/month.</p>
      <p><strong>Example (part-time):</strong> You work 25 hrs/week at {rate_display}/hr. Gross = {rate_display} × 1,300 = {fmt_num(rate * 1300, symbol)}/yr. Tax and contributions are lower at lower income.</p>
'''

    examples = f'''
      <h2>Cost-of-Living and Budgeting</h2>
      <p>At {fmt_num(net_yearly, symbol)} net ({fmt_num(net_monthly, symbol)}/month), a common budgeting rule is 30%% on rent. Cost of living varies by city. See <a href="compare-salary-offers-guide.html">Compare Salary Offers Guide</a> and <a href="salary-negotiation-guide.html">Salary Negotiation Guide</a>.</p>

      <h2>When to Use SalaryWiseCalc</h2>
      <p>Use our tools when comparing job offers, planning a budget, or negotiating pay. Use the <a href="index.html">Salary Calculator</a> for hourly ↔ yearly conversion. Use <a href="{country['calculatorPage']}">Salary Calculator {name}</a> for {name} context. Use <a href="how-salary-conversion-works.html">How Salary Conversion Works</a> for formulas.</p>
'''

    faq_section = f'''
      <div class="faq-section">
        <h2>FAQ</h2>
{faq_html}
      </div>'''

    related_section = f'''
      <div class="related-calculations">
        <h3>Related Calculations</h3>
        <ul>
{related_html}
        </ul>
      </div>'''

    disclaimer = f'''      <p class="disclaimer">This calculator provides an estimate only and is not tax or financial advice. {name} tax rates change. Consult {country['taxAuthority']} or a tax adviser. Last updated: March 2025.</p>'''

    vars_dict = {
        "META_DESCRIPTION": f"{rate_display} per hour after tax in {name}: ~{fmt_num(net_yearly, symbol)} take-home (full-time). {' '.join(country['deductions'])}. See annual, monthly. Calculator + breakdown.",
        "PAGE_TITLE": f"{rate_display} per Hour After Tax in {name} | Take-Home Pay Calculator & Breakdown",
        "OG_TITLE": f"{rate_display} per Hour After Tax in {name}",
        "OG_DESCRIPTION": f"{rate_display}/hr after tax {name}: ~{fmt_num(net_yearly, symbol)} take-home. {' '.join(country['deductions'][:3])}. Full breakdown.",
        "TWITTER_TITLE": f"{rate_display}/hr After Tax {name}",
        "TWITTER_DESCRIPTION": f"{rate_display}/hr take-home in {name}. {' '.join(country['deductions'][:2])}. Free calculator.",
        "SLUG": slug,
        "H1": f"{rate_display} per Hour After Tax in {name}",
        "INTRO_PARAGRAPH": intro,
        "KEY_RESULT": key_result,
        "EXTRA_HEAD_STYLES": extra_styles,
        "FAQ_JSONLD": faq_jsonld_str,
        "CALCULATOR_BLOCK": calculator_block,
        "SUMMARY_BLOCK": summary,
        "EXPLANATION": explanation,
        "EXAMPLES": examples,
        "FAQ_SECTION": faq_section,
        "RELATED_CALCULATIONS": related_section,
        "DISCLAIMER": disclaimer,
    }

    return render(base, vars_dict)

def main():
    parser = argparse.ArgumentParser(description="Generate SEO pages")
    parser.add_argument("--type", choices=["hourly-after-tax-country"], default="hourly-after-tax-country")
    parser.add_argument("--list", action="store_true", help="List pages that would be generated")
    parser.add_argument("--output-dir", default=str(PROJECT_ROOT), help="Output directory")
    args = parser.parse_args()

    specs = load_specs()
    out_dir = Path(args.output_dir)

    # Load pages from specs (extend page-specs.json "pages" for mass generation)
    pages_config = specs.get("pages", [])
    pages = [(p["rate"], p["unit"], p["country"]) for p in pages_config]

    if args.list:
        for rate, unit, country in pages:
            slug = f"{rate}-{unit}-per-hour-after-tax-{specs['countries'][country]['slug']}.html"
            print(slug)
        return

    for rate, unit, country in pages:
        html = build_hourly_after_tax_country(specs, rate, unit, country)
        slug = f"{rate}-{unit}-per-hour-after-tax-{specs['countries'][country]['slug']}.html"
        out_path = out_dir / slug
        out_path.write_text(html, encoding="utf-8")
        print(f"Generated {slug}")

if __name__ == "__main__":
    main()
