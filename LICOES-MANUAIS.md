# LIÇÕES — Produção dos Manuais

Compilado de erros que já custaram build vermelho. Todo manual novo nasce com este arquivo.

## CI / GitHub Actions

### Mermaid trava o PDF
O grafo mermaid do `index.qmd` bloqueia o render de PDF no runner Ubuntu (sem Chromium headless). Adicionar **antes** do render/publish:

```yaml
- run: quarto install chrome-headless-shell
```

A ferramenta é `chrome-headless-shell`, não `chromium`.

### Branch gh-pages precisa existir
`quarto-actions/publish@v2` aborta se `gh-pages` não existir no remoto. Uma vez, antes do primeiro push:

```bash
git push origin $(git commit-tree $(git hash-object -t tree /dev/null) -m 'init gh-pages'):refs/heads/gh-pages
```

### Passo "Preparar TeX" — versão definitiva
Quatro builds vermelhos no Manual de Economia identificaram quatro causas distintas:

1. `tlmgr` do TeX Live 2026 **aborta silenciosamente** qualquer `tlmgr install` enquanto `tlmgr update --self` não rodar. Sempre `update --self` primeiro.
2. **Nunca** mascarar o install com `|| true` — esconde a falha e o erro só aparece no render.
3. Binários do TinyTeX são **symlinks**. Detectar com `command -v pdflatex` ou `find` **sem** `-type f`. Com `-type f` o resultado é vazio e `TEXBIN` vira `.`.
4. Exportar o diretório com `echo "$TEXBIN" >> "$GITHUB_PATH"` **e** criar symlinks de fallback em `/usr/local/bin` para `pdflatex`, `latex`, `dvisvgm`, `kpsewhich`.

Fechar com verificações que falham alto: `kpsewhich standalone.cls`, `kpsewhich pgfplots.sty`, `dvisvgm --version`.

YAML de referência: ver `.github/workflows/publish.yml` deste repositório.

## Quarto

- **`styles.css` em `theme:`** → Quarto ≥1.9 trata como camada SCSS e exige `/*-- scss:rules --*/` na primeira linha. Sem isso o render inteiro falha com "doesn't contain at least one layer boundary". Cuidado com `*/` logo após o marcador.
- **Stub-first**: em projeto `book`, `quarto render arquivo.qmd` isolado falha com "Book chapter not found" se qualquer capítulo do `_quarto.yml` não existir em disco. Registrou um `part:`? Cria os stubs na hora.
- **Gerador de ROADMAP tem de preservar status.** Um script que regrava o `ROADMAP.md` a partir da estrutura canônica zera todo `[x]` se não reler os marcadores antes. Não é build vermelho, é pior: apaga silenciosamente a fila de produção e o próximo capítulo é reescrito por cima. Corrigido em `scripts/estrutura.py` (`status_atuais`), que imprime quantos concluídos preservou — conferir esse número.
- **`quarto render --to pdf` limpa o diretório de saída** e deixa só o PDF. Toda validação que faz grep no HTML (`?@`, `<svg`, `[?]`) tem de rodar antes do PDF. Se rodar depois, o grep não acha arquivo e o resultado vazio passa por aprovação.
- **`execute: echo: true` vaza o fonte de células de diagrama.** Um bloco `{mermaid}` é emitido duas vezes: `<pre class="sourceCode">` com botão de copiar (o vazamento visível na página) e `<pre class="mermaid">` (o diagrama). Toda célula `{mermaid}` precisa de `%%| echo: false`. Blocos cercados estáticos não são afetados.
- **Crossrefs**: `@sec-`/`@fig-`/`@tbl-` só para o que já existe. Futuro é menção textual. Label não resolvido vira `?@sec-x` em vermelho.
- **`lang: pt`** na raiz do `_quarto.yml`, nunca sob `book:`.
- **Notação**: `^{*}`, não `^\*` — quebra o PDF.
- **Química**: `\ce{...}` (mhchem) funciona em HTML e PDF. Evitar `siunitx` (só PDF, quebra MathJax) e o pacote `physics`.

