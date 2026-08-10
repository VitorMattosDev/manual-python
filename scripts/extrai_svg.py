"""Extrai os <svg> inline de um HTML do _book para arquivos soltos, para inspecao visual.

Uso: py -3 scripts/extrai_svg.py _book/vol02/capNNN-....html <destino>
"""

import re
import sys
from pathlib import Path

html = Path(sys.argv[1])
destino = Path(sys.argv[2])
destino.mkdir(parents=True, exist_ok=True)

texto = html.read_text(encoding="utf-8", errors="replace")
svgs = re.findall(r"<svg\b.*?</svg>", texto, re.DOTALL)

for i, svg in enumerate(svgs, 1):
    saida = destino / f"{html.stem}-fig{i}.svg"
    saida.write_text(svg, encoding="utf-8")
    print(f"{saida}  ({len(svg) // 1024} KB)")
