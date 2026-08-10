"""Validacao pos-render do HTML: crossrefs, figuras TikZ e citacoes orfas.

Uso:
    py -3 scripts/valida.py            # valida _book inteiro
    py -3 scripts/valida.py vol02      # valida so um volume
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BOOK = RAIZ / "_book"


def main() -> int:
    alvo = sys.argv[1] if len(sys.argv) > 1 else ""
    htmls = sorted((BOOK / alvo).rglob("*.html")) if alvo else sorted(BOOK.rglob("*.html"))
    if not htmls:
        print(f"ERRO: nenhum HTML em {BOOK / alvo}")
        return 1

    problemas = 0

    # 1. crossrefs quebrados
    for h in htmls:
        texto = h.read_text(encoding="utf-8", errors="replace")
        for quebrado in set(re.findall(r"\?@[a-z]+-[a-z0-9-]+", texto)):
            print(f"CROSSREF  {h.relative_to(BOOK)}: {quebrado}")
            problemas += 1

    # 2. citacoes orfas
    for h in htmls:
        texto = h.read_text(encoding="utf-8", errors="replace")
        if re.search(r">\s*\[\?\]\s*<", texto):
            print(f"CITACAO   {h.relative_to(BOOK)}: [?] no texto")
            problemas += 1

    # 3. fonte de diagrama vazado (mermaid sem echo: false)
    for h in htmls:
        texto = h.read_text(encoding="utf-8", errors="replace")
        if 'class="sourceCode mermaid"' in texto:
            print(f"MERMAID   {h.relative_to(BOOK)}: fonte de diagrama vazou")
            problemas += 1

    # 4. figuras: contar {.tikz} no .qmd e <svg no HTML, com tamanho
    for h in htmls:
        rel = h.relative_to(BOOK).with_suffix(".qmd")
        qmd = RAIZ / rel
        if not qmd.exists():
            continue
        fonte = qmd.read_text(encoding="utf-8", errors="replace")
        esperadas = len(re.findall(r"```\{\.tikz\}", fonte))
        if esperadas == 0:
            continue
        texto = h.read_text(encoding="utf-8", errors="replace")
        svgs = re.findall(r"<svg\b.*?</svg>", texto, re.DOTALL)
        marca = "ok"
        if len(svgs) != esperadas:
            marca = f"FALTA ({len(svgs)}/{esperadas})"
            problemas += 1
        vazias = [i for i, s in enumerate(svgs, 1) if len(s) < 1024]
        if vazias:
            marca += f" VAZIA nas posicoes {vazias}"
            problemas += 1
        tamanhos = ", ".join(f"{len(s) // 1024}KB" for s in svgs)
        print(f"FIGURAS   {rel}: {len(svgs)}/{esperadas} [{tamanhos}] {marca}")

    # 5. crossref literal dentro de bloco tikz no fonte
    fontes = sorted((RAIZ / alvo).rglob("*.qmd")) if alvo else sorted(RAIZ.rglob("vol*/*.qmd"))
    for q in fontes:
        fonte = q.read_text(encoding="utf-8", errors="replace")
        for bloco in re.findall(r"```\{\.tikz\}(.*?)```", fonte, re.DOTALL):
            for ref in re.findall(r"@(?:sec|fig|tbl)-[a-z0-9-]+", bloco):
                print(f"TIKZREF   {q.relative_to(RAIZ)}: {ref} dentro de bloco tikz")
                problemas += 1

    print(f"\n{'FALHOU' if problemas else 'OK'}: {problemas} problema(s)")
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
