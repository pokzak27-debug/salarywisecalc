#!/usr/bin/env python3
"""Insert GA4 gtag.js immediately after <head> (once per page)."""
from pathlib import Path

PROJECT = Path(__file__).parent.parent
GA_ID = "G-Y8M6Q89EPR"

GTAG_SNIPPET = f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
  </script>
"""

# Insert before GTM if present (keeps gtag first after <head>)
MARKER_GTM = "<head>\n  <!-- Google Tag Manager -->"
REPLACEMENT_GTM = "<head>\n" + GTAG_SNIPPET + "  <!-- Google Tag Manager -->"

# Fallback: no GTM yet
MARKER_META = "<head>\n  <meta charset=\"UTF-8\">"
REPLACEMENT_META = "<head>\n" + GTAG_SNIPPET + "  <meta charset=\"UTF-8\">"


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if GA_ID in text:
        return False
    if MARKER_GTM in text:
        text = text.replace(MARKER_GTM, REPLACEMENT_GTM, 1)
        path.write_text(text, encoding="utf-8")
        return True
    if MARKER_META in text:
        text = text.replace(MARKER_META, REPLACEMENT_META, 1)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for p in sorted(PROJECT.glob("*.html")):
        if inject(p):
            n += 1
            print(f"Injected GA4 gtag: {p.name}")
    print(f"Done. Updated {n} files.")


if __name__ == "__main__":
    main()
