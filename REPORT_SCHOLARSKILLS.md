# ScholarSkills — relatório da revisão do portal

**Data:** 26/11/2026
**Branch:** `rev/portal-audit-2026-11` (a partir de `main`, commit `2a88f0c`)
**Escopo:** revisão editorial e técnica do portal gerado por `scripts/build_site.py`
**Estado:** implementação concluída para P0 e P1; P2 parcial. Nada foi enviado, mergeado ou depositado.

## 1. O que foi feito

### P0 — identidade, conceito, roadmap, evidência e instalação

- **Identidade:** o portal passa a se apresentar como **ScholarSkills**, com o subtítulo “Skills científicas para agentes de inteligência artificial” e a linha “Iniciativa Métodos Digitais”. O identificador técnico (`scholarskills`, `SS-NNNN`, URL do Pages) foi preservado. `README.md` foi alinhado; `brand_note` registra que citações e depósitos antigos não são reescritos.
- **Seção conceitual:** a home mantém quatro cartões curtos e leva a uma página própria (`conceitos.html` / `en/concepts.html`) com o texto completo sobre LLM, agente, skill, ferramenta, o que é uma skill científica, exemplo Zotero e base normativa.
- **Diagrama:** SVG inline, responsivo, com `<title>`/`<desc>`, versão horizontal e versão vertical para mobile. O ciclo inclui o pesquisador, o agente, o LLM, a skill, as ferramentas, os resultados e a parada humana. A skill orienta o agente; não chama a ferramenta.
- **Roadmap:** skills planejadas saíram do grid principal e ganharam seção e template próprios. As páginas individuais continuam nas URLs antigas, mas como **registro de roadmap**: sem versão, DOI, citação, instalação ou evidência, com `noindex` e aviso explícito. Nenhum campo vazio foi preenchido com conteúdo inventado.
- **Evidência:** página nova (`evidencias.html` / `en/evidence.html`) com seis dimensões independentes: conformidade estrutural, testes funcionais, avaliação metodológica, revisão por pares, reexecução independente e replicação científica. A matriz por skill é gerada do registro. A distinção entre reexecução e replicação cita a NASEM (2019).
- **Instalação:** páginas de skill agora separam requisitos, instalação, ativação e verificação. O guia (`como-utilizar.html` / `en/using.html`) cobre Hermes Agent (`$HERMES_HOME/skills/`, `hermes skills list`, `/skill <nome>`) e Claude Code (`~/.claude/skills/`, `.claude/skills/`), com a ressalva de que a ativação não foi executada nesta revisão.

### P1 — taxonomia, trilhas, contribuição e idioma

- **Taxonomia:** tipo editorial (`methodological`, `infrastructure`, `meta`) no registro, no card, na ficha e no filtro. A classificação é explicitamente preliminar.
- **Filtros:** tipo, etapa, status, maturidade e disciplina, combináveis; busca sem distinção de caixa/acentos; botão de limpar; contador anunciado; estado vazio; filtros persistidos na URL. Nenhuma telemetria.
- **Trilhas:** deixaram de ser pills e viraram fluxos com descrição, etapas linkadas, estado de disponibilidade por etapa e contagem de etapas disponíveis hoje. O botão de filtrar por trilha continua funcional.
- **Contribuição:** a página descreve três caminhos (preparar com agente, abrir pull request, pedir orientação sem Git), o que a revisão verifica e como a revisão acontece. Remove a promessa de que o SS-0000 “faz o resto”.
- **Idioma:** o seletor aponta para a página equivalente, inclusive nas páginas de skill. Foram corrigidos os caminhos relativos PT/EN.
- **Contadores:** o número de autores deixou de ser fixo em `3`; disponíveis, planejadas, DOI e autores são derivados do catálogo.

### P2 — acessibilidade, SEO e manutenção

- Skip link, foco visível, `aria-live` para contador e cópia, labels nos filtros, `prefers-reduced-motion`, navegação por teclado nos controles nativos.
- `canonical`, `hreflang` recíproco, Open Graph, `sitemap.xml`, `robots.txt` e JSON-LD (`WebSite`, `WebPage`, `SoftwareSourceCode`, `CreativeWork` para roadmap).
- Removido `overflow-x:hidden`, que mascarava estouro horizontal. Após correções, não há overflow em 1440, 1024, 768, 390 e 320 px nas páginas testadas.
- CI: `validate.yml` passa a instalar `jsonschema` e executar `tests/test_site.py`.

## 2. Arquivos

**Editoriais e de dados**
- `registry/registry.json` — identidade, taxonomia, dimensões de evidência, tipo, limites, evidências por skill, correção de instalação.
- `registry/metadata-schema.json` — esquema reescrito para os campos reais; validação condicional para skills disponíveis.
- `README.md`, `CONTRIBUTING.md`, `registry/EDITORIAL_POLICY.md` — nome, jornada sem Git, dimensões de evidência.

**Gerador**
- `scripts/build_site.py` — novas páginas, header/footer, idioma, filtros, roadmap, evidência, SEO, sitemap, CSS e JS.
- `scripts/content.py` — texto longo PT/EN (novo).

**Testes**
- `tests/test_site.py` — 12 invariantes (novo).
- `.github/workflows/validate.yml` — execução dos testes do portal.

**Site gerado**
- `site/**` — 61 arquivos, incluindo `conceitos.html`, `como-utilizar.html`, `evidencias.html`, `sobre.html`, `en/concepts.html`, `en/using.html`, `en/evidence.html`, `en/about.html`, `sitemap.xml`, `robots.txt`.

