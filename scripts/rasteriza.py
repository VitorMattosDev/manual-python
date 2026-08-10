"""Rasteriza os <svg> inline de um HTML do _book em PNG, para inspecao visual.

Usa o chrome-headless-shell que o Quarto ja instala.

Uso: py -3 scripts/rasteriza.py _book/vol02/capNNN-....html <destino>
"""

import os
import re
import subprocess
import sys
from pathlib import Path

CHROME = Path(os.environ["LOCALAPPDATA"]) / (
    "quarto/chrome-headless-shell/chrome-headless-shell-win64/chrome-headless-shell.exe"
)

MOLDE = """<!doctype html><meta charset="utf-8">
<style>body{{margin:0;background:#fff}} svg{{display:block}}</style>
{svg}
"""


def main() -> int:
    html = Path(sys.argv[1]).resolve()
    destino = Path(sys.argv[2]).resolve()
    destino.mkdir(parents=True, exist_ok=True)

    if not CHROME.exists():
        print(f"ERRO: {CHROME} nao existe (quarto install chrome-headless-shell)")
        return 1

    texto = html.read_text(encoding="utf-8", errors="replace")
    svgs = re.findall(r"<svg\b.*?</svg>", texto, re.DOTALL)
    if not svgs:
        print(f"nenhum <svg> em {html.name}")
        return 0

    for i, svg in enumerate(svgs, 1):
        base = destino / f"{html.stem}-fig{i}"
        pagina = base.with_suffix(".html")
        # forcar largura util: o svg vem com width em pt
        svg = re.sub(r"(<svg\b[^>]*?)\swidth='[^']*'", r"\1 width='1400'", svg, count=1)
        svg = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"', r'\1 width="1400"', svg, count=1)
        svg = re.sub(r"(<svg\b[^>]*?)\sheight='[^']*'", r"\1", svg, count=1)
        svg = re.sub(r'(<svg\b[^>]*?)\sheight="[^"]*"', r"\1", svg, count=1)
        pagina.write_text(MOLDE.format(svg=svg), encoding="utf-8")

        png = base.with_suffix(".png")
        subprocess.run(
            [
                str(CHROME),
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=1400,1400",
                "--screenshot=" + str(png),
                pagina.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        pagina.unlink()
        print(f"{png}  ({png.stat().st_size // 1024} KB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
