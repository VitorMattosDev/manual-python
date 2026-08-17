"""Checagens especificas das licoes acumuladas, aplicadas ao Volume 13.

Uso: python scripts/checar_vol13.py
"""

import re
from pathlib import Path

MEDIDA = re.compile(r"^-?[\d.]+(pt|mm|cm|em|ex|in|bp|sp)$")
# chaves do pgf/TikZ que nao podem ser reusadas como nome de estilo proprio
PERIGOSAS = {"cap", "id", "pos", "at", "to", "mark", "name", "label", "text",
             "shape", "tip", "cm", "rotate", "scale", "fill", "draw", "anchor"}
# chaves legitimas do TikZ que podem abrir a lista de opcoes de um \node
TIKZ_KEYS = {"draw", "fill", "font", "text", "left", "right", "above", "below",
             "thick", "thin", "red", "blue", "gray", "node", "line", "align",
             "rot", "at", "xs", "ys", "dash", "help", "cyan", "lime", "pink"}

problemas = []
qmds = sorted(Path("vol13").glob("*.qmd"))

for q in qmds:
    txt = q.read_text(encoding="utf-8")
    blocos = re.findall(r"```\{\.tikz\}(.*?)```", txt, re.S)

    for i, b in enumerate(blocos, 1):
        onde = f"{q.name} fig{i}"

        # 1. crossref dentro de figura sai literal, sem erro
        for m in set(re.findall(r"@(?:sec|fig|tbl)-[a-z0-9-]+", b)):
            problemas.append(f"{onde}: crossref literal dentro do .tikz -> {m}")

        # 2. \\[algo] lido como medida opcional da quebra de linha
        for arg in re.findall(r"\\\\\[([^\]]*)\]", b):
            if not MEDIDA.match(arg.strip()):
                problemas.append(f"{onde}: \\\\[{arg}] nao e medida -> usar \\\\{{}}[")

        # 3. estilo proprio colidindo com chave do pgf
        for nome in re.findall(r"^\s*([a-zA-Z]+)/\.style", b, re.M):
            if nome in PERIGOSAS:
                problemas.append(f"{onde}: estilo '{nome}' colide com chave do pgf")

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
        for ch in set(b):
            if ord(ch) > 0x2500 or ch in "€🐍":
                # so o ponto de codigo: imprimir o caractere quebra o
                # console do Windows (cp1252)
                problemas.append(f"{onde}: caractere U+{ord(ch):04X} no .tikz")

        # 7. \; e amigos fora de modo matematico
        for esp in ("\\;", "\\!", "\\:"):
            if esp in b:
                problemas.append(f"{onde}: '{esp}' e espacamento matematico")

    # 8. celula executavel em vez de cerca estatica
    if re.search(r"```\{python\}", txt):
        problemas.append(f"{q.name}: celula {{python}} executavel")

    # 9. dunder / asterisco fora de crase na prosa
    fora = re.sub(r"```.*?```", "", txt, flags=re.S)      # tira blocos
    fora = re.sub(r"`[^`\n]*`", "", fora)                 # tira code inline
    for m in set(re.findall(r"__\w+__", fora)):
        problemas.append(f"{q.name}: dunder fora de crase -> {m}")
    for m in set(re.findall(r"(?<![\w*])\*\*?(?:args|kwargs)\b", fora)):
        problemas.append(f"{q.name}: {m} fora de crase")

    # 10. ** desbalanceado na linha: negrito aninhado ou nao fechado.
    #     Contar e mais confiavel que casar padrao: varios negritos separados
    #     na mesma linha sao legitimos e davam falso positivo.
    for n, linha in enumerate(fora.splitlines(), 1):
        if linha.count("**") % 2:
            problemas.append(f"{q.name}:{n}: ** desbalanceado -> {linha[:56]}")

    # 11. imagem referenciada que nao existe em disco
    for src in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", txt):
        alvo = (q.parent / src).resolve()
        if not alvo.exists():
            problemas.append(f"{q.name}: imagem ausente -> {src}")

print(f"capitulos checados : {len(qmds)}")
print(f"blocos {{.tikz}}     : "
      f"{sum(len(re.findall(r'```\{\.tikz\}', p.read_text(encoding='utf-8'))) for p in qmds)}")
print(f"problemas          : {len(problemas)}")
for p in problemas:
    print("  -", p)
print("RESULTADO:", "ok" if not problemas else "REVISAR")