## 3. Verificação executada

### Build
- `python3 scripts/build_site.py` → `built 61 files for 15 skills`.
- `python3 scripts/build_site.py --check` → `site is up to date`.
- Hash de conteúdo final: `bd5c6434a27b82a8`.

### Testes do portal
```
python3 -m unittest tests.test_site -v
Ran 12 tests ... OK
```
Cobrem: esquema do registro, IDs/slugs únicos, paridade PT/EN, links internos, placeholders, roadmap sem DOI/citação/instalação, páginas disponíveis com instalação/evidência/limites, contadores, troca de idioma, JSON-LD, sitemap, skip link, `h1` único e IDs únicos.

### Pacotes
Execução local em Python 3.14.9, 26/11/2026:

- SS-0000: validador PASS, 0 avisos; 21 testes OK.
- SS-0001: PASS, 0 avisos; 20 testes OK.
- SS-0010: PASS, 3 avisos (referências vazias, exemplos vazios, sem `benchmarks/`); 20 testes OK.
- SS-0011: PASS, 3 avisos; 21 testes OK.
- SS-0012: PASS, 3 avisos; 19 testes OK.
- SS-0013: PASS, 3 avisos; 33 testes OK.
- SS-0014: PASS, 0 avisos; 6 testes OK.

Os avisos são pré-existentes e não foram mascarados. O CI testa Python 3.10 e 3.12; a execução local foi em 3.14.9.

### Links e identificadores
- 14 DOIs de skill/coleção resolveram com HTTP 200 para registros Zenodo.
- 3 ORCIDs responderam 200 em `pub.orcid.org`.
- `agentskills.io/specification`, WCAG 2.2, CFF, Zenodo Developers e Schema.org responderam 200.
- O DOI da NASEM (`10.17226/25303`) respondeu 403 a um HEAD via `doi.org`; não foi possível confirmar por esse método. O link é mantido como referência e a limitação fica registrada.

### Interface
- Overflow horizontal: nenhum em 1440, 1024, 768, 390 e 320 px nas 10 páginas testadas.
- Nav mobile cabe em 320 px (right 304, viewport 320).
- Screenshots em `/home/hermes/.hermes/cache/scratch/ss-baseline/` (antes) e `/home/hermes/.hermes/cache/scratch/ss-after/` (depois).
- Revisão visual real: home desktop/mobile, página conceitual, diagrama desktop/mobile, página de skill, página de evidências. Foram corrigidos: nav cortada no mobile, hero desbalanceado, estatísticas em uma coluna, título duplicado, chips sem estilo, ação de instalar sem hierarquia, breadcrumb “Hub”, setas e rótulos do diagrama.
- Páginas de roadmap, contribuição e sobre foram verificadas por testes e inspeção de HTML, mas não por revisão visual dedicada.

## 4. Decisões editoriais

1. **ScholarSkills como nome de exibição; Métodos Digitais como iniciativa.** O identificador técnico e as URLs não mudam.
2. **Roadmap não é software.** Registros planejados não recebem citação, versão, DOI, instalação ou evidência. O escopo só aparece quando documentado; caso contrário, a página diz que não está documentado.
3. **Evidência não é escada.** A política editorial mantém os quatro níveis até revisão formal, mas o portal exibe seis dimensões independentes e não promove nenhum pacote automaticamente.
4. **Tipo editorial preliminar.** A classificação pode ser revista pelos autores; está marcada como preliminar na interface.
5. **Idioma.** PT-BR é a árvore principal; EN espelha as mesmas páginas. `en/contribuir.html` foi preservado como URL pública.

## 5. Não realizado / limitações

- **Ativação real em agente:** não executada. A tentativa com `HERMES_HOME` temporário foi bloqueada pelo perfil fixo `casa-test`; não foi contornada para não alterar configuração. O guia descreve o procedimento, mas não afirma teste executado.
- **Claude Code:** não testado.
- **APIs reais:** nenhuma chamada real às APIs das skills foi feita.
- **Acessibilidade:** não houve auditoria WCAG externa, teste com leitor de tela, medição automatizada de contraste nem zoom 200%. Foram feitos inspeção visual, foco visível, navegação por teclado nos controles nativos e teste de overflow.
- **Correspondência dos DOIs:** os DOIs resolvem, mas o conteúdo dos registros Zenodo não foi auditado campo a campo contra o registro local.
- **Links externos:** verificação pontual dos DOIs, ORCIDs e referências principais; não foi feito crawling de todos os links externos.
- **Documentação histórica:** `DEPLOYMENT_LOG.md` não foi reescrito. Entradas antigas continuam descrevendo estados passados.
- **P2 restante:** auditoria de contraste, revisão de todos os textos EN, validação de HTML por validador externo e teste em dispositivos reais.

## 6. Como revisar

```bash
cd /home/hermes/projects/scholarskills
git diff main --stat
git diff main -- registry/ scripts/ tests/ README.md CONTRIBUTING.md
python3 scripts/build_site.py --check
python3 -m unittest tests.test_site -v
python3 -m http.server 8811 --directory site
```

Abrir `http://127.0.0.1:8811/`, `conceitos.html`, `como-utilizar.html`, `evidencias.html`, `contribuir.html`, `sobre.html` e uma página de skill. Comparar com os screenshots de baseline.

## 7. Publicação

Nada foi enviado ao GitHub, mergeado, tagueado ou depositado no Zenodo. A branch `rev/portal-audit-2026-11` contém as mudanças. Publicar exige autorização explícita e, se houver depósito, revisão dos metadados e do DOI.
