"""Confere se as figuras TikZ entraram no PDF, contando Form XObjects por pagina.

pdftotext nao recupera texto acentuado dos rotulos e da falso negativo — por isso
a contagem e de objetos de forma, nao de texto.

Uso: py -3 scripts/confere_pdf.py
"""

from pathlib import Path

from pypdf import PdfReader

RAIZ = Path(__file__).resolve().parent.parent
PDF = RAIZ / "_book" / "Manual-de-Python.pdf"


def main() -> int:
    if not PDF.exists():
        print(f"ERRO: {PDF} nao existe")
        return 1

    leitor = PdfReader(str(PDF))
    total_paginas = len(leitor.pages)
    paginas_com_figura = []
    total_formas = 0

    for i, pagina in enumerate(leitor.pages, 1):
        recursos = pagina.get("/Resources")
        if not recursos:
            continue
        xobjs = recursos.get("/XObject")
        if not xobjs:
            continue
        formas = [
            k for k, v in xobjs.items()
            if v.get_object().get("/Subtype") == "/Form"
        ]
        if formas:
            paginas_com_figura.append((i, len(formas)))
            total_formas += len(formas)

    esperadas = sum(
        q.read_text(encoding="utf-8").count("```{.tikz}")
        for q in sorted(RAIZ.rglob("vol*/*.qmd"))
    )

    print(f"paginas no PDF ............ {total_paginas}")
    print(f"blocos {{.tikz}} no fonte ... {esperadas}")
    print(f"Form XObjects no PDF ...... {total_formas}")
    print(f"paginas com figura ........ {len(paginas_com_figura)}")
    print("  " + ", ".join(f"p{p}({n})" for p, n in paginas_com_figura))

    if total_formas < esperadas:
        print(f"\nFALHOU: faltam {esperadas - total_formas} figura(s) no PDF")
        return 1
    print("\nOK: todas as figuras entraram no PDF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
