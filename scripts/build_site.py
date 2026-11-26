#!/usr/bin/env python3
"""Generate the Métodos Digitais hub (repository: scholarskills) from registry/registry.json.

Two languages, one source of truth. Portuguese is the primary language (site root); English is
generated under /en/. Both trees are static HTML: no runtime translation, stable URLs, works
without JavaScript.

    python3 scripts/build_site.py [--out site] [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content  # noqa: E402  (editorial copy lives next to this generator)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "registry.json"
ASSETS = ROOT / "assets" / "img"

LANGS = ("pt", "en")

MATURITY = {"experimental": ("Experimental", "warn"), "tested": ("Testado", "ok"),
            "peer-reviewed": ("Revisado por pares", "accent"),
            "replicated": ("Replicado", "accent")}
MATURITY_EN = {"experimental": ("Experimental", "warn"), "tested": ("Tested", "ok"),
               "peer-reviewed": ("Peer-reviewed", "accent"),
               "replicated": ("Replicated", "accent")}
STATUS = {"available": ("Disponível", "accent"), "planned": ("Planejada", "muted"),
          "deprecated": ("Descontinuada", "bad")}
STATUS_EN = {"available": ("Available", "accent"), "planned": ("Planned", "muted"),
             "deprecated": ("Deprecated", "bad")}
# Icon files downloaded from the vendors' own sites (see DEPLOYMENT_LOG entry 025).
ICON_ASSET = {
    "python": "python.png",
    "zotero": "zotero.svg",
    "github": "github.png",
    "hermes": "hermes.png",
    "zenodo": "zenodo.svg",
}

ICON_LABEL = {"zotero": "Zotero", "hermes": "Hermes Agent", "python": "Python", "github": "GitHub"}

T = {
 "pt": {
  "switch": "English", "nav_home": "Início", "nav_skills": "Skills", "nav_stages": "Etapas",
  "nav_levels": "Maturidade", "nav_submit": "Submeter",
  "available": "disponíveis", "planned": "planejadas", "with_doi": "com DOI", "authors": "autores",
  "search": "Buscar skill, palavra-chave, autor…", "all_status": "Todos os status",
  "all_maturity": "Toda maturidade", "all_stages": "Todas as etapas",
  "empty": "Nenhuma skill corresponde a esses filtros.", "view": "Ver detalhes",
  "objective": "Objetivo", "req_h": "Requisitos",
  "req_intro": "O que você precisa ter antes de rodar esta skill. Tudo o que é exigido aparece aqui — inclusive credenciais.",
  "req_required": "Obrigatório", "req_optional": "Opcional", "req_env": "Variável de ambiente",
  "req_what": "O que é", "req_how": "Como obter", "req_note": "Cuidado",
  "req_secret": "credencial", "req_software": "software", "req_id": "identificador", "req_choice": "configuração",
  "req_none": "Nenhum requisito além do próprio pacote.",
  "nav_paths": "Trilhas", "all_disc": "Todas as disciplinas",
  "paths_h": "Trilhas de pesquisa",
  "paths_p": "Sequências de trabalho que combinam skills na ordem em que a pesquisa acontece — em vez de uma peça isolada, o caminho inteiro.",
  "path_skills": "skills", "path_open": "Ver a trilha",
  "disc_h": "Disciplinas", "disc_p": "O mesmo método serve a campos diferentes. Filtre para ver o que já foi pensado para o seu.",
  "disc": "Disciplina", "path": "Trilha", "planned_word": "planejada", "how": "Como funciona", "authors_h": "Autores", "cite": "Como citar",
  "copied": "Copiado", "install": "Instalação", "validation": "Validação",
  "factsheet": "Ficha", "links": "Links", "keywords": "Palavras-chave",
  "features": "Recursos", "stack": "Stack", "stage": "Etapa",
  "identifier": "Identificador", "version": "Versão", "maturity": "Maturidade",
  "status": "Status", "licence": "Licença", "doi_version": "DOI (versão)",
  "doi_concept": "DOI (conceito)", "added": "Adicionada em",
  "no_doi": "Sem DOI registrado. O campo fica vazio em vez de carregar um marcador.",
  "no_repo": "Ainda sem repositório público.",
  "levels_h": "Níveis de maturidade — evidência, não aspiração",
  "levels_p": "Um nível só é concedido com o artefato que o justifica. Testes verdes provam "
              "estrutura, não um método. Revisão por pares e replicação são processos sociais "
              "com registro próprio.",
  "lvl_exp": "Funciona na máquina do autor. Sem evidência independente.",
  "lvl_test": "Testes automatizados passam em ambiente registrado (tests/RESULTS.md).",
  "lvl_peer": "Dois pareceristas nomeados aplicaram a política editorial; veredictos em reviews/.",
  "lvl_repl": "Reexecutada por não-autor com relatório publicado.",
  "stages_h": "Etapas da pesquisa",
  "stages_p": "Cada skill declara a etapa metodológica que atende. A cor do card identifica a etapa.",
  "foot_note": "Código e documentação originais: MIT · sem rastreamento, sem cookies",
  "attrib": "Ícones: Zotero (marca da Corporation for Digital Scholarship) e Hermes Agent "
            "(Nous Research), usados apenas para indicar integração.",
  "val_note": "A validação estrutural prova conformidade com a especificação Agent Skills e a "
              "completude do pacote. Não prova que o método está correto. Evidência do nível de "
              "maturidade desta skill:",
  "not_recorded": "não registrada", "hub": "Hub",
  "authors_note": "ORCIDs entram apenas quando cada autor os fornece; nenhum é inventado.",
  "nav_contribute": "Contribuir", "contrib_h": "Contribuir com uma skill",
  "contrib_p": "Uma skill aqui é um pacote que descreve um método de pesquisa, roda testes e pode ser citado. Para propor uma, você não precisa escrever código sozinho: preencha o brief e entregue ao seu agente — o protocolo SS-0000 faz o resto.",
  "contrib_step1": "Baixe o brief", "contrib_step1d": "Um arquivo Markdown com as perguntas que definem a skill: tarefa, fonte de dados, limites, evidência e autoria.",
  "contrib_step2": "Preencha com o seu agente", "contrib_step2d": "O brief tem, no fim, as instruções ao agente. Campo vazio é pergunta a fazer, não lacuna a inventar.",
  "contrib_step3": "Abra uma proposta", "contrib_step3d": "Envie o diretório resultante num pull request. A revisão olha o método e a evidência, não a popularidade.",
  "contrib_download": "Baixar o brief (.md)", "contrib_guide": "Ler o guia de contribuição",
  "contrib_reqs": "O que a revisão verifica", "contrib_req1": "A skill declara a etapa da pesquisa e a disciplina a que serve.",
  "contrib_req2": "Todo requisito de execução está listado: credencial, variável de ambiente, software.",
  "contrib_req3": "Existe seção de limites: o que a skill não faz e o que ela não prova.",
  "contrib_req4": "Os testes rodam offline e `tests/RESULTS.md` traz ambiente e saída reais.",
  "contrib_req5": "Nenhuma credencial, caminho local ou dado pessoal no pacote.",
  "contrib_contact": "Contato", "contrib_contact_p": "Para propor uma skill, relatar um problema ou pedir acesso:",
  "contrib_email": "Escrever para o laboratório",
  "planned_summary": "Em desenvolvimento. Entra no ar com testes, licença e DOI quando aprovada.",
  "col_name": "Nome", "col_aff": "Afiliação", "copy": "Copiar citação",
  "copy_email": "Copiar endereço", "copy_fail": "Selecione e copie",
  "conc_h": "Antes do catálogo: modelo, agente, skill e ferramenta",
  "conc_lede": "São quatro coisas diferentes, e a diferença é o que dá sentido ao que está publicado aqui. Quem vem das humanidades lê “skill” como habilidade; quem vem da computação lê como prompt ou plugin. Nenhuma das duas leituras descreve um pacote deste catálogo.",
  "conc_m": "Modelo", "conc_m_tag": "capacidade",
  "conc_m_d": "O motor de linguagem: recebe texto e devolve texto. Sozinho, não guarda o trabalho, não consulta documento nem executa ação.",
  "conc_a": "Agente", "conc_a_tag": "ciclo",
  "conc_a_d": "Sistema que usa o modelo para perseguir um objetivo: interpreta a instrução, decide o próximo passo, chama ferramentas, lê o resultado e verifica se a tarefa foi cumprida. O modelo produz respostas; o agente organiza um ciclo de percepção, decisão, ação e verificação.",
  "conc_s": "Skill", "conc_s_tag": "método",
  "conc_s_d": "Pacote reutilizável e versionado de conhecimento e procedimento que ensina um agente a executar uma tarefa delimitada — instruções, critérios de decisão, referências, scripts, testes e limites. Não age sozinha. Não é prompt (uma frase) nem plugin (código instalável): é método escrito para ser seguido.",
  "conc_t": "Ferramenta", "conc_t_tag": "meio",
  "conc_t_d": "O recurso pelo qual a ação é efetivamente realizada: uma API, um programa, um navegador, uma base de dados. A ferramenta torna a ação possível; a skill estabelece quando, como e sob quais limites utilizá-la.",
  "sci_h": "O que é uma skill científica",
  "sci_p": "Aqui, uma skill científica é um método de pesquisa tornado operacional, inspecionável e auditável. Cada pacote explicita — e o nome da seção correspondente aparece entre parênteses:",
  "sci_1": "o problema que resolve e quando o agente deve usá-la (<i>When to use</i>);",
  "sci_2": "os requisitos e os limites de execução (<i>Requirements</i>, <i>Tools and dependencies</i>);",
  "sci_3": "a sequência de procedimentos e os critérios de parada (<i>Procedure</i>, <i>Stop criteria</i>);",
  "sci_4": "as fontes e referências que a fundamentam (<i>References</i>);",
  "sci_5": "os testes e a evidência de funcionamento, com ambiente registrado (<i>Validation</i>, <code>tests/RESULTS.md</code>);",
  "sci_6": "os limites epistemológicos — o que ela não faz e não prova — e, quando o dado envolve pessoas, os cuidados éticos e legais (<i>Limits</i>);",
  "sci_7": "versão, licença, autoria e forma de citação (ficha da skill, <code>CITATION.cff</code>).",
  "sci_note": "Isso não torna o método automático, nem os resultados verdadeiros por definição: a skill organiza a execução e deixa as escolhas examináveis; a interpretação e a validação seguem humanas.",
  "flow_1": "O pesquisador formula o problema",
  "flow_2": "O agente mobiliza a skill",
  "flow_3": "A skill orienta o uso das ferramentas",
  "flow_4": "Resultados e evidências são produzidos",
  "flow_5": "O pesquisador interpreta e valida",
  "conc_quote": "Skills não substituem métodos científicos: tornam partes desses métodos executáveis, verificáveis e reutilizáveis por agentes de IA.",
  "pending_lic": "licença pendente",
 },
 "en": {
  "switch": "Português", "nav_home": "Home", "nav_skills": "Skills", "nav_stages": "Stages",
  "nav_levels": "Maturity", "nav_submit": "Submit",
  "available": "available", "planned": "planned", "with_doi": "with DOI", "authors": "authors",
  "search": "Search skills, keywords, authors…", "all_status": "All statuses",
  "all_maturity": "All maturity levels", "all_stages": "All stages",
  "empty": "No skill matches these filters.", "view": "View details",
  "objective": "Objective", "req_h": "Requirements",
  "req_intro": "What you must have before running this skill. Everything required appears here — credentials included.",
  "req_required": "Required", "req_optional": "Optional", "req_env": "Environment variable",
  "req_what": "What it is", "req_how": "How to get it", "req_note": "Careful",
  "req_secret": "credential", "req_software": "software", "req_id": "identifier", "req_choice": "setting",
  "req_none": "No requirement beyond the package itself.",
  "nav_paths": "Paths", "all_disc": "All disciplines",
  "paths_h": "Research paths",
  "paths_p": "Work sequences that chain skills in the order research actually happens — not an isolated piece, the whole path.",
  "path_skills": "skills", "path_open": "Open the path",
  "disc_h": "Disciplines", "disc_p": "The same method serves different fields. Filter to see what was already designed for yours.",
  "disc": "Discipline", "path": "Path", "planned_word": "planned", "how": "How it works", "authors_h": "Authors", "cite": "How to cite",
  "copied": "Copied", "install": "Installation", "validation": "Validation",
  "factsheet": "Factsheet", "links": "Links", "keywords": "Keywords",
  "features": "Features", "stack": "Stack", "stage": "Stage",
  "identifier": "Identifier", "version": "Version", "maturity": "Maturity",
  "status": "Status", "licence": "Licence", "doi_version": "DOI (version)",
  "doi_concept": "DOI (concept)", "added": "Added",
  "no_doi": "No DOI registered yet. The field stays empty rather than carrying a placeholder.",
  "no_repo": "No public repository yet.",
  "levels_h": "Maturity levels — evidence, not aspiration",
  "levels_p": "A level is granted only with the artefact that justifies it. Green tests prove "
              "structure; they do not prove a method. Peer review and replication are social "
              "processes with their own records.",
  "lvl_exp": "Works on the author's machine. No independent evidence.",
  "lvl_test": "Automated tests pass in a recorded environment (tests/RESULTS.md).",
  "lvl_peer": "Two named reviewers applied the editorial policy; verdicts in reviews/.",
  "lvl_repl": "Re-executed by a non-author with a published report.",
  "stages_h": "Research stages",
  "stages_p": "Each skill declares the methodological stage it serves. Card colour identifies it.",
  "foot_note": "Original code and documentation: MIT · no tracking, no cookies",
  "attrib": "Icons: Zotero (trademark of the Corporation for Digital Scholarship) and Hermes "
            "Agent (Nous Research), used only to indicate integration.",
  "val_note": "Structural validation proves conformance to the Agent Skills specification and the "
              "completeness of the package. It does not prove that the method is correct. Evidence "
              "for this skill's maturity level:",
  "not_recorded": "not recorded", "hub": "Hub",
  "authors_note": "ORCIDs are included only when each author supplies them; none is invented.",
  "nav_contribute": "Contribute", "contrib_h": "Contribute a skill",
  "contrib_p": "A skill here is a package that describes a research method, runs tests and can be cited. To propose one you do not need to write code alone: fill the brief and hand it to your agent — the SS-0000 protocol does the rest.",
  "contrib_step1": "Download the brief", "contrib_step1d": "A Markdown file with the questions that define the skill: task, data source, limits, evidence and authorship.",
  "contrib_step2": "Fill it with your agent", "contrib_step2d": "The brief ends with instructions to the agent. An empty field is a question to ask, not a gap to invent.",
  "contrib_step3": "Open a proposal", "contrib_step3d": "Send the resulting directory as a pull request. Review looks at the method and the evidence, not at popularity.",
  "contrib_download": "Download the brief (.md)", "contrib_guide": "Read the contribution guide",
  "contrib_reqs": "What review checks", "contrib_req1": "The skill declares its research stage and the discipline it serves.",
  "contrib_req2": "Every execution requirement is listed: credential, environment variable, software.",
  "contrib_req3": "A limits section exists: what the skill does not do and does not prove.",
  "contrib_req4": "Tests run offline and `tests/RESULTS.md` carries the real environment and output.",
  "contrib_req5": "No credential, local path or personal data in the package.",
  "contrib_contact": "Contact", "contrib_contact_p": "To propose a skill, report a problem or request access:",
  "contrib_email": "Write to the laboratory",
  "planned_summary": "In development. It ships with tests, a licence and a DOI once approved.",
  "col_name": "Name", "col_aff": "Affiliation", "copy": "Copy citation",
  "copy_email": "Copy address", "copy_fail": "Select and copy",
  "conc_h": "Before the catalogue: model, agent, skill and tool",
  "conc_lede": "Four different things, and the difference is what gives meaning to what is published here. Readers from the humanities hear “skill” as an ability; readers from computing hear prompt or plugin. Neither reading describes a package in this catalogue.",
  "conc_m": "Model", "conc_m_tag": "capacity",
  "conc_m_d": "The language engine: it takes text in and gives text out. On its own it keeps no record of the work, opens no document and performs no action.",
  "conc_a": "Agent", "conc_a_tag": "cycle",
  "conc_a_d": "A system that uses the model to pursue a goal: it reads the instruction, decides the next step, calls tools, reads the result and checks whether the task was completed. The model produces answers; the agent runs a cycle of perception, decision, action and verification.",
  "conc_s": "Skill", "conc_s_tag": "method",
  "conc_s_d": "A reusable, versioned package of knowledge and procedure that teaches an agent to carry out a bounded task — instructions, decision criteria, references, scripts, tests and limits. It does not act on its own. It is neither a prompt (one sentence) nor a plugin (installable code): it is a method written to be followed.",
  "conc_t": "Tool", "conc_t_tag": "means",
  "conc_t_d": "The resource through which the action is actually carried out: an API, a program, a browser, a database. The tool makes the action possible; the skill sets when, how and within which limits to use it.",
  "sci_h": "What a scientific skill is here",
  "sci_p": "A scientific skill is a research method made operational, inspectable and auditable. Each package states — the matching section name appears in brackets:",
  "sci_1": "the problem it solves and when the agent should use it (<i>When to use</i>);",
  "sci_2": "the requirements and execution limits (<i>Requirements</i>, <i>Tools and dependencies</i>);",
  "sci_3": "the procedure and its stop criteria (<i>Procedure</i>, <i>Stop criteria</i>);",
  "sci_4": "the sources and references behind it (<i>References</i>);",
  "sci_5": "the tests and the evidence that it works, with the environment recorded (<i>Validation</i>, <code>tests/RESULTS.md</code>);",
  "sci_6": "its epistemological limits — what it does not do and does not prove — and, where data involve people, the ethical and legal safeguards (<i>Limits</i>);",
  "sci_7": "version, licence, authorship and how to cite (skill factsheet, <code>CITATION.cff</code>).",
  "sci_note": "This does not make the method automatic, nor its results true by definition: the skill organises execution and leaves its choices examinable; interpretation and validation remain human.",
  "flow_1": "The researcher frames the problem",
  "flow_2": "The agent loads the skill",
  "flow_3": "The skill governs how tools are used",
  "flow_4": "Results and evidence are produced",
  "flow_5": "The researcher interprets and validates",
  "conc_quote": "Skills do not replace scientific methods: they make parts of those methods executable, verifiable and reusable by AI agents.",
  "pending_lic": "licence pending",
 },
}

# Strings added in the 2026-11 portal revision. Kept as an overlay so the older
# vocabulary (requirements, paths, maturity) stays in one place during the transition.
T_EXTRA = {
 "pt": {
  "skip": "Pular para o conteúdo",
  "hub": "Início",
  "nav_catalogue": "Catálogo", "nav_using": "Como usar", "nav_evidence": "Evidências",
  "nav_about": "Sobre", "nav_skills": "Catálogo",
  "hero_cta_explore": "Explorar skills", "hero_cta_using": "Como utilizar",
  "hero_cta_contribute": "Contribuir com uma skill", "hero_repo": "Repositório no GitHub",
  "hero_initiative": "Iniciativa Métodos Digitais",
  "hero_note": "A iniciativa busca ampliar a transparência e a reutilização de procedimentos de pesquisa assistida por IA, preservando a responsabilidade científica humana. Nem toda skill é validada, replicada ou possui DOI: cada registro declara o que tem.",
  "hero_panel_h": "Por onde começar",
  "hero_panel_1": "Entenda o vocabulário",
  "hero_panel_1d": "Modelo, agente, skill e ferramenta, e o que torna uma skill científica.",
  "hero_panel_2": "Instale e verifique",
  "hero_panel_2d": "Do clone à confirmação de que o agente reconheceu a skill.",
  "hero_panel_3": "Leia as evidências",
  "hero_panel_3d": "Seis dimensões independentes, com o que cada pacote registra.",
  "stat_available": "Pacotes disponíveis", "stat_planned": "No roadmap",
  "stat_doi": "Com DOI", "stat_authors": "Autores",
  "stat_available_def": "Pacote com versão publicada e documentação de uso.",
  "stat_planned_def": "Registro de escopo; não é pacote publicado.",
  "stat_doi_def": "Pacote com registro arquivado e identificador persistente.",
  "stat_authors_def": "Pessoas com autoria registrada em ao menos um pacote.",
  "stats_note": "Contadores derivados do catálogo. DOI identifica um registro; não certifica qualidade científica.",
  "skills_intro": "Pacotes disponíveis e registros de roadmap. Filtre por tipo, etapa, disciplina ou evidência; a busca ignora maiúsculas e acentos.",
  "roadmap_h": "Roadmap: skills planejadas", "roadmap_badge": "Roadmap",
  "roadmap_p": "Registros de escopo, não pacotes publicados. Não há versão, DOI, citação de software ou evidência de execução; etapa e disciplinas são as previstas no registro.",
  "roadmap_none": "Escopo ainda não documentado publicamente. O registro indica etapa e disciplinas previstas; não há versão, DOI ou evidência de execução.",
  "roadmap_open": "Ver registro de roadmap",
  "roadmap_note": "Registros de roadmap não são pacotes publicados e não devem ser citados como software.",
  "type": "Tipo", "type_methodological": "Metodológica",
  "type_infrastructure": "Infraestrutura e gestão", "type_meta": "Meta-skill",
  "type_note": "Classificação editorial preliminar, sujeita a revisão pelos autores.",
  "filters_clear": "Limpar filtros", "results": "resultados", "all_types": "Todos os tipos",
  "evidence_recorded": "Registrado", "evidence_not": "Não registrado",
  "evidence_h": "Evidências", "evidence_intro": "O que este pacote registra publicamente, por dimensão. Registro não é o mesmo que qualidade científica.",
  "limits_h": "Limites", "install_h": "Instalação e ativação",
  "install_verify_h": "Verificar a ativação",
  "install_s1": "Copie o diretório do pacote para a pasta de skills do seu agente.",
  "install_s2": "Inicie uma sessão nova para que o agente releia as skills.",
  "install_s3": "Confirme que a skill aparece na lista do ambiente antes de usá-la.",
  "install_s4": "Só então peça a tarefa, com o escopo e as permissões que você concedeu.",
  "install_hermes": "No Hermes Agent: <code>hermes skills list</code> e, na sessão, <code>/skill &lt;nome&gt;</code>.",
  "install_claude": "No Claude Code: o nome do diretório vira o comando <code>/nome</code>.",
  "install_guide": "Guia passo a passo, com verificação de ativação",
  "when_h": "O que resolve", "package_links_h": "Links do pacote",
  "package_skill": "SKILL.md (procedimento)", "package_readme": "README (uso)",
  "package_tests": "Resultados dos testes", "package_license": "Licença",
  "package_citation": "CITATION.cff", "package_changelog": "Histórico de versões",
  "cite_bibtex": "BibTeX", "copy_bibtex": "Copiar BibTeX",
  "copy_cite": "Copiar citação", "cite_h": "Como citar",
  "cite_note": "O DOI de versão identifica a execução; o DOI de conceito reúne as versões.",
  "roadmap_notice": "Este é um registro de roadmap, não um pacote publicado. Não há versão, DOI, citação de software, instalação ou evidência de execução.",
  "roadmap_documented": "O que está documentado",
  "roadmap_paths": "Trilhas previstas", "roadmap_deps": "Dependências previstas",
  "roadmap_deps_none": "Não documentadas publicamente.",
  "concepts_more": "Entenda modelo, agente, skill e ferramenta",
  "concepts_short_h": "Quatro palavras que o catálogo pressupõe",
  "concepts_short_p": "Modelo, agente, skill e ferramenta não são sinônimos. A diferença é o que dá sentido ao que está publicado aqui.",
  "conc_m_s": "O motor que interpreta e gera linguagem. Sozinho, não guarda o trabalho nem executa ações.",
  "conc_a_s": "O sistema que coordena um ciclo de decisão, ação e verificação, com ferramentas e estado.",
  "conc_s_s": "O pacote versionado que orienta o agente em uma tarefa delimitada, com critérios, testes e limites.",
  "conc_t_s": "A API, o programa ou a base que efetivamente executa a operação.",
  "evidence_teaser_h": "Evidências e maturidade",
  "evidence_teaser_p": "Testes verdes não são revisão por pares. O catálogo separa seis dimensões de evidência e mostra o que cada pacote registra.",
  "evidence_teaser_cta": "Ler as dimensões de evidência",
  "page_concepts_h": "Modelos, agentes, skills e ferramentas",
  "page_concepts_p": "O vocabulário mínimo para ler o catálogo sem confundir prompt, plugin, método e ferramenta.",
  "page_concepts_d": "Definições de LLM, agente, skill e ferramenta, o que é uma skill científica no ScholarSkills e o diagrama do ciclo de uso.",
  "page_using_h": "Como utilizar uma skill",
  "page_using_p": "Do clone à verificação de que o agente reconheceu a skill, sem confundir instalação com ativação.",
  "page_using_d": "Guia para obter, instalar, ativar, verificar e citar uma skill científica em agentes compatíveis com Agent Skills.",
  "page_evidence_h": "Evidências e maturidade",
  "page_evidence_p": "Seis dimensões independentes, com o que cada uma exige e o que o catálogo registra hoje.",
  "page_evidence_d": "Dimensões de evidência do ScholarSkills: conformidade estrutural, testes funcionais, avaliação metodológica, revisão por pares, reexecução e replicação.",
  "page_about_h": "Sobre o ScholarSkills",
  "page_about_p": "Escopo, equipe, governança, licenças, acessibilidade e como citar o projeto.",
  "page_about_d": "Informações institucionais e editoriais do ScholarSkills, iniciativa do LABHDUFBA.",
  "footer_policy": "Política editorial", "footer_registry": "Catálogo JSON",
  "footer_github": "GitHub", "footer_about": "Sobre", "footer_license": "Licença",
  "lang_aria": "Mudar para inglês", "menu_aria": "Navegação principal",
  "authors_short": "Autoria", "availability": "Disponibilidade",
  "path_available": "disponível", "path_planned": "planejada",
  "path_count": "{a} de {n} etapas disponíveis hoje",
  "path_filter": "Filtrar o catálogo por esta trilha",
  "skill_actions_repo": "Ver repositório", "skill_actions_path": "Ver pacote",
  "skill_actions_install": "Instalar", "skill_actions_cite": "Citar",
  "status_roadmap": "Roadmap", "evidence_axis": "Evidência",
  "no_install": "Este pacote não publica comandos de instalação.",
  "tested_note": "O ambiente, o comando e a saída estão em tests/RESULTS.md.",
 },
 "en": {
  "skip": "Skip to content",
  "hub": "Home",
  "nav_catalogue": "Catalogue", "nav_using": "Using", "nav_evidence": "Evidence",
  "nav_about": "About", "nav_skills": "Catalogue",
  "hero_cta_explore": "Browse skills", "hero_cta_using": "How to use",
  "hero_cta_contribute": "Contribute a skill", "hero_repo": "Repository on GitHub",
  "hero_initiative": "Métodos Digitais initiative",
  "hero_note": "The initiative seeks to broaden the transparency and reuse of AI-assisted research procedures while preserving human scientific responsibility. Not every skill is validated, replicated or has a DOI: each record states what it has.",
  "hero_panel_h": "Where to start",
  "hero_panel_1": "Understand the vocabulary",
  "hero_panel_1d": "Model, agent, skill and tool, and what makes a skill scientific.",
  "hero_panel_2": "Install and check",
  "hero_panel_2d": "From clone to confirming that the agent recognised the skill.",
  "hero_panel_3": "Read the evidence",
  "hero_panel_3d": "Six independent dimensions, with what each package records.",
  "stat_available": "Available packages", "stat_planned": "On the roadmap",
  "stat_doi": "With DOI", "stat_authors": "Authors",
  "stat_available_def": "Package with a published version and usage documentation.",
  "stat_planned_def": "Scope record; not a published package.",
  "stat_doi_def": "Package with an archived record and a persistent identifier.",
  "stat_authors_def": "People with authorship recorded in at least one package.",
  "stats_note": "Counters derived from the catalogue. A DOI identifies a record; it does not certify scientific quality.",
  "skills_intro": "Available packages and roadmap records. Filter by type, stage, discipline or evidence; search ignores case and accents.",
  "roadmap_h": "Roadmap: planned skills", "roadmap_badge": "Roadmap",
  "roadmap_p": "Scope records, not published packages. There is no version, DOI, software citation or execution evidence; stage and disciplines are those planned in the record.",
  "roadmap_none": "Scope not yet publicly documented. The record states the planned stage and disciplines; there is no version, DOI or execution evidence.",
  "roadmap_open": "View roadmap record",
  "roadmap_note": "Roadmap records are not published packages and must not be cited as software.",
  "type": "Type", "type_methodological": "Methodological",
  "type_infrastructure": "Research infrastructure", "type_meta": "Meta-skill",
  "type_note": "Preliminary editorial classification, subject to author review.",
  "filters_clear": "Clear filters", "results": "results", "all_types": "All types",
  "evidence_recorded": "Recorded", "evidence_not": "Not recorded",
  "evidence_h": "Evidence", "evidence_intro": "What this package records publicly, dimension by dimension. A record is not the same as scientific quality.",
  "limits_h": "Limits", "install_h": "Installation and activation",
  "install_verify_h": "Check activation",
  "install_s1": "Copy the package directory into your agent's skills folder.",
  "install_s2": "Start a new session so the agent re-reads its skills.",
  "install_s3": "Confirm the skill appears in the environment's list before using it.",
  "install_s4": "Only then ask for the task, within the scope and permissions you granted.",
  "install_hermes": "In Hermes Agent: <code>hermes skills list</code> and, in session, <code>/skill &lt;name&gt;</code>.",
  "install_claude": "In Claude Code: the directory name becomes the <code>/name</code> command.",
  "install_guide": "Step-by-step guide with activation check",
  "when_h": "What it solves", "package_links_h": "Package links",
  "package_skill": "SKILL.md (procedure)", "package_readme": "README (usage)",
  "package_tests": "Test results", "package_license": "Licence",
  "package_citation": "CITATION.cff", "package_changelog": "Changelog",
  "cite_bibtex": "BibTeX", "copy_bibtex": "Copy BibTeX",
  "copy_cite": "Copy citation", "cite_h": "How to cite",
  "cite_note": "The version DOI identifies the run; the concept DOI gathers the versions.",
  "roadmap_notice": "This is a roadmap record, not a published package. There is no version, DOI, software citation, installation or execution evidence.",
  "roadmap_documented": "What is documented",
  "roadmap_paths": "Planned paths", "roadmap_deps": "Planned dependencies",
  "roadmap_deps_none": "Not publicly documented.",
  "concepts_more": "Understand model, agent, skill and tool",
  "concepts_short_h": "Four words the catalogue assumes",
  "concepts_short_p": "Model, agent, skill and tool are not synonyms. The difference is what gives meaning to what is published here.",
  "conc_m_s": "The engine that interprets and generates language. On its own it keeps no record and performs no action.",
  "conc_a_s": "The system that coordinates a cycle of decision, action and verification, with tools and state.",
  "conc_s_s": "The versioned package that guides the agent through a bounded task, with criteria, tests and limits.",
  "conc_t_s": "The API, program or database that actually performs the operation.",
  "evidence_teaser_h": "Evidence and maturity",
  "evidence_teaser_p": "Green tests are not peer review. The catalogue separates six evidence dimensions and shows what each package records.",
  "evidence_teaser_cta": "Read the evidence dimensions",
  "page_concepts_h": "Models, agents, skills and tools",
  "page_concepts_p": "The minimum vocabulary for reading the catalogue without confusing prompt, plugin, method and tool.",
  "page_concepts_d": "Definitions of LLM, agent, skill and tool, what a scientific skill is in ScholarSkills, and the use-cycle diagram.",
  "page_using_h": "How to use a skill",
  "page_using_p": "From clone to checking that the agent recognised the skill, without confusing installation with activation.",
  "page_using_d": "A guide to obtaining, installing, activating, checking and citing a scientific skill in Agent Skills-compatible agents.",
  "page_evidence_h": "Evidence and maturity",
  "page_evidence_p": "Six independent dimensions, what each requires and what the catalogue records today.",
  "page_evidence_d": "ScholarSkills evidence dimensions: structural conformance, functional tests, methodological assessment, peer review, re-execution and replication.",
  "page_about_h": "About ScholarSkills",
  "page_about_p": "Scope, team, governance, licences, accessibility and how to cite the project.",
  "page_about_d": "Institutional and editorial information for ScholarSkills, a LABHDUFBA initiative.",
  "footer_policy": "Editorial policy", "footer_registry": "JSON catalogue",
  "footer_github": "GitHub", "footer_about": "About", "footer_license": "Licence",
  "lang_aria": "Switch to Portuguese", "menu_aria": "Main navigation",
  "authors_short": "Authorship", "availability": "Availability",
  "path_available": "available", "path_planned": "planned",
  "path_count": "{a} of {n} stages available today",
  "path_filter": "Filter the catalogue by this path",
  "skill_actions_repo": "View repository", "skill_actions_path": "View package",
  "skill_actions_install": "Install", "skill_actions_cite": "Cite",
  "status_roadmap": "Roadmap", "evidence_axis": "Evidence",
  "no_install": "This package publishes no installation commands.",
  "tested_note": "The environment, command and output are in tests/RESULTS.md.",
 },
}
for _lang, _vals in T_EXTRA.items():
    T[_lang].update(_vals)


def esc(v) -> str:
    return html.escape(str(v)) if v is not None else ""


def t(lang: str, key: str) -> str:
    return T[lang][key]


# Page slugs. Portuguese is the primary tree; English mirrors it under /en/.
# `contribuir.html` is preserved in English too: it is a public URL and must not break.
PAGES = {
    "home": ("index.html", "index.html"),
    "concepts": ("conceitos.html", "concepts.html"),
    "using": ("como-utilizar.html", "using.html"),
    "evidence": ("evidencias.html", "evidence.html"),
    "contribute": ("contribuir.html", "contribuir.html"),
    "about": ("sobre.html", "about.html"),
}


def site_root(hub: dict) -> str:
    return (hub.get("site_url") or "https://labhdufba.github.io/scholarskills/").rstrip("/") + "/"


def page_path(page: str, lang: str) -> str:
    pt, en = PAGES[page]
    if lang == "pt":
        return pt
    return "en/" + en


def skill_path(slug: str, lang: str) -> str:
    return f"skills/{slug}.html" if lang == "pt" else f"en/skills/{slug}.html"


def alt_path(page: str, lang: str, slug: str | None = None) -> str:
    """Path of the same page in the other language, relative to the current page's directory."""
    other = "en" if lang == "pt" else "pt"
    target = skill_path(slug, other) if page == "skill" else page_path(page, other)
    if page == "skill":
        return ("../" if lang == "pt" else "../../") + target
    return target if lang == "pt" else "../" + target


