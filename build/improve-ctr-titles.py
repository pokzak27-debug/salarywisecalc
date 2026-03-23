#!/usr/bin/env python3
"""
Improve all titles and meta descriptions for maximum CTR.
Rules: start with keyword, add curiosity, add benefit, keep clear and natural.
"""

import re
from pathlib import Path

PROJECT = Path(__file__).parent.parent

# Mapping: filename pattern or exact name -> (title, meta_description)
# Use {amount}, {amt}, {country}, {currency} etc. for templates

UPDATES = {}

def add_exact(name, title, desc):
    UPDATES[name] = (title, desc)

def add_pattern(pattern, title_fn, desc_fn):
    UPDATES[("pattern", pattern, title_fn, desc_fn)] = None

# --- Main calculators ---
add_exact("index.html", 
    "Salary Calculator: What's Your Hourly Wage Worth Per Year? (Free + Tax Estimate)",
    "Convert hourly to yearly—or yearly to hourly—in seconds. See your real take-home after tax. Free calculator. No signup.")
add_exact("hourly-to-salary.html",
    "$X an Hour is How Much a Year? Convert Any Wage Instantly (Free Calculator)",
    "Type your hourly rate. Get yearly salary + take-home in 2 clicks. Free calculator with tax estimate. Compare offers.")
add_exact("salary-to-hourly.html",
    "$60k, $70k, $100k = How Much Per Hour? (Free Salary to Hourly Calculator)",
    "Convert any salary to hourly wage instantly. See what you really earn per hour after tax. Free. No signup.")

# --- Salary guides hub ---
add_exact("salary-guides.html",
    "Salary Calculators & Guides: Find Your Rate, After-Tax Pay & More (Free)",
    "Every salary tool you need: hourly to yearly, after-tax, country-specific. Find your number in seconds. All free.")

# --- Hourly to yearly (N-dollar-an-hour-is-how-much-a-year) ---
def hourly_year_title(m):
    amt = m.group(1)
    return f"${amt} an Hour is How Much a Year? (Full Breakdown + Calculator)"
def hourly_year_desc(m):
    amt = m.group(1)
    annual = int(amt) * 2080
    return f"${amt}/hr = ${annual:,}/year. See exact monthly, biweekly & take-home. Free calculator. Answer in seconds."
add_pattern(r"(\d+)-dollar-an-hour-is-how-much-a-year\.html", hourly_year_title, hourly_year_desc)

# --- Salary after tax (N-salary-after-tax, Nk-salary-after-tax) ---
def sal_at_title(m):
    amt = m.group(1)
    if amt.endswith("k"):
        return f"${amt} After Tax: How Much Do You Really Take Home? (Free Calculator)"
    return f"${int(amt):,} After Tax: How Much Do You Really Take Home? (Free Calculator)"
def sal_at_desc(m):
    amt = m.group(1)
    if amt.endswith("k"):
        return f"${amt} salary after tax—see your real take-home. Free calculator + monthly & biweekly breakdown. Plan your budget."
    return f"${int(amt):,} after tax: see your real take-home. Free calculator + monthly & biweekly breakdown. Plan your budget."
add_pattern(r"(\d+k|\d+)-salary-after-tax\.html", sal_at_title, sal_at_desc)

# --- Year to month (N-a-year-is-how-much-a-month) ---
def year_month_title(m):
    amt = int(m.group(1))
    return f"${amt:,} a Year is How Much a Month? (Exact Amount + Budget Calculator)"
def year_month_desc(m):
    amt = int(m.group(1))
    mo = amt // 12
    return f"${amt:,}/year = ${mo:,}/month. See take-home estimate. Free calculator. Plan your budget in seconds."
add_pattern(r"(\d+)-a-year-is-how-much-a-month\.html", year_month_title, year_month_desc)

# --- Hourly monthly (N-an-hour-monthly-pay) ---
def hourly_mo_title(m):
    return f"${m.group(1)} an Hour is How Much a Month? (Monthly Pay Calculator)"
