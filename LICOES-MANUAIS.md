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
- **Caractere de desenho de caixa some no PDF, sem erro.** Árvore de diretórios com `├── │ └──` e saída de terminal com `╰─>` renderizam no HTML e **desaparecem** no PDF: o `xelatex` só emite `Missing character: There is no ├ (U+251C) in font [lmmono10-regular]` no log, que o Quarto não mostra, e o build fica verde com a árvore mutilada. Verificado com `pypdf`: zero ocorrências no texto extraído. Usar indentação ASCII pura em árvore de diretórios. (`×`, `→`, `•` e aspas curvas **existem** na fonte e podem ficar.)
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
- **Barra (`/`) dentro da lista de um `\foreach \a/\b in {...}` corrompe a figura.** A barra é o separador dos campos, então `//6` (o caractere `/` na posição 6) é lido como campo vazio e desalinha toda a lista — no Manual de Python isso comeu o `h` e as duas barras de `https://` numa figura de 26 caixas. O `pdflatex` sai com *error code 1* e mensagem inútil (`look up 'weird error' in the index to The TeXbook`), **mas o SVG é gerado assim mesmo, no tamanho normal** — o `grep -c '<svg'` e a checagem de tamanho passam as duas. Só a rasterização pega. Regra: para lista com pontuação, usar `\foreach \c [count=\i from 0] in {a,b,{:},{/},...}` e envolver em chaves todo caractere que não seja letra ou algarismo.
- **Emoji e símbolos fora da Latin-1 não existem nas fontes do pdflatex.** `\node{🐍}` e `\node{€}` derrubam o render com *error code 1* e o caractere simplesmente **não aparece** na figura (o `€` sai como glifo quebrado, o emoji some e deixa a linha vazia). O SVG continua saindo em tamanho normal. Dentro de `{.tikz}`, representar esses caracteres pelo ponto de código (`U+1F40D`) e um rótulo textual; o caractere de verdade fica no texto corrido e nos blocos de código, onde o HTML e o `fvextra` dão conta.
- **Nó posicionado acima do conteúdo mais alto é cortado pela caixa delimitadora.** Uma seta ou rótulo colocado acima de todos os nós pode ficar fora do *bounding box* que o `dvisvgm` calcula e sair pela metade no SVG, sem erro nenhum. Forçar a caixa com um `\path (x1,y1) rectangle (x2,y2);` invisível no começo do `tikzpicture` resolve e é barato.
- **Caixa encostada na vizinha faz a seta entre as duas apontar para trás.** Numa fileira de nós ligados por `\draw[->] (a) -- (b);`, se o espaço entre as bordas for zero ou quase (centros separados por 3,2 cm com `text width=3,2 cm`), a seta tem comprimento nulo ou negativo e o `>=stealth` é desenhado **invertido**, dentro da caixa seguinte. O pdflatex não reclama, o SVG sai no tamanho normal e a checagem de tamanho passa — o diagrama simplesmente afirma o contrário do que deveria. Aconteceu três vezes no Volume 10 do Manual de Python (caps 063 e 064). Regra: deixar pelo menos 0,6–0,9 cm de folga entre as bordas, isto é, `text width` no máximo igual ao espaçamento dos centros menos 0,8 cm. Só a rasterização pega.
- **Nó largo com `text width` e `anchor=west` invade o vizinho da direita sem erro.** Dois rótulos lado a lado, ou um rótulo ao lado de uma caixa, se sobrepõem em silêncio quando a soma `x + text width` passa do início do vizinho. Conferir a aritmética das posições antes de renderizar, e rasterizar sempre.
- **`\\[` no texto de um nó é lido como `\\[<comprimento>]` e derruba a figura.** `{[tool.ruff]\\[tool.pytest.ini\_options]}` faz o LaTeX interpretar `tool.pytest.ini\_options` como a medida opcional da quebra de linha; o erro sai como `! LaTeX Error: There's no line here to end.` seguido de `look up 'weird error' in the index to The TeXbook`, que não aponta para nada. Acontece sempre que a linha seguinte a um `\\` começa com colchete — comum em figura que mostra seção de TOML ou de INI. Correção: `\\{}[tool...]`. Detectar com um regex que busque `\\\\\[([^\]]*)\]` dentro dos blocos `{.tikz}` e reclame quando o argumento não casar com `^-?[\d.]+(pt|mm|cm|em|ex|in|bp|sp)$`.
- **O cache do filtro TikZ mascara figura quebrada — build verde local, vermelho no CI.** O `tikz.lua` guarda o SVG em `~/.cache/tikz-diagram-filter/<nome>.<hash8>.svg`, e a chave é o hash do **código da figura**. Se a figura foi construída com sucesso e o defeito entrou depois numa edição que **não** mudou o hash usado na consulta — ou se o arquivo bom ficou lá de uma versão anterior —, o render local reusa o SVG antigo e passa. O runner tem cache frio, recompila do zero e falha. Sintoma: `Error compiling TikZ figure '<nome>'` no CI, sobre uma figura que renderiza aqui há meses e cuja última edição foi noutro capítulo. **Contar hashes por nome no cache não serve de diagnóstico** — o diretório é compartilhado por todos os manuais e várias entradas para o mesmo nome só significam que a figura foi editada com o tempo. O único teste equivalente ao do runner é apagar a entrada (`rm ~/.cache/tikz-diagram-filter/<nome>.*`) e renderizar de novo; o log tem de mostrar `output written to <nome>.svg`, sinal de que recompilou de verdade em vez de reusar. Fazer isso para toda figura tocada antes do push.
- **Conferir tamanho do SVG, não só a ausência de erro.** `grep -c '<svg'` conta figura quebrada como figura boa. Medir cada bloco `<svg>...</svg>`: abaixo de ~1 KB é figura vazia.
- **Preferir nós explícitos a `\foreach` quando o conteúdo tiver pontuação.** Além do problema conhecido da barra (`/`) como separador de campos, item com `\`, `{`, `}` ou `\\` dentro de lista de `\foreach` é fonte de falha difícil de diagnosticar. Doze `\node` escritos à mão são mais longos e não quebram.
- **Rótulo de aresta em diagrama de estados: usar `sloped` com `bend`, não `above left`/`below right` com `out`/`in`.** Rótulos posicionados por canto colidem entre si e com as legendas dos nós assim que há três ou mais transições saindo do mesmo nó. `to[bend left=16] node[lb,sloped,above,pos=0.5]{...}` acompanha a curva e não sobrepõe. E, quando o nó precisa de descrição, colocá-la **dentro** do nó (`\textbf{R}\\executando`) em vez de num `\node` solto ao lado — elimina a classe inteira de colisão.
- **Bloqueio mais comum é PATH, não pacote faltando.** `quarto install tinytex` não adiciona o bin ao PATH da sessão. Sintoma: figura não renderiza e `tikz.lua` falha com `imgdata nil` (~linha 587). Prepend do bin do TinyTeX antes de qualquer render.
- **Só as bibliotecas TikZ listadas no template existem.** O `tikz.lua` carrega `calc, angles, quotes, arrows.meta, positioning, intersections, decorations.pathreplacing, decorations.markings, patterns, through, backgrounds` — e mais nada. Usar `fit=(a)(b)` (biblioteca `fit`, não carregada) para cercar um grupo de nós derruba a figura. Conferir a linha `\usetikzlibrary` do `tikz.lua` antes de usar chave desconhecida; para cercar nós, `\draw ... rectangle ...` com coordenadas explícitas resolve sem depender de biblioteca.
- Pacotes: `tlmgr install standalone pgf pgfplots dvisvgm xcolor amsmath amsfonts`

## Windows / Claude Code

- **`tlmgr` no Git Bash é `tlmgr.bat`.** `command -v tlmgr` e `tlmgr install ...` falham com *command not found*, porque o Bash não resolve `.bat` pelo PATH sem a extensão. Chamar pelo caminho completo: `"$HOME/AppData/Roaming/TinyTeX/bin/windows/tlmgr.bat" install ...`. O `find` acha (`-name 'tlmgr*'`), o `command -v` não. Nada a ver com o PATH estar errado.
- **`quarto install chrome-headless-shell` travando** quando a ferramenta já está instalada e só há atualização disponível. Checar antes com `quarto list tools`: se aparece "Update available", já dá para renderizar — não esperar o install.
- **PDF via `pdftotext` não recupera acentos** das figuras TikZ (glifos compostos no encoding padrão). Para conferir se a figura entrou no PDF, contar Form XObjects por página com `pypdf` em vez de procurar o texto do rótulo.
- **`python` no Windows pode ser o stub da Microsoft Store.** Se `python --version` abre a loja, usar `py -3` ou o caminho do venv. Dentro do venv, sempre `python -m pip`, nunca `pip` solto — evita instalar no interpretador errado.
- Commits com `-m "..."` simples. Here-string do PowerShell (`@'...'@`) dentro do Bash vaza o `@` para a mensagem e exige `--amend`.
- Emoji em `print()` de Python quebra no console do Windows. Em conteúdo de arquivo UTF-8 é seguro.
- Substituição em massa de LaTeX (`\`, `*`, `^`): `str.replace` do Python. `sed` corrompe superscritos, `grep -c` dá contagem enganosa. **Mas rodar esse Python por heredoc do Bash (`python - <<'PY'`) come as barras invertidas do padrão de busca** — o `replace` não casa, o script grava o arquivo inalterado e imprime "ok", o que parece sucesso. Sintoma: `SyntaxWarning: "\d" is an invalid escape sequence` num trecho onde você escreveu `\\d`. Para padrão com `\`, usar a ferramenta Edit, ou gravar o script `.py` em arquivo e chamar `python arquivo.py`.
- **`Invoke-WebRequest` sem `-UseBasicParsing` falha e parece site fora do ar.** No Windows PowerShell 5.1 ele tenta o motor do Internet Explorer para analisar a resposta; sem IE disponível, pede interação e a chamada morre com *"O Windows PowerShell está no modo NonInteractive"* — **sem** código HTTP. Num laço de checagem de URLs, o resultado é uma coluna inteira de erro que se lê como 404 e faz procurar defeito no deploy que está perfeito. Sempre `Invoke-WebRequest -Uri ... -Method Head -UseBasicParsing`.
- **Checar o Pages logo após o `gh run watch` do publish dá 404 legítimo.** O `quarto-actions/publish` empurra para `gh-pages` e **outro** workflow (`pages-build-deployment`) faz o deploy. Entre um e outro, `gh api repos/<u>/<r>/pages -q '.status'` responde `building`. Esperar virar `built` (ou dar `gh run watch` no run de `pages-build-deployment`) antes de concluir qualquer coisa sobre a URL.
- Write após heredoc exige Read antes ("File has not been read yet").
- Ignorar sempre: `LF will be replaced by CRLF` e "Node.js 20 is deprecated".

## Processo

- Fatia vertical: fechar volume antes de abrir o próximo; fase antes da próxima fase.
- Um capítulo por sessão, `/clear` entre capítulos, `/compact` perto de 80%.
- `/model opus` para escrever; `/model sonnet` para tarefa mecânica.
- `ROADMAP.md` é a fila autoritativa. Commit `cap NNN: <titulo>` com status atualizado junto.
- Volume novo começa com smoke test de uma figura TikZ antes do primeiro capítulo.
- CSL ABNT: `raw.githubusercontent.com/citation-style-language/styles/master/associacao-brasileira-de-normas-tecnicas.csl`
