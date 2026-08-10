# CLAUDE.md — Manual de Python

Instruções de trabalho para o Claude Code neste repositório.

## O que é este projeto

Livro Quarto (HTML + PDF) em português do Brasil, publicado no GitHub Pages via GitHub Actions. **104 capítulos, 16 volumes, 5 fases.** A versão de referência é o **Python 3.13** em ambiente Linux (Kali/Debian), com notas para Windows e macOS onde importa. A fila autoritativa está no `ROADMAP.md`. A estrutura canônica vive em `scripts/estrutura.py` — qualquer mudança de capítulos começa por lá.

## Modo de execução

Execução autônoma. Você está pré-aprovado para criar e editar arquivos, gerar figuras, rodar comandos de validação e fazer commits sem pedir confirmação a cada passo. **Única condição de parada:** erro real de bloqueio.

Um capítulo por sessão. `/clear` entre capítulos, `/compact` perto de 80% de contexto.

## Bootstrap da toolchain (rodar se ainda não foi rodado)

Faça isso antes do primeiro `quarto preview`, sem esperar ser pedido:

```bash
quarto install tinytex
# tlmgr pode não estar no PATH — localizar sem -type f (são symlinks)
TLMGR="$(command -v tlmgr || find "$HOME" -name tlmgr | head -n1)"
"$TLMGR" update --self
"$TLMGR" install standalone pgf pgfplots dvisvgm xcolor amsmath amsfonts fvextra koma-script
```

E **prepend do bin do TinyTeX no PATH da sessão** — este é o motivo mais comum de figura TikZ não renderizar (falha em `tikz.lua`, `imgdata nil`, ~linha 587). Não é pacote faltando, é PATH:

- Windows: `$HOME/AppData/Roaming/TinyTeX/bin/windows`
- Linux/macOS: `~/.TinyTeX/bin/<plataforma>`

## Anatomia de um capítulo

````markdown
# Título do capítulo {#sec-capNNN}

Parágrafo de abertura situando um problema concreto — nunca começar com definição
de dicionário. De preferência, um cenário real de quem escreve código Python para
resolver um problema de verdade.

## Seções de conteúdo

Texto explicativo, exemplos executáveis, diagramas TikZ, blocos de código
comentados. Todo exemplo é para ser digitado: mostrar o código, a saída esperada
e o que interpretar nela. Exemplo curto e completo vale mais do que fragmento
que não roda.

## 🐍 Jeito Pythônico

A forma idiomática de fazer o que o capítulo ensinou: o que a comunidade escreve
de verdade, qual PEP fundamenta a escolha, qual é o antipadrão equivalente e por
que ele machuca (legibilidade, desempenho, manutenção). Quando houver diferença
entre versões do Python (walrus, match, `|` em tipos, `tomllib`, free-threading),
dizer a partir de qual versão vale. OBRIGATÓRIA em todo capítulo.

## 🧪 Laboratório

Roteiro prático reproduzível: passos numerados que o leitor executa no próprio
ambiente (venv limpo, de preferência), com o resultado esperado de cada passo.
Termina com algo que funciona, não com um trecho solto.
OBRIGATÓRIA em todo capítulo.

## Resumo

3 a 6 bullets com o essencial.
````

Alvo: 2.500–4.000 palavras por capítulo. Densidade acima de volume.

## Política editorial

Manual técnico, prático e correto. Ensinar fazendo: cada conceito vem com o código que o exercita.

**Versão de referência: Python 3.13.** Nada de sintaxe morta (`%` como formatação principal, `os.path` onde `pathlib` resolve, `typing.List` onde `list` basta). Onde um recurso é recente, marcar a versão mínima. Onde ainda se encontra código legado em produção, explicar o que era feito antes e por que mudou — sem transformar o capítulo em arqueologia.

**Todo código mostrado precisa rodar.** Antes de commitar um capítulo, os exemplos não triviais são executados num `venv` de teste e a saída colada é a saída real. Saída inventada é o erro mais caro deste manual, porque não quebra o build — só o leitor.

**Dependências externas** só quando o assunto é a dependência. Fase 1 a 3 usa biblioteca padrão; `pandas`, `FastAPI`, `pytest` e afins entram nos volumes que tratam deles. Quando um pacote for instalado, mostrar o comando (`pip install`, `uv add`) e a versão usada.