def hourly_mo_desc(m):
    amt = int(m.group(1))
    mo = amt * 2080 // 12
    return f"${amt}/hr = ${mo:,}/month gross. Free calculator + after-tax estimate. Plan your budget."
add_pattern(r"(\d+)-an-hour-monthly-pay\.html", hourly_mo_title, hourly_mo_desc)

# --- Hourly biweekly (N-an-hour-biweekly-pay) ---
def hourly_bi_title(m):
    return f"${m.group(1)} an Hour is How Much Biweekly? (Paycheck Calculator)"
def hourly_bi_desc(m):
    amt = int(m.group(1))
    bi = amt * 80
    return f"${amt}/hr = ${bi:,} biweekly (80 hrs). See after-tax estimate. Free calculator."
add_pattern(r"(\d+)-an-hour-biweekly-pay\.html", hourly_bi_title, hourly_bi_desc)

# --- Hourly after tax USA (N-an-hour-after-tax.html, not country-specific) ---
def hourly_at_title(m):
    return f"${m.group(1)} an Hour After Tax: What You Really Take Home (Free Calculator)"
def hourly_at_desc(m):
    amt = int(m.group(1))
    gross = amt * 2080
    return f"${amt}/hr full-time = ${gross:,} gross. See your real take-home after federal tax. Free calculator + breakdown."
add_pattern(r"(\d+)-an-hour-after-tax\.html", hourly_at_title, hourly_at_desc)

# --- Guides ---
add_exact("how-salary-conversion-works.html",
    "How Salary Conversion Works: Hourly, Yearly, Monthly & After-Tax (Simple Guide)",
    "Learn the exact formulas. How does $25/hr become yearly? Why gross ≠ take-home? Clear examples + table.")
add_exact("gross-vs-net-salary.html",
    "Gross vs Net Salary: What's the Difference? (And Why It Matters for Your Budget)",
    "Gross is before tax. Net is what you keep. See real examples. Plan your budget with the right number.")
add_exact("weekly-vs-biweekly-vs-monthly-pay.html",
    "Weekly vs Biweekly vs Monthly Pay: Which Gives You More? (Pay Frequency Explained)",
    "Same salary, different paycheck size. Why do some months have 3 paychecks? Free conversion calculator.")
add_exact("salary-negotiation-guide.html",
    "Salary Negotiation Guide: How to Compare Offers & Get More (Gross vs Take-Home)",
    "Don't accept until you know your real take-home. Use our calculators. Negotiate from strength.")
add_exact("compare-salary-offers-guide.html",
    "Compare Salary Offers: Gross Isn't Enough—See Your Real Take-Home (Free Calculator)",
    "Two offers, same salary? Benefits & location change everything. Compare net pay before you decide.")
add_exact("salary-raise-calculator-guide.html",
    "Salary Raise Calculator: What Does That Raise Really Add to Your Paycheck? (Free)",
    "5% raise ≠ 5% more in your pocket. See your real take-home gain. Free calculator + examples.")
add_exact("salary-budgeting-guide.html",
    "Salary Budgeting Guide: 50-30-20 Rule, Rent Limits & How to Plan With Take-Home (Free)",
    "Budget with net, not gross. 50-30-20 rule, rent rules, real examples. Free calculators included.")
add_exact("cost-of-living-salary-guide.html",
    "Cost of Living vs Salary: Does $70k in Austin Feel Like $90k in NYC? (Location Guide)",
    "Same salary, different lifestyle. How location changes your take-home. Compare before you move.")
add_exact("part-time-salary-calculator.html",
    "Part-Time Salary Calculator: 20 or 30 Hours = How Much a Year? (Free)",
    "Convert part-time hourly to yearly. 20 hrs? 30 hrs? Get your number in seconds. Free calculator.")
add_exact("salary-comparison-guides.html",
    "Salary Comparison: Side-by-Side Hourly, Yearly & After-Tax (Free Tools)",
    "Compare rates, salaries, and take-home pay. See the real difference. Free calculators.")