def canonical(page: str, lang: str, hub: dict, slug: str | None = None) -> str:
    target = skill_path(slug, lang) if page == "skill" else page_path(page, lang)
    return site_root(hub) + target


def norm(value: str) -> str:
    """Case- and accent-insensitive search key (NFD strips combining marks)."""
    text = unicodedata.normalize("NFD", str(value or ""))
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn").casefold().strip()


def unique_authors(reg: dict) -> list[dict]:
    seen, people = set(), []
    for person in (reg.get("hub", {}).get("authors") or []):
        key = norm(person.get("orcid") or person.get("name") or "")
        if key and key not in seen:
            seen.add(key)
            people.append(person)
    for s in reg.get("skills") or []:
        for person in (s.get("authors") or []):
            key = norm(person.get("orcid") or person.get("name") or "")
            if key and key not in seen:
                seen.add(key)
                people.append(person)
    return people


def type_label(value: str, lang: str) -> str:
    return t(lang, "type_" + (value or "methodological"))


def type_badge(value: str, lang: str) -> str:
    if not value:
        return ""
    return f'<span class="badge kind">{esc(type_label(value, lang))}</span>'


INK = {"#0072B2": "#0b4a70", "#009E73": "#0d6b52", "#8C6D00": "#5d4700", "#7B52AB": "#4e3374",
       "#CC79A7": "#8a3d68", "#D55E00": "#8c3d00", "#0891B2": "#075f75", "#4E5A6B": "#333d4a", "#B03030": "#7a2020", "#8B2E4A": "#6d2138"}


