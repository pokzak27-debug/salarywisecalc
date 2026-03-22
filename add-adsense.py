#!/usr/bin/env python3
"""Add Google AdSense to all HTML pages."""

import os
import re

# Replace with your AdSense publisher ID and ad slot IDs after approval
ADSENSE_CLIENT = "ca-pub-XXXXXXXXXXXXXXXX"
AD_SLOT_TOP = "1111111111"
AD_SLOT_MID = "2222222222"
AD_SLOT_FOOTER = "3333333333"

HEAD_SCRIPT = f'''  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
'''

AD_BLOCK = '''    <div class="ad-slot ad-slot-{pos}">
      <ins class="adsbygoogle" style="display:block" data-ad-client="{client}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
'''

def ad_block(pos, slot):
    return AD_BLOCK.format(pos=pos, client=ADSENSE_CLIENT, slot=slot)


def add_adsense(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Skip if already has AdSense
    if "adsbygoogle.js" in html:
        return False

    # 1. Add script in head (before </head>)
    html = html.replace("</head>", HEAD_SCRIPT + "</head>")

    # 2. Add ad slots
    # Ad top: before hero-calculator OR before first calculator-card (after salary-highlight if present)
    if '<div class="hero-calculator"' in html:
        html = html.replace(
            '<main>\n    <div class="hero-calculator"',
            '<main>\n' + ad_block("top", AD_SLOT_TOP) + '    <div class="hero-calculator"'
        )
    elif '</div>\n\n    <div class="calculator-card"' in html:
        # Pages with salary-highlight then calculator-card
        html = html.replace(
            '</div>\n\n    <div class="calculator-card"',
            '</div>\n\n' + ad_block("top", AD_SLOT_TOP) + '    <div class="calculator-card"'
        )
    elif '<div class="calculator-card"' in html and '<div class="page-intro">' in html:
        # hourly-to-salary, salary-to-hourly: page-intro then calculator-card
        html = html.replace(
            '</div>\n\n    <div class="calculator-card"',
            '</div>\n\n' + ad_block("top", AD_SLOT_TOP) + '    <div class="calculator-card"'
        )
    else:
        # Simple pages (about, contact, etc): after page-intro, before page-content
        html = html.replace(
            '</div>\n\n    <section class="page-content',
            '</div>\n\n' + ad_block("top", AD_SLOT_TOP) + '    <section class="page-content'
        )

    # Ad mid: after calculator/hero, before next section
    has_calculator = 'calculator-card' in html or 'hero-calculator' in html
    if '</div>\n\n    <div class="internal-links">' in html:
        html = html.replace(
            '</div>\n\n    <div class="internal-links">',
            '</div>\n\n' + ad_block("mid", AD_SLOT_MID) + '    <div class="internal-links">'
        )
    elif '</div>\n\n    <section class="page-content' in html and has_calculator:
        html = html.replace(
            '</div>\n\n    <section class="page-content',
            '</div>\n\n' + ad_block("mid", AD_SLOT_MID) + '    <section class="page-content',
            1  # Only first occurrence (after calculator)
        )
    elif not has_calculator and '</section>\n  </main>' in html:
        # Simple pages: ad mid before closing main
        html = html.replace(
            '</section>\n  </main>',
            '</section>\n' + ad_block("mid", AD_SLOT_MID) + '  </main>'
        )

    # Ad footer: at start of footer, before footer-inner
    html = html.replace(
        '<footer class="site-footer">\n    <div class="footer-inner">',
        '<footer class="site-footer">\n' + ad_block("footer", AD_SLOT_FOOTER) + '    <div class="footer-inner">'
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    count = 0
    for name in sorted(os.listdir(".")):
        if name.endswith(".html"):
            if add_adsense(name):
                count += 1
                print(f"Updated {name}")
    print(f"\nDone. Updated {count} files.")
    print("\nIMPORTANT: Replace placeholders in this script (or in HTML):")
    print(f"  - {ADSENSE_CLIENT} -> your AdSense publisher ID")
    print(f"  - {AD_SLOT_TOP}, {AD_SLOT_MID}, {AD_SLOT_FOOTER} -> your ad unit IDs")


if __name__ == "__main__":
    main()