# --- Hourly after tax USA (full breakdown) ---
add_exact("25-an-hour-after-taxes-usa.html",
    "$25 an Hour After Tax USA: Your Real Take-Home (Full Breakdown + Calculator)",
    "$25/hr full-time in USA. See your real take-home after federal & state tax. Free calculator + full breakdown.")
add_exact("40-an-hour-after-taxes-usa.html",
    "$40 an Hour After Tax USA: Your Real Take-Home (Full Breakdown + Calculator)",
    "$40/hr full-time in USA. See your real take-home after federal & state tax. Free calculator + full breakdown.")

# --- Salary after tax USA ---
add_exact("salary-after-tax-usa.html",
    "Salary After Tax USA: How Much Do You Really Take Home? (Free Calculator)",
    "Enter any salary. See your take-home after federal tax. Monthly, biweekly. Free. No signup.")

# --- Country salary calculators ---
COUNTRIES = {
    "usa": ("USA", "US workers"),
    "uk": ("UK", "UK workers"),
    "canada": ("Canada", "Canadian workers"),
    "australia": ("Australia", "Australian workers"),
    "ireland": ("Ireland", "Irish workers"),
    "new-zealand": ("New Zealand", "Kiwi workers"),
    "south-africa": ("South Africa", "South African workers"),
    "singapore": ("Singapore", "Singapore workers"),
    "jamaica": ("Jamaica", "Jamaican workers"),
    "trinidad-and-tobago": ("Trinidad & Tobago", "Trinidad & Tobago workers"),
    "barbados": ("Barbados", "Barbadian workers"),
    "bahamas": ("Bahamas", "Bahamian workers"),
    "philippines": ("Philippines", "Filipino workers"),
    "nigeria": ("Nigeria", "Nigerian workers"),
    "kenya": ("Kenya", "Kenyan workers"),
    "uae": ("UAE", "workers in Dubai, Abu Dhabi & UAE"),
    "morocco": ("Morocco", "Moroccan workers"),
}
for slug, (name, workers) in COUNTRIES.items():
    add_exact(f"salary-calculator-{slug}.html",
        f"{name} Salary Calculator: Hourly to Yearly in Seconds (Free + Tax Estimate)",
        f"Convert hourly to yearly for {workers}. Tax context included. Free calculator. Plan your budget.")

# --- Country-specific overrides ---
add_exact("salary-calculator-uae.html",
    "UAE Salary Calculator: Dubai, Abu Dhabi—Hourly to Yearly (No Income Tax)",
    "Convert hourly to yearly for Dubai, Abu Dhabi & UAE. No income tax. Free calculator. Plan in AED.")
add_exact("salary-calculator-bahamas.html",
    "Bahamas Salary Calculator: Hourly to Yearly (No Income Tax—NIB Only)",
    "Convert hourly to yearly for Bahamas. No income tax—NIB only. Free calculator. Plan in BSD.")

# --- Country hourly after tax (e.g. 20-an-hour-after-tax-uk, 30-an-hour-after-tax-canada) ---
def country_hr_at_title(m):
    amt, country = m.group(1), m.group(2).replace("-", " ").title()
    return f"${amt} an Hour After Tax {country}: Your Real Take-Home (Free Calculator)"
def country_hr_at_desc(m):
    amt, country = m.group(1), m.group(2).replace("-", " ")
    return f"${amt}/hr after tax in {country}. See your real take-home. Free calculator + breakdown."
add_pattern(r"(\d+)-an-hour-after-tax-([a-z-]+)\.html", country_hr_at_title, country_hr_at_desc)

# --- Special currency hourly after tax ---
add_exact("200-rand-an-hour-after-tax-south-africa.html",
    "R200 an Hour After Tax South Africa: Your Real Take-Home (Free Calculator)",
    "R200/hr after tax in South Africa. See your real take-home. Free calculator + breakdown.")