def stage_style(stage) -> str:
    if not stage:
        return 'style="--stage:#94a3b8;--stage-soft:#f1f5f9;--stage-ink:#475569"'
    return (f'style="--stage:{stage["color"]};--stage-soft:{stage["soft"]};'
            f'--stage-ink:{INK.get(stage["color"], "#333d4a")}"')


def badge(value, table) -> str:
    if not value:
        return '<span class="badge muted">&mdash;</span>'
    label, klass = table.get(value, (value, "muted"))
    return f'<span class="badge {klass}">{esc(label)}</span>'


def css() -> str:
    return """@font-face{font-family:'Heebo';font-style:normal;font-weight:400 600;
  font-display:swap;src:url('fonts/heebo.woff2') format('woff2');
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Signika';font-style:normal;font-weight:600 700;
  font-display:swap;src:url('fonts/signika.woff2') format('woff2');
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}

/* Métodos Digitais hub - no framework, no tracking, no build step.
   Colours: categorical palette (Okabe-Ito, colour-vision safe). Every stage ink was darkened
   until it reaches >=4.5:1 contrast on its own soft background (WCAG AA for body text). */
:root{
  /* LABHD design tokens — sampled from labhdufba.github.io: green-600 #16a34a, green-400 #4ade80,
     green-100 #bbf7d0, green-50 #f0fdf4; neutrals gray-900 #111827, gray-500 #6b7280,
     gray-200 #e5e7eb; deep badge green #0a1f0c. */
  --bg:#ffffff; --bg-soft:#f8faf9; --surface:#fff; --ink:#111827; --muted:#6b7280;
  --line:#e5e7eb;
  --brand:#16a34a; --brand-ink:#15803d; --brand-soft:#f0fdf4; --brand-line:#bbf7d0;
  --deep:#0a1f0c;
  --ok:#15803d; --ok-soft:#f0fdf4;
  --warn:#7a5300; --warn-soft:#fbf1dd;
  --bad:#9d2d2d; --bad-soft:#fbeaea;
  --radius:12px; --maxw:1120px;
  --font-head:'Signika',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --font-body:'Heebo',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{font-size:112.5%}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font:1rem/1.65 var(--font-body);
  -webkit-font-smoothing:antialiased}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
header.site{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;gap:16px;height:72px;flex-wrap:nowrap}
.brand{order:0;display:flex;align-items:center;gap:11px;font-family:var(--font-head);min-height:44px;
  font-weight:600;color:var(--ink);letter-spacing:-.01em;font-size:1.062rem}
.brand .mark{width:38px;height:38px;border-radius:50%;overflow:hidden;background:var(--deep);
  display:grid;place-items:center;flex:0 0 auto}
.brand .mark img{width:38px;height:38px;display:block;object-fit:cover}
.brand small{font-family:var(--font-body);font-weight:400;color:var(--muted);font-size:0.7812rem}
nav.site{margin-left:auto;display:flex;gap:22px;font-size:0.875rem;align-items:center}
nav.site a{color:var(--muted);display:inline-flex;align-items:center;min-height:44px}
nav.site a:hover{color:var(--ink)}
nav.site a.on{color:var(--brand-ink);font-weight:600}
header.site .lang{order:4}
header.site .theme-toggle{order:3}
header.site nav.site{order:2;margin-left:auto}
.lang .short{display:none}
.lang{border:1px solid var(--line);border-radius:6px;padding:5px 12px;font-size:0.8125rem;
  color:var(--ink);background:var(--surface);font-weight:600;min-height:44px;display:inline-flex;
  align-items:center}
.cta{font-size:0.8125rem;color:#fff !important;background:var(--brand-ink);border:1px solid var(--brand-ink);
  border-radius:6px;padding:10px 14px;font-weight:600;min-height:44px;display:inline-flex;
  align-items:center}
.cta:hover{background:var(--brand-ink);border-color:var(--brand-ink);text-decoration:none}
.lang:hover{border-color:var(--brand);text-decoration:none}
/* ---------- path bar (compact filters) ---------- */
.pathbar{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:6px 0 14px;
  padding:12px 14px;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--bg-soft)}
.pathbar-h{font-size:0.75rem;text-transform:uppercase;letter-spacing:.06em;
  font-weight:700;color:var(--muted);margin-right:4px}
.pathpill{display:inline-flex;align-items:center;gap:9px;font:inherit;font-size:0.8125rem;
  font-weight:600;color:var(--ink);background:var(--surface);border:1px solid var(--line);
  border-radius:999px;padding:6px 12px;cursor:pointer;line-height:1.25;min-height:44px}
.pathpill:hover{border-color:var(--brand);color:var(--brand-ink)}
.pathpill.on{background:var(--brand-soft);border-color:var(--brand-line);color:var(--brand-ink)}
.pathpill-chain{font-family:var(--mono);font-size:0.6875rem;color:var(--muted);
  letter-spacing:-.02em}
.pathpill.on .pathpill-chain{color:var(--brand-ink)}
@media(max-width:640px){
  .pathbar{padding:10px 12px;flex-wrap:nowrap;overflow-x:auto;gap:8px;
    scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .pathbar::-webkit-scrollbar{display:none}
  .pathbar-h{flex:0 0 auto}
  .pathpill{flex:0 0 auto;font-size:0.7813rem;padding:6px 11px;white-space:nowrap}
  .pathpill-chain{display:none}
}

/* ---------- theme toggle ---------- */
.theme-toggle{display:inline-grid;place-items:center;width:44px;height:44px;
  border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--ink);
  cursor:pointer;padding:0;flex:0 0 auto;line-height:1}
.theme-toggle:hover{border-color:var(--brand);color:var(--brand-ink)}
.theme-toggle svg{width:17px;height:17px;display:block}
.theme-toggle .i-sun{display:none}
html[data-theme=dark] .theme-toggle .i-sun{display:block}
html[data-theme=dark] .theme-toggle .i-moon{display:none}
@media(prefers-color-scheme:dark){
  html:not([data-theme=light]) .theme-toggle .i-sun{display:block}
  html:not([data-theme=light]) .theme-toggle .i-moon{display:none}
}
.hero{padding:58px 0 36px;border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,#ecfdf3 0%,#f7fdf9 55%,#fff 100%)}
.hero .eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:0.75rem;
  letter-spacing:.09em;text-transform:uppercase;color:var(--brand-ink);font-weight:700;
  background:#fff;border:1px solid var(--brand-line);border-radius:999px;
  padding:5px 12px;margin-bottom:16px}
.hero h1{margin:0 0 12px;font-family:var(--font-head);font-weight:700;
  font-size:clamp(30px,4vw,44px);line-height:1.12;letter-spacing:-.015em;color:#040404;
  text-wrap:balance}
.hero .lede{margin:0;max-width:60ch;color:var(--muted);font-size:1.125rem;line-height:1.55;
  text-wrap:pretty}
.hero .desc{margin:16px 0 0;max-width:74ch;color:var(--muted);font-size:0.9062rem}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 18px;
  flex:1 1 0;min-width:140px}
.stat b{display:block;font-size:1.375rem;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat span{font-size:0.7188rem;color:var(--muted);text-transform:uppercase;letter-spacing:.07em}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:26px 0 6px}
.toolbar input,.toolbar select{font:inherit;font-size:0.875rem;padding:9px 12px;border:1px solid var(--line);
  border-radius:10px;background:var(--surface);color:var(--ink);min-width:170px}
.toolbar input{flex:1 1 300px;max-width:420px}
.toolbar input:focus,.toolbar select:focus{outline:2px solid var(--brand-soft);border-color:var(--brand)}
.count{margin-left:auto;font-size:0.8125rem;color:var(--muted);font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px;
  padding:10px 0 56px;min-width:0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  display:flex;flex-direction:column;min-width:0;overflow:hidden;
  transition:box-shadow .16s ease,border-color .16s ease,transform .16s ease}
.card:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(10,31,12,.07);
  border-color:var(--brand-line)}
.card .bar{height:4px;background:var(--stage)}
.card .inner{padding:20px 22px 18px;display:flex;flex-direction:column;gap:11px;flex:1}
.card .top{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.code{font-family:var(--mono);font-size:0.7188rem;color:#5b6472;background:#f3f5f9;
  border:1px solid var(--line);border-radius:6px;padding:2px 7px}
.card h3{margin:0;font-family:var(--font-head);font-weight:600;font-size:1.094rem;
  line-height:1.32;letter-spacing:-.005em}
.card h3 a{color:var(--ink);display:inline-flex;align-items:center;min-height:44px}
.card p{margin:0;color:var(--muted);font-size:0.875rem}
.card .feats{display:flex;flex-wrap:wrap;gap:6px}
.feat{font-size:0.7188rem;padding:3px 9px;border-radius:999px;background:var(--stage-soft,var(--brand-soft));
  color:var(--stage-ink,var(--brand-ink));font-weight:600}
.card .stack{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding-top:10px;
  border-top:1px dashed var(--line);margin-top:auto}
.stack{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.stack .chip{display:flex;align-items:center;gap:6px;font-size:0.7188rem;color:var(--muted);
  background:var(--bg-soft);border:1px solid var(--line);border-radius:999px;padding:3px 9px 3px 4px}
.stack .chip img{width:22px;height:22px;border-radius:6px;display:block;
  object-fit:cover;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.08) inset}
.card[data-status="planned"] .stack .chip{opacity:.62}
.stack .chip b{font-weight:600;color:var(--ink)}
.card .foot{display:flex;align-items:center;gap:8px;font-size:0.7812rem;color:var(--muted);flex-wrap:wrap}
.card .foot .arrow{margin-left:auto}
.card .foot .arrow a{font-weight:650;color:var(--stage-ink);display:inline-flex;
  align-items:center;min-height:44px;padding:0 2px}
.authors{font-size:0.7812rem;color:var(--muted)}
a.orcid{display:inline-flex;align-items:center;gap:6px;text-decoration:none;color:var(--brand-ink);min-height:44px;
  font-variant-numeric:tabular-nums;font-size:0.8125rem}
a.orcid:hover span{text-decoration:underline}
.author-grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));margin:18px 0 8px}
.author-card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;
  display:flex;flex-direction:column;gap:4px}
.author-name{font-weight:600;font-size:1rem;color:var(--ink)}
.author-role{font-size:0.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-ink)}
.author-aff{font-size:0.8125rem;color:var(--muted);margin-bottom:6px}
.sec-h{font-size:1.375rem;margin:34px 0 6px;color:var(--ink)}
.sec-p{color:var(--muted);font-size:0.9375rem;max-width:70ch;margin:0 0 6px}
.csteps{list-style:none;padding:0;margin:44px 0 0;display:grid;gap:14px}
.csteps li{margin:0}
.cstep{display:flex;gap:14px;align-items:flex-start;background:var(--surface);
  border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.cnum{flex:0 0 30px;height:30px;border-radius:50%;background:var(--brand-soft);color:var(--brand-ink);
  display:grid;place-items:center;font-weight:700;font-size:0.875rem;border:1px solid var(--brand-line)}
.cstep b{display:block;color:var(--ink);margin-bottom:2px}
.cstep p{margin:0;color:var(--muted);font-size:0.9375rem;max-width:72ch}
p code,td code,li code,.req-ex code,.creqs code{overflow-wrap:anywhere}
dd a.doi,dd .doi{overflow-wrap:normal;word-break:normal;font-variant-numeric:tabular-nums}
.cstep code{background:var(--bg-soft);border:1px solid var(--line);border-radius:4px;
  padding:1px 5px;font-size:0.875em;color:var(--ink)}
.creqs{margin:8px 0 18px;padding-left:20px;color:var(--ink)}
.creqs li{margin:6px 0;line-height:1.55}
.hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 0}
.contact-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:12px 0 0}
a.mail{display:inline-flex;align-items:center;gap:9px;min-height:45px;padding:10px 16px;
  border:1px solid var(--brand-line);border-radius:8px;background:var(--brand-soft);
  color:var(--brand-ink);font-weight:700;font-size:0.9375rem;text-decoration:none}
a.mail:hover{background:var(--brand-ink);color:#fff;border-color:var(--brand-ink);text-decoration:none}
a.mail svg{flex:0 0 auto}
.badge{font-size:0.6875rem;font-weight:650;padding:3px 9px;border-radius:999px;letter-spacing:.02em;
  border:1px solid transparent;white-space:nowrap}
.badge.ok{background:var(--ok-soft);color:var(--ok);border-color:var(--brand-line)}
.badge.warn{background:var(--warn-soft);color:var(--warn)}
.badge.accent{background:var(--brand-soft);color:var(--brand-ink);border-color:var(--brand-line)}
.badge.muted{background:#f3f5f9;color:#5b6472}
.badge.bad{background:var(--bad-soft);color:var(--bad)}
.badge.stage{background:var(--stage-soft);color:var(--stage-ink)}
.skill-head{padding:44px 0 26px;border-bottom:1px solid var(--line);position:relative}
.skill-head::before{content:"";position:absolute;inset:0 0 auto 0;height:4px;background:var(--stage)}
.crumbs{font-size:0.8125rem;color:var(--muted);margin-bottom:14px}
.crumbs a{color:var(--brand-ink);display:inline-flex;align-items:center;min-height:44px;
  margin-block:-11px;padding-inline:2px}
.crumbs .current{color:var(--ink);font-weight:550}
.skill-head h1{margin:0 0 12px;font-family:var(--font-head);font-weight:700;
  font-size:clamp(26px,3.4vw,38px);letter-spacing:-.015em;line-height:1.18;color:#040404}
.skill-head .sub{margin:0;max-width:70ch;color:var(--muted);font-size:1rem}
.meta-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:16px;font-size:0.8125rem;
  color:var(--muted)}
.cols{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:44px;padding:38px 0 72px}

/* ---------- requirements block ---------- */
.reqs{display:flex;flex-direction:column;gap:12px;margin:14px 0 4px}
.req{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:15px 16px;border-left:3px solid var(--line)}
.req.required{border-left-color:var(--stage,var(--brand))}
.req-top{display:flex;flex-direction:column;align-items:flex-start;gap:6px;margin-bottom:9px}
.req h3{font-size:0.9375rem;font-weight:600;margin:0;line-height:1.3}
.req-badges{display:flex;flex-wrap:wrap;gap:5px;align-items:center}
.badge.kind{background:#f3f4f6;color:#54606d;border-color:var(--line);text-transform:none;
  letter-spacing:0;font-weight:600}
code.env{font-family:var(--mono);font-size:0.7188rem;background:var(--stage-soft,#f3f4f6);
  color:var(--stage-ink,#374151);border:1px solid rgba(0,0,0,.05);padding:3px 7px;border-radius:5px}
.req p{margin:0 0 8px;font-size:0.875rem;line-height:1.55;color:var(--ink)}
.req p b{color:var(--stage-ink,var(--ink));font-weight:600}
.req p:last-child{margin-bottom:0}
.req-links{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 0}
.req-btn{font-size:0.7812rem;padding:7px 12px;border-color:var(--brand-line);
  background:var(--brand-soft);color:var(--brand-ink);font-weight:600}
.req-btn:hover{background:var(--brand-ink);color:#fff !important;border-color:var(--brand-ink)}
.req-btn.primary{background:var(--brand-ink);color:#fff !important;border-color:var(--brand-ink)}
.req-btn.primary:hover{background:#116635;border-color:#116635}
.req-ex{margin:10px 0 0;padding:10px 12px;background:#0f1712;color:#d6e6da;border-radius:6px;
  font-family:var(--mono);font-size:0.75rem;line-height:1.55;overflow-x:auto}
.req-ex code{font-family:inherit;background:none;border:none;padding:0;color:inherit}
.req-note{font-size:0.8125rem;color:var(--warn);background:var(--warn-soft);border-radius:6px;
  border-left:3px solid #d9a441;padding:9px 12px;margin-top:10px}
.req-note b{color:#8a5b00}


/* ---------- research paths ---------- */
.paths{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,400px),1fr));
  gap:16px;margin:16px 0 0}
.path{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:18px;border-top:3px solid var(--stage,var(--brand));min-width:0;
  display:flex;flex-direction:column;gap:10px}
.path h3{font-size:1.031rem;font-weight:600;line-height:1.32;color:var(--ink)}
.path p{margin:0;font-size:0.8438rem;color:var(--muted);line-height:1.5;
  min-height:3em}
.path-chain{display:flex;flex-direction:column;gap:6px;margin-top:2px;position:relative}
.path-skill{display:flex;align-items:baseline;gap:8px;font-size:0.8125rem;color:var(--ink);
  padding:7px 10px;border-radius:7px;background:var(--stage-soft,#f7f8f7);
  border:1px solid rgba(0,0,0,.04);line-height:1.35}
.path-skill:hover{text-decoration:none;border-color:var(--stage);color:var(--stage-ink)}
.path-skill .ps-step{flex:0 0 auto;width:18px;height:18px;border-radius:50%;
  background:var(--stage,var(--brand));color:#fff;font-size:0.6562rem;font-weight:700;
  display:grid;place-items:center;align-self:center}
.path-skill .ps-id{font-family:var(--mono);font-size:0.6562rem;color:var(--stage-ink);
  font-weight:600;flex:0 0 auto;opacity:.85}
.path-skill .ps-name{min-width:0}
.path-skill.plan{opacity:.72}
.ps-plan{flex:0 0 auto;margin-left:auto;font-size:0.5938rem;text-transform:uppercase;
  letter-spacing:.05em;font-weight:700;color:#4b5563;background:rgba(0,0,0,.06);
  padding:2px 6px;border-radius:4px}
.path-foot{font-size:0.7188rem;color:var(--muted);text-transform:uppercase;
  letter-spacing:.05em;font-weight:600;margin-top:auto}

@media(max-width:900px){.cols{grid-template-columns:1fr;gap:28px}}
h2.sec{font-size:0.7812rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);
  margin:34px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
h2.sec:first-child{margin-top:0}
.steps{margin:0;padding-left:22px}
.steps li{margin-bottom:10px}
pre{background:#101318;color:#e9edf3;padding:16px 18px;border-radius:12px;overflow:auto;
  font-family:var(--mono);font-size:0.8125rem;line-height:1.55}
blockquote{margin:0;padding:16px 20px;background:var(--brand-soft);border-left:3px solid var(--brand);
  border-radius:0 10px 10px 0;font-size:0.9062rem;color:#1d2b38}
table.authors-t{width:100%;border-collapse:collapse;font-size:0.875rem}
table.authors-t th{text-align:left;color:var(--muted);font-size:0.7188rem;text-transform:uppercase;
  letter-spacing:.07em;padding:8px 0;border-bottom:1px solid var(--line);font-weight:600}
table.authors-t td{padding:9px 0;border-bottom:1px solid var(--line);vertical-align:top}
aside .panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:20px;margin-bottom:16px}
aside .panel h4{margin:0 0 12px;font-size:0.7188rem;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted)}
dl.facts{margin:0;display:grid;grid-template-columns:auto 1fr;gap:9px 14px;font-size:0.8438rem}
dl.facts dt{color:var(--muted)}
dl.facts dt{color:var(--muted)}
dl.facts dd{margin:0;text-align:left;overflow-wrap:anywhere;line-height:1.45}
dl.facts dd .doi{font-size:0.8125rem;display:inline-flex;align-items:center;min-height:24px}
.btn{display:inline-block;padding:9px 15px;border-radius:6px;font-size:0.8438rem;font-weight:600;
  border:1px solid var(--line);color:var(--ink);background:var(--surface);cursor:pointer}
.btn:hover{border-color:var(--brand);color:var(--brand-ink);text-decoration:none}
.btn.primary{background:var(--brand-ink);border-color:var(--brand-ink);color:#fff !important;
  min-height:44px;display:inline-flex;align-items:center}
.btn.primary:hover{background:var(--brand);border-color:var(--brand);color:#fff !important}
.btn{min-height:44px;display:inline-flex;align-items:center}
.note{font-size:0.7812rem;color:var(--muted);margin-top:10px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
footer.site{border-top:1px solid var(--line);padding:30px 0 44px;font-size:0.7812rem;color:var(--muted)}
footer.site .wrap{display:flex;flex-direction:column;gap:8px}
.empty{padding:34px 0;color:var(--muted)}
.levels{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;padding-top:16px}
.stage-legend{display:flex;flex-wrap:wrap;gap:8px;padding:12px 0 0}
.stage-legend a{display:flex;align-items:center;gap:7px;font-size:0.7812rem;color:var(--muted);
  border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:5px 11px}
.stage-legend .dot{width:9px;height:9px;border-radius:50%;background:var(--c)}

/* ---------- page de skill: mesma linguagem do card ---------- */
.cols{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:40px;
  padding:32px 0 56px;align-items:start}
.cols>div{min-width:0}
.cols h2.sec{margin:30px 0 10px;font-size:1.125rem;font-weight:600;
  padding-bottom:7px;border-bottom:1px solid var(--line)}
.cols h2.sec:first-child{margin-top:0}
.crumbs{font-size:0.8125rem;color:var(--muted);margin-bottom:14px}
.crumbs a{color:var(--brand-ink);display:inline-flex;align-items:center;min-height:44px;
  margin-block:-11px;padding-inline:2px}
.crumbs .current{color:var(--ink);font-weight:600}
.skill-head{padding:34px 0 30px;border-bottom:1px solid var(--line);
  border-top:4px solid var(--stage,var(--line));
  background:linear-gradient(180deg,var(--stage-soft,#f8faf9) 0%,var(--bg) 94%)}
.skill-head h1{font-weight:700;font-size:clamp(1.5625rem,3.4vw,2.3125rem);line-height:1.18;
  color:#040404;margin:0 0 12px}
.skill-head .sub{margin:0;font-size:1.062rem;color:var(--muted);max-width:72ch;line-height:1.55}
.meta-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:16px;
  font-size:0.8125rem;color:var(--muted)}
dl.facts{margin:0}
dl.facts dt{font-size:0.7188rem;color:var(--muted);margin-top:9px}
dl.facts dt:first-child{margin-top:0}
dl.facts dd{margin:1px 0 0;font-size:0.8438rem;overflow-wrap:anywhere}
table.authors-t{width:100%;border-collapse:collapse;font-size:0.875rem;margin:0 0 8px}
table.authors-t th{text-align:left;font-size:0.75rem;text-transform:uppercase;letter-spacing:.05em;
  color:var(--muted);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--line)}
table.authors-t td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}
table.authors-t tr:last-child td{border-bottom:none}
ol.steps{margin:0 0 12px;padding-left:22px}
ol.steps li{margin:0 0 8px;line-height:1.55}
ol.steps li::marker{color:var(--stage-ink,var(--brand-ink));font-weight:700}
blockquote{margin:0 0 12px;padding:14px 16px;border-left:3px solid var(--stage,var(--brand));
  background:color-mix(in srgb, var(--stage-soft, var(--brand-soft)) 65%, var(--bg));
  border-radius:0 8px 8px 0;font-size:0.875rem;
  line-height:1.55;color:var(--ink)}
pre{margin:0 0 12px;padding:14px 16px;background:#0f1712;color:#d6e6da;border-radius:8px;
  font-family:var(--mono);font-size:0.7812rem;line-height:1.6;overflow-x:auto}
aside{display:flex;flex-direction:column;gap:14px;min-width:0}
.panel h4{font-size:0.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
  margin:0 0 12px;font-weight:700}
aside.side{position:sticky;top:80px;align-self:start}
.skill-head .stack{flex-wrap:wrap;gap:7px;align-items:center}
.skill-head .stack .chip{max-width:100%}
@media(max-width:900px){aside.side{position:static}}

@media(max-width:900px){
  .cols{grid-template-columns:1fr;gap:8px;padding:26px 0 44px}
  aside{order:2;margin-top:14px}
  .hero{padding:38px 0 28px}
  .hero .lede{font-size:1.031rem}
  .stat{padding:11px 13px;min-width:calc(50% - 8px)}
  header.site .wrap{height:auto;padding:8px 16px;flex-wrap:wrap;justify-content:space-between;gap:8px}
  nav.site{gap:0 12px;flex-wrap:wrap;justify-content:flex-start;width:100%;
    padding:0;overflow:visible;
    -webkit-mask-image:none;mask-image:none}
  nav.site::-webkit-scrollbar{display:none}
  nav.site a{min-height:40px;flex:0 0 auto}
  /* Order is declared here with the same specificity as the desktop rule, otherwise
     `header.site nav.site` wins and the menu lands on its own row between the controls. */
  header.site .brand{order:0}
  header.site .theme-toggle{order:1;margin-left:auto;margin-right:8px}
  header.site .lang{order:2;margin-left:0}
  header.site nav.site{order:3;margin-left:0;width:100%}
  nav.site a{font-size:0.75rem;white-space:nowrap;min-height:40px}
  nav.site a.cta{padding:5px 10px}
}
@media(max-width:430px){
  /* Tighter spacing well before the edge: the six items fit at 390 px even at the wider sizes,
     but with no slack at all, and a font fallback would push the last item past the viewport. */
  nav.site{gap:0 8px}
  nav.site a{font-size:0.7188rem}
  nav.site a.cta{padding:4px 8px}
}
@media(max-width:365px){
  /* At 320 px no spacing trick fits six items honestly: wrap to a second line instead of
     hiding the last one behind a scroll the reader has no reason to suspect. */
  nav.site{flex-wrap:wrap;overflow-x:visible;gap:0 10px;justify-content:center;
    -webkit-mask-image:none;mask-image:none}
  nav.site a{font-size:0.7188rem}
  .lang{padding:4px 9px;font-size:0.75rem}
  .lang .full{display:none}
  .lang .short{display:inline}

}
@media(max-width:560px){
  .wrap{padding:0 16px}
  .grid{grid-template-columns:1fr}
  .toolbar input[type=search]{flex:1 1 100%;max-width:none}
  .toolbar select{flex:1 1 calc(50% - 5px)}
  .toolbar .count{margin-left:0;width:100%}
  .brand .mark,.brand .mark img{width:30px;height:30px}
  .hero h1{font-size:1.625rem}
  .skill-head{padding:24px 0 22px}
  .skill-head h1{font-size:1.438rem}
  .skill-head .sub{font-size:0.9688rem}
  table.authors-t th,table.authors-t td{padding:8px 6px}
}

/* ---------- conceitos: modelo, agente, skill, ferramenta ---------- */
.concepts{padding-top:46px;padding-bottom:10px}
.conc-lede{max-width:78ch;color:var(--muted);font-size:0.9688rem;margin:6px 0 20px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:14px}
.ccard{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;display:flex;flex-direction:column;gap:7px;min-width:0}
.ccard h3{margin:0;font-family:var(--font-head);font-weight:600;font-size:1.0625rem;
  color:var(--ink);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ccard .what{font-size:0.6562rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  color:var(--brand-ink);background:var(--brand-soft);border:1px solid var(--brand-line);
  border-radius:999px;padding:2px 8px;white-space:nowrap}
.ccard p{margin:0;font-size:0.875rem;line-height:1.55;color:var(--muted)}
.sci{margin:26px 0 0;background:var(--bg-soft);border:1px solid var(--line);border-radius:14px;
  padding:20px 22px}
.sci h3{margin:0 0 6px;font-family:var(--font-head);font-weight:600;font-size:1.125rem;color:var(--ink)}
.sci p{margin:0;color:var(--muted);font-size:0.9375rem;line-height:1.55;max-width:82ch}
.slist{list-style:none;padding:0;margin:14px 0 0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:8px 26px}
.slist li{position:relative;padding-left:20px;font-size:0.875rem;line-height:1.5;color:var(--ink);
  overflow-wrap:anywhere}
.slist li::before{content:"";position:absolute;left:2px;top:.62em;width:8px;height:8px;
  border-radius:2px;background:var(--brand)}
.slist code{font-family:var(--mono);font-size:0.7812rem;background:var(--surface);
  border:1px solid var(--line);border-radius:4px;padding:1px 5px}
.sci .note{margin:14px 0 0;font-size:0.8438rem;color:var(--muted);max-width:none;
  border-top:1px dashed var(--line);padding-top:12px}
.flow{list-style:none;padding:0;margin:20px 0 0;display:grid;gap:10px;grid-template-columns:1fr}
.flow li{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:10px 12px;font-size:0.8125rem;line-height:1.4;color:var(--ink);min-width:0}
.flow .n{display:block;font-size:0.6562rem;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--brand-ink);margin-bottom:2px}
@media(min-width:900px){
  .flow{grid-template-columns:repeat(5,minmax(0,1fr))}
  .flow li{padding-right:20px}
  .flow li:not(:last-child)::after{content:"→";position:absolute;right:-9px;top:50%;
    transform:translateY(-50%);color:var(--muted);font-size:0.8125rem;line-height:1}
}
@media(max-width:899px){
  .flow li:not(:last-child)::after{content:"↓";position:absolute;left:50%;bottom:-11px;
    transform:translateX(-50%);color:var(--muted);font-size:0.8125rem;line-height:1;
    background:var(--bg);padding:0 3px}
}
.conc-quote{margin:20px 0 34px;padding:14px 18px;background:var(--brand-soft);
  border-left:4px solid var(--brand);border-radius:0 10px 10px 0;color:var(--ink);
  font-size:0.9688rem;line-height:1.5;font-weight:550}
@media(max-width:640px){.concepts{padding-top:34px;padding-bottom:6px}.sci{padding:16px 16px}}

/* tema escuro: padrão do sistema, sobreponível pelo botão de tema */
@media(prefers-color-scheme:dark){
html:not([data-theme=light]){--bg:#0b0f0c;--bg-soft:#0e1310;--surface:#141a15;--ink:#e9efe9;--muted:#9aa79c;
  --line:#26302a;--brand:#4ade80;--brand-ink:#86efac;--brand-soft:#12261a;
  --brand-line:#1f3b2a;--deep:#0a1f0c;--ok:#86efac;--ok-soft:#12261a;
  --warn:#e2c07a;--warn-soft:#2a2113;--bad:#e89292;--bad-soft:#2a1616}
html:not([data-theme=light]) .code{background:#1a211c;color:#c9d3cc}
html:not([data-theme=light]) .badge.muted{background:#1f2822;color:#c9d3cc;border-color:var(--line)}
/* In dark mode --brand-ink is light green: white on it measures 1.4:1. Ink text instead. */
html:not([data-theme=light]) .cta,
html:not([data-theme=light]) .btn.primary{background:var(--brand-ink);border-color:var(--brand-ink);color:#08130b !important}
html:not([data-theme=light]) .cta:hover,
html:not([data-theme=light]) .btn.primary:hover{background:var(--brand);border-color:var(--brand);color:#08130b !important}
html:not([data-theme=light]) header.site{background:rgba(11,15,12,.92)}
html:not([data-theme=light]) .hero{background:linear-gradient(180deg,#0f1a12 0%,var(--bg) 80%)}
html:not([data-theme=light]) .hero .eyebrow,html:not([data-theme=light]) .hero h1,html:not([data-theme=light]) .skill-head h1{color:var(--ink)}
html:not([data-theme=light]) .hero .eyebrow{background:#121a14}
html:not([data-theme=light]) blockquote{color:#cfe0d4}
html:not([data-theme=light]) .chip img{background:rgba(255,255,255,.07)}
html:not([data-theme=light]) blockquote{background:color-mix(in srgb, var(--stage-soft,#12261a) 14%, var(--bg))}
html:not([data-theme=light]) .badge.kind,html:not([data-theme=light]) .badge.muted{background:#1a211c;color:var(--muted)}
html:not([data-theme=light]) .code{background:#1a211c}
html:not([data-theme=light]) .req-note{color:var(--warn);background:var(--warn-soft)}
html:not([data-theme=light]) .req-note b{color:#f0d79a}
html:not([data-theme=light]) pre,html:not([data-theme=light]) .req-ex{background:#0a120d}
html:not([data-theme=light]) .stat,html:not([data-theme=light]) .panel,html:not([data-theme=light]) .req,html:not([data-theme=light]) .path{background:var(--surface)}
html:not([data-theme=light]) .skill-head{background:linear-gradient(180deg,
  color-mix(in srgb, var(--stage-soft,#12261a) 18%, var(--bg)) 0%,var(--bg) 92%)}
html:not([data-theme=light]) .badge.stage{background:color-mix(in srgb, var(--stage,#16a34a) 22%, var(--surface));
  color:color-mix(in srgb, var(--stage-ink,#374151) 55%, #ffffff);
  border-color:color-mix(in srgb, var(--stage,#16a34a) 45%, transparent)}
html:not([data-theme=light]) .feat,html:not([data-theme=light]) .path-skill,html:not([data-theme=light]) code.env{
  background:color-mix(in srgb, var(--stage-soft,#e5e7eb) 16%, var(--surface));
  color:color-mix(in srgb, var(--stage-ink,#374151) 28%, #eaf1eb);
  border-color:color-mix(in srgb, var(--stage,#16a34a) 26%, transparent)}
html:not([data-theme=light]) .path-skill .ps-id{color:color-mix(in srgb, var(--stage-ink,#374151) 45%, #cfe3d5)}
html:not([data-theme=light]) .path-skill:hover{background:color-mix(in srgb, var(--stage) 24%, var(--surface))}
html:not([data-theme=light]) .ps-plan{background:#1f2822;color:#c9d3cc}
html:not([data-theme=light]) .badge.accent,html:not([data-theme=light]) .badge.ok{background:var(--brand-soft);color:var(--brand-ink);
  border-color:var(--brand-line)}
html:not([data-theme=light]) .req-btn{background:color-mix(in srgb, var(--brand) 14%, var(--surface));
  color:var(--brand-ink);border-color:var(--brand-line)}
html:not([data-theme=light]) .card:hover{box-shadow:0 10px 24px rgba(0,0,0,.45)}
}
html[data-theme=dark]{--bg:#0b0f0c;--bg-soft:#0e1310;--surface:#141a15;--ink:#e9efe9;--muted:#9aa79c;
  --line:#26302a;--brand:#4ade80;--brand-ink:#86efac;--brand-soft:#12261a;
  --brand-line:#1f3b2a;--deep:#0a1f0c;--ok:#86efac;--ok-soft:#12261a;
  --warn:#e2c07a;--warn-soft:#2a2113;--bad:#e89292;--bad-soft:#2a1616}
html[data-theme=dark] .code{background:#1a211c;color:#c9d3cc}
html[data-theme=dark] .badge.muted{background:#1f2822;color:#c9d3cc;border-color:var(--line)}
html[data-theme=dark] header.site{background:rgba(11,15,12,.92)}
html[data-theme=dark] .hero{background:linear-gradient(180deg,#0f1a12 0%,var(--bg) 80%)}
html[data-theme=dark] .hero .eyebrow,html[data-theme=dark] .hero h1,html[data-theme=dark] .skill-head h1{color:var(--ink)}
html[data-theme=dark] .hero .eyebrow{background:#121a14}
html[data-theme=dark] blockquote{color:#cfe0d4}
html[data-theme=dark] .chip img{background:rgba(255,255,255,.07)}
html[data-theme=dark] blockquote{background:color-mix(in srgb, var(--stage-soft,#12261a) 14%, var(--bg))}
html[data-theme=dark] .badge.kind,html[data-theme=dark] .badge.muted{background:#1a211c;color:var(--muted)}
html[data-theme=dark] .code{background:#1a211c}
html[data-theme=dark] .req-note{color:var(--warn);background:var(--warn-soft)}
html[data-theme=dark] .req-note b{color:#f0d79a}
html[data-theme=dark] pre,html[data-theme=dark] .req-ex{background:#0a120d}
html[data-theme=dark] .stat,html[data-theme=dark] .panel,html[data-theme=dark] .req,html[data-theme=dark] .path{background:var(--surface)}
html[data-theme=dark] .skill-head{background:linear-gradient(180deg,
  color-mix(in srgb, var(--stage-soft,#12261a) 18%, var(--bg)) 0%,var(--bg) 92%)}
html[data-theme=dark] .badge.stage{background:color-mix(in srgb, var(--stage,#16a34a) 22%, var(--surface));
  color:color-mix(in srgb, var(--stage-ink,#374151) 55%, #ffffff);
  border-color:color-mix(in srgb, var(--stage,#16a34a) 45%, transparent)}
html[data-theme=dark] .feat,html[data-theme=dark] .path-skill,html[data-theme=dark] code.env{
  background:color-mix(in srgb, var(--stage-soft,#e5e7eb) 16%, var(--surface));
  color:color-mix(in srgb, var(--stage-ink,#374151) 28%, #eaf1eb);
  border-color:color-mix(in srgb, var(--stage,#16a34a) 26%, transparent)}
html[data-theme=dark] .path-skill .ps-id{color:color-mix(in srgb, var(--stage-ink,#374151) 45%, #cfe3d5)}
html[data-theme=dark] .path-skill:hover{background:color-mix(in srgb, var(--stage) 24%, var(--surface))}
html[data-theme=dark] .ps-plan{background:#1f2822;color:#c9d3cc}
html[data-theme=dark] .badge.accent,html[data-theme=dark] .badge.ok{background:var(--brand-soft);color:var(--brand-ink);
  border-color:var(--brand-line)}
html[data-theme=dark] .req-btn{background:color-mix(in srgb, var(--brand) 14%, var(--surface));
  color:var(--brand-ink);border-color:var(--brand-line)}
html[data-theme=dark] .card:hover{box-shadow:0 10px 24px rgba(0,0,0,.45)}
/* Same rule as the system-preference block: --brand-ink is light green in dark mode. */
html[data-theme=dark] .cta,
html[data-theme=dark] .btn.primary{background:var(--brand-ink);border-color:var(--brand-ink);color:#08130b !important}
html[data-theme=dark] .cta:hover,
html[data-theme=dark] .btn.primary:hover{background:var(--brand);border-color:var(--brand);color:#08130b !important}

/* ---------- 2026-11 revision: identity, long-form pages, roadmap, evidence ---------- */
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;border:0}
.skip-link{position:absolute;left:12px;top:-60px;z-index:100;background:var(--brand-ink);
  color:#fff;padding:10px 16px;border-radius:0 0 8px 8px;font-weight:600;text-decoration:none}
.skip-link:focus{top:0;color:#fff}
:focus-visible{outline:3px solid var(--brand-ink);outline-offset:3px}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,
summary:focus-visible{outline:3px solid var(--brand-ink);outline-offset:3px}
.brand-name{display:flex;flex-direction:column;line-height:1.1;gap:2px}
.brand-name small{font-size:0.6562rem;letter-spacing:.04em;text-transform:uppercase;
  color:var(--muted);font-weight:600;margin-top:3px}
.initiative{margin:0 0 6px;font-size:0.75rem;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--brand-ink)}
.hero-sub{margin:0 0 14px;font-family:var(--font-head);font-size:clamp(18px,2.1vw,24px);
  font-weight:600;color:var(--ink);line-height:1.3;max-width:60ch}
.hero .desc{max-width:72ch;margin-top:12px}
.hero-actions{align-items:center}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,.65fr);gap:44px;
  align-items:start}
.hero-panel{background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:20px 22px;box-shadow:0 8px 24px rgba(10,31,12,.05)}
.hero-panel h2{margin:0 0 12px;font-family:var(--font-head);font-size:1rem;color:var(--ink)}
.hero-panel ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.hero-panel li a{display:block;padding:9px 0;border-top:1px solid var(--line);color:var(--ink)}
.hero-panel li:first-child a{border-top:none;padding-top:0}
.hero-panel li b{display:block;font-size:0.875rem;color:var(--brand-ink)}
.hero-panel li span{display:block;font-size:0.8125rem;color:var(--muted);line-height:1.45;margin-top:2px}
.hero-panel .repo-link{margin-top:12px;font-size:0.75rem}
@media(max-width:1000px){.hero-grid{grid-template-columns:1fr;gap:24px}.hero-panel{display:none}}
.repo-link{font-size:0.8125rem;color:var(--brand-ink);font-weight:600;display:inline-flex;
  align-items:center;min-height:44px}
.stats-note{margin:12px 0 0;font-size:0.75rem;color:var(--muted);max-width:82ch}
.concepts-link{margin:16px 0 0}
.concepts{padding-top:38px;padding-bottom:4px}
.lede-p{max-width:80ch;color:var(--ink);font-size:1rem;margin:0 0 22px;line-height:1.62}
.page{padding-bottom:48px}
.page-head{padding:42px 0 18px;border-bottom:1px solid var(--line);margin-bottom:26px;max-width:76ch}
.page-head h1{margin:0 0 10px;font-family:var(--font-head);font-size:clamp(26px,3.4vw,38px);
  line-height:1.16;color:var(--ink);letter-spacing:-.01em}
.page-head .lede{margin:0;max-width:74ch;color:var(--muted);font-size:1.031rem;line-height:1.55}
.prose{max-width:76ch}
.prose a{overflow-wrap:anywhere}
.prose h3{margin:26px 0 6px;font-family:var(--font-head);font-size:1.0938rem;color:var(--ink)}
.prose p{margin:0 0 12px;line-height:1.62}
.prose ul{margin:0 0 14px;padding-left:20px}
.prose li{margin:0 0 7px;line-height:1.55}
.callout{margin:18px 0;padding:14px 18px;background:var(--brand-soft);border-left:4px solid var(--brand);
  border-radius:0 8px 8px 0;color:var(--ink);font-size:0.9375rem;line-height:1.55;max-width:80ch}
.example-box{background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;max-width:80ch;margin:10px 0 24px}
.example-box p{margin:0 0 8px}
.page-back{margin:30px 0 0}
.page-back a{font-weight:600}
.diagram-figure{margin:26px 0 30px;padding:16px;background:var(--surface);border:1px solid var(--line);
  border-radius:14px}
.diagram-figure figcaption{margin-top:10px;font-size:0.8125rem;color:var(--muted);max-width:82ch}
.dg{display:block;width:100%;height:auto}
.dg-tall{display:none}
.dg-box rect{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.dg-box.dg-skill rect{fill:var(--brand-soft);stroke:var(--brand);stroke-width:2}
.dg-box.dg-agent rect{fill:var(--bg-soft);stroke:var(--brand-line)}
.dg-h{font:600 16px var(--font-head);fill:var(--ink)}
.dg-t{font:13px var(--font-body);fill:var(--muted)}
.dg-small{font-size:11px}
.dg-line path{fill:none;stroke:var(--muted);stroke-width:1.5}
.dg-label text{font:11px var(--font-body);fill:var(--muted)}
.dg-head{fill:var(--muted)}
@media(max-width:700px){
  .dg-wide{display:none}
  .dg-tall{display:block}
}
.dims{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:14px;
  margin:18px 0 10px}
.dim{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.dim h3{margin:0 0 6px;font-family:var(--font-head);font-size:1rem;color:var(--ink)}
.dim p{margin:0;font-size:0.8438rem;color:var(--muted);line-height:1.5}
.table-wrap{overflow-x:auto;margin:14px 0 28px;border:1px solid var(--line);border-radius:12px}
.evidence-table{width:100%;border-collapse:collapse;font-size:0.8125rem;min-width:760px}
.evidence-table th,.evidence-table td{padding:10px 12px;border-bottom:1px solid var(--line);
  text-align:left;vertical-align:top}
.evidence-table thead th{background:var(--bg-soft);font-size:0.6875rem;text-transform:uppercase;
  letter-spacing:.05em;color:var(--muted);position:sticky;top:0}
.evidence-table tbody th{font-weight:500;min-width:260px}
.evidence-table tbody th a{color:var(--ink);display:inline-flex;gap:7px;align-items:baseline}
.evidence-table tr:last-child th,.evidence-table tr:last-child td{border-bottom:none}
.ev{display:inline-block;font-size:0.6875rem;font-weight:700;padding:3px 8px;border-radius:999px;
  border:1px solid transparent;white-space:nowrap}
.ev.yes{background:var(--ok-soft);color:var(--ok);border-color:var(--brand-line)}
.ev.no{background:#f3f5f9;color:#5b6472}
html[data-theme=dark] .ev.no,html:not([data-theme=light]) .ev.no{background:#1a211c;color:var(--muted)}
.roadmap{margin:10px 0 34px;padding:26px 24px 20px;background:var(--bg-soft);
  border:1px solid var(--line);border-radius:16px}
.roadmap .grid{padding-bottom:8px}
.card.plan{border-style:dashed;background:color-mix(in srgb, var(--surface) 88%, var(--bg-soft))}
.card.plan .bar{opacity:.55}
.card.plan h3 a{color:var(--ink)}
.badge.plan{background:var(--bg-soft);color:var(--muted);border-color:var(--line)}
.legend-section{padding:4px 0 30px}
.teaser{margin:0 0 50px;padding:24px;border:1px solid var(--line);border-radius:16px;
  background:var(--surface)}
.teaser .btn{margin-top:6px}
.paths{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,400px),1fr));gap:16px;margin:16px 0 22px}
.path h3{margin:0}
.path-chain{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.path-skill{display:flex;align-items:center;gap:8px}
.path-skill .ps-name{flex:1 1 auto;min-width:0;color:var(--ink)}
.path-skill .ps-state{flex:0 0 auto;font-size:0.6562rem;text-transform:uppercase;letter-spacing:.05em;
  font-weight:700;color:var(--muted);background:rgba(0,0,0,.05);border-radius:4px;padding:2px 6px}
.path-skill:not(.plan) .ps-state{color:var(--brand-ink);background:var(--brand-soft)}
.path-filter{margin-top:auto;align-self:flex-start;font:inherit;font-size:0.75rem;font-weight:600;
  color:var(--brand-ink);background:var(--surface);border:1px solid var(--brand-line);
  border-radius:6px;padding:7px 11px;cursor:pointer;min-height:40px}
.path-filter:hover{background:var(--brand-soft)}
.path-filter.on{background:var(--brand-ink);color:#fff;border-color:var(--brand-ink)}
.toolbar{gap:8px}
.toolbar input[type=search]{flex:1 1 240px;max-width:360px}
.toolbar select{min-width:0;flex:0 1 165px;max-width:210px}
.toolbar .clear{flex:0 0 auto;font-size:0.8125rem;padding:8px 12px}
.filter-note{margin:0 0 8px}
.dims-list{list-style:none;margin:10px 0 16px;padding:0;display:flex;flex-direction:column;gap:9px}
.dims-list li{border:1px solid var(--line);border-radius:9px;padding:11px 13px;background:var(--surface)}
.dim-line{display:flex;align-items:center;gap:9px;justify-content:space-between}
.dim-line b{font-size:0.875rem}
.dims-list p{margin:4px 0 0;font-size:0.8125rem;color:var(--muted);line-height:1.45}
.dims-list .dim-req{font-size:0.75rem;color:var(--muted);opacity:.9}
.notice{margin:0 0 22px;padding:14px 16px;border-left:4px solid #d9a441;background:var(--warn-soft);
  color:var(--warn);border-radius:0 8px 8px 0;font-size:0.9062rem;line-height:1.5}
.skill-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.pkg-links{display:flex;flex-wrap:wrap;gap:8px}
.pkg-links .btn{margin:0!important}
.bibtex{margin-top:16px;border:1px solid var(--line);border-radius:10px;padding:12px 14px;
  background:var(--bg-soft)}
.bibtex summary{cursor:pointer;font-weight:600;font-size:0.875rem;min-height:32px}
.bibtex pre{margin-top:10px}
.footer-nav{display:flex;flex-wrap:wrap;gap:6px 10px}
.footer-nav a{color:var(--brand-ink)}
.install-steps{margin-top:8px}
@media(max-width:900px){
  .brand-name small{display:none}
  .page-head{padding-top:30px}
  .roadmap{padding:20px 16px 14px}
  .toolbar select{flex:1 1 calc(50% - 4px);max-width:none}
  .toolbar .clear{flex:1 1 100%}
}
@media(max-width:560px){
  .hero-sub{font-size:1.0625rem}
  .page-head h1{font-size:1.625rem}
  .diagram-figure{padding:8px}
  .evidence-table{min-width:640px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .card{transition:none}
  .card:hover{transform:none}
  *{animation-duration:.001ms!important;animation-iteration-count:1!important;
    transition-duration:.001ms!important}
}
"""


