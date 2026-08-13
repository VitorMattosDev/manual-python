# ROADMAP — Manual de Python

Fila autoritativa de producao. Status: `[ ]` pendente | `[~]` em andamento | `[x]` concluido.

Commit por capitulo: `cap NNN: <titulo>` com o status atualizado no mesmo commit.


## Fase 1 — Fundamentos da Linguagem


### Volume 1 — Primeiros Passos com Python

- [x] **cap 001** - O que é Python: história, filosofia e o Zen da linguagem - `vol01/cap001-o-que-e-python-historia-filosofia-e-o-zen-da.qmd`
- [x] **cap 002** - Como o Python executa código: interpretador, bytecode e CPython - `vol01/cap002-como-o-python-executa-codigo-interpretador.qmd`
- [x] **cap 003** - Instalando o Python: versões, gerenciadores e o Python do sistema - `vol01/cap003-instalando-o-python-versoes-gerenciadores-e-o.qmd`
- [x] **cap 004** - O REPL, os scripts e o primeiro programa - `vol01/cap004-o-repl-os-scripts-e-o-primeiro-programa.qmd`
- [x] **cap 005** - Ambiente de trabalho: editor, VS Code, Jupyter e o terminal - `vol01/cap005-ambiente-de-trabalho-editor-vs-code-jupyter-e.qmd`
- [x] **cap 006** - Sintaxe essencial: indentação, linhas lógicas e comentários - `vol01/cap006-sintaxe-essencial-indentacao-linhas-logicas-e.qmd`
- [x] **cap 007** - Erros e tracebacks: como ler o que o Python está dizendo - `vol01/cap007-erros-e-tracebacks-como-ler-o-que-o-python.qmd`

### Volume 2 — Tipos, Operadores e Expressões

- [x] **cap 008** - Objetos, variáveis e o modelo de referências - `vol02/cap008-objetos-variaveis-e-o-modelo-de-referencias.qmd`
- [x] **cap 009** - Números inteiros, de ponto flutuante e complexos - `vol02/cap009-numeros-inteiros-de-ponto-flutuante-e.qmd`
- [x] **cap 010** - Precisão numérica: decimal, fractions e as armadilhas do float - `vol02/cap010-precisao-numerica-decimal-fractions-e-as.qmd`
- [x] **cap 011** - Booleanos, valor-verdade e os operadores lógicos - `vol02/cap011-booleanos-valor-verdade-e-os-operadores.qmd`
- [x] **cap 012** - Strings: criação, indexação e fatiamento - `vol02/cap012-strings-criacao-indexacao-e-fatiamento.qmd`
- [x] **cap 013** - Métodos de string, formatação e f-strings - `vol02/cap013-metodos-de-string-formatacao-e-f-strings.qmd`
- [x] **cap 014** - Unicode, bytes e codificação de caracteres - `vol02/cap014-unicode-bytes-e-codificacao-de-caracteres.qmd`

### Volume 3 — Controle de Fluxo e Funções

- [x] **cap 015** - Condicionais: if, elif, else e a expressão condicional - `vol03/cap015-condicionais-if-elif-else-e-a-expressao.qmd`
- [x] **cap 016** - Laços: while, for e o protocolo de iteração - `vol03/cap016-lacos-while-for-e-o-protocolo-de-iteracao.qmd`
- [x] **cap 017** - break, continue, else em laços e o casamento de padrões - `vol03/cap017-break-continue-else-em-lacos-e-o-casamento-de.qmd`
- [x] **cap 018** - Definindo funções: parâmetros, argumentos e retorno - `vol03/cap018-definindo-funcoes-parametros-argumentos-e.qmd`
- [x] **cap 019** - Argumentos nomeados, valores padrão, `*args` e `**kwargs` - `vol03/cap019-argumentos-nomeados-valores-padrao-args-e.qmd`
- [x] **cap 020** - Escopo, closures e a regra LEGB - `vol03/cap020-escopo-closures-e-a-regra-legb.qmd`
- [x] **cap 021** - Funções como objetos: lambda, map, filter e ordem superior - `vol03/cap021-funcoes-como-objetos-lambda-map-filter-e.qmd`

### Volume 4 — Estruturas de Dados Nativas

