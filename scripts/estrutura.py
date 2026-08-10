"""
Fonte unica de verdade da estrutura do Manual de Python.

Gera:
  - o bloco `chapters:` do _quarto.yml
  - todos os stubs .qmd (regra stub-first)
  - o ROADMAP.md

Uso:
    python scripts/estrutura.py --stubs      # cria stubs faltantes
    python scripts/estrutura.py --quarto     # imprime o bloco chapters:
    python scripts/estrutura.py --roadmap    # regrava ROADMAP.md
    python scripts/estrutura.py --tudo
"""

import argparse
import os
import re
import unicodedata

# (fase, [(volume, titulo_volume, [titulos_capitulos])])
ESTRUTURA = [
    ("Fase 1 — Fundamentos da Linguagem", [
        ("Primeiros Passos com Python", [
            "O que é Python: história, filosofia e o Zen da linguagem",
            "Como o Python executa código: interpretador, bytecode e CPython",
            "Instalando o Python: versões, gerenciadores e o Python do sistema",
            "O REPL, os scripts e o primeiro programa",
            "Ambiente de trabalho: editor, VS Code, Jupyter e o terminal",
            "Sintaxe essencial: indentação, linhas lógicas e comentários",
            "Erros e tracebacks: como ler o que o Python está dizendo",
        ]),
        ("Tipos, Operadores e Expressões", [
            "Objetos, variáveis e o modelo de referências",
            "Números inteiros, de ponto flutuante e complexos",
            "Precisão numérica: decimal, fractions e as armadilhas do float",
            "Booleanos, valor-verdade e os operadores lógicos",
            "Strings: criação, indexação e fatiamento",
            "Métodos de string, formatação e f-strings",
            "Unicode, bytes e codificação de caracteres",
        ]),
        ("Controle de Fluxo e Funções", [
            "Condicionais: if, elif, else e a expressão condicional",
            "Laços: while, for e o protocolo de iteração",
            "break, continue, else em laços e o casamento de padrões",
            "Definindo funções: parâmetros, argumentos e retorno",
            "Argumentos nomeados, valores padrão, `*args` e `**kwargs`",
            "Escopo, closures e a regra LEGB",
            "Funções como objetos: lambda, map, filter e ordem superior",
        ]),
        ("Estruturas de Dados Nativas", [
            "Listas: operações, mutabilidade e cópia",
            "Tuplas, empacotamento e desempacotamento",
            "Dicionários: chaves, ordem e os métodos essenciais",
            "Conjuntos e operações de conjunto",
            "Compreensões de lista, dicionário e conjunto",
            "Ordenação, chaves de ordenação e comparação de objetos",
            "Escolhendo a estrutura certa: custo das operações",
        ]),
    ]),
    ("Fase 2 — Python Estruturado", [
        ("Módulos, Pacotes e o Ambiente", [
            "Módulos, import e o caminho de busca",
            "Pacotes, `__init__.py` e a organização de um projeto",
            "Ambientes virtuais: venv, pip e o isolamento de dependências",
            "Empacotamento moderno: pyproject.toml, build e publicação",
            "uv, pipx e Poetry: o ecossistema de gerenciamento",
            "Ponto de entrada: `__main__`, scripts de console e a linha de comando",
        ]),
        ("Arquivos, Erros e Contextos", [
            "Leitura e escrita de arquivos de texto",
            "Arquivos binários, buffers e o módulo io",
            "Caminhos e o sistema de arquivos com pathlib",
            "Exceções: hierarquia e o bloco try, except, else e finally",
            "Levantando exceções e criando exceções próprias",
            "Gerenciadores de contexto e a instrução with",
        ]),
        ("Programação Orientada a Objetos", [
            "Classes, instâncias e o self",
            "Atributos, propriedades e encapsulamento",
            "Herança, MRO e a função super",
            "Composição, delegação e quando não herdar",
            "Métodos estáticos, métodos de classe e o desenho da API",
            "Dataclasses, NamedTuple e enumerações",
            "Classes abstratas, protocolos e duck typing",
        ]),
        ("O Modelo de Dados de Python", [
            "Métodos especiais: o protocolo por trás da sintaxe",
            "Iteradores e o protocolo de iteração",
            "Geradores, yield e a avaliação preguiçosa",
            "Decoradores de função",
            "Decoradores de classe, functools e metadados preservados",
            "Descritores, `__slots__` e o acesso a atributos",
            "Metaclasses e `__init_subclass__`: quando (não) usar",
        ]),
    ]),
    ("Fase 3 — Biblioteca Padrão e Qualidade", [
        ("A Biblioteca Padrão Essencial", [
            "os, sys e a interação com o sistema",
            "datetime, zoneinfo e o tratamento de tempo",
            "collections: deque, Counter, defaultdict e namedtuple",
            "itertools e functools: a caixa de ferramentas funcional",
            "math, statistics e random",
            "logging: registrando o que o programa faz",
        ]),
        ("Texto, Dados e Serialização", [
            "Expressões regulares com o módulo re",
            "JSON, CSV e formatos tabulares",
            "YAML, TOML e arquivos de configuração",
            "Serialização binária: pickle, struct e os riscos envolvidos",
            "SQLite e a DB-API: banco de dados sem servidor",
            "hashlib, secrets e o tratamento de dados sensíveis",
        ]),
        ("Qualidade: Testes, Tipagem e Ferramentas", [
            "Estilo, PEP 8 e formatação automática com Ruff e Black",
            "Anotações de tipo: fundamentos e o módulo typing",
            "Tipagem avançada: genéricos, protocolos e mypy",
            "Testes com pytest: fundamentos, asserções e fixtures",
            "Parametrização, dublês de teste e cobertura",
            "Depuração: pdb, breakpoint e o traceback difícil",
            "Documentação: docstrings, doctest e Sphinx",
        ]),
    ]),
    ("Fase 4 — Python Aplicado", [
        ("Automação, Sistema e Redes", [
            "Scripts de automação: arquivos, planilhas e tarefas repetitivas",
            "subprocess: chamando programas externos com segurança",
            "Interfaces de linha de comando com argparse, Click e Typer",
            "Redes com sockets: TCP, UDP e o modelo cliente-servidor",
            "Requisições HTTP com requests e httpx",
            "Raspagem de dados responsável: HTML, seletores e limites éticos",
        ]),
        ("Dados, Análise e Visualização", [
            "NumPy: arrays, vetorização e broadcasting",
            "pandas: Series, DataFrame e a carga de dados",
            "Limpeza, transformação e agregação com pandas",
            "Visualização de dados com Matplotlib",
            "SciPy e a computação científica aplicada",
            "Introdução ao aprendizado de máquina com scikit-learn",
        ]),
        ("Web, APIs e Bancos de Dados", [
            "Como funciona uma aplicação web: HTTP, WSGI e ASGI",
            "Validação de dados com Pydantic",
            "APIs REST com FastAPI",
            "Flask e Django: quando usar cada um",
            "Bancos de dados relacionais com SQLAlchemy",
            "Autenticação, autorização e segurança em aplicações Python",
            "Implantação: contêineres, servidores de aplicação e produção",
        ]),
    ]),
    ("Fase 5 — Avançado e Fronteira", [
        ("Concorrência, Desempenho e Internos", [
            "Concorrência, paralelismo e o GIL",
            "Threads e o módulo threading",
            "Multiprocessing e o paralelismo real",
            "Programação assíncrona: async, await e asyncio",
            "Medindo desempenho: timeit, profiling e otimização",
            "Memória, contagem de referências e o coletor de lixo",
        ]),
        ("Fronteira e Prática Contínua", [
            "Estendendo Python: C, Cython e ligações nativas",
            "Python acelerado: PyPy, Numba e o interpretador sem GIL",
            "Arquitetura de projetos e código sustentável",
            "Git, pre-commit e integração contínua para projetos Python",
            "Python e inteligência artificial: LLMs, APIs e agentes",
            "Para onde ir depois: PEPs, comunidade e prática contínua",
        ]),
    ]),
]


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    t = re.sub(r"-+", "-", t).strip("-")
    if len(t) > 46:
        t = t[:46].rsplit("-", 1)[0]
    return t