def js() -> str:
    return """// Progressive enhancement: without JS every card is visible and every link works.

(function(){
  var root=document.documentElement, KEY='smd-theme', btn=document.getElementById('theme-toggle');
  function current(){
    var set=root.getAttribute('data-theme');
    if(set) return set;
    return (window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';
  }
  function paint(){
    var t=current();
    if(btn){
      btn.setAttribute('aria-pressed', t==='dark'?'true':'false');
      btn.title = t==='dark' ? 'Mudar para tema claro' : 'Mudar para tema escuro';
    }
  }
  if(btn){
    btn.addEventListener('click',function(){
      var next = current()==='dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try{ localStorage.setItem(KEY, next); }catch(e){}
      paint();
    });
  }
  paint();
})();

// Catalogue filter. Separate scope: pages without cards must not stop the rest of the file.
// Search folds case and accents; filters persist in the query string; the count is announced.
(function(){
  var q=document.getElementById('q'), ty=document.getElementById('f-type'),
      st=document.getElementById('f-status'), mt=document.getElementById('f-maturity'),
      sg=document.getElementById('f-stage'), dc=document.getElementById('f-disc'),
      clear=document.getElementById('clear-filters'), pb=document.querySelectorAll('[data-path-jump]'),
      cards=[].slice.call(document.querySelectorAll('[data-skill]')),
      count=document.getElementById('count'), empty=document.getElementById('empty');
  if(!cards.length) return;
  var PATH='';
  function fold(s){
    s=(s||'').toString();
    if(s.normalize){ s=s.normalize('NFD').replace(/[\u0300-\u036f]/g,''); }
    return s.toLowerCase().trim();
  }
  function values(){
    return {
      q: q&&q.value||'', tipo: ty&&ty.value||'', status: st&&st.value||'',
      maturidade: mt&&mt.value||'', etapa: sg&&sg.value||'', disciplina: dc&&dc.value||''
    };
  }
  function apply(persist){
    var v=values(), term=fold(v.q), shown=0;
    cards.forEach(function(c){
      var hay=c.dataset.search||'';
      var ok=(!term||hay.indexOf(term)>-1)&&(!v.tipo||c.dataset.type===v.tipo)&&
             (!v.status||c.dataset.status===v.status)&&(!v.maturidade||c.dataset.maturity===v.maturidade)&&
             (!v.etapa||c.dataset.stage===v.etapa)&&(!v.disciplina||(c.dataset.disc||'').indexOf(v.disciplina)>-1)&&
             (!PATH||(c.dataset.paths||'').indexOf(PATH)>-1);
      c.hidden=!ok;
      if(ok) shown++;
    });
    if(count) count.textContent=shown;
    if(empty) empty.hidden=shown>0;
    if(persist) syncUrl(v);
  }
  function syncUrl(v){
    var p=new URLSearchParams();
    ['q','tipo','status','maturidade','etapa','disciplina'].forEach(function(k){
      if(v[k]) p.set(k, v[k]);
    });
    if(PATH) p.set('trilha', PATH);
    var qs=p.toString();
    try{ history.replaceState(null,'',location.pathname+(qs?'?'+qs:'')+location.hash); }catch(e){}
  }
  function readUrl(){
    var p=new URLSearchParams(location.search);
    if(q) q.value=p.get('q')||'';
    if(ty) ty.value=p.get('tipo')||'';
    if(st) st.value=p.get('status')||'';
    if(mt) mt.value=p.get('maturidade')||'';
    if(sg) sg.value=p.get('etapa')||'';
    if(dc) dc.value=p.get('disciplina')||'';
    PATH=p.get('trilha')||'';
    [].slice.call(pb).forEach(function(b){
      b.classList.toggle('on', !!PATH && b.dataset.pathJump===PATH);
    });
  }
  [q,ty,st,mt,sg,dc].forEach(function(el){
    if(!el) return;
    el.addEventListener('input',function(){ apply(true); });
    el.addEventListener('change',function(){ apply(true); });
  });
  [].slice.call(pb).forEach(function(b){
    b.addEventListener('click',function(){
      var on=b.classList.contains('on');
      [].slice.call(pb).forEach(function(x){ x.classList.remove('on'); });
      PATH=on?'':b.dataset.pathJump;
      if(!on) b.classList.add('on');
      apply(true);
    });
  });
  if(clear){
    clear.addEventListener('click',function(){
      [q,ty,st,mt,sg,dc].forEach(function(el){ if(el) el.value=''; });
      PATH='';
      [].slice.call(pb).forEach(function(x){ x.classList.remove('on'); });
      apply(true);
      if(q) q.focus();
    });
  }
  readUrl();
  apply(false);
})();

// Copy buttons. Independent scope, and the answer never depends on the clipboard permission:
// if the async API is blocked the text is selected so one keystroke finishes the job.
(function(){
  var live=document.getElementById('copy-status');
  function announce(msg){ if(live){ live.textContent=''; setTimeout(function(){ live.textContent=msg; },30); } }
  [].slice.call(document.querySelectorAll('[data-copy]')).forEach(function(btn){
    btn.addEventListener('click',function(){
      var target=document.getElementById(btn.dataset.copy);
      if(!target) return;
      var text=(target.innerText||target.textContent||'').trim();
      var label=btn.dataset.label||btn.textContent;
      function done(ok){
        if(ok){
          btn.textContent=btn.dataset.done||'Copied';
          announce(btn.dataset.done||'Copied');
          setTimeout(function(){ btn.textContent=label; },1600);
          return;
        }
        try{
          var r=document.createRange(); r.selectNodeContents(target);
          var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        }catch(e){}
        btn.textContent=btn.dataset.fail||label;
        announce(btn.dataset.fail||label);
        setTimeout(function(){ btn.textContent=label; },2400);
      }
      function legacy(){
        try{
          var ta=document.createElement('textarea');
          ta.value=text; ta.setAttribute('readonly','');
          ta.style.position='fixed'; ta.style.top='-1000px'; ta.style.opacity='0';
          document.body.appendChild(ta); ta.select();
          var ok=document.execCommand('copy');
          document.body.removeChild(ta); done(ok);
        }catch(e){ done(false); }
      }
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(text).then(function(){ done(true); }, legacy);
      } else { legacy(); }
    });
  });
})();
"""