- [x] **cap 022** - Listas: operações, mutabilidade e cópia - `vol04/cap022-listas-operacoes-mutabilidade-e-copia.qmd`
- [x] **cap 023** - Tuplas, empacotamento e desempacotamento - `vol04/cap023-tuplas-empacotamento-e-desempacotamento.qmd`
- [x] **cap 024** - Dicionários: chaves, ordem e os métodos essenciais - `vol04/cap024-dicionarios-chaves-ordem-e-os-metodos.qmd`
- [x] **cap 025** - Conjuntos e operações de conjunto - `vol04/cap025-conjuntos-e-operacoes-de-conjunto.qmd`
- [x] **cap 026** - Compreensões de lista, dicionário e conjunto - `vol04/cap026-compreensoes-de-lista-dicionario-e-conjunto.qmd`
- [x] **cap 027** - Ordenação, chaves de ordenação e comparação de objetos - `vol04/cap027-ordenacao-chaves-de-ordenacao-e-comparacao-de.qmd`
- [x] **cap 028** - Escolhendo a estrutura certa: custo das operações - `vol04/cap028-escolhendo-a-estrutura-certa-custo-das.qmd`

## Fase 2 — Python Estruturado


### Volume 5 — Módulos, Pacotes e o Ambiente

- [x] **cap 029** - Módulos, import e o caminho de busca - `vol05/cap029-modulos-import-e-o-caminho-de-busca.qmd`
- [x] **cap 030** - Pacotes, `__init__.py` e a organização de um projeto - `vol05/cap030-pacotes-init-py-e-a-organizacao-de-um-projeto.qmd`
- [x] **cap 031** - Ambientes virtuais: venv, pip e o isolamento de dependências - `vol05/cap031-ambientes-virtuais-venv-pip-e-o-isolamento-de.qmd`
- [x] **cap 032** - Empacotamento moderno: pyproject.toml, build e publicação - `vol05/cap032-empacotamento-moderno-pyproject-toml-build-e.qmd`
- [x] **cap 033** - uv, pipx e Poetry: o ecossistema de gerenciamento - `vol05/cap033-uv-pipx-e-poetry-o-ecossistema-de.qmd`
- [x] **cap 034** - Ponto de entrada: `__main__`, scripts de console e a linha de comando - `vol05/cap034-ponto-de-entrada-main-scripts-de-console-e-a.qmd`

### Volume 6 — Arquivos, Erros e Contextos

- [x] **cap 035** - Leitura e escrita de arquivos de texto - `vol06/cap035-leitura-e-escrita-de-arquivos-de-texto.qmd`
- [x] **cap 036** - Arquivos binários, buffers e o módulo io - `vol06/cap036-arquivos-binarios-buffers-e-o-modulo-io.qmd`
- [x] **cap 037** - Caminhos e o sistema de arquivos com pathlib - `vol06/cap037-caminhos-e-o-sistema-de-arquivos-com-pathlib.qmd`
- [x] **cap 038** - Exceções: hierarquia e o bloco try, except, else e finally - `vol06/cap038-excecoes-hierarquia-e-o-bloco-try-except-else.qmd`
- [x] **cap 039** - Levantando exceções e criando exceções próprias - `vol06/cap039-levantando-excecoes-e-criando-excecoes.qmd`
- [x] **cap 040** - Gerenciadores de contexto e a instrução with - `vol06/cap040-gerenciadores-de-contexto-e-a-instrucao-with.qmd`

### Volume 7 — Programação Orientada a Objetos

- [x] **cap 041** - Classes, instâncias e o self - `vol07/cap041-classes-instancias-e-o-self.qmd`
- [x] **cap 042** - Atributos, propriedades e encapsulamento - `vol07/cap042-atributos-propriedades-e-encapsulamento.qmd`
- [x] **cap 043** - Herança, MRO e a função super - `vol07/cap043-heranca-mro-e-a-funcao-super.qmd`
- [x] **cap 044** - Composição, delegação e quando não herdar - `vol07/cap044-composicao-delegacao-e-quando-nao-herdar.qmd`
- [x] **cap 045** - Métodos estáticos, métodos de classe e o desenho da API - `vol07/cap045-metodos-estaticos-metodos-de-classe-e-o.qmd`
- [x] **cap 046** - Dataclasses, NamedTuple e enumerações - `vol07/cap046-dataclasses-namedtuple-e-enumeracoes.qmd`
- [x] **cap 047** - Classes abstratas, protocolos e duck typing - `vol07/cap047-classes-abstratas-protocolos-e-duck-typing.qmd`

### Volume 8 — O Modelo de Dados de Python

- [x] **cap 048** - Métodos especiais: o protocolo por trás da sintaxe - `vol08/cap048-metodos-especiais-o-protocolo-por-tras-da.qmd`
- [x] **cap 049** - Iteradores e o protocolo de iteração - `vol08/cap049-iteradores-e-o-protocolo-de-iteracao.qmd`
- [x] **cap 050** - Geradores, yield e a avaliação preguiçosa - `vol08/cap050-geradores-yield-e-a-avaliacao-preguicosa.qmd`
- [x] **cap 051** - Decoradores de função - `vol08/cap051-decoradores-de-funcao.qmd`
- [x] **cap 052** - Decoradores de classe, functools e metadados preservados - `vol08/cap052-decoradores-de-classe-functools-e-metadados.qmd`
- [x] **cap 053** - Descritores, `__slots__` e o acesso a atributos - `vol08/cap053-descritores-slots-e-o-acesso-a-atributos.qmd`
- [x] **cap 054** - Metaclasses e `__init_subclass__`: quando (não) usar - `vol08/cap054-metaclasses-e-init-subclass-quando-nao-usar.qmd`

