"""Extrai os <svg> de um capitulo renderizado e gera PNG de cada um.

Uso: python scripts/rasterizar_figuras.py vol09/cap055-....qmd [destino]
"""

import re
import subprocess
import sys
from pathlib import Path

CHROME = Path.home() / ("AppData/Local/quarto/chrome-headless-shell/"
                        "chrome-headless-shell-win64/chrome-headless-shell.exe")

qmd = Path(sys.argv[1])
destino = Path(sys.argv[2] if len(sys.argv) > 2 else "_figuras-check")
destino.mkdir(parents=True, exist_ok=True)

html = Path("_book") / qmd.with_suffix(".html")
h = html.read_text(encoding="utf-8")
svgs = re.findall(r"<svg.*?</svg>", h, re.S)

base = qmd.stem.split("-")[0]
for i, svg in enumerate(svgs, 1):
    pagina = destino / f"{base}-fig{i}.html"
    pagina.write_text(
        "<html><body style='margin:0;background:#fff'>" + svg + "</body></html>",
        encoding="utf-8")
    png = destino / f"{base}-fig{i}.png"
    subprocess.run([str(CHROME), "--headless", "--disable-gpu",
                    "--hide-scrollbars", "--window-size=1500,900",
                    f"--screenshot={png.resolve()}", pagina.resolve().as_uri()],
                   capture_output=True)
    print(f"{png}  {png.stat().st_size if png.exists() else 0} bytes")