def html_head(title: str, description: str, rel: str, lang: str, hub: dict,
              page: str = "home", slug: str | None = None,
              jsonld: dict | None = None, robots: str = "index,follow") -> str:
    css_hash = CSS_HASH
    can = canonical(page, lang, hub, slug)
    other = canonical(page, "en" if lang == "pt" else "pt", hub, slug)
    pt_url = canonical(page, "pt", hub, slug)
    en_url = canonical(page, "en", hub, slug)
    locale = "pt_BR" if lang == "pt" else "en_US"
    alt_locale = "en_US" if lang == "pt" else "pt_BR"
    image = site_root(hub) + "assets/img/labhd.png"
    ld = ""
    if jsonld:
        ld = ('\n<script type="application/ld+json">'
              + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))
              + "</script>")
    return f"""<!doctype html>
<html lang="{'pt-BR' if lang == 'pt' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{esc(robots)}">
<link rel="canonical" href="{esc(can)}">
<link rel="alternate" hreflang="pt-BR" href="{esc(pt_url)}">
<link rel="alternate" hreflang="en" href="{esc(en_url)}">
<link rel="alternate" hreflang="x-default" href="{esc(pt_url)}">
<meta property="og:site_name" content="ScholarSkills">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(can)}">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:image" content="{esc(image)}">
<meta name="twitter:card" content="summary">
<link rel="preload" href="{rel}assets/fonts/heebo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel}assets/fonts/signika.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel}assets/style.css?v={css_hash}">
<link rel="icon" href="{rel}assets/img/labhd.png">
<script>try{{var t=localStorage.getItem('smd-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>{ld}
</head>
<body>
<a class="skip-link" href="#main">{esc(t(lang, 'skip'))}</a>
<p id="copy-status" class="sr-only" role="status" aria-live="polite"></p>"""