## Código nos capítulos (manuais de linguagem e de sistema)

- **Bloco cercado estático, não célula executável.** ```` ```python ```` e ```` ```bash ````, nunca ```` ```{python} ```` nem ```` ```{bash} ````. Célula executável exige kernel no runner, interage mal com `freeze: auto` (o cache fica preso a um estado que ninguém revisou) e faz o CI executar código do livro — inclusive `pip install`, socket e escrita em disco. A saída dos exemplos é colada depois de rodada localmente.
- **Saída colada tem de ser saída real.** É o erro que não quebra o build: o render fica verde, o PDF sai bonito e o exemplo mente. Rodar num `venv` limpo e copiar o que o interpretador imprimiu, inclusive o traceback quando o exemplo é de erro. Endereço de objeto (`<object at 0x7f...>`), ordem de `set`, timestamp e caminho absoluto mudam a cada execução — ou fixar (`sorted`, `seed`) ou avisar no texto que varia.
- **Dunder e asterisco em prosa viram formatação Markdown.** `__init__`, `__name__`, `*args`, `**kwargs` fora de crase são lidos como ênfase: os underscores/asteriscos somem e o miolo sai em negrito. Vale para título, legenda de figura, item de lista e linha de ROADMAP. Sempre em `code` inline.
- **Underscore em texto corrido quebra o PDF.** `snake_case` fora de crase vira subscrito no LaTeX (`Missing $ inserted` ou, pior, sai renderizado errado sem erro). Identificador sempre em crase.
- **Linha de código longa estoura a caixa no PDF.** O `fvextra` com `breaklines` no `include-in-header` resolve a maioria, mas linha sem espaço (URL, string longa, cadeia de métodos) ainda vaza. Quebrar o exemplo à mão em até ~78 colunas.
- **Bloco de código dentro de callout precisa de cerca maior.** Um `:::` com ```` ``` ```` dentro fecha errado; usar ````` ```` ````` de quatro crases na cerca externa quando o conteúdo tiver crases.

## TikZ

- Extensão `danmackinlay/tikz` com **patches locais** (`figuras-tikz-kit.zip` / `FIGURAS.md`). **Nunca** `quarto add` ou `quarto update` — baixa o upstream sem patches.
- Filtro `tikz` **antes** de `quarto` na lista de filters; `tikz: svg-engine: dvisvgm`.
- O template sempre chama `\usepackage{pgfplots}` — toda figura depende dele, mesmo uma seta.
- Estilos e cores predefinidos vêm do template: usar direto, nunca redefinir.
- **`\\` dentro de grupo `{...}` aninhado no texto de um nó quebra a figura inteira.** Com `align=center`, o TikZ implementa `\\` como fim de linha do alinhamento; dentro de um grupo extra isso desbalanceia o grupo e o erro sai como `Undefined control sequence` em `\tikz@finish@orig ...=\tikzscope@linewidth`, seguido de `I do not know the key '/tikz/<estilo>'` nos nós seguintes — sintomas que não apontam para a causa. O SVG sai vazio (~220 bytes no HTML) e o render **não** falha alto. Regra: quebra de linha só no nível superior do texto do nó. Trocar `{\bfseries\color{x}Título}\\...` por `\textbf{\textcolor{x}{Título}}\\...`, e usar `\scriptsize\color{y}` como chave (switch) em vez de `{\scriptsize\color{y}...}` quando houver `\\` depois.
- **Nome de estilo próprio não pode colidir com chave existente do TikZ/pgfplots.** Definir `cap/.style={...}` ou `id/.style={...}` e usá-los como `\node[cap,...]` faz o pdflatex abortar com `Package pgfkeys Error: The key '/tikz/cap' requires a value` — a chave já existe no pgf e é lida antes do estilo local. O erro aparece no render **do livro inteiro** e pode não aparecer no render isolado do capítulo, o que faz o smoke test passar e o build cair depois. Nomes seguros: prefixar (`nd`, `bx`, `lb`, `nt`, `fl`, `leg`, `ident`, `seg`, `stg`, `dlm`) e evitar palavras curtas do vocabulário do TikZ (`cap`, `id`, `pos`, `at`, `to`, `mark`, `name`, `label`, `text`, `shape`, `tip`, `cm`). O `cm` derrubou duas figuras do Volume 11 do Manual de Linux (`cm/.style` para "comando"): é a chave de matriz de transformação do pgf, e o erro sai como `The key '/tikz/cm' requires a value` repetido — desta vez **já no render isolado do capítulo**, ao contrário do `cap`.
- **Estilo TikZ inexistente não gera erro: a figura sai sem estilo.** Renomear `st/.style` para `stg/.style` e esquecer de renomear os `\node[st,...]` correspondentes **não** derruba o build. O pdflatex aceita, o SVG sai no tamanho normal, o `grep -c '<svg'` conta como boa — e a figura vem com os nós na fonte errada, sem `align=center` (então todo `\\` é ignorado e o texto vira uma linha só) e sem `rounded corners`. É o oposto do caso `cap`/`cm`, que falha alto. Só a inspeção visual pega. Reforça a regra: rasterizar e olhar, sempre.
- **`\;` é espaçamento de modo matemático e derruba a figura em texto corrido.** Num rótulo como `\texttt{list} \; = \; \texttt{array}`, o `\;` fora de `$...$` gera `Missing $ inserted`. Em modo texto, usar `\quad`, `\,` ou espaço simples. Vale também para `\!`, `\:` e `\>`.
- **`\\` dentro de `\textbf{}` é o mesmo caso do grupo aninhado, e é fácil de escrever sem perceber.** `{\textbf{contagem\\de referências}\\\tiny ...}` derruba a figura com `Giving up on this path. Did you forget a semicolon?` + `Extra }`. A forma certa é fechar o grupo antes da quebra: `\textbf{contagem}\\\textbf{de referências}\\\tiny ...`. Título de nó em duas linhas é o gatilho mais comum.
- **Underscore em rótulo de nó TikZ é subscrito, não caractere.** `\node{__init__}` sai como um traço com o resto rebaixado. Dentro da figura, usar `\texttt{\_\_init\_\_}` ou trocar por um rótulo sem underscore.
- **Legenda solta ao lado de um bloco pode invadir o bloco seguinte sem erro nenhum.** Um `\node[anchor=west] at (x,y)` cuja largura o TikZ não limita cresce para a direita até por cima do próximo nó. O LaTeX compila, o SVG sai no tamanho normal e só a rasterização mostra a sobreposição. Ou dar `text width=` ao rótulo, ou deixar folga generosa entre ele e o vizinho.
- **Crossref dentro de figura TikZ sai literal, sem erro nenhum.** Escrever `(@sec-cap023)` no texto de um nó ou na nota de rodapé da figura não é processado pelo Quarto — o bloco `{.tikz}` vai inteiro para o LaTeX antes do filtro de crossref. O build fica verde, o `grep` de `?@` não acha nada (não é label quebrado, é texto), e a figura sai com `(@sec-cap023)` impresso. Só a rasterização pega. Regra: dentro de `{.tikz}`, referência a capítulo é sempre menção textual sem `@`. Vale checar com um `re.findall(r'@(?:sec|fig|tbl)-[a-z0-9-]+')` restrito ao conteúdo dos blocos `{.tikz}`.
- **Conferir tamanho do SVG, não só a ausência de erro.** `grep -c '<svg'` conta figura quebrada como figura boa. Medir cada bloco `<svg>...</svg>`: abaixo de ~1 KB é figura vazia.
- **Rótulo de aresta em diagrama de estados: usar `sloped` com `bend`, não `above left`/`below right` com `out`/`in`.** Rótulos posicionados por canto colidem entre si e com as legendas dos nós assim que há três ou mais transições saindo do mesmo nó. `to[bend left=16] node[lb,sloped,above,pos=0.5]{...}` acompanha a curva e não sobrepõe. E, quando o nó precisa de descrição, colocá-la **dentro** do nó (`\textbf{R}\\executando`) em vez de num `\node` solto ao lado — elimina a classe inteira de colisão.
- **Bloqueio mais comum é PATH, não pacote faltando.** `quarto install tinytex` não adiciona o bin ao PATH da sessão. Sintoma: figura não renderiza e `tikz.lua` falha com `imgdata nil` (~linha 587). Prepend do bin do TinyTeX antes de qualquer render.
- Pacotes: `tlmgr install standalone pgf pgfplots dvisvgm xcolor amsmath amsfonts`

## Windows / Claude Code

- **`tlmgr` no Git Bash é `tlmgr.bat`.** `command -v tlmgr` e `tlmgr install ...` falham com *command not found*, porque o Bash não resolve `.bat` pelo PATH sem a extensão. Chamar pelo caminho completo: `"$HOME/AppData/Roaming/TinyTeX/bin/windows/tlmgr.bat" install ...`. O `find` acha (`-name 'tlmgr*'`), o `command -v` não. Nada a ver com o PATH estar errado.
- **`quarto install chrome-headless-shell` travando** quando a ferramenta já está instalada e só há atualização disponível. Checar antes com `quarto list tools`: se aparece "Update available", já dá para renderizar — não esperar o install.
- **PDF via `pdftotext` não recupera acentos** das figuras TikZ (glifos compostos no encoding padrão). Para conferir se a figura entrou no PDF, contar Form XObjects por página com `pypdf` em vez de procurar o texto do rótulo.
- **`python` no Windows pode ser o stub da Microsoft Store.** Se `python --version` abre a loja, usar `py -3` ou o caminho do venv. Dentro do venv, sempre `python -m pip`, nunca `pip` solto — evita instalar no interpretador errado.
- Commits com `-m "..."` simples. Here-string do PowerShell (`@'...'@`) dentro do Bash vaza o `@` para a mensagem e exige `--amend`.
- Emoji em `print()` de Python quebra no console do Windows. Em conteúdo de arquivo UTF-8 é seguro.
- Substituição em massa de LaTeX (`\`, `*`, `^`): `str.replace` do Python. `sed` corrompe superscritos, `grep -c` dá contagem enganosa. **Mas rodar esse Python por heredoc do Bash (`python - <<'PY'`) come as barras invertidas do padrão de busca** — o `replace` não casa, o script grava o arquivo inalterado e imprime "ok", o que parece sucesso. Sintoma: `SyntaxWarning: "\d" is an invalid escape sequence` num trecho onde você escreveu `\\d`. Para padrão com `\`, usar a ferramenta Edit, ou gravar o script `.py` em arquivo e chamar `python arquivo.py`.
- Write após heredoc exige Read antes ("File has not been read yet").
- Ignorar sempre: `LF will be replaced by CRLF` e "Node.js 20 is deprecated".

## Processo

- Fatia vertical: fechar volume antes de abrir o próximo; fase antes da próxima fase.
- Um capítulo por sessão, `/clear` entre capítulos, `/compact` perto de 80%.
- `/model opus` para escrever; `/model sonnet` para tarefa mecânica.
- `ROADMAP.md` é a fila autoritativa. Commit `cap NNN: <titulo>` com status atualizado junto.
- Volume novo começa com smoke test de uma figura TikZ antes do primeiro capítulo.
- CSL ABNT: `raw.githubusercontent.com/citation-style-language/styles/master/associacao-brasileira-de-normas-tecnicas.csl`
