# Manual de Python

Livro técnico em português do Brasil sobre a linguagem **Python**, do primeiro script ao código de produção. Cobre a linguagem a fundo, a biblioteca padrão, as ferramentas de qualidade (testes, tipagem, empacotamento) e o ecossistema aplicado — automação, dados, web e concorrência. Versão de referência: **Python 3.13**.

Construído com [Quarto](https://quarto.org) (HTML + PDF), publicado no GitHub Pages via GitHub Actions.

## Estrutura

**104 capítulos, 16 volumes, 5 fases:**

1. **Fundamentos da Linguagem** — sintaxe, tipos, controle de fluxo, funções e estruturas de dados
2. **Python Estruturado** — módulos e ambientes, arquivos e exceções, orientação a objetos e o modelo de dados
3. **Biblioteca Padrão e Qualidade** — stdlib essencial, serialização, testes, tipagem e ferramentas
4. **Python Aplicado** — automação e redes, dados e visualização, web, APIs e bancos de dados
5. **Avançado e Fronteira** — concorrência, desempenho, internos, extensão em C e prática contínua

A fila de produção está no [`ROADMAP.md`](ROADMAP.md). A estrutura canônica (fonte única de verdade) vive em [`scripts/estrutura.py`](scripts/estrutura.py).

## Seções fixas de cada capítulo

- **🐍 Jeito Pythônico** — a forma idiomática, a PEP que a fundamenta e o antipadrão correspondente
- **🧪 Laboratório** — roteiro prático reproduzível, passo a passo, com o resultado esperado

## Como produzir

Este repositório é escrito capítulo a capítulo com o Claude Code em modo autônomo. Para começar, abra o repositório no Claude Code e cole o conteúdo de [`PROMPT-INICIAL.md`](PROMPT-INICIAL.md). As convenções e os erros já conhecidos estão em [`CLAUDE.md`](CLAUDE.md) e [`LICOES-MANUAIS.md`](LICOES-MANUAIS.md).

## Build local

```bash
# gerar/atualizar stubs e ROADMAP a partir da estrutura canônica
python scripts/estrutura.py --tudo

# renderizar (HTML primeiro; --to pdf apaga o HTML do _book/)
quarto render --to html
quarto render --to pdf
```

Requer Quarto, TinyTeX (para o PDF e as figuras TikZ) e a extensão TikZ local em `_extensions/`. Ver [`FIGURAS.md`](FIGURAS.md).

Os exemplos de código são executados num ambiente virtual separado antes de entrar no texto:

```bash
python -m venv .venv-exemplos
. .venv-exemplos/bin/activate
python --version
```

## Licença

Conteúdo sob CC BY-SA 4.0. Código e exemplos sob licença MIT.