def caminhos():
    """Retorna lista de (fase, num_vol, titulo_vol, num_cap, titulo_cap, path)."""
    out = []
    nvol = 0
    ncap = 0
    for fase, volumes in ESTRUTURA:
        for titulo_vol, capitulos in volumes:
            nvol += 1
            for titulo_cap in capitulos:
                ncap += 1
                path = f"vol{nvol:02d}/cap{ncap:03d}-{slug(titulo_cap)}.qmd"
                out.append((fase, nvol, titulo_vol, ncap, titulo_cap, path))
    return out


def gerar_stubs(raiz="."):
    criados = 0
    for _, _, _, ncap, titulo, path in caminhos():
        destino = os.path.join(raiz, path)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        if os.path.exists(destino):
            continue
        with open(destino, "w", encoding="utf-8") as f:
            f.write(f"# {titulo} {{#sec-cap{ncap:03d}}}\n\n*(em elaboracao)*\n")
        criados += 1
    print(f"stubs criados: {criados}")


def bloco_quarto():
    linhas = ["  chapters:", "    - index.qmd"]
    fase_atual = None
    nvol = 0
    for fase, vol, titulo_vol, _, _, path in caminhos():
        if fase != fase_atual:
            fase_atual = fase
            linhas.append(f"    # ===== {fase} =====")
        if vol != nvol:
            nvol = vol
            linhas.append("    - part: |")
            linhas.append(f"        Volume {vol} — {titulo_vol}")
            linhas.append("      chapters:")
        linhas.append(f"        - {path}")
    linhas.append("    - referencias.qmd")
    return "\n".join(linhas)


