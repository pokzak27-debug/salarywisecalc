#!/usr/bin/env python3
"""Generate SEO pages for SalaryWiseCalc: $X an hour is how much a year."""

RATES = [12, 14, 16, 17, 19, 21, 23, 24, 26, 27, 29, 31, 32, 33, 34, 36, 37, 38, 39, 42]
ALL_RATES = sorted([12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 45, 50, 60, 70, 80])

def slug(r):
    return f"{r}-dollar-an-hour-is-how-much-a-year.html"

def fmt(n):
    return f"${n:,.0f}"

def yearly(r):
    return r * 2080

def monthly(r):
    return yearly(r) / 12

def weekly(r):
    return r * 40

def adjacent_links(current):
    idx = ALL_RATES.index(current)
    start = max(0, idx - 4)
    end = min(len(ALL_RATES), idx + 7)
    nearby = [r for r in ALL_RATES[start:end] if r != current][:10]
    return nearby

EXPLANATIONS = [
    "This rate is common for entry-level or part-time roles in many sectors.",
    "Many retail and service jobs offer wages in this range.",
    "This falls within typical pay for skilled hourly workers.",
    "Overtime, bonuses, or a different schedule will change your actual earnings.",
    "Your take-home will be less after federal and state taxes.",
]

def get_explanation(rate):
    return EXPLANATIONS[rate % len(EXPLANATIONS)]

def get_faqs(rate):
    y = yearly(rate)
    low = int(y * 0.84)
    high = int(y * 0.91)
    return [
        (f"How much is ${rate} an hour per year after taxes?",
         f"After federal taxes (approx.), ${rate}/hr full-time nets around ${low:,}–${high:,} per year. State taxes and deductions vary."),
        (f"How much is ${rate} an hour weekly?",
         f"At 40 hours per week, ${rate}/hr gives you {fmt(weekly(rate))} gross per week."),
        (f"Is ${rate} an hour a livable wage?",
         "It depends on location and household size. In lower-cost areas it can cover basics; in cities, it may be tight."),
    ]

def page(rate):
    y, m, w = yearly(rate), monthly(rate), weekly(rate)
    links = adjacent_links(rate)
    faqs = get_faqs(rate)
    fname = slug(rate)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="${rate}/hr = {fmt(y)}/year. Free calculator + full breakdown. Tax estimate & net pay. Answer in seconds.">
  <title>${rate} an Hour is How Much a Year? (Calculator + Breakdown)</title>
  <link rel="canonical" href="https://salarywisecalc.com/{fname}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${rate} an Hour is How Much a Year? (Calculator + Breakdown)">
  <meta property="og:description" content="${rate}/hr = {fmt(y)}/year. Free calculator + full breakdown.">
  <meta property="og:url" content="https://salarywisecalc.com/{fname}">
  <meta property="og:site_name" content="SalaryWiseCalc">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="${rate} an Hour is How Much a Year? (Calculator + Breakdown)">
  <meta name="twitter:description" content="${rate}/hr = {fmt(y)}/year. Free calculator.">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="index.html" class="site-logo">SalaryWiseCalc</a>
      <nav class="nav-links" aria-label="Main navigation">
        <a href="index.html">Calculator</a>
        <a href="hourly-to-salary.html">Hourly → Salary</a>
        <a href="salary-to-hourly.html">Salary → Hourly</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="page-intro">
      <h1>${rate} an Hour Is How Much a Year?</h1>
      <p>If you earn ${rate} per hour and work 40 hours per week for 52 weeks, your gross annual salary is <strong>{fmt(y)}</strong>. Use the calculator below to see tax estimate and net pay.</p>
    </div>

    <div class="salary-highlight">
      <span class="amount">{fmt(y)}</span> per year · {fmt(m)}/mo · {fmt(w)}/wk (gross, 40 hrs)
    </div>

    <div class="calculator-card" data-calculator="hourly-to-salary">
      <h2>Try a Different Rate</h2>
      <p class="subtitle">Adjust the hourly rate to see the annual equivalent. Based on 40 hrs/week.</p>
      <div class="form-group">
        <label for="hourly">Hourly rate ($)</label>
        <input type="number" id="hourly" data-input="hourly" inputmode="decimal" value="{rate}" min="0" step="0.01">
      </div>
      <div class="results-section">
        <h3>Results</h3>
        <div class="result-item highlight">
          <span class="label">Annual salary (gross)</span>
          <span class="value" data-output="gross-yearly">{fmt(y)}</span>
        </div>
        <div class="result-item">
          <span class="label">Est. tax (approx.)</span>
          <span class="value" data-output="tax-estimate">$0</span>
        </div>
        <div class="result-item">
          <span class="label">Net annual (approx.)</span>
          <span class="value" data-output="net-yearly">$0</span>
        </div>
      </div>
    </div>

    <section class="page-content">
      <h2>Understanding ${rate} an Hour</h2>
      <p>${rate} hourly works out to about {fmt(m)} per month and {fmt(w)} per week before taxes. {get_explanation(rate)} Overtime, bonuses, or a different schedule will change your actual earnings.</p>

      <div class="faq-section">
        <h2>FAQ</h2>
''' + "\n".join(f'''        <div class="faq-item">
          <h3>{q}</h3>
          <p>{a}</p>
        </div>''' for q, a in faqs) + '''

      </div>

      <div class="internal-links">
        <p>Related hourly to yearly:</p>
        <ul>
''' + "\n".join(f'          <li><a href="{slug(r)}">${r} an hour</a></li>' for r in links) + '''
          <li><a href="index.html">Salary Calculator</a></li>
          <li><a href="hourly-to-salary.html">Hourly to Salary Calculator</a></li>
        </ul>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-links">
        <a href="index.html">Calculator</a>
        <a href="hourly-to-salary.html">Hourly → Salary</a>
        <a href="salary-to-hourly.html">Salary → Hourly</a>
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
</html>
'''

def main():
    for r in RATES:
        with open(slug(r), "w") as f:
            f.write(page(r))
        print(f"Created {slug(r)}")

if __name__ == "__main__":
    main()
