"""Checagens das licoes acumuladas, aplicaveis a qualquer volume.

Generaliza o `checar_vol13.py`: recebe o diretorio do volume como argumento
e traz um auto-teste com os defeitos plantados de proposito -- sem ele nao
se distingue "esta limpo" de "o checador esta cego" (LICOES-MANUAIS.md).

Uso:
    python scripts/checar_volume.py vol14
    python scripts/checar_volume.py --autoteste
"""

import re
import sys
import tempfile
from pathlib import Path

MEDIDA = re.compile(r"^-?[\d.]+(pt|mm|cm|em|ex|in|bp|sp)$")
# chaves do pgf/TikZ que nao podem ser reusadas como nome de estilo proprio
PERIGOSAS = {"cap", "id", "pos", "at", "to", "mark", "name", "label", "text",
             "shape", "tip", "cm", "rotate", "scale", "fill", "draw", "anchor"}
# chaves legitimas do TikZ que podem abrir a lista de opcoes de um \node
TIKZ_KEYS = {"draw", "fill", "font", "text", "left", "right", "above", "below",
             "thick", "thin", "red", "blue", "gray", "node", "line", "align",
             "rot", "at", "xs", "ys", "dash", "help", "cyan", "lime", "pink"}


def nos_do_tikz(bloco: str):
    """Devolve (opcoes, texto) de cada \\node, com chaves balanceadas.

    Regex nao serve para o texto do no: ele contem grupos aninhados, e e
    justamente dentro deles que mora o defeito procurado.
    """
    for m in re.finditer(r"\\node\[([^\]]*)\]", bloco):
        i = bloco.find("{", m.end())
        if i < 0:
            continue
        nivel, j = 0, i
        while j < len(bloco):
            if bloco[j] == "{":
                nivel += 1
            elif bloco[j] == "}":
                nivel -= 1
                if nivel == 0:
                    break
            j += 1
        yield m.group(1), bloco[i + 1:j]


def alinhamento(opcoes: str, bloco: str) -> str | None:
    """Alinhamento efetivo de um no: das opcoes locais ou do estilo usado."""
    achado = re.search(r"align\s*=\s*(\w+)", opcoes)
    if achado:
        return achado.group(1)
    for nome in (p.strip() for p in opcoes.split(",")):
        if not re.fullmatch(r"[a-zA-Z]{2,6}", nome):
            continue
        est = re.search(re.escape(nome) + r"/\.style\s*=\s*\{([^{}]*)\}", bloco)
        if est:
            a = re.search(r"align\s*=\s*(\w+)", est.group(1))
            if a:
                return a.group(1)
    return None


def checar_texto(nome: str, txt: str, raiz: Path) -> list[str]:
    problemas = []
    blocos = re.findall(r"```\{\.tikz\}(.*?)```", txt, re.S)

    for i, b in enumerate(blocos, 1):
        onde = f"{nome} fig{i}"

        # 1. crossref dentro de figura sai literal, sem erro
        for m in sorted(set(re.findall(r"@(?:sec|fig|tbl)-[a-z0-9-]+", b))):
            problemas.append(f"{onde}: crossref literal dentro do .tikz -> {m}")

        # 2. \\[algo] lido como medida opcional da quebra de linha
        for arg in re.findall(r"\\\\\[([^\]]*)\]", b):
            if not MEDIDA.match(arg.strip()):
                problemas.append(f"{onde}: \\\\[{arg}] nao e medida -> usar \\\\{{}}[")

        # 3. estilo proprio colidindo com chave do pgf.
        #    Sem ancora de inicio de linha: o estilo declarado logo apos
        #    `\begin{tikzpicture}[` escapava da versao anterior da regra.
        for nm in re.findall(r"(?<![\w/.])([a-zA-Z]+)/\.style", b):
            if nm in PERIGOSAS:
                problemas.append(f"{onde}: estilo '{nm}' colide com chave do pgf")

        # 4. estilo usado mas nunca definido (figura sai sem estilo, sem erro)
        definidos = set(re.findall(r"([a-zA-Z]+)/\.style", b))
        for usados in re.findall(r"\\node\[([^\]]*)\]", b):
            primeiro = usados.split(",")[0].strip()
            if (primeiro and re.fullmatch(r"[a-z]{2,4}", primeiro)
                    and primeiro not in definidos
                    and primeiro not in TIKZ_KEYS):
                problemas.append(f"{onde}: \\node[{primeiro}] usa estilo nao definido")

        # 5. barra dentro de lista de \foreach corrompe a figura
        for lista in re.findall(r"\\foreach[^{]*\{([^}]*)\}", b):
            if "/" in lista and "{/}" not in lista:
                problemas.append(f"{onde}: '/' solto em lista de \\foreach")

        # 6. caractere fora do latin-1 dentro do .tikz
        for ch in sorted(set(b)):
            if ord(ch) > 0x2500 or ch in "\u20ac\U0001f40d":
                # so o ponto de codigo: imprimir o caractere quebra o
                # console do Windows (cp1252)
                problemas.append(f"{onde}: caractere U+{ord(ch):04X} no .tikz")

        # 7. \; e amigos fora de modo matematico
        for esp in ("\\;", "\\!", "\\:"):
            if esp in b:
                problemas.append(f"{onde}: '{esp}' e espacamento matematico")

        # 8. \\ dentro de grupo aninhado quebra o no -- mas SO quando o no
        #    alinha ao centro. Com align=left o mesmo texto compila; checar
        #    a figura inteira daria falso positivo nos capitulos publicados.
        for opts, texto in nos_do_tikz(b):
            if alinhamento(opts, b) != "center":
                continue
            for cmd, arg in re.findall(r"\\(textbf|texttt|textit|emph)"
                                       r"\{([^{}]*)\}", texto):
                if "\\\\" in arg:
                    problemas.append(
                        f"{onde}: \\\\ dentro de \\{cmd}{{}} num no "
                        f"align=center quebra a figura")

    # 9. celula executavel em vez de cerca estatica
    if re.search(r"```\{python\}", txt):
        problemas.append(f"{nome}: celula {{python}} executavel")

    # 10. dunder / asterisco fora de crase na prosa
    fora = re.sub(r"```.*?```", "", txt, flags=re.S)      # tira blocos
    fora = re.sub(r"`[^`\n]*`", "", fora)                 # tira code inline
    for m in sorted(set(re.findall(r"__\w+__", fora))):
        problemas.append(f"{nome}: dunder fora de crase -> {m}")
    for m in sorted(set(re.findall(r"(?<![\w*])\*\*?(?:args|kwargs)\b", fora))):
        problemas.append(f"{nome}: {m} fora de crase")

    # 11. ** desbalanceado na linha: negrito aninhado ou nao fechado.
    #     Contar e mais confiavel que casar padrao: varios negritos separados
    #     na mesma linha sao legitimos e davam falso positivo.
    for n, linha in enumerate(fora.splitlines(), 1):
        if linha.count("**") % 2:
            problemas.append(f"{nome}:{n}: ** desbalanceado -> {linha[:56]}")

    # 12. imagem referenciada que nao existe em disco
    for src in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", txt):
        if not (raiz / src).resolve().exists():
            problemas.append(f"{nome}: imagem ausente -> {src}")

    return problemas