def status_atuais(raiz="."):
    """Le o ROADMAP.md existente e devolve {num_cap: marcador}.

    Sem isso, regravar o ROADMAP zeraria todo capitulo ja concluido -- o
    arquivo e a fila autoritativa de producao, nao um artefato descartavel.
    """
    destino = os.path.join(raiz, "ROADMAP.md")
    if not os.path.exists(destino):
        return {}
    with open(destino, encoding="utf-8") as f:
        conteudo = f.read()
    achados = re.findall(r"^- \[([ x~])\] \*\*cap (\d{3})\*\*", conteudo, re.M)
    return {int(num): marca for marca, num in achados}


def gerar_roadmap(raiz="."):
    status = status_atuais(raiz)
    L = ["# ROADMAP — Manual de Python", "",
         "Fila autoritativa de producao. Status: `[ ]` pendente | `[~]` em andamento | `[x]` concluido.",
         "", "Commit por capitulo: `cap NNN: <titulo>` com o status atualizado no mesmo commit.", ""]
    fase_atual = None
    nvol = 0
    for fase, vol, titulo_vol, ncap, titulo, path in caminhos():
        if fase != fase_atual:
            fase_atual = fase
            L += ["", f"## {fase}", ""]
        if vol != nvol:
            nvol = vol
            L += ["", f"### Volume {vol} — {titulo_vol}", ""]
        marca = status.get(ncap, " ")
        L.append(f"- [{marca}] **cap {ncap:03d}** - {titulo} - `{path}`")
    total = len(caminhos())
    concluidos = sum(1 for m in status.values() if m == "x")
    L += ["", "---", "",
          f"**Total:** {total} capitulos em {nvol} volumes "
          f"({concluidos} concluidos).", ""]
    with open(os.path.join(raiz, "ROADMAP.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"ROADMAP.md gravado ({total} capitulos, "
          f"{concluidos} concluidos preservados)")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--stubs", action="store_true")
    p.add_argument("--quarto", action="store_true")
    p.add_argument("--roadmap", action="store_true")
    p.add_argument("--tudo", action="store_true")
    a = p.parse_args()
    if a.tudo or a.stubs:
        gerar_stubs()
    if a.tudo or a.roadmap:
        gerar_roadmap()
    if a.quarto:
        print(bloco_quarto())
    if not any([a.stubs, a.quarto, a.roadmap, a.tudo]):
        c = caminhos()
        print(f"{len(c)} capitulos, {c[-1][1]} volumes")