## Fase 3 — Biblioteca Padrão e Qualidade


### Volume 9 — A Biblioteca Padrão Essencial

- [x] **cap 055** - os, sys e a interação com o sistema - `vol09/cap055-os-sys-e-a-interacao-com-o-sistema.qmd`
- [x] **cap 056** - datetime, zoneinfo e o tratamento de tempo - `vol09/cap056-datetime-zoneinfo-e-o-tratamento-de-tempo.qmd`
- [x] **cap 057** - collections: deque, Counter, defaultdict e namedtuple - `vol09/cap057-collections-deque-counter-defaultdict-e.qmd`
- [x] **cap 058** - itertools e functools: a caixa de ferramentas funcional - `vol09/cap058-itertools-e-functools-a-caixa-de-ferramentas.qmd`
- [x] **cap 059** - math, statistics e random - `vol09/cap059-math-statistics-e-random.qmd`
- [x] **cap 060** - logging: registrando o que o programa faz - `vol09/cap060-logging-registrando-o-que-o-programa-faz.qmd`

### Volume 10 — Texto, Dados e Serialização

- [x] **cap 061** - Expressões regulares com o módulo re - `vol10/cap061-expressoes-regulares-com-o-modulo-re.qmd`
- [x] **cap 062** - JSON, CSV e formatos tabulares - `vol10/cap062-json-csv-e-formatos-tabulares.qmd`
- [x] **cap 063** - YAML, TOML e arquivos de configuração - `vol10/cap063-yaml-toml-e-arquivos-de-configuracao.qmd`
- [x] **cap 064** - Serialização binária: pickle, struct e os riscos envolvidos - `vol10/cap064-serializacao-binaria-pickle-struct-e-os.qmd`
- [x] **cap 065** - SQLite e a DB-API: banco de dados sem servidor - `vol10/cap065-sqlite-e-a-db-api-banco-de-dados-sem-servidor.qmd`
- [x] **cap 066** - hashlib, secrets e o tratamento de dados sensíveis - `vol10/cap066-hashlib-secrets-e-o-tratamento-de-dados.qmd`

### Volume 11 — Qualidade: Testes, Tipagem e Ferramentas

- [x] **cap 067** - Estilo, PEP 8 e formatação automática com Ruff e Black - `vol11/cap067-estilo-pep-8-e-formatacao-automatica-com-ruff.qmd`
- [x] **cap 068** - Anotações de tipo: fundamentos e o módulo typing - `vol11/cap068-anotacoes-de-tipo-fundamentos-e-o-modulo.qmd`
- [x] **cap 069** - Tipagem avançada: genéricos, protocolos e mypy - `vol11/cap069-tipagem-avancada-genericos-protocolos-e-mypy.qmd`
- [x] **cap 070** - Testes com pytest: fundamentos, asserções e fixtures - `vol11/cap070-testes-com-pytest-fundamentos-assercoes-e.qmd`
- [x] **cap 071** - Parametrização, dublês de teste e cobertura - `vol11/cap071-parametrizacao-dubles-de-teste-e-cobertura.qmd`
- [x] **cap 072** - Depuração: pdb, breakpoint e o traceback difícil - `vol11/cap072-depuracao-pdb-breakpoint-e-o-traceback-dificil.qmd`
- [x] **cap 073** - Documentação: docstrings, doctest e Sphinx - `vol11/cap073-documentacao-docstrings-doctest-e-sphinx.qmd`

## Fase 4 — Python Aplicado


### Volume 12 — Automação, Sistema e Redes

- [x] **cap 074** - Scripts de automação: arquivos, planilhas e tarefas repetitivas - `vol12/cap074-scripts-de-automacao-arquivos-planilhas-e.qmd`
- [x] **cap 075** - subprocess: chamando programas externos com segurança - `vol12/cap075-subprocess-chamando-programas-externos-com.qmd`
- [x] **cap 076** - Interfaces de linha de comando com argparse, Click e Typer - `vol12/cap076-interfaces-de-linha-de-comando-com-argparse.qmd`
- [x] **cap 077** - Redes com sockets: TCP, UDP e o modelo cliente-servidor - `vol12/cap077-redes-com-sockets-tcp-udp-e-o-modelo-cliente.qmd`
- [x] **cap 078** - Requisições HTTP com requests e httpx - `vol12/cap078-requisicoes-http-com-requests-e-httpx.qmd`
- [x] **cap 079** - Raspagem de dados responsável: HTML, seletores e limites éticos - `vol12/cap079-raspagem-de-dados-responsavel-html-seletores.qmd`

