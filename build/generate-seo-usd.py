#!/usr/bin/env python3
"""
Generate 30 new USD SEO pages: hourly-yearly, salary-after-tax, monthly-pay, biweekly-pay.
Uses template structure. Does NOT overwrite existing pages.
"""

import json
from pathlib import Path

BUILD_DIR = Path(__file__).parent
PROJECT_ROOT = BUILD_DIR.parent
SPECS_FILE = BUILD_DIR / "page-specs.json"

HOURS_PER_WEEK = 40
WEEKS_PER_YEAR = 52

def yearly_from_hourly(hourly):
    return hourly * HOURS_PER_WEEK * WEEKS_PER_YEAR

def monthly_from_yearly(yearly):
    return yearly / 12

def biweekly_from_yearly(yearly):
    return yearly / 26

def get_tax_rate(annual):
    if annual <= 11000: return 0.10
    if annual <= 44725: return 0.12
    if annual <= 95375: return 0.22
    if annual <= 182100: return 0.24
    if annual <= 231250: return 0.32
    if annual <= 578125: return 0.35
    return 0.37

def estimate_net(gross):
    rate = get_tax_rate(gross)
    return int(gross * (1 - rate))

def fmt(n):
    return f"${n:,.0f}"

COMMON_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y8M6Q89EPR"></script>
  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Y8M6Q89EPR');
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-W67HQBMS');</script>
  <!-- End Google Tag Manager -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{META_DESC}}">
  <title>{{PAGE_TITLE}}</title>
  <link rel="canonical" href="https://salarywisecalc.com/{{SLUG}}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{OG_TITLE}}">
  <meta property="og:description" content="{{OG_DESC}}">
  <meta property="og:url" content="https://salarywisecalc.com/{{SLUG}}">
  <meta property="og:site_name" content="SalaryWiseCalc">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{TW_TITLE}}">
  <meta name="twitter:description" content="{{TW_DESC}}">
  <link rel="stylesheet" href="style.css">
  <script type="application/ld+json">{{FAQ_JSONLD}}</script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7502486843743422" crossorigin="anonymous"></script>
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W67HQBMS"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
  <header class="site-header">
    <div class="header-inner">
      <a href="index.html" class="site-logo">SalaryWiseCalc</a>
      <nav class="nav-links" aria-label="Main navigation">
        <a href="index.html">Calculator</a>
        <a href="hourly-to-salary.html">Hourly → Salary</a>
        <a href="salary-to-hourly.html">Salary → Hourly</a>
        <a href="salary-guides.html">Guides</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="page-intro">
      <h1>{{H1}}</h1>
      <p>{{INTRO}}</p>
    </div>

    <div class="ad-slot ad-slot-below-h1">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="1111111111" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
    <div class="salary-highlight">
      {{HIGHLIGHT}}
    </div>

    {{CALCULATOR}}

    <section class="page-content">
      {{CONTENT}}
      {{FAQ}}
      {{RELATED}}
      <p class="disclaimer">This calculator provides an estimate only and is not tax or financial advice. Last updated: March 2025.</p>
    </section>
    <div class="ad-slot ad-slot-end">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="3333333333" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-links">
        <a href="index.html">Calculator</a>
        <a href="hourly-to-salary.html">Hourly → Salary</a>
        <a href="salary-to-hourly.html">Salary → Hourly</a>
        <a href="salary-guides.html">Guides</a>
        <a href="sitemap.html">Sitemap</a>
      </div>
      <div class="footer-links footer-legal">
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
        <a href="privacy-policy.html">Privacy</a>
        <a href="terms.html">Terms</a>
      </div>
      <p class="copyright">© SalaryWiseCalc. Free salary conversion tool.</p>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>'''

EXPLANATIONS = [
    "This rate is common for entry-level or part-time roles.",
    "Many retail and service jobs offer wages in this range.",
    "This falls within typical pay for skilled hourly workers.",
    "Overtime, bonuses, or a different schedule will change your actual earnings.",
    "Your take-home will be less after federal and state taxes.",
]

def build_hourly_yearly(rate):
    slug = f"{rate}-dollar-an-hour-is-how-much-a-year.html"
    y = yearly_from_hourly(rate)
    m = monthly_from_yearly(y)
    w = rate * 40
    net = estimate_net(y)
    low, high = int(net * 0.96), int(net * 1.02)

    faqs = [
        (f"How much is ${rate} an hour per year after taxes?",
         f"After federal taxes (approx.), ${rate}/hr full-time nets around ${low:,}–${high:,} per year. State taxes and deductions vary."),
        (f"How much is ${rate} an hour weekly?",
         f"At 40 hours per week, ${rate}/hr gives you {fmt(w)} gross per week."),
        (f"Is ${rate} an hour a livable wage?",
         "It depends on location and household size. In lower-cost areas it can cover basics; in cities, it may be tight."),
        (f"How much is ${rate} an hour biweekly?",
         f"At 80 hours per pay period, ${rate}/hr = {fmt(rate*80)} gross per biweekly check. Take-home about {fmt(rate*80*0.78)} after federal tax."),
        (f"How much is ${rate} an hour monthly?",
         f"At 40 hrs/week, ${rate}/hr is about {fmt(m)} gross per month. After federal tax, roughly {fmt(net/12)} per month take-home."),
        (f"Is ${rate} an hour good pay?",
         f"{fmt(y)}/year is above the median for individual earners in many US regions. Solid for a single person or small household."),
    ]

    # Adjacent links (avoid dupes with existing)
    all_rates = list(range(12, 81)) + [42, 45, 50, 60, 70, 80]
    all_rates = sorted(set(all_rates))
    idx = all_rates.index(rate) if rate in all_rates else 0
    nearby = [r for r in all_rates[max(0,idx-3):idx+6] if r != rate][:8]
    related = "".join(f'<li><a href="{r}-dollar-an-hour-is-how-much-a-year.html">${r} an hour</a></li>\n          ' for r in nearby)
    related += '<li><a href="index.html">Salary Calculator</a></li>\n          <li><a href="hourly-to-salary.html">Hourly to Salary</a></li>\n          <li><a href="salary-guides.html">Salary Guides</a></li>'
    if rate in [25, 30, 40]:
        related += f'\n          <li><a href="{rate}-an-hour-after-tax.html">${rate}/hr after tax</a></li>'

    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})

    html = COMMON_HEAD.replace("{{META_DESC}}", f"${rate}/hr = {fmt(y)}/year. Free calculator + tax estimate. See monthly, biweekly & take-home.")
    html = html.replace("{{PAGE_TITLE}}", f"${rate} an Hour is How Much a Year? (Calculator + Breakdown)")
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{OG_TITLE}}", f"${rate} an Hour is How Much a Year?")
    html = html.replace("{{OG_DESC}}", f"${rate}/hr = {fmt(y)}/year. Free calculator + tax estimate.")
    html = html.replace("{{TW_TITLE}}", f"${rate}/hr to Yearly")
    html = html.replace("{{TW_DESC}}", f"${rate}/hr = {fmt(y)}/year. Free calculator.")
    html = html.replace("{{H1}}", f"${rate} an Hour Is How Much a Year?")
    html = html.replace("{{INTRO}}", f"Working full-time at ${rate} per hour (40 hours per week, 52 weeks) gives you a gross annual income of <strong>{fmt(y)}</strong>. Use the calculator below to see your estimated take-home after taxes.")
    html = html.replace("{{HIGHLIGHT}}", f'<span class="amount">{fmt(y)}</span> per year · {fmt(m)}/mo · {fmt(w)}/wk (gross, 40 hrs)')
    html = html.replace("{{FAQ_JSONLD}}", faq_ld)

    calc = f'''<div class="calculator-card" data-calculator="hourly-to-salary">
      <h2>Convert Your Hourly Rate</h2>
      <p class="subtitle">Change the rate to find any hourly-to-yearly conversion. Assumes 40 hours per week.</p>
      <div class="form-group">
        <label for="hourly">Hourly rate ($)</label>
        <input type="number" id="hourly" data-input="hourly" inputmode="decimal" value="{rate}" min="0" step="0.01">
      </div>
      <div class="ad-slot ad-slot-in-calculator">
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="2222222222" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
      <div class="results-section">
        <h3>Results</h3>
        <div class="result-item highlight"><span class="label">Annual salary (gross)</span><span class="value" data-output="gross-yearly">{fmt(y)}</span></div>
        <div class="result-item"><span class="label">Est. tax (approx.)</span><span class="value" data-output="tax-estimate">$0</span></div>
        <div class="result-item"><span class="label">Net annual (approx.)</span><span class="value" data-output="net-yearly">$0</span></div>
      </div>
      <div class="related-calculations"><h3>Related Calculations</h3><ul>{related}</ul></div>
    </div>'''
    html = html.replace("{{CALCULATOR}}", calc)

    exp = EXPLANATIONS[rate % len(EXPLANATIONS)]
    content = f'''<h2>Understanding ${rate} an Hour</h2>
      <h3>How This Calculation Works</h3>
      <p>${rate} per hour at 40 hours per week for 52 weeks equals ${rate} × 2,080 = {fmt(y)} per year gross. We use the standard full-time schedule (2,080 hours). The calculator above applies this formula and estimates federal tax so you see your approximate take-home.</p>
      <h3>Example With Real Numbers</h3>
      <p>At ${rate}/hr full-time, you earn {fmt(y)} gross per year. That's {fmt(m)} per month or {fmt(w)} per week before taxes. After federal taxes (about {int(get_tax_rate(y)*100)}% at this level), you'd take home roughly {fmt(net)} per year. State tax and deductions will reduce this further.</p>
      <h3>When This Calculator Is Useful</h3>
      <p>{exp} Use it when comparing a ${rate}/hr offer to a salaried job, when budgeting or applying for loans, or when negotiating.</p>'''

    faq_html = "<h2>FAQ</h2>\n" + "\n".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in faqs)

    related_block = f'''<div class="internal-links"><p>Related:</p><ul>
          {related}
        </ul></div>'''

    html = html.replace("{{CONTENT}}", content)
    html = html.replace("{{FAQ}}", f'<div class="faq-section">\n{faq_html}\n</div>')
    html = html.replace("{{RELATED}}", related_block)

    return slug, html

def build_salary_after_tax(amount):
    slug = f"{amount}-salary-after-tax.html"
    net = estimate_net(amount)
    net_mo = net // 12
    net_bi = net // 26

    faqs = [
        (f"How much is ${amount:,} after tax monthly?",
         f"Roughly ${net_mo:,} per month after federal taxes. State tax, 401k, and health insurance will reduce your actual paycheck."),
        (f"What federal tax bracket is ${amount:,}?",
         f"${amount:,} gross falls in the {int(get_tax_rate(amount)*100)}% federal bracket. Effective rate is around {int(get_tax_rate(amount)*100)-2}–{int(get_tax_rate(amount)*100)}%."),
        (f"How much is ${amount:,} after tax biweekly?",
         f"About ${net_bi:,} per biweekly paycheck after federal tax. State tax and pre-tax deductions will reduce this."),
        (f"Is ${amount:,} a good salary after tax?",
         f"After federal tax, you keep about ${net:,}. In many areas that supports a modest to comfortable lifestyle. Location and expenses matter."),
        (f"What reduces ${amount:,} take-home pay?",
         "State tax, 401(k), health insurance, FICA, and other deductions all reduce your actual take-home."),
    ]

    disp = f"${amount//1000}k" if amount >= 10000 else f"${amount:,}"
    nearby_salaries = [55000,58000,60000,62000,65000,68000,70000,72000,75000,78000,80000,82000,85000,88000,90000,92000,95000,100000]
    nearby = [s for s in nearby_salaries if abs(s-amount) <= 30000 and s != amount][:6]
    def sal_slug(s):
        return f"{s//1000}k-salary-after-tax.html" if s >= 100000 else f"{s}-salary-after-tax.html"
    def sal_text(s):
        return f"${s//1000}k salary after tax" if s >= 10000 else f"${s:,} salary after tax"
    related = "".join(f'<li><a href="{sal_slug(s)}">{sal_text(s)}</a></li>\n          ' for s in nearby)
    related += '<li><a href="salary-guides.html">Salary Guides</a></li>\n          <li><a href="salary-after-tax-usa.html">Salary after tax USA</a></li>\n          <li><a href="index.html">Salary Calculator</a></li>'

    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})

    html = COMMON_HEAD.replace("{{META_DESC}}", f"${amount:,} salary after tax: ~${net:,} take-home. Free calculator + monthly & biweekly breakdown.")
    html = html.replace("{{PAGE_TITLE}}", f"${amount:,} Salary After Tax (Free Take-Home Calculator)")
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{OG_TITLE}}", f"${amount:,} Salary After Tax")
    html = html.replace("{{OG_DESC}}", f"{disp} after tax ≈ ${net:,} take-home. Free calculator.")
    html = html.replace("{{TW_TITLE}}", f"${amount:,} Salary After Tax")
    html = html.replace("{{TW_DESC}}", f"{disp} after tax ≈ ${net:,} take-home.")
    html = html.replace("{{H1}}", f"${amount:,} Salary After Tax")
    html = html.replace("{{INTRO}}", f"A ${amount:,} gross salary leaves roughly <strong>${net:,}</strong> after federal taxes (approx.). Your actual take-home depends on state tax, deductions, and filing status.")
    html = html.replace("{{HIGHLIGHT}}", f'<span class="amount">~${net:,}</span> after tax per year (federal estimate)')
    html = html.replace("{{FAQ_JSONLD}}", faq_ld)

    calc = f'''<div class="calculator-card" data-calculator="salary-to-hourly">
      <h2>Try a Different Salary</h2>
      <p class="subtitle">Enter any annual salary to see the after-tax estimate. Federal brackets only.</p>
      <div class="form-group">
        <label for="yearly">Annual salary ($)</label>
        <input type="number" id="yearly" data-input="yearly" inputmode="numeric" value="{amount}" min="0" step="1000">
      </div>
      <div class="ad-slot ad-slot-in-calculator">
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="2222222222" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
      <div class="results-section">
        <h3>Results</h3>
        <div class="result-item"><span class="label">Gross annual</span><span class="value" data-output="gross-yearly">${amount:,}</span></div>
        <div class="result-item"><span class="label">Est. tax (approx.)</span><span class="value" data-output="tax-estimate">$0</span></div>
        <div class="result-item highlight"><span class="label">Net annual (approx.)</span><span class="value" data-output="net-yearly">$0</span></div>
      </div>
      <div class="related-calculations"><h3>Related Calculations</h3><ul>{related}</ul></div>
    </div>'''
    html = html.replace("{{CALCULATOR}}", calc)

    content = f'''<h2>Understanding ${amount:,} Salary After Tax</h2>
      <h3>How After-Tax Salary Is Estimated</h3>
      <p>A ${amount:,} gross salary falls in the {int(get_tax_rate(amount)*100)}% federal tax bracket (2024 rates). Federal tax is progressive. After federal tax, you keep roughly ${net:,} per year. The calculator above applies these brackets.</p>
      <h3>Example With Real Numbers</h3>
      <p>At ${amount:,} gross, you pay about ${amount-net:,} in federal tax, leaving ${net:,} net per year. That is ${net_mo:,} per month or ${net_bi:,} per biweekly paycheck after federal tax. State tax and pre-tax deductions will reduce your actual paycheck.</p>
      <h3>When This Calculator Is Useful</h3>
      <p>Use it when evaluating a {disp} offer, planning a budget, or applying for a loan. It helps you see the gap between gross and take-home.</p>'''

    faq_html = "<h2>FAQ</h2>\n" + "\n".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in faqs)
    related_block = f'<div class="internal-links"><p>Related:</p><ul>{related}</ul></div>'

    html = html.replace("{{CONTENT}}", content)
    html = html.replace("{{FAQ}}", f'<div class="faq-section">\n{faq_html}\n</div>')
    html = html.replace("{{RELATED}}", related_block)

    return slug, html

def build_monthly_pay(rate):
    slug = f"{rate}-an-hour-monthly-pay.html"
    y = yearly_from_hourly(rate)
    m = monthly_from_yearly(y)
    net = estimate_net(y)
    net_mo = net // 12

    faqs = [
        (f"How much is ${rate} an hour per month gross?",
         f"At 40 hours per week, ${rate}/hr = ${m:,.0f} per month gross. Multiply hourly by 173.33 or annual ÷ 12."),
        (f"How much is ${rate} an hour per month after tax?",
         f"After federal taxes (approx.), about ${net_mo:,} per month take-home. State tax and deductions will reduce this."),
        (f"What is ${rate} an hour annually?",
         f"${rate}/hr full-time = {fmt(y)} per year gross. See our ${rate} an hour yearly guide for the full breakdown."),
        ("Is monthly pay the same every month?",
         "Gross monthly is consistent for full-time. Take-home can vary with deductions, bonus pay, or months with 3 biweekly checks."),
        (f"What can change my monthly take-home at ${rate}/hr?",
         "State tax, 401(k), health insurance, overtime, and filing status all affect your actual paycheck."),
    ]

    related = f'<li><a href="{rate}-dollar-an-hour-is-how-much-a-year.html">${rate} an hour to yearly</a></li>\n          <li><a href="{rate}-an-hour-biweekly-pay.html">${rate} an hour biweekly</a></li>\n          <li><a href="25-an-hour-monthly-pay.html">$25 an hour monthly</a></li>\n          <li><a href="30-an-hour-monthly-pay.html">$30 an hour monthly</a></li>\n          <li><a href="60000-a-year-is-how-much-a-month.html">$60k a year monthly</a></li>\n          <li><a href="salary-guides.html">Salary Guides</a></li>\n          <li><a href="index.html">Salary Calculator</a></li>'

    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})

    html = COMMON_HEAD.replace("{{META_DESC}}", f"${rate}/hr = ${m:,.0f}/month gross (40 hrs). Free calculator + after-tax estimate.")
    html = html.replace("{{PAGE_TITLE}}", f"${rate} an Hour is How Much a Month? (Monthly Pay Calculator)")
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{OG_TITLE}}", f"${rate} an Hour is How Much a Month?")
    html = html.replace("{{OG_DESC}}", f"${rate}/hr = ${m:,.0f}/month gross. Free calculator.")
    html = html.replace("{{TW_TITLE}}", f"${rate}/hr Monthly Pay")
    html = html.replace("{{TW_DESC}}", f"${rate}/hr = ${m:,.0f}/month. Free calculator.")
    html = html.replace("{{H1}}", f"${rate} an Hour is How Much a Month?")
    html = html.replace("{{INTRO}}", f"At ${rate} per hour working 40 hours per week, your gross monthly pay is <strong>${m:,.0f}</strong>. Use the calculator below to adjust the rate or see your estimated take-home after taxes.")
    html = html.replace("{{HIGHLIGHT}}", f'<span class="amount">${m:,.0f}</span> per month gross (40 hrs/week)')
    html = html.replace("{{FAQ_JSONLD}}", faq_ld)

    calc = f'''<div class="calculator-card" data-calculator="hourly-to-salary">
      <h2>Try a Different Rate</h2>
      <p class="subtitle">Enter any hourly wage to see yearly, monthly, and take-home. Assumes 40 hrs/week.</p>
      <div class="form-group">
        <label for="hourly">Hourly rate ($)</label>
        <input type="number" id="hourly" data-input="hourly" inputmode="decimal" value="{rate}" min="0" step="0.01">
      </div>
      <div class="ad-slot ad-slot-in-calculator">
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="2222222222" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
      <div class="results-section">
        <h3>Results</h3>
        <div class="result-item"><span class="label">Annual salary (gross)</span><span class="value" data-output="gross-yearly">{fmt(y)}</span></div>
        <div class="result-item highlight"><span class="label">Monthly (gross)</span><span class="value">${m:,.0f}</span></div>
        <div class="result-item"><span class="label">Est. tax (approx.)</span><span class="value" data-output="tax-estimate">$0</span></div>
        <div class="result-item"><span class="label">Net annual (approx.)</span><span class="value" data-output="net-yearly">$0</span></div>
      </div>
      <div class="related-calculations"><h3>Related Calculations</h3><ul>{related}</ul></div>
    </div>'''
    html = html.replace("{{CALCULATOR}}", calc)

    content = f'''<h2>Understanding ${rate} an Hour Monthly Pay</h2>
      <h3>How Monthly Pay Is Calculated</h3>
      <p>Monthly pay from an hourly rate: hourly × 40 × 52 ÷ 12 = hourly × 173.33. For ${rate}/hr: ${rate} × 173.33 = ${m:,.0f} per month gross.</p>
      <h3>Example With Real Numbers</h3>
      <p>At ${rate}/hr full-time, you earn {fmt(y)} per year gross. Divide by 12: ${m:,.0f} per month. After federal taxes, take-home is roughly ${net_mo:,} per month.</p>
      <h3>When This Page Is Useful</h3>
      <p>Use it when budgeting for rent, comparing a ${rate}/hr offer to a salaried role, or planning monthly expenses.</p>'''

    faq_html = "<h2>FAQ</h2>\n" + "\n".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in faqs)
    related_block = f'<div class="internal-links"><p>Related:</p><ul>{related}</ul></div>'
    html = html.replace("{{CONTENT}}", content)
    html = html.replace("{{FAQ}}", f'<div class="faq-section">\n{faq_html}\n</div>')
    html = html.replace("{{RELATED}}", related_block)

    return slug, html

def build_biweekly_pay(rate):
    slug = f"{rate}-an-hour-biweekly-pay.html"
    y = yearly_from_hourly(rate)
    bi = biweekly_from_yearly(y)
    net = estimate_net(y)
    net_bi = net // 26

    faqs = [
        (f"How much is ${rate} an hour biweekly gross?",
         f"At 80 hours per pay period, ${rate}/hr = ${bi:,.0f} gross per biweekly check."),
        (f"How much is ${rate} an hour biweekly after tax?",
         f"After federal taxes (approx.), about ${net_bi:,} per biweekly paycheck. State tax and deductions will reduce this."),
        (f"What is ${rate} an hour per year?",
         f"${rate}/hr full-time = {fmt(y)} per year gross. Biweekly = {fmt(y)} ÷ 26 = ${bi:,.0f}."),
        ("How many biweekly paychecks per year?",
         "26. Biweekly = every 2 weeks, so 52 ÷ 2 = 26 pay periods."),
        (f"What can change my biweekly take-home at ${rate}/hr?",
         "State tax, 401(k), health insurance, overtime, and filing status all affect your actual paycheck."),
    ]

    related = f'<li><a href="{rate}-dollar-an-hour-is-how-much-a-year.html">${rate} an hour to yearly</a></li>\n          <li><a href="{rate}-an-hour-monthly-pay.html">${rate} an hour monthly</a></li>\n          <li><a href="25-an-hour-biweekly-pay.html">$25 an hour biweekly</a></li>\n          <li><a href="30-an-hour-biweekly-pay.html">$30 an hour biweekly</a></li>\n          <li><a href="60000-a-year-is-how-much-a-month.html">$60k a year monthly</a></li>\n          <li><a href="salary-guides.html">Salary Guides</a></li>\n          <li><a href="index.html">Salary Calculator</a></li>'

    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})

    html = COMMON_HEAD.replace("{{META_DESC}}", f"${rate}/hr = ${bi:,.0f} biweekly gross (80 hrs). Free calculator + after-tax estimate.")
    html = html.replace("{{PAGE_TITLE}}", f"${rate} an Hour is How Much Biweekly? (Biweekly Pay Calculator)")
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{OG_TITLE}}", f"${rate} an Hour is How Much Biweekly?")
    html = html.replace("{{OG_DESC}}", f"${rate}/hr = ${bi:,.0f} biweekly gross. Free calculator.")
    html = html.replace("{{TW_TITLE}}", f"${rate}/hr Biweekly Pay")
    html = html.replace("{{TW_DESC}}", f"${rate}/hr = ${bi:,.0f} biweekly. Free calculator.")
    html = html.replace("{{H1}}", f"${rate} an Hour is How Much Biweekly?")
    html = html.replace("{{INTRO}}", f"At ${rate} per hour working 40 hours per week, your gross biweekly pay (every 2 weeks) is <strong>${bi:,.0f}</strong>. Use the calculator below to adjust the rate or see your estimated take-home.")
    html = html.replace("{{HIGHLIGHT}}", f'<span class="amount">${bi:,.0f}</span> per biweekly paycheck gross (80 hrs)')
    html = html.replace("{{FAQ_JSONLD}}", faq_ld)

    calc = f'''<div class="calculator-card" data-calculator="hourly-to-salary">
      <h2>Try a Different Rate</h2>
      <p class="subtitle">Enter any hourly wage to see yearly and take-home. Biweekly = yearly ÷ 26.</p>
      <div class="form-group">
        <label for="hourly">Hourly rate ($)</label>
        <input type="number" id="hourly" data-input="hourly" inputmode="decimal" value="{rate}" min="0" step="0.01">
      </div>
      <div class="ad-slot ad-slot-in-calculator">
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-7502486843743422" data-ad-slot="2222222222" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
      <div class="results-section">
        <h3>Results</h3>
        <div class="result-item"><span class="label">Annual salary (gross)</span><span class="value" data-output="gross-yearly">{fmt(y)}</span></div>
        <div class="result-item highlight"><span class="label">Biweekly (gross)</span><span class="value">${bi:,.0f}</span></div>
        <div class="result-item"><span class="label">Est. tax (approx.)</span><span class="value" data-output="tax-estimate">$0</span></div>
        <div class="result-item"><span class="label">Net annual (approx.)</span><span class="value" data-output="net-yearly">$0</span></div>
      </div>
      <div class="related-calculations"><h3>Related Calculations</h3><ul>{related}</ul></div>
    </div>'''
    html = html.replace("{{CALCULATOR}}", calc)

    content = f'''<h2>Understanding ${rate} an Hour Biweekly Pay</h2>
      <h3>How Biweekly Pay Is Calculated</h3>
      <p>Biweekly = paid every two weeks. Full-time workers work 80 hours per pay period. So: ${rate} × 80 = ${bi:,.0f} per biweekly check. You receive 26 paychecks per year.</p>
      <h3>Example With Real Numbers</h3>
      <p>At ${rate}/hr full-time, you earn {fmt(y)} per year gross. Biweekly: ${bi:,.0f} gross. After federal taxes, take-home is roughly ${net_bi:,} per biweekly paycheck.</p>
      <h3>When This Page Is Useful</h3>
      <p>Use it when your employer pays biweekly and you need to plan around each paycheck, when comparing offers, or when budgeting for bills due every two weeks.</p>'''

    faq_html = "<h2>FAQ</h2>\n" + "\n".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q,a in faqs)
    related_block = f'<div class="internal-links"><p>Related:</p><ul>{related}</ul></div>'
    html = html.replace("{{CONTENT}}", content)
    html = html.replace("{{FAQ}}", f'<div class="faq-section">\n{faq_html}\n</div>')
    html = html.replace("{{RELATED}}", related_block)

    return slug, html

# 30 new pages - DO NOT include existing
EXISTING_HOURLY = {12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,45,50,60,70,80}
EXISTING_SALARY = {60000,70000,75000,80000,85000,90000,95000,100000,110000,120000}
EXISTING_MONTHLY = {25, 30}
EXISTING_BIWEEKLY = {20, 25, 30}

HOURLY_RATES = [13, 41, 43, 44, 46, 47, 48, 49, 51, 52]
SALARY_AMOUNTS = [55000, 58000, 62000, 65000, 68000, 72000, 78000, 82000, 88000, 92000]
MONTHLY_RATES = [22, 27, 31, 35, 40]
BIWEEKLY_RATES = [22, 27, 31, 35, 40]

def main():
    generated = []
    out_dir = PROJECT_ROOT

    for rate in HOURLY_RATES:
        if rate in EXISTING_HOURLY:
            continue
        slug, html = build_hourly_yearly(rate)
        (out_dir / slug).write_text(html, encoding="utf-8")
        generated.append(slug)

    for amount in SALARY_AMOUNTS:
        if amount in EXISTING_SALARY:
            continue
        slug, html = build_salary_after_tax(amount)
        (out_dir / slug).write_text(html, encoding="utf-8")
        generated.append(slug)

    for rate in MONTHLY_RATES:
        if rate in EXISTING_MONTHLY:
            continue
        slug, html = build_monthly_pay(rate)
        (out_dir / slug).write_text(html, encoding="utf-8")
        generated.append(slug)

    for rate in BIWEEKLY_RATES:
        if rate in EXISTING_BIWEEKLY:
            continue
        slug, html = build_biweekly_pay(rate)
        (out_dir / slug).write_text(html, encoding="utf-8")
        generated.append(slug)

    for s in generated:
        print(f"Generated {s}")
    print(f"\nTotal: {len(generated)} pages")
    return generated

if __name__ == "__main__":
    main()