DEFEITUOSO = r"""# Teste negativo {#sec-teste}

Prosa com __init__ solto e com *args solto, mais um **negrito nao fechado.

::: {#fig-x}
```{.tikz}
\begin{tikzpicture}[cap/.style={draw}, bx/.style={draw,align=center},
                    ok/.style={draw,align=left}]
  \node[cap] at (0,0) {ver @sec-cap001};
  \node[zz] at (1,0) {a\\[tool.ruff]};
  \node[bx] at (2,0) {\textbf{duas\\linhas} \; fim};
  \node[ok] at (3,0) {\textit{isto\\compila} e nao deve ser acusado};
  \foreach \a/\b in {a/1,//6} { \node at (\a,0) {\b}; }
\end{tikzpicture}
```
Legenda.
:::

```{python}
print("celula executavel")
```

![ausente](../figuras/nao-existe-mesmo.png)
"""

ESPERADOS = [
    "crossref literal", "nao e medida", "colide com chave do pgf",
    "usa estilo nao definido", "solto em lista de \\foreach",
    "espacamento matematico", "align=center quebra a figura", "celula {python}",
    "dunder fora de crase", "fora de crase", "** desbalanceado",
    "imagem ausente",
]


def autoteste() -> int:
    with tempfile.TemporaryDirectory() as d:
        achados = checar_texto("negativo.qmd", DEFEITUOSO, Path(d))
    juntos = "\n".join(achados)
    faltando = [e for e in ESPERADOS if e not in juntos]
    print(f"regras exercitadas : {len(ESPERADOS)}")
    print(f"achados no arquivo : {len(achados)}")
    for a in achados:
        print("  -", a)
    if faltando:
        print("REGRAS CEGAS:", faltando)
        return 1
    print("RESULTADO: ok (toda regra pegou o seu defeito plantado)")
    return 0


def main() -> int:
    if "--autoteste" in sys.argv:
        return autoteste()
    alvo = Path(sys.argv[1] if len(sys.argv) > 1 else "vol14")
    qmds = sorted(alvo.glob("*.qmd"))
    problemas = []
    tikz = 0
    for q in qmds:
        txt = q.read_text(encoding="utf-8")
        tikz += len(re.findall(r"```\{\.tikz\}", txt))
        problemas += checar_texto(q.name, txt, q.parent)
    print(f"capitulos checados : {len(qmds)} em {alvo}")
    print(f"blocos {{.tikz}}     : {tikz}")
    print(f"problemas          : {len(problemas)}")
    for p in problemas:
        print("  -", p)
    print("RESULTADO:", "ok" if not problemas else "REVISAR")
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
