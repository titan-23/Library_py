# furo

if __name__ == "__main__":
    # css
    css = """
/* user settings */
/* コードブロックのスタイル */
pre {
  max-height: 30em !important;
}
"""
    with open(
        "./_docs/_build/_static/styles/furo-extensions.css", "a", encoding="utf-8"
    ) as f:
        print(css, file=f)
