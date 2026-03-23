#!/usr/bin/env python3
"""Inject Google Tag Manager into all HTML pages (once)."""
from pathlib import Path

PROJECT = Path(__file__).parent.parent
GTM_ID = "GTM-W67HQBMS"

HEAD_SNIPPET = f"""  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{GTM_ID}');</script>
  <!-- End Google Tag Manager -->
"""

BODY_SNIPPET = f"""  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
"""


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if GTM_ID in text:
        return False
    if "<head>" not in text or "<body>" not in text:
        return False
    if "<head>\n" in text:
        text = text.replace("<head>\n", "<head>\n" + HEAD_SNIPPET, 1)
    elif "<head>\r\n" in text:
        text = text.replace("<head>\r\n", "<head>\r\n" + HEAD_SNIPPET.replace("\n", "\r\n"), 1)
    else:
        text = text.replace("<head>", "<head>\n" + HEAD_SNIPPET, 1)
    if "<body>\n" in text:
        text = text.replace("<body>\n", "<body>\n" + BODY_SNIPPET, 1)
    elif "<body>\r\n" in text:
        text = text.replace("<body>\r\n", "<body>\r\n" + BODY_SNIPPET.replace("\n", "\r\n"), 1)
    else:
        text = text.replace("<body>", "<body>\n" + BODY_SNIPPET, 1)
    path.write_text(text, encoding="utf-8")
    return True


def main():
    n = 0
    for p in sorted(PROJECT.glob("*.html")):
        if inject(p):
            n += 1
            print(f"Injected GTM: {p.name}")
    print(f"Done. Updated {n} files.")


if __name__ == "__main__":
    main()
