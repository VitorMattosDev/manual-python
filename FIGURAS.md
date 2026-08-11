# Figuras — TikZ

## Instalação da extensão (com patches)

A pasta `_extensions/danmackinlay/tikz/` deve ser copiada de `figuras-tikz-kit.zip` (ou de um dos manuais já existentes), que contém a versão **com os patches locais**.

> **Nunca** rodar `quarto add danmackinlay/tikz` nem `quarto update`. Ambos baixam o upstream sem os patches e quebram a renderização.

## Configuração no `_quarto.yml`

```yaml
filters:
  - tikz      # precisa vir ANTES de quarto
  - quarto

tikz:
  svg-engine: dvisvgm
  cache: true
```

## Sintaxe padrão

````markdown
::: {#fig-nome-da-figura}
```{.tikz}
%%| filename: nome-da-figura
%%| alt: Descrição textual da figura para acessibilidade
\begin{tikzpicture}
  \draw[curva] (0,0) -- (3,2);
  \node[ponto] at (3,2) {};
\end{tikzpicture}
```
Legenda da figura, antes do fechamento do div.
:::
````

Referência no texto: `@fig-nome-da-figura`.

## Estilos disponíveis (do template — não redefinir)

- Linhas: `curva`, `destaque`, `auxiliar`, `eixo`
- Nós: `ponto`, `vetor`
- Cores: `manualblue`, `manualred`, `manualgreen`, `manualyellow`, `manualgray`

## Diagramas típicos deste manual

| Tema | Tipo de figura |
|---|---|
| Variáveis, objetos e referências | Caixas com setas para o heap |
| Mutabilidade, cópia rasa e profunda | Dois estados lado a lado |
| Escopo e a regra LEGB | Caixas aninhadas |
| Pilha de chamadas e recursão | Pilha vertical de quadros |
| Herança e MRO | Árvore/grafo com ordem numerada |
| Protocolo de iteração e geradores | Máquina de estados |
| Decoradores | Envelopamento (função dentro de função) |
| Modelo de execução: fonte → bytecode → VM | Fluxo em etapas |
| GIL, threads e processos | Linhas do tempo paralelas |
| Event loop do asyncio | Ciclo com fila de tarefas |
| Contagem de referências e ciclos | Grafo de objetos |
| Empacotamento e ambientes virtuais | Diagrama de camadas |

## Cuidados específicos deste manual

- **Underscore em rótulo é subscrito no LaTeX.** `\node{__init__}` sai errado. Usar `\texttt{\_\_init\_\_}`.
- **Chave e cifrão em código dentro da figura** (`{`, `}`, `$`, `%`, `#`) precisam de escape: `\{`, `\}`, `\$`, `\%`, `\#`.
- **Crossref dentro do bloco `{.tikz}` sai literal** — dentro da figura, referência a capítulo é menção textual sem `@`.

## Cuidados que já quebraram figura neste manual

- **Barra dentro de `\foreach \a/\b in {...}`.** A `/` é o separador dos campos: `//6` desalinha a lista inteira. Usar `\foreach \c [count=\i from 0] in {a,b,{:},{/}}` e envolver pontuação em chaves.
- **Emoji e `€` não existem nas fontes do pdflatex.** Representar por ponto de código (`U+1F40D`) dentro da figura; o caractere de verdade fica no texto e no código.
- **Nó acima do conteúdo mais alto sai cortado.** Forçar a caixa com um `\path (x1,y1) rectangle (x2,y2);` invisível.

Os três falham com `error code 1` no `pdflatex` **e mesmo assim produzem um SVG de tamanho normal** — a contagem e a medição passam. Só a rasterização pega.

## Checagem obrigatória

```bash
quarto render --to html
py -3 scripts/valida.py                 # crossrefs, citacoes, contagem e tamanho dos SVG
py -3 scripts/rasteriza.py _book/volNN/capNNN-....html <destino>   # PNG por figura, para olhar
quarto render --to pdf                  # so depois, porque apaga o HTML
py -3 scripts/confere_pdf.py            # Form XObjects por pagina contra blocos {.tikz}
```

O `valida.py` compara `<svg` no HTML com os blocos `{.tikz}` do `.qmd` e mede cada bloco: abaixo de ~1 KB é figura vazia, e o `grep -c` sozinho a contaria como boa. Divergência na contagem é quase sempre PATH do TinyTeX.

O `rasteriza.py` usa o `chrome-headless-shell` que o Quarto já instala e é o único passo que pega figura que compilou e saiu errada — caractere sumido, estilo inexistente, rótulo sobreposto, nó cortado.