add_exact("200-rand-per-hour-after-tax-south-africa.html",
    "R200 an Hour After Tax South Africa: Your Real Take-Home (Free Calculator)",
    "R200/hr after tax in South Africa. See your real take-home. Free calculator + breakdown.")
add_exact("200-peso-per-hour-after-tax-philippines.html",
    "₱200 an Hour After Tax Philippines: Your Real Take-Home (Free Calculator)",
    "₱200/hr after tax in Philippines. See your real take-home. Free calculator + breakdown.")
add_exact("5000-naira-per-hour-after-tax-nigeria.html",
    "₦5,000 an Hour After Tax Nigeria: Your Real Take-Home (Free Calculator)",
    "₦5,000/hr after tax in Nigeria. See your real take-home. Free calculator + breakdown.")
add_exact("1000-shilling-per-hour-after-tax-kenya.html",
    "KES 1,000 an Hour After Tax Kenya: Your Real Take-Home (Free Calculator)",
    "KES 1,000/hr after tax in Kenya. See your real take-home. Free calculator + breakdown.")

# --- Australia 80k ---
add_exact("80000-salary-after-tax-australia.html",
    "AU$80,000 After Tax Australia: How Much Do You Really Take Home? (Free Calculator)",
    "AU$80k after tax in Australia. See your real take-home. Free calculator + breakdown. Plan your budget.")

# --- Sitemap, About, Contact, Legal ---
add_exact("sitemap.html",
    "Sitemap | All Salary Calculators & Guides | SalaryWiseCalc",
    "Browse all salary calculators, hourly guides, after-tax tools, and country pages. Find your rate fast.")
add_exact("about.html",
    "About SalaryWiseCalc | Free Salary & Wage Calculator",
    "Free salary calculator. Convert hourly to yearly, see take-home after tax. No signup, no data stored.")
add_exact("contact.html",
    "Contact SalaryWiseCalc | Questions & Feedback",
    "Have a question about our salary calculator? Get in touch. We respond quickly.")
add_exact("privacy-policy.html",
    "Privacy Policy | SalaryWiseCalc—We Don't Store Your Salary Data",
    "Your salary data stays in your browser. We don't collect or store it. No cookies for calculations.")
add_exact("terms.html",
    "Terms of Use | SalaryWiseCalc",
    "Simple terms for using our free salary calculator. Estimates only—not professional tax or financial advice.")


def get_title_desc(filename):
    """Return (title, desc) for filename or None if no update."""
    if filename in UPDATES:
        return UPDATES[filename]

    for k, v in UPDATES.items():
        if not isinstance(k, tuple):
            continue
        _, pattern, title_fn, desc_fn = k
        m = re.match(pattern, filename)
        if m:
            title = title_fn(m)
            desc = desc_fn(m)
            return (title, desc)
    return None


def update_file(path):
    content = path.read_text(encoding="utf-8")
    name = path.name
    td = get_title_desc(name)
    if not td:
        return False
    title, desc = td

    # Escape for regex
    desc_esc = re.escape(desc)
    title_esc = re.escape(title)

    # Update meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc}">',
        content, count=1
    )
    # Update title
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{title}</title>',
        content, count=1
    )
    # Update og:title
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{title}">',
        content, count=1
    )
    # Update og:description
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{desc}">',
        content, count=1
    )
    # Update twitter:title (if exists)
    content = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{title}">',
        content, count=1
    )
    # Update twitter:description (if exists)
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{desc}">',
        content, count=1
    )

    path.write_text(content, encoding="utf-8")
    return True


def main():
    updated = 0
    skipped = []
    for f in sorted(PROJECT.glob("*.html")):
        if f.name.startswith(".") or "templates" in str(f):
            continue
        if update_file(f):
            updated += 1
            print(f"Updated {f.name}")
        else:
            skipped.append(f.name)
    print(f"\nUpdated {updated} files.")
    if skipped:
        print(f"Skipped (no rule): {', '.join(skipped[:15])}{'...' if len(skipped) > 15 else ''}")


if __name__ == "__main__":
    main()