def site_header(rel: str, lang: str, hub: dict, page: str = "home",
                slug: str | None = None, active: str = "home") -> str:
    """One header for every page. `active` follows the page, and the language link goes to the
    equivalent page rather than dropping the reader on the home page of the other language."""

    def item(key: str, href: str, label: str, cls: str = "") -> str:
        classes = [c for c in (cls, "on" if key == active else "") if c]
        attrs = (' class="' + " ".join(classes) + '"') if classes else ""
        cur = ' aria-current="page"' if key == active else ""
        return f'<a{attrs} href="{href}"{cur}>{label}</a>'

    nav_html = "\n    ".join([
        item("home", f"{rel}{page_path('home', lang)}", t(lang, "nav_home")),
        item("catalogue", f"{rel}{page_path('home', lang)}#skills", t(lang, "nav_catalogue")),
        item("using", f"{rel}{page_path('using', lang)}", t(lang, "nav_using")),
        item("paths", f"{rel}{page_path('home', lang)}#paths", t(lang, "nav_paths")),
        item("evidence", f"{rel}{page_path('evidence', lang)}", t(lang, "nav_evidence")),
        item("contribute", f"{rel}{page_path('contribute', lang)}", t(lang, "nav_contribute"), "cta"),
    ])

    brand_small = "LABHDUFBA · UFBA"
    return f"""<header class="site"><div class="wrap">
  <a class="brand" href="{rel}{page_path('home', lang)}">
    <span class="mark"><img src="{rel}assets/img/labhd.webp" alt="LABHDUFBA"></span>
    <span class="brand-name">ScholarSkills<small>{brand_small}</small></span></a>
  <button class="theme-toggle" id="theme-toggle" type="button"
    aria-label="Alternar tema claro e escuro" title="Tema claro / escuro">
    <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
      stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
      stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
  </button>
  <a class="lang" href="{alt_path(page, lang, slug)}" hreflang="{'en' if lang == 'pt' else 'pt-BR'}"
     aria-label="{esc(t(lang, 'lang_aria'))}"><span class="full">{t(lang, 'switch')}</span><span class="short">{'EN' if lang == 'pt' else 'PT'}</span></a>
  <nav class="site" aria-label="{esc(t(lang, 'menu_aria'))}">
    {nav_html}
  </nav>
</div></header>"""


def site_footer(hub: dict, lang: str, rel: str) -> str:
    repo = (hub.get("repo_url") or "https://github.com/LABHDUFBA/scholarskills").rstrip("/")
    links = [
        f'<a href="{rel}{page_path("about", lang)}">{t(lang, "footer_about")}</a>',
        f'<a href="{repo}" rel="noopener">{t(lang, "footer_github")}</a>',
        f'<a href="{rel}api/registry.json">{t(lang, "footer_registry")}</a>',
        f'<a href="{repo}/blob/main/registry/EDITORIAL_POLICY.md">{t(lang, "footer_policy")}</a>',
        f'<a href="{repo}/blob/main/LICENSE">{t(lang, "footer_license")}</a>',
    ]
    return f"""<footer class="site"><div class="wrap">
  <span><img src="{rel}assets/img/labhd.webp" alt="" style="width:20px;height:20px;border-radius:50%;vertical-align:-5px;margin-right:7px;background:#0a1f0c">{esc(hub.get('institution', ''))}</span>
  <nav class="footer-nav" aria-label="{esc(t(lang, 'footer_about'))}">{' · '.join(links)}</nav>
  <span>{t(lang, 'foot_note')}</span>
  <span>{t(lang, 'attrib')}</span>
</div></footer>
<script src="{rel}assets/app.js?v={CSS_HASH}"></script>
</body></html>"""


def features_of(s: dict, lang: str) -> list:
    if lang == "en" and s.get("features_en"):
        return s["features_en"]
    return s.get("features") or []


def icons_of(s: dict, rel: str) -> str:
    out = []
    planned = s.get("status") == "planned"
    tag = ' title="Previsto" ' if planned else ' '
    for k in (s.get("integrations") or []):
        asset = ICON_ASSET.get(k)
        if not asset:
            continue
        out.append(f'<span class="chip"{tag}><img src="{rel}assets/img/{asset}" alt="" '
                   f'width="18" height="18" loading="lazy" decoding="async">'
                   f'<b>{esc(ICON_LABEL.get(k, k.title()))}</b></span>')
    return "".join(out)


def card(s: dict, lang: str, stages: dict, rel: str) -> str:
    stage = stages.get(s.get("stage") or "")
    name = (stage or {}).get(lang) or "—"
    planned = s.get("status") == "planned"
    authors = s.get("authors") or []
    names = ", ".join(a.get("name", "") for a in authors) if authors else ""
    feats = features_of(s, lang) if not planned else []
    feats_html = "".join(f'<span class="feat">{esc(f)}</span>' for f in feats[:3])
    icons = icons_of(s, rel) if not planned else ""
    title = s.get("title_pt") if (lang == "pt" and s.get("title_pt")) else s.get("title")
    summary = s.get("summary_pt") if (lang == "pt" and s.get("summary_pt")) else s.get("summary")
    if planned and not summary:
        summary = t(lang, "roadmap_none")
    search = norm(" ".join(filter(None, [
        s.get("id"), s.get("slug"), s.get("title"), s.get("title_pt"),
        s.get("summary"), s.get("summary_pt"), names, type_label(s.get("type"), lang),
        type_label(s.get("type"), "en" if lang == "pt" else "pt"),
        " ".join(s.get("keywords") or []), " ".join(feats),
    ])))
    href = f"{rel}{skill_path(s.get('slug'), lang)}"
    top = [f'<span class="code">{esc(s.get("id"))}</span>', type_badge(s.get("type"), lang)]
    if planned:
        top.append(f'<span class="badge plan">{esc(t(lang, "roadmap_badge"))}</span>')
    else:
        top.append(badge(s.get("maturity"), MATURITY if lang == "pt" else MATURITY_EN))
        top.append(badge(s.get("status"), STATUS if lang == "pt" else STATUS_EN))
    foot_label = t(lang, "roadmap_open") if planned else t(lang, "view")
    return f"""<article class="card{' plan' if planned else ''}" data-skill data-status="{esc(s.get('status'))}"
  data-maturity="{esc(s.get('maturity') or '')}" data-stage="{esc(s.get('stage') or '')}"
  data-type="{esc(s.get('type') or '')}"
  data-disc="{esc(' '.join(s.get('disciplines') or []))}"
  data-paths="{esc(' '.join(s.get('paths') or []))}"
  data-search="{esc(search)}" {stage_style(stage)}>
  <div class="bar"></div>
  <div class="inner">
    <div class="top">
      {''.join(top)}
    </div>
    <h3><a href="{href}">{esc(title)}</a></h3>
    <p>{esc(summary)}</p>
    {f'<div class="feats">{feats_html}</div>' if feats_html else ''}
    {f'<div class="authors">{esc(names)}</div>' if names else ''}
    {f'<div class="stack">{icons}</div>' if icons else ''}
    <div class="foot">
      <span>{t(lang,'stage')}: <b style="color:var(--stage-ink)">{esc(name)}</b></span>
      <span class="arrow"><a href="{href}">{foot_label} &rarr;</a></span>
    </div>
  </div>
</article>"""


def render_paths(reg: dict, lang: str, rel: str) -> str:
    """Research paths as readable flows: each step links to its page and declares availability.

    The sequences are editorial proposals, not tested interoperability. A planned step is labelled
    as such, and the footer states how much of the path exists today.
    """
    cols = reg.get("collections") or []
    if not cols:
        return ""
    skills = {s.get("id"): s for s in reg.get("skills") or []}
    stages = reg.get("stages") or {}
    out = ['<div class="paths" id="paths">']
    for c in cols:
        stage = stages.get(c.get("stage") or "")
        name = c.get("pt") if lang == "pt" else c.get("en")
        desc = c.get("desc_pt") if lang == "pt" else c.get("desc_en")
        ids = c.get("skills") or []
        items, available = [], 0
        for i, sid in enumerate(ids, 1):
            s = skills.get(sid)
            if not s:
                continue
            planned = s.get("status") != "available"
            if not planned:
                available += 1
            title = s.get("title_pt") if (lang == "pt" and s.get("title_pt")) else s.get("title")
            state = t(lang, "path_planned" if planned else "path_available")
            items.append(
                f'<li class="path-skill{" plan" if planned else ""}">'
                f'<span class="ps-step">{i}</span>'
                f'<span class="ps-id">{esc(sid)}</span>'
                f'<a class="ps-name" href="{rel}{skill_path(s.get("slug"), lang)}">{esc(title)}</a>'
                f'<span class="ps-state">{esc(state)}</span></li>')
        count = t(lang, "path_count").format(a=available, n=len(ids))
        out.append(f"""<article class="path" {stage_style(stage)}>
  <h3>{esc(name)}</h3>
  <p>{esc(desc or '')}</p>
  <ol class="path-chain">{''.join(items)}</ol>
  <p class="path-foot">{esc(count)}</p>
  <button type="button" class="path-filter" data-path-jump="{esc(c.get('slug'))}">
    {esc(t(lang, 'path_filter'))}</button>
</article>""")
    out.append('</div>')
    return "\n".join(out)


def site_name(hub: dict, lang: str) -> str:
    """Display name, read from the registry so copy and <title> cannot diverge again.

    The technical identifier (repository `scholarskills`, `SS-` prefix, Pages URL) is deliberately not
    derived from this: it is what has already been cited and deposited.
    """
    key = "short_name" if lang == "pt" else "short_name_en"
    return hub.get(key) or hub.get("short_name") or ("Métodos Digitais" if lang == "pt" else "Digital Methods")


def render_concepts(hub: dict, lang: str, rel: str) -> str:
    """Four short cards on the home page; the long definitions live on their own page."""
    cards = [("conc_m", "conc_m_s"), ("conc_a", "conc_a_s"),
             ("conc_s", "conc_s_s"), ("conc_t", "conc_t_s")]
    out = ['<section class="concepts wrap" id="conceitos">',
           f'<h2 class="sec-h" style="margin-top:0">{esc(t(lang, "concepts_short_h"))}</h2>',
           f'<p class="conc-lede">{esc(t(lang, "concepts_short_p"))}</p>',
           '<div class="cgrid">']
    for term, body in cards:
        out.append(f'<article class="ccard"><h3>{esc(t(lang, term))}</h3>'
                   f'<p>{esc(t(lang, body))}</p></article>')
    out.append('</div>')
    out.append(f'<p class="concepts-link"><a class="btn" href="{rel}{page_path("concepts", lang)}">'
               f'{esc(t(lang, "concepts_more"))} &rarr;</a></p>')
    out.append('</section>')
    return "\n".join(out)


def render_index(reg: dict, lang: str) -> str:
    hub = reg.get("hub", {})
    stages = reg.get("stages", {})
    skills = reg["skills"]
    rel = "" if lang == "pt" else "../"
    available = [s for s in skills if s.get("status") == "available"]
    planned = [s for s in skills if s.get("status") == "planned"]
    with_doi = [s for s in skills if s.get("doi_version") or s.get("doi_concept")]
    people = unique_authors(reg)
    ordered = sorted(skills, key=lambda s: (0 if s.get("status") == "available" else 1,
                                            0 if s.get("highlight") else 1, s.get("id") or ""))
    title = ((hub.get("title_pt") if lang == "pt" else hub.get("title"))
             or "ScholarSkills")
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "ScholarSkills",
        "alternateName": "Métodos Digitais",
        "url": site_root(hub),
        "description": hub.get("description" if lang == "en" else "description_pt", ""),
        "inLanguage": ["pt-BR", "en"],
        "publisher": {"@type": "Organization", "name": "LABHDUFBA",
                      "url": "https://labhd.ufba.br"},
    }

    out = html_head(title, hub.get("description_pt" if lang == "pt" else "description", ""),
                    rel, lang, hub, page="home", jsonld=jsonld)
    out += site_header(rel, lang, hub, page="home", active="home")
    out += f"""<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div class="hero-copy">
      <p class="initiative">{esc(t(lang, 'hero_initiative'))}</p>
      <h1>ScholarSkills</h1>
      <p class="hero-sub">{esc(hub.get('tagline_pt' if lang == 'pt' else 'tagline', ''))}</p>
      <p class="lede">{esc(hub.get('description_pt' if lang == 'pt' else 'description', ''))}</p>
      <p class="desc">{esc(t(lang, 'hero_note'))}</p>
      <div class="hero-actions">
        <a class="btn primary" href="#skills">{esc(t(lang, 'hero_cta_explore'))}</a>
        <a class="btn" href="{rel}{page_path('using', lang)}">{esc(t(lang, 'hero_cta_using'))}</a>
        <a class="btn" href="{rel}{page_path('contribute', lang)}">{esc(t(lang, 'hero_cta_contribute'))}</a>
      </div>
    </div>
    <aside class="hero-panel" aria-labelledby="start-h">
      <h2 id="start-h">{esc(t(lang, 'hero_panel_h'))}</h2>
      <ol>
        <li><a href="{rel}{page_path('concepts', lang)}"><b>{esc(t(lang, 'hero_panel_1'))}</b>
          <span>{esc(t(lang, 'hero_panel_1d'))}</span></a></li>
        <li><a href="{rel}{page_path('using', lang)}"><b>{esc(t(lang, 'hero_panel_2'))}</b>
          <span>{esc(t(lang, 'hero_panel_2d'))}</span></a></li>
        <li><a href="{rel}{page_path('evidence', lang)}"><b>{esc(t(lang, 'hero_panel_3'))}</b>
          <span>{esc(t(lang, 'hero_panel_3d'))}</span></a></li>
      </ol>
      <a class="repo-link" href="{esc(hub.get('repo_url', 'https://github.com/LABHDUFBA/scholarskills'))}" rel="noopener">{esc(t(lang, 'hero_repo'))} &nearr;</a>
    </aside>
  </div>
  <div class="stats">
    <div class="stat" title="{esc(t(lang, 'stat_available_def'))}"><b>{len(available)}</b><span>{esc(t(lang, 'stat_available'))}</span></div>
    <div class="stat" title="{esc(t(lang, 'stat_planned_def'))}"><b>{len(planned)}</b><span>{esc(t(lang, 'stat_planned'))}</span></div>
    <div class="stat" title="{esc(t(lang, 'stat_doi_def'))}"><b>{len(with_doi)}</b><span>{esc(t(lang, 'stat_doi'))}</span></div>
    <div class="stat" title="{esc(t(lang, 'stat_authors_def'))}"><b>{len(people)}</b><span>{esc(t(lang, 'stat_authors'))}</span></div>
  </div>
  <p class="stats-note">{esc(t(lang, 'stats_note'))}</p>
</div></section>
"""
    out += render_concepts(hub, lang, rel)
    out += f"""
<main id="main" class="wrap">
  <section id="skills" aria-labelledby="skills-h">
    <h2 class="sec-h" id="skills-h">{t(lang,"nav_catalogue")}</h2>
    <p class="sec-p">{esc(t(lang, 'skills_intro'))}</p>
    {render_paths(reg, lang, rel)}
  <div class="toolbar" role="search">
    <label class="sr-only" for="q">{esc(t(lang,'search'))}</label>
    <input id="q" type="search" placeholder="{esc(t(lang,'search'))}" autocomplete="off">
    <label class="sr-only" for="f-type">{esc(t(lang,'all_types'))}</label>
    <select id="f-type">
      <option value="">{t(lang,'all_types')}</option>
      {''.join(f'<option value="{esc(k)}">{esc(v[lang])}</option>' for k, v in (reg.get("taxonomy") or {}).items())}
    </select>
    <label class="sr-only" for="f-stage">{esc(t(lang,'all_stages'))}</label>
    <select id="f-stage">
      <option value="">{t(lang,'all_stages')}</option>
      {''.join(f'<option value="{esc(k)}">{esc(v[lang])}</option>' for k, v in stages.items())}
    </select>
    <label class="sr-only" for="f-status">{esc(t(lang,'all_status'))}</label>
    <select id="f-status">
      <option value="">{t(lang,'all_status')}</option>
      <option value="available">{(STATUS if lang=='pt' else STATUS_EN)['available'][0]}</option>
      <option value="planned">{(STATUS if lang=='pt' else STATUS_EN)['planned'][0]}</option>
      <option value="deprecated">{(STATUS if lang=='pt' else STATUS_EN)['deprecated'][0]}</option>
    </select>
    <label class="sr-only" for="f-maturity">{esc(t(lang,'all_maturity'))}</label>
    <select id="f-maturity">
      <option value="">{t(lang,'all_maturity')}</option>
      {''.join(f'<option value="{k}">{v[0]}</option>' for k, v in (MATURITY if lang=='pt' else MATURITY_EN).items())}
    </select>
    <label class="sr-only" for="f-disc">{esc(t(lang,'all_disc'))}</label>
    <select id="f-disc">
      <option value="">{t(lang,'all_disc')}</option>
      {''.join(f'<option value="{esc(k)}">{esc(v[lang])}</option>' for k, v in (reg.get("disciplines") or {}).items())}
    </select>
    <button type="button" class="btn clear" id="clear-filters">{esc(t(lang,'filters_clear'))}</button>
    <span class="count" role="status" aria-live="polite"><span id="count">{len(skills)}</span> {esc(t(lang,'results'))}</span>
  </div>
  <p class="note filter-note">{esc(t(lang, 'type_note'))}</p>
  <div class="grid">
"""
    out += "\n".join(card(s, lang, stages, rel) for s in ordered)
    out += f"""
  </div>
  <p class="empty" id="empty" hidden>{t(lang,'empty')}</p>

  <section id="stages" class="legend-section" aria-labelledby="stages-h">
    <h2 class="sec" id="stages-h">{t(lang,'stages_h')}</h2>
    <p class="sec-p">{t(lang,'stages_p')}</p>
    <div class="stage-legend">
      {''.join(f'<a href="#skills"><span class="dot" style="--c:{v["color"]}"></span>{esc(v[lang])}</a>' for v in stages.values())}
    </div>
  </section>

  <section id="roadmap" class="roadmap" aria-labelledby="roadmap-h">
    <h2 class="sec-h" id="roadmap-h">{t(lang,'roadmap_h')}</h2>
    <p class="sec-p">{esc(t(lang,'roadmap_p'))}</p>
    <div class="grid roadmap-grid">
"""
    out += "\n".join(card(s, lang, stages, rel) for s in planned)
    out += f"""
    </div>
    <p class="note">{esc(t(lang,'roadmap_note'))}</p>
  </section>

  <section id="levels" class="teaser" aria-labelledby="levels-h">
    <h2 class="sec-h" id="levels-h">{esc(t(lang,'evidence_teaser_h'))}</h2>
    <p class="sec-p">{esc(t(lang,'evidence_teaser_p'))}</p>
    <a class="btn" href="{rel}{page_path('evidence', lang)}">{esc(t(lang,'evidence_teaser_cta'))} &rarr;</a>
  </section>
</main>
"""
    out += render_authors_block(hub, lang, rel)
    out += site_footer(hub, lang, rel)
    return out