**Código destrutivo ou perigoso** (`shutil.rmtree`, `os.remove`, `subprocess` com `shell=True`, `pickle.load` de fonte não confiável, `eval`) sempre com aviso claro na linha anterior e, quando possível, um ensaio seguro (`tmp_path`, diretório descartável, `--dry-run`). `shell=True` e `pickle` de fonte externa aparecem como exemplo do que **não** fazer, com a alternativa segura ao lado.

## Figuras

TikZ para diagramas esquemáticos e didáticos (modelo de referências e objetos, pilha de chamadas, MRO, ciclo de vida de um gerador, fluxo do event loop do asyncio, layout de memória de uma lista, árvore de herança). SVG/PNG embutido para o que depender de captura de tela de editor ou de notebook.

- Extensão: `_extensions/danmackinlay/tikz/` com **patches locais**
- **NUNCA rodar `quarto add` ou `quarto update`** nessa extensão — baixa o upstream sem os patches e quebra tudo
- Filtro `tikz` vem **antes** de `quarto` na lista de filters
- O template sempre chama `\usepackage{pgfplots}` — toda figura precisa dele, mesmo uma seta simples
- Estilos predefinidos (`curva`, `destaque`, `auxiliar`, `eixo`, `ponto`, `vetor`; cores `manualblue`, `manualred`, `manualgreen`, `manualyellow`, `manualgray`) vêm do template: **usar direto, nunca redefinir**

Sintaxe:

````markdown
::: {#fig-modelo-referencias}
```{.tikz}
%%| filename: modelo-referencias
%%| alt: Duas variáveis apontando para o mesmo objeto na memória
\begin{tikzpicture}
  ...
\end{tikzpicture}
```
Duas variáveis referenciando o mesmo objeto.
:::
````

Referência no texto via `@fig-modelo-referencias`.

## Regras que já custaram build vermelho

Ver `LICOES-MANUAIS.md` para o compilado completo. Os pontos que mais mordem:

- **Blocos de código Python são estáticos, não células executáveis.** Usar cerca estática ```` ```python ````, nunca ```` ```{python} ````. Célula executável exige Jupyter no runner, congela em `freeze`, e faz o CI executar código que pode instalar pacote, abrir socket ou apagar arquivo. A saída dos exemplos é **colada** no bloco (ou num bloco `text` logo abaixo) depois de rodada localmente. Célula executável só para algo comprovadamente inócuo, determinístico e com propósito — e, nesse caso, com `#| echo: fenced` consciente.
- **Stub-first**: em projeto `book`, renderizar um `.qmd` isolado falha com "Book chapter not found" se qualquer capítulo listado no `_quarto.yml` não existir em disco. Rodar `python scripts/estrutura.py --stubs` após qualquer mudança de estrutura.
- **`--roadmap` e `--tudo` regravam o `ROADMAP.md` inteiro.** O `scripts/estrutura.py` **preserva** os marcadores `[x]` e `[~]` (função `status_atuais`, que relê o arquivo antes de reescrever) — mas a proteção é frágil: se o formato da linha (`- [x] **cap NNN**`) mudar, o regex para de casar e todo capítulo concluído volta a `[ ]` sem aviso. Não alterar esse formato, e conferir a contagem que o script imprime (`N concluidos preservados`). Na dúvida, usar só `--stubs`.
- **`quarto render --to pdf` limpa o `_book/`** e deixa apenas o PDF. As checagens de `?@`, de `<svg` e de `[?]` são feitas no HTML, então a ordem é sempre: render HTML → validar → render PDF. Invertido, o grep não acha os arquivos e o silêncio parece aprovação.
- **`execute: echo: true` vaza o fonte das células de diagrama.** Toda célula `{mermaid}` precisa de `%%| echo: false`. Blocos cercados estáticos não são células e não sofrem disso — e são o padrão aqui.
- **Dunder em prosa vira negrito.** `__init__`, `__slots__`, `__name__` fora de crase são lidos como ênfase forte pelo Markdown: o texto sai "init" em negrito e os underscores somem. Todo nome com underscore duplo vai entre crases, inclusive em título de capítulo, legenda e item de lista. O mesmo vale para `*args`, `**kwargs` e qualquer `*` colado em palavra.
- **Underscore em texto corrido quebra o PDF.** `snake_case` fora de crase vira subscrito no LaTeX. Nome de função, de variável e de módulo sempre em `code` inline.
- **Nome de estilo TikZ próprio não pode colidir com chave do pgf.** `cap/.style` e `id/.style` derrubam o build com `The key '/tikz/cap' requires a value` — e o erro pode não aparecer no render isolado do capítulo, só no do livro inteiro. Usar `leg`, `ident`, `nd`, `bx`, `lb`, `nt`, `fl`, `seg`, `stg`, `dlm`; evitar `cap`, `id`, `pos`, `at`, `to`, `mark`, `name`, `label`, `text`, `shape`, `cm`.
- **Variável de `\foreach` no TikZ nunca pode ter nome de macro de acento do LaTeX** (`\c`, `\d`, `\t`, `\i`, `\u`, `\v`, `\r`, `\b`, `\k`, `\l`, `\o`, `\a`). Redefini-las num laço com texto acentuado dentro causa `TeX capacity exceeded`. Usar nomes de duas letras ou mais (`\idx`, `\tit`, `\cor`).
- **Crossrefs**: `@sec-`, `@fig-` e `@tbl-` **só** para o que já foi escrito. Referência a capítulo futuro é menção textual ("tema do Volume 12"), nunca link. Label não resolvido vira `?@sec-x` em vermelho.
- **`lang: pt`** fica na raiz do `_quarto.yml`, não sob `book:`.
- **`styles.css`** precisa de `/*-- scss:rules --*/` na primeira linha (está em `theme:`). Evitar `*/` logo após o marcador.
- **Notação LaTeX**: usar `^{*}` e não `^\*` — quebra o PDF.
- **Cuidado com caracteres especiais em prosa e legendas**: `$`, `\`, `{`, `}`, `~`, `^`, `&`, `_`, `#`, `%` são especiais no LaTeX. Em bloco de código não há problema; em texto corrido e legendas de figura, escapar (`\$`, `\&`, `\_`, `\#`, `\%`, `\~{}`, `\^{}`) ou usar `code` inline (crase).
- **Substituição em massa** de notação: usar `str.replace` do Python, em arquivo `.py` — não por heredoc. Nunca `sed` nem `grep -c`.
- **Commits**: apenas `-m "..."` simples. Nada de here-string do PowerShell dentro do Bash.
- **Emoji em `print()`** de script Python quebra no console do Windows. Em conteúdo de arquivo UTF-8 é seguro.
- **Write após heredoc**: se um arquivo foi modificado por bash/heredoc, a ferramenta Write exige um Read antes.
- **Avisos inofensivos**: `LF will be replaced by CRLF` e "Node.js 20 is deprecated" — ignorar.

## Validação antes de cada commit

Ordem obrigatória: **HTML primeiro, validar, PDF por último** — `--to pdf` apaga o HTML do `_book/`.

```bash
quarto render --to html
# 1. figuras: contar <svg no HTML gerado vs {.tikz} no .qmd
# 2. crossrefs quebrados — precisa retornar zero:
grep -rhoE '\?@[a-z-]+' _book/**/*.html
# 3. citações órfãs: procurar [?] no HTML
# 4. fonte de diagrama vazado: nenhum <pre class="sourceCode"> com o corpo
#    de um bloco {mermaid} (sintoma de célula sem `%%| echo: false`)
# 5. código do capítulo executado num venv limpo, saída conferida
# 6. PDF local antes de qualquer push (LaTeX quebra no que o HTML aceita).
#    Este passo destrói o HTML acima, então roda só depois de 1–5:
quarto render --to pdf
```

Para conferir se uma figura TikZ entrou no PDF, contar Form XObjects por página com `pypdf` — `pdftotext` não recupera texto acentuado dos rótulos e dá falso negativo.

Commit no formato `cap NNN: <título>`, com o status do `ROADMAP.md` atualizado no mesmo commit.

## Validação antes do push

1. Render HTML completo do livro
2. Zero `?@` no grep
3. Todas as figuras TikZ produziram SVG
4. Nenhuma citação `@chave` crua sobrando no HTML
5. Exemplos de código do capítulo executados e saída conferida
6. Após o push: `gh run watch <id> --exit-status` e depois `curl -I` na URL do Pages esperando 200

## Estratégia de produção

Fatia vertical: fechar um volume inteiro antes de abrir o próximo; fechar a Fase 1 antes da Fase 2. Em volume novo, o primeiro passo é o smoke test — validar que **uma** figura TikZ renderiza para SVG no HTML antes de escrever capítulo a capítulo.

`/model opus` para escrever capítulo. `/model sonnet` para tarefa mecânica (atualizar `_quarto.yml`, mover arquivo, ajustar ROADMAP).