### Volume 13 — Dados, Análise e Visualização

- [ ] **cap 080** - NumPy: arrays, vetorização e broadcasting - `vol13/cap080-numpy-arrays-vetorizacao-e-broadcasting.qmd`
- [ ] **cap 081** - pandas: Series, DataFrame e a carga de dados - `vol13/cap081-pandas-series-dataframe-e-a-carga-de-dados.qmd`
- [ ] **cap 082** - Limpeza, transformação e agregação com pandas - `vol13/cap082-limpeza-transformacao-e-agregacao-com-pandas.qmd`
- [ ] **cap 083** - Visualização de dados com Matplotlib - `vol13/cap083-visualizacao-de-dados-com-matplotlib.qmd`
- [ ] **cap 084** - SciPy e a computação científica aplicada - `vol13/cap084-scipy-e-a-computacao-cientifica-aplicada.qmd`
- [ ] **cap 085** - Introdução ao aprendizado de máquina com scikit-learn - `vol13/cap085-introducao-ao-aprendizado-de-maquina-com.qmd`

### Volume 14 — Web, APIs e Bancos de Dados

- [ ] **cap 086** - Como funciona uma aplicação web: HTTP, WSGI e ASGI - `vol14/cap086-como-funciona-uma-aplicacao-web-http-wsgi-e.qmd`
- [ ] **cap 087** - Validação de dados com Pydantic - `vol14/cap087-validacao-de-dados-com-pydantic.qmd`
- [ ] **cap 088** - APIs REST com FastAPI - `vol14/cap088-apis-rest-com-fastapi.qmd`
- [ ] **cap 089** - Flask e Django: quando usar cada um - `vol14/cap089-flask-e-django-quando-usar-cada-um.qmd`
- [ ] **cap 090** - Bancos de dados relacionais com SQLAlchemy - `vol14/cap090-bancos-de-dados-relacionais-com-sqlalchemy.qmd`
- [ ] **cap 091** - Autenticação, autorização e segurança em aplicações Python - `vol14/cap091-autenticacao-autorizacao-e-seguranca-em.qmd`
- [ ] **cap 092** - Implantação: contêineres, servidores de aplicação e produção - `vol14/cap092-implantacao-conteineres-servidores-de.qmd`

## Fase 5 — Avançado e Fronteira


### Volume 15 — Concorrência, Desempenho e Internos

- [ ] **cap 093** - Concorrência, paralelismo e o GIL - `vol15/cap093-concorrencia-paralelismo-e-o-gil.qmd`
- [ ] **cap 094** - Threads e o módulo threading - `vol15/cap094-threads-e-o-modulo-threading.qmd`
- [ ] **cap 095** - Multiprocessing e o paralelismo real - `vol15/cap095-multiprocessing-e-o-paralelismo-real.qmd`
- [ ] **cap 096** - Programação assíncrona: async, await e asyncio - `vol15/cap096-programacao-assincrona-async-await-e-asyncio.qmd`
- [ ] **cap 097** - Medindo desempenho: timeit, profiling e otimização - `vol15/cap097-medindo-desempenho-timeit-profiling-e.qmd`
- [ ] **cap 098** - Memória, contagem de referências e o coletor de lixo - `vol15/cap098-memoria-contagem-de-referencias-e-o-coletor.qmd`

### Volume 16 — Fronteira e Prática Contínua

- [ ] **cap 099** - Estendendo Python: C, Cython e ligações nativas - `vol16/cap099-estendendo-python-c-cython-e-ligacoes-nativas.qmd`
- [ ] **cap 100** - Python acelerado: PyPy, Numba e o interpretador sem GIL - `vol16/cap100-python-acelerado-pypy-numba-e-o-interpretador.qmd`
- [ ] **cap 101** - Arquitetura de projetos e código sustentável - `vol16/cap101-arquitetura-de-projetos-e-codigo-sustentavel.qmd`
- [ ] **cap 102** - Git, pre-commit e integração contínua para projetos Python - `vol16/cap102-git-pre-commit-e-integracao-continua-para.qmd`
- [ ] **cap 103** - Python e inteligência artificial: LLMs, APIs e agentes - `vol16/cap103-python-e-inteligencia-artificial-llms-apis-e.qmd`
- [ ] **cap 104** - Para onde ir depois: PEPs, comunidade e prática contínua - `vol16/cap104-para-onde-ir-depois-peps-comunidade-e-pratica.qmd`

---

**Total:** 104 capitulos em 16 volumes (79 concluidos).