def _fill(text: str, lang: str, rel: str, hub: dict) -> str:
    repo = (hub.get("repo_url") or "https://github.com/LABHDUFBA/scholarskills").rstrip("/")
    values = {
        "{rel}": rel,
        "{catalogue}": rel + page_path("home", lang) + "#skills",
        "{using}": rel + page_path("using", lang),
        "{evidence}": rel + page_path("evidence", lang),
        "{contribute}": rel + page_path("contribute", lang),
        "{about}": rel + page_path("about", lang),
        "{concepts}": rel + page_path("concepts", lang),
        "{policy}": repo + "/blob/main/registry/EDITORIAL_POLICY.md",
        "{repo}": repo,
        "{registry}": rel + "api/registry.json",
        "{email}": hub.get("contact_email") or "",
        "{skill_zotero}": rel + skill_path("zotero-reference-management", lang),
        "{skill_ss0000}": rel + skill_path("scientific-agent-skill-development", lang),
        "{guide}": repo + "/blob/main/CONTRIBUTING.md",
    }
    for key, value in values.items():
        text = text.replace(key, value)
    return text


def _diagram(lang: str) -> tuple[str, str]:
    labels = {
        "pt": {
            "title": "Como um agente mobiliza uma skill",
            "desc": ("Diagrama do ciclo: o pesquisador define o problema e supervisiona; o agente carrega a skill, "
                     "consulta o LLM, opera ferramentas e produz resultados; o pesquisador interpreta, valida ou interrompe."),
            "r_agent": "problema, instrução, supervisão", "agent_llm_in": "consulta",
            "agent_llm_out": "interpretação", "agent_llm": "consulta e resposta",
            "skill_agent": "orienta", "agent_tool": "opera", "tool_agent": "retorna",
            "agent_results": "produz", "human_loop": "revisão humana e parada possível",
        },
        "en": {
            "title": "How an agent mobilises a skill",
            "desc": ("Cycle diagram: the researcher frames the problem and supervises; the agent loads the skill, "
                     "consults the LLM, operates tools and produces results; the researcher interprets, validates or stops."),
            "r_agent": "problem, instruction, supervision", "agent_llm_in": "query",
            "agent_llm_out": "interpretation", "agent_llm": "query and response",
            "skill_agent": "guides", "agent_tool": "operates", "tool_agent": "returns",
            "agent_results": "produces", "human_loop": "human review and possible stop",
        },
    }[lang]
    return (content.DIAGRAM_WIDE.format(**labels), content.DIAGRAM_TALL.format(**labels))


def _webpage_ld(page: str, lang: str, hub: dict, title: str, description: str,
                slug: str | None = None) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical(page, lang, hub, slug),
        "inLanguage": "pt-BR" if lang == "pt" else "en",
        "isPartOf": {"@type": "WebSite", "name": "ScholarSkills", "url": site_root(hub)},
    }


def render_static_page(hub: dict, lang: str, page: str, title: str, lede: str,
                       description: str, body: str, active: str) -> str:
    rel = "" if lang == "pt" else "../"
    out = html_head(title, description, rel, lang, hub, page=page,
                    jsonld=_webpage_ld(page, lang, hub, title, description))
    out += site_header(rel, lang, hub, page=page, active=active)
    out += f"""<main id="main" class="wrap page">
  <header class="page-head">
    <h1>{esc(title)}</h1>
    <p class="lede">{esc(lede)}</p>
  </header>
  {body}
</main>
"""
    out += site_footer(hub, lang, rel)
    return out


def render_concepts_page(hub: dict, lang: str) -> str:
    rel = "" if lang == "pt" else "../"
    body = _fill(content.CONCEPTS[lang], lang, rel, hub)
    wide, tall = _diagram(lang)
    body = body.replace("{diagram_wide}", wide).replace("{diagram_tall}", tall)
    return render_static_page(
        hub, lang, "concepts", t(lang, "page_concepts_h"), t(lang, "page_concepts_p"),
        t(lang, "page_concepts_d"), body, active="concepts")


def render_using_page(hub: dict, lang: str) -> str:
    rel = "" if lang == "pt" else "../"
    body = _fill(content.USING[lang], lang, rel, hub)
    return render_static_page(
        hub, lang, "using", t(lang, "page_using_h"), t(lang, "page_using_p"),
        t(lang, "page_using_d"), body, active="using")


def render_evidence_page(reg: dict, hub: dict, lang: str) -> str:
    rel = "" if lang == "pt" else "../"
    dims = reg.get("evidence_dimensions") or []
    cards = "\n".join(
        f'<article class="dim"><h3>{esc(d.get(lang) or d.get("pt"))}</h3>'
        f'<p>{esc(d.get("req_pt" if lang == "pt" else "req_en"))}</p></article>'
        for d in dims)
    headers = "".join(
        f'<th scope="col" title="{esc(d.get("req_pt" if lang == "pt" else "req_en"))}">'
        f'{esc(d.get(lang) or d.get("pt"))}</th>' for d in dims)
    rows = []
    for s in reg["skills"]:
        if s.get("status") != "available":
            continue
        dims_data = s.get("evidence_dimensions") or {}
        cells = []
        for d in dims:
            item = dims_data.get(d.get("key")) or {}
            recorded = item.get("status") == "recorded"
            note = item.get("note_pt" if lang == "pt" else "note") or ""
            cls = "yes" if recorded else "no"
            label = t(lang, "evidence_recorded" if recorded else "evidence_not")
            cells.append(f'<td><span class="ev {cls}" title="{esc(note)}">{esc(label)}</span></td>')
        title = s.get("title_pt") if (lang == "pt" and s.get("title_pt")) else s.get("title")
        rows.append(
            f'<tr><th scope="row"><a href="{rel}{skill_path(s.get("slug"), lang)}">'
            f'<span class="code">{esc(s.get("id"))}</span> {esc(title)}</a></th>{"".join(cells)}</tr>')
    body = content.EVIDENCE[lang].replace("{dimension_cards}", cards) \
                                 .replace("{dim_headers}", headers) \
                                 .replace("{evidence_rows}", "\n".join(rows))
    body = _fill(body, lang, rel, hub)
    return render_static_page(
        hub, lang, "evidence", t(lang, "page_evidence_h"), t(lang, "page_evidence_p"),
        t(lang, "page_evidence_d"), body, active="evidence")


def render_about_page(hub: dict, lang: str) -> str:
    rel = "" if lang == "pt" else "../"
    body = _fill(content.ABOUT[lang], lang, rel, hub)
    return render_static_page(
        hub, lang, "about", t(lang, "page_about_h"), t(lang, "page_about_p"),
        t(lang, "page_about_d"), body, active="about")


def render_requirements(s: dict, lang: str) -> str:
    reqs = s.get("requirements") or []
    if not reqs:
        return ""
    out = [f'<h2 class="sec">{t(lang,"req_h")}</h2>',
           f'<p class="note" style="margin-top:-2px">{t(lang,"req_intro")}</p>',
           '<div class="reqs">']
    for r in reqs:
        name = r.get("name_en") if lang == "en" and r.get("name_en") else r.get("name") or ""
        what = r.get("what_en") if lang == "en" and r.get("what_en") else r.get("what_pt") or r.get("what") or ""
        how = r.get("how_en") if lang == "en" and r.get("how_en") else r.get("how_pt") or r.get("how") or ""
        note = r.get("note_en") if lang == "en" and r.get("note_en") else r.get("note_pt") or r.get("note")
        typ = r.get("type") or ""
        sev = " required" if r.get("required") else ""
        badges = f'<span class="badge accent">{t(lang,"req_required")}</span>' if r.get("required") else f'<span class="badge muted">{t(lang,"req_optional")}</span>'
        if typ in ("secret", "id", "software", "choice"):
            badges += f'<span class="badge kind">{t(lang, "req_" + typ)}</span>'
        env = (f'<code class="env">{esc(r.get("env"))}</code>' if r.get("env") else "")
        links = []
        if r.get("url"):
            lab = (r.get("url_label_en") if lang == "en" and r.get("url_label_en")
                   else r.get("url_label")) or r["url"]
            links.append(f'<a class="btn req-btn primary" href="{esc(r["url"])}" target="_blank" '
                         f'rel="noopener">{esc(lab)} &nearr;</a>')
        if r.get("doc_url"):
            lab2 = (r.get("doc_label_en") if lang == "en" and r.get("doc_label_en")
                    else r.get("doc_label")) or r["doc_url"]
            links.append(f'<a class="btn req-btn" href="{esc(r["doc_url"])}" target="_blank" '
                         f'rel="noopener">{esc(lab2)} &nearr;</a>')
        out.append(f"""<article class="req{sev}">
  <div class="req-top">
    <h3>{esc(name)}</h3>
    <div class="req-badges">{badges}{env}</div>
  </div>
  {f'<p><b>{t(lang,"req_what")}:</b> {esc(what)}</p>' if what else ''}
  {f'<p><b>{t(lang,"req_how")}:</b> {esc(how)}</p>' if how else ''}
  {f'<pre class="req-ex"><code>{esc(r.get("example"))}</code></pre>' if r.get("example") else ''}
  {f'<div class="req-links">{"".join(links)}</div>' if links else ''}
  {f'<p class="req-note"><b>{t(lang,"req_note")}:</b> {esc(note)}</p>' if note else ''}
</article>""")
    out.append('</div>')
    return "\n".join(out)


CSS_HASH = "0"


def _css_hash(text: str) -> str:
    """Cache-busting that cannot go stale: the query is the digest of the very CSS being written."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-[\dX]{4}$")


def orcid_cell(a: dict, rel: str) -> str:
    """A bare 16-digit string is not a citation: the ORCID becomes a link with its own mark."""
    o = (a.get("orcid") or "").strip()
    if not o:
        return '<span class="note">—</span>'
    if not ORCID_RE.match(o):
        # a malformed identifier is worse than a missing one: show it as text, never as a link
        return f'<span class="note" title="formato inválido">{esc(o)}</span>'
    return (f'<a class="orcid" href="https://orcid.org/{esc(o)}" target="_blank" '
            f'rel="noopener"><img src="{rel}assets/img/orcid.svg" alt="" width="14" height="14" '
            f'aria-hidden="true"><span>{esc(o)}</span></a>')


def render_authors_block(hub: dict, lang: str, rel: str) -> str:
    """Authorship on the home page, with the identifier next to the name."""
    people = hub.get("authors") or []
    if not people:
        return ""
    cards = []
    for a in people:
        role = a.get("role_pt") if lang == "pt" else a.get("role")
        cards.append(
            f'<div class="author-card">'
            f'<div class="author-name">{esc(a.get("name"))}</div>'
            f'<div class="author-role">{esc(role or "")}</div>'
            f'<div class="author-aff">{esc(a.get("affiliation") or "")}</div>'
            f'{orcid_cell(a, rel)}</div>')
    head = "Autoria" if lang == "pt" else "Authorship"
    sub = ("Quem assina o catálogo. O ORCID liga cada pessoa à sua produção registrada; ele aparece "
           "porque a responsabilidade pelo método é nomeada." if lang == "pt" else
           "Who signs the catalogue. ORCID links each person to their registered output; it appears "
           "because responsibility for a method is named.")
    return (f'<section class="wrap" id="autores"><h2 class="sec-h">{head}</h2>'
            f'<p class="sec-p">{sub}</p>'
            f'<div class="author-grid">{"".join(cards)}</div></section>')


def package_links(s: dict, lang: str) -> list[tuple[str, str]]:
    """Links to files that actually exist in the package directory, never to invented URLs."""
    repo = (s.get("repository") or "").rstrip("/")
    slug = s.get("slug") or ""
    if not repo:
        return []
    wanted = [
        ("SKILL.md", "package_skill"),
        ("README.md", "package_readme"),
        ("tests/RESULTS.md", "package_tests"),
        ("LICENSE", "package_license"),
        ("CITATION.cff", "package_citation"),
        ("CHANGELOG.md", "package_changelog"),
    ]
    out = []
    for relpath, label in wanted:
        if (ROOT / slug / relpath).exists():
            out.append((t(lang, label), f"{repo}/blob/main/{slug}/{relpath}"))
    return out


def bibtex_of(s: dict) -> str:
    authors = " and ".join(a.get("name", "") for a in (s.get("authors") or []))
    year = (s.get("added") or "")[:4] or "n.d."
    key = "ss" + (s.get("id") or "0000").split("-")[-1]
    doi = s.get("doi_version") or s.get("doi_concept") or ""
    fields = [
        ("author", authors),
        ("title", s.get("title") or ""),
        ("year", year),
        ("version", s.get("version") or ""),
        ("publisher", "Digital Humanities Laboratory, Federal University of Bahia"),
        ("url", s.get("repository") or ""),
        ("doi", doi),
    ]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@software{{{key},\n{body}\n}}"


def evidence_list(s: dict, dims: list, lang: str) -> str:
    data = s.get("evidence_dimensions") or {}
    items = []
    for d in dims:
        key = d.get("key")
        item = data.get(key) or {}
        recorded = item.get("status") == "recorded"
        note = item.get("note_pt" if lang == "pt" else "note") or ""
        label = t(lang, "evidence_recorded" if recorded else "evidence_not")
        cls = "yes" if recorded else "no"
        req = d.get("req_pt" if lang == "pt" else "req_en")
        items.append(
            f'<li><div class="dim-line"><b>{esc(d.get(lang) or d.get("pt"))}</b>'
            f'<span class="ev {cls}">{esc(label)}</span></div>'
            f'<p>{esc(note)}</p><p class="dim-req">{esc(req)}</p></li>')
    return f'<ul class="dims-list">{"".join(items)}</ul>'


def evidence_url(s: dict) -> str:
    """The registry stores either a URL or a repository-relative path; both must leave the site."""
    value = (s.get("evidence") or "").strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    repo = (s.get("repository") or "").rstrip("/")
    return f"{repo}/blob/main/{value.lstrip('/')}"


def render_skill(s: dict, hub: dict, stages: dict, lang: str, reg_disc: dict = None,
                 dims: list | None = None) -> str:
    if s.get("status") != "available":
        return render_roadmap(s, hub, stages, lang, reg_disc)
    rel = "../" if lang == "pt" else "../../"  # pages live in <base>/skills/
    stage = stages.get(s.get("stage") or "")
    name = (stage or {}).get(lang) or "—"
    title = s.get("title_pt") if (lang == "pt" and s.get("title_pt")) else s.get("title")
    sub = s.get("summary_pt") if (lang == "pt" and s.get("summary_pt")) else s.get("summary")
    reg_disc = reg_disc or {}
    reqs_html = render_requirements(s, lang)
    repo = (s.get("repository") or "").rstrip("/")
    pkg = f"{repo}/tree/main/{s.get('slug')}"
    doi = s.get("doi_version")
    jsonld = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": title,
        "identifier": s.get("id"),
        "version": s.get("version"),
        "description": sub,
        "codeRepository": repo,
        "license": s.get("license"),
        "author": [{"@type": "Person", "name": a.get("name"),
                    **({"@id": "https://orcid.org/" + a["orcid"]} if a.get("orcid") else {})}
                   for a in (s.get("authors") or [])],
        "datePublished": s.get("added"),
    }
    if doi:
        jsonld["sameAs"] = "https://doi.org/" + doi
    out = html_head(f"{title} — {site_name(hub, lang)}", sub or "", rel, lang, hub,
                    page="skill", slug=s.get("slug"), jsonld=jsonld)
    out += site_header(rel, lang, hub, page="skill", slug=s.get("slug"), active="catalogue")

    authors = s.get("authors") or []
    rows = "".join(
        f"<tr><td><b>{esc(a.get('name'))}</b></td><td>{esc(a.get('affiliation') or '—')}</td>"
        f"<td>{orcid_cell(a, rel)}</td></tr>" for a in authors) \
        or '<tr><td colspan="3">—</td></tr>'
    steps = (s.get("how_it_works_pt") if (lang == "pt" and s.get("how_it_works_pt"))
             else s.get("how_it_works")) or []
    objective = (s.get("objective_pt") if (lang == "pt" and s.get("objective_pt"))
                 else s.get("objective")) or sub or "—"
    limits = (s.get("limits_pt") if lang == "pt" and s.get("limits_pt") else s.get("limits"))
    install = (s.get("install_pt") if (lang == "pt" and s.get("install_pt"))
               else s.get("install"))
    steps_html = (f'<ol class="steps">' + "".join(f"<li>{esc(x)}</li>" for x in steps) + "</ol>"
                  ) if steps else '<p class="note">—</p>'
    feats = features_of(s, lang)
    feats_html = "".join(f'<span class="feat">{esc(f)}</span>' for f in feats)
    icons = icons_of(s, rel)
    cite = s.get("cite") or ""
    plinks = package_links(s, lang)
    link_html = "".join(
        f'<a class="btn" style="margin:0 8px 8px 0" href="{esc(u)}">{esc(label)}</a>'
        for label, u in plinks)
    install_block = f'<pre><code>{esc(install)}</code></pre>' if install else f'<p class="note">{esc(t(lang, "no_install"))}</p>'

    out += f"""<section class="skill-head" {stage_style(stage)}><div class="wrap">
  <div class="crumbs"><a href="{rel}{page_path('home', lang)}">{t(lang,'hub')}</a> /
    <a href="{rel}{page_path('home', lang)}#skills">{t(lang,'nav_catalogue')}</a> /
    <span class="current">{esc(s.get('id'))}</span></div>
  <h1>{esc(title)}</h1>
  <p class="sub">{esc(sub or '')}</p>
  <div class="meta-row">
    <span class="code">{esc(s.get('id'))}</span>
    {type_badge(s.get('type'), lang)}
    {badge(s.get('maturity'), MATURITY if lang=='pt' else MATURITY_EN)}
    {badge(s.get('status'), STATUS if lang=='pt' else STATUS_EN)}
    <span class="badge stage">{esc(name)}</span>
    <span>v{esc(s.get('version') or '—')}</span><span>&middot;</span>
    <span>{esc(s.get('license') or t(lang,'pending_lic'))}</span>
  </div>
  <div class="skill-actions">
    <a class="btn" href="{esc(repo)}" rel="noopener">{esc(t(lang, 'skill_actions_repo'))} &nearr;</a>
    <a class="btn" href="{esc(pkg)}" rel="noopener">{esc(t(lang, 'skill_actions_path'))} &nearr;</a>
    <a class="btn primary" href="#install">{esc(t(lang, 'skill_actions_install'))}</a>
    <a class="btn" href="#cite">{esc(t(lang, 'skill_actions_cite'))}</a>
  </div>
  {f'<div class="stack" style="margin-top:14px">{icons}</div>' if icons else ''}
