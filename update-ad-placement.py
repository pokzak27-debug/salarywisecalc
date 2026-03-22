#!/usr/bin/env python3
"""Restructure ad placements: below H1, between inputs/results, end of page."""

import os
import re

ADSENSE_CLIENT = "ca-pub-XXXXXXXXXXXXXXXX"
AD_SLOT_BELOW_H1 = "1111111111"
AD_SLOT_IN_CALC = "2222222222"
AD_SLOT_END = "3333333333"

AD_BLOCK = '''    <div class="ad-slot ad-slot-{pos}">
      <ins class="adsbygoogle" style="display:block" data-ad-client="{client}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
'''

# Regex to remove existing ad blocks (any of top/mid/footer) - keep surrounding newlines
AD_REMOVE = re.compile(
    r'\n    <div class="ad-slot ad-slot-(?:top|mid|footer)">\s*'
    r'<ins class="adsbygoogle"[^>]*></ins>\s*'
    r'<script>\(adsbygoogle[^<]*</script>\s*'
    r'</div>',
    re.DOTALL
)


def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Remove all existing ad slots
    html = AD_REMOVE.sub("", html)

    ad_below_h1 = AD_BLOCK.format(pos="below-h1", client=ADSENSE_CLIENT, slot=AD_SLOT_BELOW_H1)
    ad_in_calc = AD_BLOCK.format(pos="in-calculator", client=ADSENSE_CLIENT, slot=AD_SLOT_IN_CALC)
    ad_end = AD_BLOCK.format(pos="end", client=ADSENSE_CLIENT, slot=AD_SLOT_END)

    # 2. Ad below H1
    if '<div class="hero-calculator"' in html:
        # Index: after hero-subtitle, before form-row
        html = html.replace(
            '<p class="hero-subtitle">Convert hourly wage to yearly salary and back. Tax estimate included.</p>\n\n      <div class="form-row">',
            '<p class="hero-subtitle">Convert hourly wage to yearly salary and back. Tax estimate included.</p>\n' + ad_below_h1 + '      <div class="form-row">'
        )
    elif '<div class="salary-highlight">' in html:
        # SEO/after-tax: after page-intro, before salary-highlight
        html = html.replace(
            '</div>\n\n    <div class="salary-highlight">',
            '</div>\n\n' + ad_below_h1 + '    <div class="salary-highlight">'
        )
    elif '<div class="calculator-card"' in html and '<div class="page-intro">' in html:
        # Hourly/salary: after page-intro, before calculator-card
        html = html.replace(
            '</div>\n\n    <div class="calculator-card"',
            '</div>\n\n' + ad_below_h1 + '    <div class="calculator-card"'
        )
    else:
        # Simple pages: after page-intro, before page-content
        html = html.replace(
            '</div>\n\n    <section class="page-content',
            '</div>\n\n' + ad_below_h1 + '    <section class="page-content'
        )

    # 3. Ad between inputs and results (calculator pages only)
    if '<div class="form-row">' in html and '<div class="results-box">' in html:
        # Index: form-row then results-box
        html = html.replace(
            '      </div>\n\n      <div class="results-box">',
            '      </div>\n\n' + ad_in_calc + '      <div class="results-box">'
        )
    elif '<div class="results-section">' in html:
        # Calculator-card: form-group then results-section
        html = html.replace(
            '      </div>\n      <div class="results-section">',
            '      </div>\n' + ad_in_calc + '      <div class="results-section">',
            1
        )

    # 4. Ad at end of page (last element in main, before </main>)
    html = html.replace(
        '\n  </main>\n\n  <footer class="site-footer">',
        '\n' + ad_end + '  </main>\n\n  <footer class="site-footer">'
    )
    # That adds ad before </main> but the newline - we need ad to be inside main.
    # So: ... </div> \n  </main> becomes ... </div> \n AD \n  </main>
    # The ad_end has trailing newline. So we get ... </div> \n "    <div class=ad-slot>..." \n  </main>
    # The ad div has 4 spaces indent - it should be inside main which has 2 spaces. So we need 4 spaces for children of main. The main's direct children have 4 spaces. Good.

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    count = 0
    for name in sorted(os.listdir(".")):
        if name.endswith(".html"):
            try:
                update_file(name)
                count += 1
                print(f"Updated {name}")
            except Exception as e:
                print(f"Error {name}: {e}")
    print(f"\nDone. Updated {count} files.")


if __name__ == "__main__":
    main()
