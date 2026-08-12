"""Checagens pos-render de um capitulo (HTML).

Uso: python scripts/checar_capitulo.py vol09/cap055-....qmd
"""

import re
import sys
from pathlib import Path

qmd = Path(sys.argv[1])
html = Path("_book") / qmd.with_suffix(".html")

fonte = qmd.read_text(encoding="utf-8")
blocos = re.findall(r"```\{\.tikz\}(.*?)```", fonte, re.S)
print(f"blocos {{.tikz}} no .qmd : {len(blocos)}")

# crossref dentro de bloco tikz sai literal
for i, b in enumerate(blocos, 1):
    achados = re.findall(r"@(?:sec|fig|tbl)-[a-z0-9-]+", b)
    if achados:
        print(f"  !! bloco {i}: crossref dentro do tikz -> {achados}")

if not html.exists():
    print(f"!! HTML nao encontrado: {html}")
    raise SystemExit(1)

h = html.read_text(encoding="utf-8")
svgs = re.findall(r"<svg.*?</svg>", h, re.S)
print(f"<svg> no HTML          : {len(svgs)}")
for i, s in enumerate(svgs, 1):
    marca = "  !! VAZIO" if len(s) < 1000 else ""
    print(f"  svg {i}: {len(s):>7} bytes{marca}")

quebrados = re.findall(r"\?@[a-z-]+", h)
print(f"crossrefs quebrados    : {len(quebrados)} {sorted(set(quebrados))}")

orfas = re.findall(r"\[\?\]", h)
print(f"citacoes orfas [?]     : {len(orfas)}")

# fonte de diagrama vazado (celula mermaid sem echo:false)
vazou = re.findall(r'<pre class="sourceCode mermaid"', h)
print(f"fonte mermaid vazada   : {len(vazou)}")

palavras = len(re.sub(r"```.*?```", "", fonte, flags=re.S).split())
print(f"palavras (fora do codigo): {palavras}")

ok = (len(blocos) == len(svgs) and not quebrados and not orfas
      and not vazou and all(len(s) >= 1000 for s in svgs))
print("RESULTADO:", "ok" if ok else "PROBLEMA")