</div></section>

<main id="main" class="wrap"><div class="cols">
  <div>
    <h2 class="sec">{t(lang,'when_h')}</h2>
    <p>{esc(objective)}</p>
    {f'<div class="chips" {stage_style(stage)}>{feats_html}</div>' if feats_html else ''}

    {reqs_html}

    <h2 class="sec" id="install">{t(lang,'install_h')}</h2>
    {install_block}
    <ol class="steps install-steps">
      <li>{esc(t(lang,'install_s1'))}</li>
      <li>{esc(t(lang,'install_s2'))}</li>
      <li>{esc(t(lang,'install_s3'))}</li>
      <li>{esc(t(lang,'install_s4'))}</li>
    </ol>
    <p class="note">{t(lang,'install_hermes')}</p>
    <p class="note">{t(lang,'install_claude')}</p>
    <p class="note"><a href="{rel}{page_path('using', lang)}">{esc(t(lang,'install_guide'))} &rarr;</a></p>

    <h2 class="sec">{t(lang,'how')}</h2>
    {steps_html}

    <h2 class="sec">{t(lang,'evidence_h')}</h2>
    <p class="note">{esc(t(lang,'evidence_intro'))}</p>
    {evidence_list(s, dims or [], lang)}
    <p class="note">{esc(t(lang,'tested_note'))}
      {f'<a href="{esc(evidence_url(s))}" rel="noopener">tests/RESULTS.md &nearr;</a>' if s.get('evidence') else ''}</p>

    <h2 class="sec">{t(lang,'limits_h')}</h2>
    <p>{esc(limits or '—')}</p>

    <h2 class="sec">{t(lang,'authors_h')}</h2>
    <table class="authors-t">
      <thead><tr><th>{t(lang,'col_name')}</th><th>{t(lang,'col_aff')}</th><th>ORCID</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="note">{t(lang,'authors_note')}</p>
    <p class="note">{t(lang,'licence')}: <b>{esc(s.get('license') or '—')}</b></p>

    <h2 class="sec" id="cite">{t(lang,'cite_h')}</h2>
    <blockquote id="cite-text">{esc(cite or title)}</blockquote>
    <button class="btn" data-copy="cite-text" data-label="{esc(t(lang,'copy_cite'))}"
      data-done="{esc(t(lang,'copied'))}" style="margin-top:10px">{t(lang,'copy_cite')}</button>
    <p class="note">{('DOI: ' + esc(doi)) if doi else t(lang,'no_doi')}</p>
    <p class="note">{esc(t(lang, 'cite_note'))}</p>
    <details class="bibtex">
      <summary>{esc(t(lang, 'cite_bibtex'))}</summary>
      <pre><code id="bibtex-text">{esc(bibtex_of(s))}</code></pre>
      <button class="btn" data-copy="bibtex-text" data-label="{esc(t(lang,'copy_bibtex'))}"
        data-done="{esc(t(lang,'copied'))}">{t(lang,'copy_bibtex')}</button>
    </details>

    <h2 class="sec">{t(lang,'package_links_h')}</h2>
    <div class="pkg-links">{link_html or f'<p class="note">{t(lang,"no_repo")}</p>'}</div>
  </div>

  <aside class="side" aria-label="{t(lang,'factsheet')}">
    <div class="panel" {stage_style(stage)}>
      <h4>{t(lang,'factsheet')}</h4>
      <dl class="facts">
        <dt>{t(lang,'identifier')}</dt><dd>{esc(s.get('id'))}</dd>
        <dt>{t(lang,'type')}</dt><dd>{esc(type_label(s.get('type'), lang))}</dd>
        <dt>{t(lang,'stage')}</dt><dd style="font-weight:600">{esc(name)}</dd>
        <dt>{t(lang,'version')}</dt><dd>{esc(s.get('version') or '—')}</dd>
        <dt>{t(lang,'maturity')}</dt><dd>{esc(((MATURITY if lang=='pt' else MATURITY_EN).get(s.get('maturity')) or ['—'])[0])}</dd>
        <dt>{t(lang,'status')}</dt><dd>{esc(((STATUS if lang=='pt' else STATUS_EN).get(s.get('status')) or ['—'])[0])}</dd>
        <dt>{t(lang,'licence')}</dt><dd>{esc(s.get('license') or '—')}</dd>
        {f'<dt>{t(lang,"doi_version")}</dt><dd>{doi_cell(doi)}</dd>' if doi else ''}
        {f'<dt>{t(lang,"doi_concept")}</dt><dd>{doi_cell(s.get("doi_concept"))}</dd>' if s.get('doi_concept') else ''}
        <dt>{t(lang,'disc')}</dt><dd>{esc(', '.join((reg_disc.get(k) or {}).get(lang, k) for k in (s.get('disciplines') or [])) or '—')}</dd>
        <dt>{t(lang,'added')}</dt><dd>{esc(s.get('added') or '—')}</dd>
      </dl>
    </div>
    <div class="panel"><h4>{t(lang,'links')}</h4>
      {link_html or f'<p class="note">{t(lang,"no_repo")}</p>'}</div>
    <div class="panel"><h4>{t(lang,'keywords')}</h4>
      <p class="note">{esc(', '.join(s.get('keywords') or []) or '—')}</p></div>
  </aside>
</div></main>
"""
    out += site_footer(hub, lang, rel)
    return out


def render_roadmap(s: dict, hub: dict, stages: dict, lang: str, reg_disc: dict = None) -> str:
    """A roadmap record is not a package page: no version, DOI, citation, install or evidence."""
    rel = "../" if lang == "pt" else "../../"
    stage = stages.get(s.get("stage") or "")
    name = (stage or {}).get(lang) or "—"
    title = s.get("title_pt") if (lang == "pt" and s.get("title_pt")) else s.get("title")
    summary = s.get("summary_pt") if (lang == "pt" and s.get("summary_pt")) else s.get("summary")
    reg_disc = reg_disc or {}
    out = html_head(f"{title} — {site_name(hub, lang)}", t(lang, "roadmap_notice"), rel, lang,
                    hub, page="skill", slug=s.get("slug"), robots="noindex,follow",
                    jsonld={"@context": "https://schema.org", "@type": "CreativeWork",
                            "name": title, "identifier": s.get("id"),
                            "creativeWorkStatus": "UnderDevelopment",
                            "inLanguage": "pt-BR" if lang == "pt" else "en"})
    out += site_header(rel, lang, hub, page="skill", slug=s.get("slug"), active="catalogue")
    out += f"""<section class="skill-head" {stage_style(stage)}><div class="wrap">
  <div class="crumbs"><a href="{rel}{page_path('home', lang)}">{t(lang,'hub')}</a> /
    <a href="{rel}{page_path('home', lang)}#roadmap">{t(lang,'roadmap_h')}</a> /
    <span class="current">{esc(s.get('id'))}</span></div>
  <h1>{esc(title)}</h1>
  <div class="meta-row">
    <span class="code">{esc(s.get('id'))}</span>
    {type_badge(s.get('type'), lang)}
    <span class="badge plan">{esc(t(lang,'roadmap_badge'))}</span>
    <span class="badge stage">{esc(name)}</span>
  </div>
</div></section>
<main id="main" class="wrap"><div class="cols">
  <div>
    <p class="notice">{esc(t(lang,'roadmap_notice'))}</p>
    <h2 class="sec">{t(lang,'roadmap_documented')}</h2>
    <p>{esc(summary or t(lang,'roadmap_none'))}</p>
    <h2 class="sec">{t(lang,'disc')}</h2>
    <p>{esc(', '.join((reg_disc.get(k) or {}).get(lang, k) for k in (s.get('disciplines') or [])) or '—')}</p>
    <h2 class="sec">{t(lang,'roadmap_paths')}</h2>
    <p>{esc(', '.join(s.get('paths') or []) or '—')}</p>
    <h2 class="sec">{t(lang,'roadmap_deps')}</h2>
    <p>{esc(t(lang,'roadmap_deps_none'))}</p>
    <p style="margin-top:28px"><a class="btn primary" href="{rel}{page_path('contribute', lang)}">{t(lang,'hero_cta_contribute')}</a></p>
  </div>
  <aside class="side">
    <div class="panel" {stage_style(stage)}>
      <h4>{t(lang,'factsheet')}</h4>
      <dl class="facts">
        <dt>{t(lang,'identifier')}</dt><dd>{esc(s.get('id'))}</dd>
        <dt>{t(lang,'type')}</dt><dd>{esc(type_label(s.get('type'), lang))}</dd>
        <dt>{t(lang,'stage')}</dt><dd>{esc(name)}</dd>
        <dt>{t(lang,'status')}</dt><dd>{esc(t(lang,'roadmap_badge'))}</dd>
      </dl>
    </div>
  </aside>
</div></main>
"""
    out += site_footer(hub, lang, rel)
    return out



def render_contribute(hub: dict, lang: str) -> str:
    """A contribution journey that does not assume Git fluency and does not promise review."""
    rel = "" if lang == "pt" else "../"
    title = t(lang, "contrib_h")
    body = _fill(content.CONTRIBUTE[lang], lang, rel, hub)
    actions = (f'<p class="hero-actions" style="margin:-8px 0 26px">'
               f'<a class="btn primary" href="{rel}assets/downloads/skill-brief.md" download>'
               f'{esc(t(lang, "contrib_download"))}</a>'
               f'<a class="btn" href="{esc(hub.get("submission_url") or "")}">'
               f'{esc(t(lang, "contrib_guide"))}</a></p>')
    return render_static_page(
        hub, lang, "contribute", title, t(lang, "contrib_p"),
        t(lang, "contrib_p")[:150], actions + body, active="contribute")


def doi_cell(value: str) -> str:
    """A DOI is read and copied as one token: link it, and allow a break only after the slash."""
    v = (value or "").strip()
    if not v:
        return "—"
    if not v.startswith("10."):
        return esc(v)
    head, _, tail = v.partition("/")
    inner = f'{esc(head)}/<wbr>{esc(tail)}' if tail else esc(head)
    return (f'<a class="doi" href="https://doi.org/{esc(v)}" rel="noopener">{inner}</a>')

def sitemap(reg: dict, hub: dict) -> str:
    urls = []
    for lang in LANGS:
        for page in ("home", "concepts", "using", "evidence", "contribute", "about"):
            urls.append((canonical(page, lang, hub), "1.0" if page == "home" else "0.7"))
        for s in reg["skills"]:
            prio = "0.8" if s.get("status") == "available" else "0.4"
            urls.append((canonical("skill", lang, hub, s.get("slug")), prio))
    body = "\n".join(f"  <url><loc>{html.escape(u)}</loc><priority>{p}</priority></url>"
                     for u, p in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + "\n</urlset>\n")


def _write_html(path: Path, text: str) -> None:
    """Write generated HTML without trailing whitespace, so `git diff --check` stays clean."""
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")


def build(out: Path) -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    hub = reg.get("hub", {})
    stages = reg.get("stages", {})
    dims = reg.get("evidence_dimensions") or []

    for lang in LANGS:
        base = out if lang == "pt" else out / lang
        (base / "skills").mkdir(parents=True, exist_ok=True)
        _write_html(base / "index.html", render_index(reg, lang))
        _write_html(base / ("conceitos.html" if lang == "pt" else "concepts.html"),
                    render_concepts_page(hub, lang))
        _write_html(base / ("como-utilizar.html" if lang == "pt" else "using.html"),
                    render_using_page(hub, lang))
        _write_html(base / ("evidencias.html" if lang == "pt" else "evidence.html"),
                    render_evidence_page(reg, hub, lang))
        _write_html(base / "contribuir.html", render_contribute(hub, lang))
        _write_html(base / ("sobre.html" if lang == "pt" else "about.html"),
                    render_about_page(hub, lang))
        for s in reg["skills"]:
            _write_html(base / "skills" / f"{s['slug']}.html",
                        render_skill(s, hub, stages, lang, reg.get("disciplines") or {}, dims))

    (out / "assets").mkdir(parents=True, exist_ok=True)
    (out / "assets" / "style.css").write_text(css(), encoding="utf-8")
    (out / "assets" / "app.js").write_text(js(), encoding="utf-8")
    img = out / "assets" / "img"
    img.mkdir(parents=True, exist_ok=True)
    for f in ASSETS.glob("*"):
        if f.is_file():
            shutil.copy(f, img / f.name)
    fonts_src = ROOT / "assets" / "fonts"
    if fonts_src.exists():
        fonts_out = out / "assets" / "fonts"
        fonts_out.mkdir(parents=True, exist_ok=True)
        for f in fonts_src.glob("*.woff2"):
            shutil.copy(f, fonts_out / f.name)

    dl = out / "assets" / "downloads"
    dl.mkdir(parents=True, exist_ok=True)
    brief = ROOT / "templates" / "skill-brief.md"
    if brief.exists():
        shutil.copy(brief, dl / "skill-brief.md")

    (out / "api").mkdir(parents=True, exist_ok=True)
    (out / "api" / "registry.json").write_text(
        json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    (out / "sitemap.xml").write_text(sitemap(reg, hub), encoding="utf-8")
    (out / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + site_root(hub) + "sitemap.xml\n", encoding="utf-8")

    files = sorted(p for p in out.rglob("*") if p.is_file())
    digest = hashlib.sha256(b"".join(p.read_bytes() for p in files)).hexdigest()[:16]
    return {"files": len(files), "hash": digest, "skills": len(reg["skills"])}


def main(argv=None) -> int:
    global CSS_HASH
    CSS_HASH = _css_hash(css())
    ap = argparse.ArgumentParser(description="Build the Métodos Digitais hub.")
    ap.add_argument("--out", type=Path, default=ROOT / "site")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    out: Path = args.out
    if args.check:
        tmp = out.parent / ".site-check"
        if tmp.exists():
            shutil.rmtree(tmp)
        build(tmp)
        a = sorted((str(p.relative_to(tmp)), p.read_bytes()) for p in tmp.rglob("*") if p.is_file())
        b = sorted((str(p.relative_to(out)), p.read_bytes()) for p in out.rglob("*") if p.is_file())
        shutil.rmtree(tmp)
        ok = a == b
        print("site is up to date" if ok else "site is STALE — run scripts/build_site.py")
        return 0 if ok else 1

    info = build(out)
    print(f"built {info['files']} files for {info['skills']} skills into {out}")
    print(f"content hash: {info['hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
