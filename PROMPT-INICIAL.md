# Prompt de abertura — primeira sessão no Claude Code

Cole o texto abaixo na primeira sessão, dentro da pasta do repositório.

---

Você vai trabalhar no **Manual de Python**, um livro Quarto em português do Brasil. Leia `CLAUDE.md`, `LICOES-MANUAIS.md` e `FIGURAS.md` antes de qualquer coisa — eles contêm as convenções e os erros já pagos em builds vermelhos dos outros manuais da série (Economia, História, Segurança, Linux). Depois leia o `ROADMAP.md`, que é a fila autoritativa de produção.

A versão de referência é o **Python 3.13**, em ambiente Linux (Kali/Debian). O código é moderno: `pathlib` em vez de `os.path`, f-strings em vez de `%`, `list[int]` em vez de `typing.List[int]`, `match` onde couber. Onde um recurso for recente, marque a versão mínima; onde o código legado ainda for comum em produção, explique o que se fazia antes e por que mudou.

Modo autônomo: você está pré-aprovado para criar e editar arquivos, gerar figuras, rodar validações e fazer commits sem me consultar a cada passo. Só pare em erro real de bloqueio.

**Tarefa desta sessão, em ordem:**

1. **Bootstrap da toolchain.** Instale TinyTeX e os pacotes LaTeX e instale o `chrome-headless-shell`. Localize o `tlmgr` com `find` sem `-type f` se ele não estiver no PATH, e rode `tlmgr update --self` antes de qualquer `install`. Faça o prepend do bin do TinyTeX no PATH da sessão — sem isso as figuras TikZ falham em silêncio.

2. **Ambiente Python de teste.** Crie um `venv` só para rodar os exemplos do livro (`python -m venv .venv-exemplos`, fora do controle de versão). Todo código que entra num capítulo é executado nele antes de a saída ser colada. Confirme a versão com `python --version` e registre-a no capítulo 1.

3. **CSL da ABNT.** O arquivo `associacao-brasileira-de-normas-tecnicas.csl` já está na raiz (copiado dos outros manuais). Confirme que começa com `<?xml` e que tem um `<style`. Se estiver corrompido, rebaixe de:

   ```bash
   curl -fsSL -o associacao-brasileira-de-normas-tecnicas.csl \
     https://raw.githubusercontent.com/citation-style-language/styles/master/associacao-brasileira-de-normas-tecnicas.csl
   ```

4. **Extensão TikZ.** Copie `_extensions/danmackinlay/tikz/` de um dos manuais existentes (é a versão com os patches locais). **Não** rode `quarto add` nem `quarto update` nessa extensão em hipótese alguma.

5. **Stubs.** Rode `python scripts/estrutura.py --tudo` e confirme que os 104 stubs existem em disco. Renderizar sem eles falha com "Book chapter not found". Confira a contagem de `concluidos preservados` que o script imprime.

6. **Smoke test.** Antes de escrever qualquer conteúdo, crie uma figura TikZ mínima em `vol01/cap001-*.qmd` e rode `quarto render --to html`. Confirme que ela virou `<svg` no HTML gerado — e que o SVG tem mais de 1 KB. Se não virou, o problema é PATH; resolva antes de seguir. Depois rode `quarto render --to pdf` e confirme que o PDF sai.

7. **Bootstrap do gh-pages.** Crie o branch vazio no remoto antes do primeiro publish:

   ```bash
   git push origin $(git commit-tree $(git hash-object -t tree /dev/null) -m 'init gh-pages'):refs/heads/gh-pages
   ```

8. **Primeiro capítulo.** Escreva o **cap 001 — "O que é Python: história, filosofia e o Zen da linguagem"** por inteiro, seguindo a anatomia do `CLAUDE.md`: abertura por problema concreto, corpo denso de 2.500 a 4.000 palavras, e as duas seções obrigatórias — `🐍 Jeito Pythônico` e `🧪 Laboratório`. Sem crossref para capítulo que ainda não existe: referência a volume futuro é menção textual.

9. **Validação e commit.** Render HTML e PDF, `grep -rhoE '\?@[a-z-]+' _book/**/*.html` retornando zero, contagem de `<svg` batendo com os blocos `{.tikz}`, e todo exemplo do capítulo executado no venv com a saída conferida. Commit como `cap 001: O que é Python`, com o status atualizado no `ROADMAP.md` no mesmo commit. Push e `gh run watch <id> --exit-status`.

**Contexto para os exemplos:** trabalho em um provedor de internet (fibra e rádio) atendendo zona rural, então exemplos que envolvem processar logs, consultar APIs, automatizar relatórios, mexer em arquivos de configuração e falar com equipamentos de rede são bem-vindos. O manual é um manual de Python de propósito geral, não um manual de automação de ISP — mas os exemplos podem beber dessa realidade em vez de inventar `foo` e `bar`. Uso Kali no dia a dia, então os comandos de shell podem assumir Linux, com nota para Windows onde a diferença importa.

**Lembrete importante sobre código:** todo exemplo mostrado precisa rodar de verdade, e a saída colada precisa ser a saída real do interpretador — inclusive nos exemplos de erro, onde o traceback vai completo. Saída inventada não quebra o build; quebra o leitor. E os blocos são cercas estáticas ```` ```python ````, nunca células executáveis ```` ```{python} ````.
