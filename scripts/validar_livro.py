"""Validacao global do livro renderizado em HTML.

Uso: python scripts/validar_livro.py
"""

import re
from pathlib import Path

livro = Path("_book")
htmls = sorted(livro.rglob("*.html"))

quebrados, orfas, vazados, svg_vazios = [], [], [], []
total_svg = 0

for h in htmls:
    txt = h.read_text(encoding="utf-8", errors="replace")
    for m in set(re.findall(r"\?@[a-z-]+", txt)):
        quebrados.append(f"{h.name}: {m}")
    if "[?]" in txt:
        orfas.append(h.name)
    if re.search(r'<pre class="sourceCode mermaid"', txt):
        vazados.append(h.name)
    for s in re.findall(r"<svg.*?</svg>", txt, re.S):
        total_svg += 1
        if len(s) < 1000:
            svg_vazios.append(f"{h.name}: {len(s)} bytes")

# figuras esperadas: contar blocos {.tikz} em todos os .qmd
esperadas = 0
for q in sorted(Path(".").glob("vol*/*.qmd")):
    esperadas += len(re.findall(r"```\{\.tikz\}", q.read_text(encoding="utf-8")))

print(f"paginas HTML          : {len(htmls)}")
print(f"blocos {{.tikz}} nos .qmd: {esperadas}")
print(f"<svg> no HTML         : {total_svg}")
print(f"svg suspeitos (<1 KB) : {len(svg_vazios)} {svg_vazios}")
print(f"crossrefs quebrados   : {len(quebrados)} {quebrados}")
print(f"citacoes orfas [?]    : {len(orfas)} {orfas}")
print(f"fonte mermaid vazada  : {len(vazados)} {vazados}")

ok = not (quebrados or orfas or vazados or svg_vazios) and total_svg >= esperadas
print("RESULTADO:", "ok" if ok else "PROBLEMA")
