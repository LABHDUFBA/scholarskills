"""Long-form editorial copy for the ScholarSkills hub.

Kept out of build_site.py so that changing a paragraph does not mean editing the
renderer. Every string here is display copy: identifiers, DOIs, counts and links
still come from registry/registry.json. Placeholders in braces are replaced by the
renderer with page-relative URLs.
"""

DIAGRAM_WIDE = """<svg class="dg dg-wide" viewBox="0 0 940 470" role="img" aria-labelledby="dg-title dg-desc">
  <title id="dg-title">{title}</title>
  <desc id="dg-desc">{desc}</desc>
  <defs>
    <marker id="dg-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="dg-head"/>
    </marker>
  </defs>
  <g class="dg-line">
    <path d="M245 95 H282 V165 H320" marker-end="url(#dg-arrow)"/>
    <path d="M245 315 H292 V205 H320" marker-end="url(#dg-arrow)"/>
    <path d="M560 160 H600 V90 H640" marker-end="url(#dg-arrow)"/>
    <path d="M640 120 H615 V225 H560" marker-end="url(#dg-arrow)"/>
    <path d="M560 245 H600 V320 H640" marker-end="url(#dg-arrow)"/>
    <path d="M640 350 H615 V255 H560" marker-end="url(#dg-arrow)"/>
    <path d="M440 265 V335" marker-end="url(#dg-arrow)"/>
    <path d="M320 420 H30 V95 H40" marker-end="url(#dg-arrow)"/>
  </g>
  <g class="dg-box"><rect x="40" y="40" width="205" height="110" rx="12"/>
    <text x="142" y="82" text-anchor="middle" class="dg-h">Pesquisador</text>
    <text x="142" y="105" text-anchor="middle" class="dg-t">problema, decisão</text>
    <text x="142" y="124" text-anchor="middle" class="dg-t">e supervisão humana</text></g>
  <g class="dg-box dg-agent"><rect x="320" y="130" width="240" height="135" rx="12"/>
    <text x="440" y="170" text-anchor="middle" class="dg-h">Agente</text>
    <text x="440" y="194" text-anchor="middle" class="dg-t">interpreta, decide,</text>
    <text x="440" y="213" text-anchor="middle" class="dg-t">age e verifica</text>
    <text x="440" y="240" text-anchor="middle" class="dg-t dg-small">ciclo com parada possível</text></g>
  <g class="dg-box"><rect x="640" y="40" width="220" height="110" rx="12"/>
    <text x="750" y="82" text-anchor="middle" class="dg-h">LLM</text>
    <text x="750" y="105" text-anchor="middle" class="dg-t">interpretação e geração</text>
    <text x="750" y="124" text-anchor="middle" class="dg-t">de linguagem</text></g>
  <g class="dg-box dg-skill"><rect x="40" y="285" width="205" height="110" rx="12"/>
    <text x="142" y="327" text-anchor="middle" class="dg-h">Skill</text>
    <text x="142" y="350" text-anchor="middle" class="dg-t">procedimento, critérios,</text>
    <text x="142" y="369" text-anchor="middle" class="dg-t">testes e limites</text></g>
  <g class="dg-box"><rect x="640" y="285" width="220" height="110" rx="12"/>
    <text x="750" y="327" text-anchor="middle" class="dg-h">Ferramentas</text>
    <text x="750" y="350" text-anchor="middle" class="dg-t">API, código, banco,</text>
    <text x="750" y="369" text-anchor="middle" class="dg-t">navegador</text></g>
  <g class="dg-box"><rect x="320" y="335" width="240" height="95" rx="12"/>
    <text x="440" y="372" text-anchor="middle" class="dg-h">Resultados e registros</text>
    <text x="440" y="396" text-anchor="middle" class="dg-t">saídas, evidências, proveniência</text></g>
  <g class="dg-label">
    <text x="250" y="88">{r_agent}</text>
    <text x="596" y="80">{agent_llm_in}</text>
    <text x="596" y="242">{agent_llm_out}</text>
    <text x="250" y="305">{skill_agent}</text>
    <text x="596" y="310">{agent_tool}</text>
    <text x="596" y="368">{tool_agent}</text>
    <text x="450" y="305">{agent_results}</text>
    <text x="22" y="300" class="dg-small" transform="rotate(-90 22 300)">{human_loop}</text>
  </g>
</svg>"""

DIAGRAM_TALL = """<svg class="dg dg-tall" viewBox="0 0 400 700" role="img" aria-labelledby="dg-title-m dg-desc-m">
  <title id="dg-title-m">{title}</title>
  <desc id="dg-desc-m">{desc}</desc>
  <defs>
    <marker id="dg-arrow-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="dg-head"/>
    </marker>
  </defs>
  <g class="dg-line">
    <path d="M200 100 V140" marker-end="url(#dg-arrow-m)"/>
    <path d="M120 280 V230" marker-end="url(#dg-arrow-m)"/>
    <path d="M280 230 V280" marker-start="url(#dg-arrow-m)" marker-end="url(#dg-arrow-m)"/>
    <path d="M200 230 V420" marker-end="url(#dg-arrow-m)"/>
    <path d="M200 505 V560" marker-end="url(#dg-arrow-m)"/>
    <path d="M65 600 H10 V60 H65" marker-end="url(#dg-arrow-m)"/>
  </g>
  <g class="dg-box"><rect x="65" y="20" width="270" height="80" rx="12"/>
    <text x="200" y="52" text-anchor="middle" class="dg-h">Pesquisador</text>
    <text x="200" y="76" text-anchor="middle" class="dg-t">problema, decisão e supervisão</text></g>
  <g class="dg-box dg-agent"><rect x="65" y="140" width="270" height="90" rx="12"/>
    <text x="200" y="172" text-anchor="middle" class="dg-h">Agente</text>
    <text x="200" y="196" text-anchor="middle" class="dg-t">interpreta, decide, age, verifica</text>
    <text x="200" y="216" text-anchor="middle" class="dg-t dg-small">ciclo com parada possível</text></g>
  <g class="dg-box dg-skill"><rect x="30" y="280" width="140" height="95" rx="12"/>
    <text x="100" y="312" text-anchor="middle" class="dg-h">Skill</text>
    <text x="100" y="335" text-anchor="middle" class="dg-t">procedimento,</text>
    <text x="100" y="354" text-anchor="middle" class="dg-t">critérios, limites</text></g>
  <g class="dg-box"><rect x="230" y="280" width="140" height="95" rx="12"/>
    <text x="300" y="312" text-anchor="middle" class="dg-h">LLM</text>
    <text x="300" y="335" text-anchor="middle" class="dg-t">interpretação</text>
    <text x="300" y="354" text-anchor="middle" class="dg-t">e geração</text></g>
  <g class="dg-box"><rect x="65" y="420" width="270" height="85" rx="12"/>
    <text x="200" y="452" text-anchor="middle" class="dg-h">Ferramentas</text>
    <text x="200" y="476" text-anchor="middle" class="dg-t">API, código, banco, navegador</text></g>
  <g class="dg-box"><rect x="65" y="560" width="270" height="85" rx="12"/>
    <text x="200" y="592" text-anchor="middle" class="dg-h">Resultados e registros</text>
    <text x="200" y="616" text-anchor="middle" class="dg-t">saídas, evidências, proveniência</text></g>
  <g class="dg-label">
    <text x="208" y="125">{r_agent}</text>
    <text x="128" y="258">{skill_agent}</text>
    <text x="288" y="258">{agent_llm}</text>
    <text x="208" y="408">{agent_tool}</text>
    <text x="208" y="540">{agent_results}</text>
    <text x="14" y="350" class="dg-small" transform="rotate(-90 14 350)">{human_loop}</text>
  </g>
</svg>"""

CONCEPTS = {
"pt": """
<p class="lede-p">A utilização de inteligência artificial na pesquisa científica não se limita à interação com modelos de linguagem por meio de prompts. Sistemas agênticos articulam modelos, mecanismos de coordenação, recursos procedimentais e ferramentas computacionais. Compreender esses componentes ajuda a entender como procedimentos de pesquisa podem ser documentados e mobilizados por agentes de IA, sob supervisão humana.</p>

<div class="prose">
<h3>Modelos de linguagem de grande escala (LLMs): interpretação e geração</h3>
<p>Modelos de linguagem de grande escala (<i>Large Language Models</i>, LLMs) são modelos de inteligência artificial treinados para processar e gerar linguagem. Alguns incorporam capacidades multimodais, permitindo também trabalhar com imagens, áudio e outros tipos de dados. Em sistemas agênticos, esses modelos podem interpretar instruções, gerar propostas de ação e selecionar operações, conforme os recursos disponibilizados pelo sistema. Exemplos: famílias GPT, Claude, Qwen e Llama.</p>

<h3>Agentes de IA: coordenação de tarefas</h3>
<p>Um agente é um sistema que utiliza um ou mais modelos de IA para perseguir objetivos por meio de etapas de decisão e ação. Conforme sua arquitetura, pode manter estado, recuperar informações, consultar ferramentas, avaliar resultados e solicitar intervenção humana. Exemplos de ambientes agênticos: Hermes Agent e Claude Code. Autonomia não é sinônimo de confiabilidade.</p>

<h3>Skills: conhecimento procedimental reutilizável</h3>
<p>Uma skill é um pacote de instruções e recursos que orienta um agente na execução de uma tarefa delimitada. Pode reunir procedimentos, critérios de decisão, referências, scripts, exemplos e testes. Diferentemente de uma instrução pontual, pode ser organizada, versionada, distribuída e reutilizada em diferentes tarefas e ambientes compatíveis. Prompts podem fazer parte de uma skill; plugins podem disponibilizar recursos utilizados por ela. Não são categorias necessariamente excludentes.</p>

<h3>Ferramentas: recursos de execução</h3>
<p>Ferramentas são interfaces ou recursos que permitem ao agente realizar operações específicas, como executar código Python, consultar uma API, recuperar referências no Zotero ou buscar dados no Elasticsearch. A ferramenta disponibiliza uma operação; a skill pode orientar sua seleção, seu uso e os critérios de verificação.</p>
</div>

<p class="callout"><b>Síntese didática:</b> o modelo interpreta e gera, o agente coordena, a skill orienta e a ferramenta executa operações. Trata-se de uma simplificação: as funções podem se sobrepor conforme a arquitetura.</p>

<figure class="diagram-figure">
{diagram_wide}
{diagram_tall}
<figcaption>O pesquisador define o problema, supervisiona e pode interromper o ciclo. O agente carrega a skill, consulta o modelo e opera ferramentas; a skill não chama a ferramenta por conta própria. Resultados e registros voltam ao pesquisador para interpretação e validação.</figcaption>
</figure>

<h2 class="sec-h">O que é uma skill científica no ScholarSkills?</h2>
<div class="prose">
<p>No ScholarSkills, uma skill científica é um pacote documentado que operacionaliza procedimentos metodológicos ou atividades de apoio à pesquisa. A proposta editorial do projeto acrescenta ao formato técnico de Agent Skills requisitos de fundamentação, transparência, avaliação, atribuição de autoria e explicitação de limites.</p>
<p>Uma skill deve declarar, conforme sua finalidade: objetivo e condições de uso; entradas e saídas; requisitos e permissões; procedimento e critérios de parada; referências verificáveis; testes e evidências; limites metodológicos, éticos e legais; versão, licença, autoria e citação quando disponível.</p>
<p class="callout">A operacionalização de um procedimento não garante validade científica nem transforma resultados em evidências confiáveis automaticamente. A responsabilidade pelo desenho, interpretação e avaliação da pesquisa permanece humana.</p>
</div>

<h2 class="sec-h">Exemplo concreto: Zotero (SS-0001)</h2>
<div class="example-box">
<p>Um pesquisador solicita uma exportação das referências de uma coleção. O agente interpreta o pedido usando um LLM, consulta a skill <a href="{skill_zotero}">SS-0001</a> para identificar o procedimento e as condições de acesso, utiliza a API do Zotero com permissões adequadas e entrega os registros para conferência. A qualidade das referências e sua adequação à pesquisa continuam sujeitas à avaliação humana.</p>
<p class="note"><b>Exemplo ilustrativo.</b> Não é o relato de um teste executado nesta revisão.</p>
</div>

<h2 class="sec-h">Base normativa e terminológica</h2>
<div class="prose">
<p>A <a href="https://agentskills.io/specification" rel="noopener">especificação aberta Agent Skills</a> define o formato técnico mínimo: um arquivo <code>SKILL.md</code> com frontmatter YAML contendo <code>name</code> e <code>description</code>, além de recursos opcionais. O ScholarSkills acrescenta requisitos editoriais e científicos próprios, descritos na <a href="{policy}">política editorial</a>.</p>
<p>README, DOI, testes, revisão por pares e <code>CITATION.cff</code> não são exigências universais da especificação: são escolhas deste projeto para tornar a proveniência e a avaliação explícitas.</p>
</div>
<p class="page-back"><a href="{catalogue}">Explorar o catálogo</a></p>
""",
"en": """
<p class="lede-p">The use of artificial intelligence in scientific research is not limited to interacting with language models through prompts. Agentic systems combine models, coordination mechanisms, procedural resources and computational tools. Understanding these components helps explain how research procedures can be documented and mobilised by AI agents under human supervision.</p>

<div class="prose">
<h3>Large language models (LLMs): interpretation and generation</h3>
<p>Large language models are AI models trained to process and generate language. Some add multimodal capabilities and can also work with images, audio and other data types. In agentic systems, these models can interpret instructions, propose actions and select operations according to the resources the system makes available. Examples: the GPT, Claude, Qwen and Llama families.</p>

<h3>AI agents: task coordination</h3>
<p>An agent is a system that uses one or more AI models to pursue goals through steps of decision and action. Depending on its architecture, it can keep state, retrieve information, call tools, evaluate results and request human intervention. Examples of agent environments: Hermes Agent and Claude Code. Autonomy is not the same as reliability.</p>

<h3>Skills: reusable procedural knowledge</h3>
<p>A skill is a package of instructions and resources that guides an agent through a bounded task. It may combine procedures, decision criteria, references, scripts, examples and tests. Unlike a one-off instruction, it can be organised, versioned, distributed and reused across tasks and compatible environments. Prompts may be part of a skill; plugins may provide resources a skill uses. The categories are not mutually exclusive.</p>

<h3>Tools: execution resources</h3>
<p>Tools are interfaces or resources that let the agent perform specific operations, such as running Python code, querying an API, retrieving Zotero references or searching Elasticsearch. The tool exposes an operation; the skill can guide its selection, use and verification criteria.</p>
</div>

<p class="callout"><b>Teaching summary:</b> the model interprets and generates, the agent coordinates, the skill guides and the tool executes operations. This is a simplification: the functions can overlap depending on the architecture.</p>

<figure class="diagram-figure">
{diagram_wide}
{diagram_tall}
<figcaption>The researcher frames the problem, supervises and can stop the cycle. The agent loads the skill, consults the model and operates tools; the skill does not call the tool on its own. Results and records return to the researcher for interpretation and validation.</figcaption>
</figure>

<h2 class="sec-h">What is a scientific skill in ScholarSkills?</h2>
<div class="prose">
<p>In ScholarSkills, a scientific skill is a documented package that operationalises methodological procedures or research-support activities. The project's editorial proposal adds requirements of grounding, transparency, assessment, authorship and explicit limits to the technical Agent Skills format.</p>
<p>A skill should state, as its purpose requires: objective and conditions of use; inputs and outputs; requirements and permissions; procedure and stop criteria; verifiable references; tests and evidence; methodological, ethical and legal limits; version, licence, authorship and citation when available.</p>
<p class="callout">Operationalising a procedure does not guarantee scientific validity, nor does it automatically turn results into reliable evidence. Responsibility for research design, interpretation and assessment remains human.</p>
</div>

<h2 class="sec-h">A concrete example: Zotero (SS-0001)</h2>
<div class="example-box">
<p>A researcher asks for an export of the references in a collection. The agent interprets the request with an LLM, consults skill <a href="{skill_zotero}">SS-0001</a> for the procedure and access conditions, uses the Zotero API with adequate permissions and returns the records for checking. The quality of the references and their fit to the research remain subject to human assessment.</p>
<p class="note"><b>Illustrative example.</b> It is not a report of a test run in this revision.</p>
</div>

<h2 class="sec-h">Normative and terminological basis</h2>
<div class="prose">
<p>The open <a href="https://agentskills.io/specification" rel="noopener">Agent Skills specification</a> defines the minimum technical format: a <code>SKILL.md</code> file with YAML frontmatter containing <code>name</code> and <code>description</code>, plus optional resources. ScholarSkills adds its own editorial and scientific requirements, described in the <a href="{policy}">editorial policy</a>.</p>
<p>README, DOI, tests, peer review and <code>CITATION.cff</code> are not universal requirements of the specification: they are this project's choices for making provenance and assessment explicit.</p>
</div>
<p class="page-back"><a href="{catalogue}">Browse the catalogue</a></p>
""",
}

USING = {
"pt": """
<h2 class="sec-h">Antes de começar</h2>
<div class="prose">
<p>Uma skill não é um programa que se instala e roda sozinho. Ela é um conjunto de instruções e, às vezes, de scripts que um agente lê para conduzir uma tarefa. Instalar uma skill significa colocá-la onde o agente procura por skills; usá-la significa pedir ao agente que a consulte e conferir o que ele fez.</p>
<p>Você precisa de três coisas: <b>Python 3.10 ou superior</b> para os pacotes que trazem scripts, <b>Git</b> para obter o repositório e um <b>agente compatível com Agent Skills</b>. Algumas skills pedem rede ou credenciais próprias; a página de cada pacote lista o que é obrigatório e o que é condicional.</p>
</div>

<h2 class="sec-h">1. Escolha o ambiente</h2>
<div class="prose">
<p><b>Hermes Agent.</b> Skills ficam em <code>$HERMES_HOME/skills/</code>, por padrão <code>~/.hermes/skills/</code>. Depois de copiar um pacote, comece uma sessão nova e confira com <code>hermes skills list</code>; dentro da sessão, <code>/skills</code> lista e <code>/skill &lt;nome&gt;</code> carrega uma skill.</p>
<p><b>Claude Code.</b> Skills pessoais ficam em <code>~/.claude/skills/&lt;nome&gt;/SKILL.md</code> e valem em todos os projetos; skills de projeto ficam em <code>.claude/skills/</code> na raiz do repositório. O nome do diretório se torna o comando <code>/nome</code>.</p>
<p><b>Outro ambiente compatível.</b> Siga a <a href="https://agentskills.io/specification" rel="noopener">especificação Agent Skills</a> do próprio ambiente. Não presuma que o caminho de um agente vale para outro.</p>
</div>

<h2 class="sec-h">2. Obtenha o pacote</h2>
<div class="prose"><p>O repositório reúne todas as skills. Para uma skill isolada, copie apenas o diretório dela.</p></div>
<pre><code>git clone https://github.com/LABHDUFBA/scholarskills.git
cd scholarskills</code></pre>

<h2 class="sec-h">3. Ative a skill no agente</h2>
<div class="prose"><p><b>Hermes Agent:</b></p></div>
<pre><code>mkdir -p ~/.hermes/skills
cp -R zotero-reference-management ~/.hermes/skills/</code></pre>
<div class="prose"><p><b>Claude Code (pessoal):</b></p></div>
<pre><code>mkdir -p ~/.claude/skills
cp -R zotero-reference-management ~/.claude/skills/</code></pre>

<h2 class="sec-h">4. Verifique se a skill foi reconhecida</h2>
<div class="prose">
<p>Copiar arquivos não prova ativação. No Hermes, <code>hermes skills list</code> deve mostrar o nome da skill; em uma sessão nova, peça: <i>“Liste as skills disponíveis e diga quando você usaria a skill zotero-reference-management.”</i> No Claude Code, o nome do diretório aparece como <code>/zotero-reference-management</code>.</p>
<p>Se a skill não aparecer, confira três coisas: o arquivo <code>SKILL.md</code> está na raiz do diretório copiado; o frontmatter tem <code>name</code> e <code>description</code> válidos; a sessão foi iniciada depois da cópia.</p>
</div>

<h2 class="sec-h">5. Configure requisitos com cuidado</h2>
<div class="prose">
<p>Leia a seção <b>Requisitos</b> da skill. Separe o que é obrigatório do que é condicional, e não instale dependências globais: use um ambiente virtual.</p>
</div>
<pre><code>cd zotero-reference-management
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt</code></pre>
<div class="prose">
<p>Credenciais vão em variáveis de ambiente ou em um arquivo <code>.env</code> que nunca é versionado. Não cole chaves em prompts, exemplos, capturas de tela ou arquivos do repositório. Conceda à chave o menor escopo que resolve a tarefa.</p>
</div>

<h2 class="sec-h">6. Execute um exemplo seguro</h2>
<div class="prose">
<p>Comece pelo exemplo que o pacote documenta, de preferência um que rode com dados sintéticos ou fixtures e sem rede. Peça ao agente que mostre o comando antes de executar e que registre a saída. Operações de escrita em serviços reais exigem confirmação explícita.</p>
</div>

<h2 class="sec-h">7. Leia a evidência antes de confiar</h2>
<div class="prose">
<p>Testes verdes provam que o código faz o que o teste descreve, não que o método é adequado à sua pesquisa. A página <a href="{evidence}">Evidências e maturidade</a> explica as dimensões e mostra o que cada pacote registra. O <code>tests/RESULTS.md</code> do pacote traz ambiente, comando e resultado.</p>
</div>

<h2 class="sec-h">8. Cite a versão que usou</h2>
<div class="prose">
<p>Quando existe DOI de versão, cite esse DOI para a execução específica e explique o DOI de conceito como o registro que reúne as versões. A ficha de cada skill traz a citação pronta e os dois identificadores, quando existem.</p>
</div>

<h2 class="sec-h">O que esta revisão testou</h2>
<div class="prose">
<p>Esta revisão verificou o build estático, os links internos e a validação estrutural dos pacotes. Não testou a ativação em Hermes Agent ou Claude Code, chamadas reais às APIs externas, todos os sistemas operacionais nem a adequação científica de cada método. O relatório da revisão registra o que passou, o que falhou e o que não foi executado.</p>
</div>
<p class="page-back"><a href="{catalogue}">Ver as skills disponíveis</a></p>
""",
"en": """
<h2 class="sec-h">Before you start</h2>
<div class="prose">
<p>A skill is not a program that installs and runs by itself. It is a set of instructions, sometimes with scripts, that an agent reads to carry out a task. Installing a skill means placing it where the agent looks for skills; using it means asking the agent to consult it and checking what the agent did.</p>
<p>You need three things: <b>Python 3.10 or newer</b> for packages with scripts, <b>Git</b> to obtain the repository and an <b>Agent Skills-compatible agent</b>. Some skills need network access or their own credentials; each package page lists what is required and what is conditional.</p>
</div>

<h2 class="sec-h">1. Choose the environment</h2>
<div class="prose">
<p><b>Hermes Agent.</b> Skills live in <code>$HERMES_HOME/skills/</code>, by default <code>~/.hermes/skills/</code>. After copying a package, start a new session and check with <code>hermes skills list</code>; inside a session, <code>/skills</code> lists them and <code>/skill &lt;name&gt;</code> loads one.</p>
<p><b>Claude Code.</b> Personal skills live in <code>~/.claude/skills/&lt;name&gt;/SKILL.md</code> and apply to every project; project skills live in <code>.claude/skills/</code> at the repository root. The directory name becomes the <code>/name</code> command.</p>
<p><b>Other compatible environments.</b> Follow that environment's own implementation of the <a href="https://agentskills.io/specification" rel="noopener">Agent Skills specification</a>. Do not assume one agent's path applies to another.</p>
</div>

<h2 class="sec-h">2. Get the package</h2>
<div class="prose"><p>The repository holds every skill. For a single skill, copy only its directory.</p></div>
<pre><code>git clone https://github.com/LABHDUFBA/scholarskills.git
cd scholarskills</code></pre>

<h2 class="sec-h">3. Enable the skill in the agent</h2>
<div class="prose"><p><b>Hermes Agent:</b></p></div>
<pre><code>mkdir -p ~/.hermes/skills
cp -R zotero-reference-management ~/.hermes/skills/</code></pre>
<div class="prose"><p><b>Claude Code (personal):</b></p></div>
<pre><code>mkdir -p ~/.claude/skills
cp -R zotero-reference-management ~/.claude/skills/</code></pre>

<h2 class="sec-h">4. Check that the skill was recognised</h2>
<div class="prose">
<p>Copying files does not prove activation. In Hermes, <code>hermes skills list</code> should show the skill name; in a new session, ask: <i>“List the available skills and say when you would use zotero-reference-management.”</i> In Claude Code, the directory name appears as <code>/zotero-reference-management</code>.</p>
<p>If the skill does not appear, check three things: <code>SKILL.md</code> sits at the root of the copied directory; the frontmatter has valid <code>name</code> and <code>description</code>; the session started after the copy.</p>
</div>

<h2 class="sec-h">5. Configure requirements carefully</h2>
<div class="prose">
<p>Read the skill's <b>Requirements</b> section. Separate what is required from what is conditional, and do not install dependencies globally: use a virtual environment.</p>
</div>
<pre><code>cd zotero-reference-management
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt</code></pre>
<div class="prose">
<p>Credentials belong in environment variables or in a <code>.env</code> file that is never committed. Do not paste keys into prompts, examples, screenshots or repository files. Grant the key the smallest scope that solves the task.</p>
</div>

<h2 class="sec-h">6. Run a safe example</h2>
<div class="prose">
<p>Start with the example the package documents, preferably one that runs on synthetic data or fixtures without network access. Ask the agent to show the command before running it and to record the output. Write operations against real services require explicit confirmation.</p>
</div>

<h2 class="sec-h">7. Read the evidence before trusting it</h2>
<div class="prose">
<p>Green tests prove that the code does what the test describes, not that the method suits your research. The <a href="{evidence}">Evidence and maturity</a> page explains the dimensions and shows what each package records. The package's <code>tests/RESULTS.md</code> carries the environment, command and result.</p>
</div>

<h2 class="sec-h">8. Cite the version you used</h2>
<div class="prose">
<p>Where a version DOI exists, cite that DOI for the specific run and explain the concept DOI as the record that gathers the versions. Each skill page provides the ready citation and both identifiers where they exist.</p>
</div>

<h2 class="sec-h">What this revision tested</h2>
<div class="prose">
<p>This revision checked the static build, internal links and structural validation of the packages. It did not test activation in Hermes Agent or Claude Code, real calls to external APIs, every operating system or the scientific adequacy of each method. The revision report records what passed, what failed and what was not run.</p>
</div>
<p class="page-back"><a href="{catalogue}">See the available skills</a></p>
""",
}

EVIDENCE = {
"pt": """
<h2 class="sec-h">Evidência não é uma escada</h2>
<div class="prose">
<p>A versão anterior do portal apresentava quatro níveis em sequência: experimental, testado, revisão por pares, replicação. A sequência é útil como vocabulário, mas sugere que um pacote sobe degraus e que o degrau de cima cobre os de baixo. Não cobre. Um pacote pode ter testes funcionais sólidos e nenhuma avaliação metodológica; pode ser reexecutado por terceiros sem ter passado por revisão por pares.</p>
<p>Por isso o catálogo passa a tratar evidência como dimensões independentes. Nenhuma é promovida automaticamente; cada uma exige o artefato que a sustenta.</p>
</div>

<div class="dims">
{dimension_cards}
</div>

<p class="callout"><b>Reexecução não é replicação.</b> Reexecução computacional verifica se o mesmo código, no mesmo ambiente, produz o mesmo resultado. Replicação científica avalia se o achado se sustenta em novos dados ou em um novo estudo, segundo um protocolo definido. A distinção segue o relatório da NASEM, <a href="https://doi.org/10.17226/25303" rel="noopener"><i>Reproducibility and Replicability in Science</i></a> (2019), e o uso dos termos varia entre disciplinas.</p>

<h2 class="sec-h">O que cada pacote registra hoje</h2>
<div class="prose">
<p>A matriz abaixo é gerada a partir do registro do catálogo. “Registrado” significa que o artefato existe e está referenciado; “não registrado” não significa que a dimensão falhou, apenas que não há registro público que a sustente.</p>
</div>
<div class="table-wrap">
<table class="evidence-table">
<thead><tr><th scope="col">Skill</th>{dim_headers}</tr></thead>
<tbody>{evidence_rows}</tbody>
</table>
</div>

<h2 class="sec-h">Status editorial, DOI e evidência</h2>
<div class="prose">
<p>Status editorial (planejada, disponível, descontinuada) descreve a situação do registro no catálogo. Maturidade descreve o que foi documentado sobre o pacote. DOI identifica um depósito arquivado; não certifica qualidade científica. Um teste offline com fixtures não demonstra desempenho contra uma API real, e um teste de integração não demonstra que o agente conduz a tarefa de ponta a ponta.</p>
<p>Os testes registrados nos pacotes são, em sua maioria, automatizados e sem rede. Eles exercitam casos positivos, negativos e de borda do código; não substituem avaliação por pares nem reexecução independente. A <a href="{policy}">política editorial</a> define o que cada registro exige e como correções são versionadas.</p>
</div>
<p class="page-back"><a href="{catalogue}">Voltar ao catálogo</a></p>
""",
"en": """
<h2 class="sec-h">Evidence is not a ladder</h2>
<div class="prose">
<p>The previous version of the portal presented four levels in sequence: experimental, tested, peer-reviewed, replicated. The sequence is useful vocabulary, but it suggests that a package climbs steps and that the top step covers the ones below. It does not. A package can have solid functional tests and no methodological assessment; it can be re-executed by third parties without having been peer-reviewed.</p>
<p>The catalogue therefore treats evidence as independent dimensions. None is granted automatically; each requires the artefact that supports it.</p>
</div>

<div class="dims">
{dimension_cards}
</div>

<p class="callout"><b>Re-execution is not replication.</b> Computational re-execution checks whether the same code, in the same environment, produces the same result. Scientific replication assesses whether the finding holds on new data or in a new study under a defined protocol. The distinction follows the NASEM report <a href="https://doi.org/10.17226/25303" rel="noopener"><i>Reproducibility and Replicability in Science</i></a> (2019); terminology varies across disciplines.</p>

<h2 class="sec-h">What each package records today</h2>
<div class="prose">
<p>The matrix below is generated from the catalogue registry. “Recorded” means the artefact exists and is referenced; “not recorded” does not mean the dimension failed, only that no public record supports it.</p>
</div>
<div class="table-wrap">
<table class="evidence-table">
<thead><tr><th scope="col">Skill</th>{dim_headers}</tr></thead>
<tbody>{evidence_rows}</tbody>
</table>
</div>

<h2 class="sec-h">Editorial status, DOI and evidence</h2>
<div class="prose">
<p>Editorial status (planned, available, deprecated) describes the record's situation in the catalogue. Maturity describes what has been documented about the package. A DOI identifies an archived deposit; it does not certify scientific quality. An offline test with fixtures does not demonstrate performance against a real API, and an integration test does not demonstrate that the agent conducts the task end to end.</p>
<p>The tests recorded in the packages are mostly automated and offline. They exercise positive, negative and edge cases of the code; they do not replace peer review or independent re-execution. The <a href="{policy}">editorial policy</a> defines what each record requires and how corrections are versioned.</p>
</div>
<p class="page-back"><a href="{catalogue}">Back to the catalogue</a></p>
""",
}

ABOUT = {
"pt": """
<h2 class="sec-h">Escopo</h2><div class="prose">
<p>O ScholarSkills é um repositório acadêmico aberto de skills para agentes de IA, mantido pelo Laboratório de Humanidades Digitais da Universidade Federal da Bahia (LABHDUFBA), no âmbito da iniciativa Métodos Digitais. Reúne pacotes que operacionalizam procedimentos de pesquisa ou atividades de apoio à pesquisa, com documentação, testes, limites e autoria explícitos.</p>
<p>O catálogo não é um diretório de prompts nem uma loja de plugins. A inclusão de um pacote não implica revisão por pares, replicação ou endosso institucional de seus resultados.</p>
</div>

<h2 class="sec-h">Equipe</h2>
<div class="prose"><p>Coordenação e coautoria estão nomeadas na seção de autoria da página inicial, com afiliação e ORCID quando fornecido. A autoria de cada pacote aparece na respectiva página; nem todas as pessoas do projeto assinam todas as skills.</p></div>

<h2 class="sec-h">Governança e política editorial</h2>
<div class="prose">
<p>A <a href="{policy}">política editorial</a> define o conteúdo exigido de uma submissão, as dimensões de evidência, os critérios de revisão e o procedimento de correção e retirada. Duas pessoas revisam cada submissão e registram o veredito; a política vigente é preservada até revisão formal pelos responsáveis. O parecer humano não é substituído por LLM.</p>
<p>Depósitos em DOI exigem autorização explícita dos mantenedores. Uma alteração no branch principal não atualiza um registro arquivado no Zenodo.</p>
</div>

<h2 class="sec-h">Como citar</h2>
<div class="prose">
<p>Para o catálogo, use o <code>CITATION.cff</code> do repositório e o DOI de conceito do projeto. Para uma skill específica, use o DOI de versão indicado na página do pacote, quando existir. O DOI de conceito identifica o registro que reúne as versões; o DOI de versão identifica a execução que você usou.</p>
</div>

<h2 class="sec-h">Licenças e direitos</h2>
<div class="prose">
<p>O código e a documentação originais do projeto usam MIT, conforme o <code>LICENSE</code> da raiz e os arquivos de licença de cada pacote. Fontes, logotipos, marcas e imagens de terceiros podem ter termos próprios; a presença neste repositório não concede direitos MIT sobre eles. Dados externos mantêm a licença da fonte.</p>
</div>

<h2 class="sec-h">Acessibilidade</h2>
<div class="prose">
<p>O portal tem como objetivo de engenharia o nível AA das <a href="https://www.w3.org/TR/WCAG22/" rel="noopener">WCAG 2.2</a>: contraste, foco visível, navegação por teclado, texto alternativo, reflow e respeito à redução de movimento. Isso não é uma certificação: não houve auditoria externa de acessibilidade. Problemas podem ser relatados pelo contato abaixo.</p>
</div>

<h2 class="sec-h">Contato</h2>
<div class="prose"><p>Para propor uma skill, relatar um problema ou pedir esclarecimento: <a href="mailto:{email}">{email}</a>. O repositório fica em <a href="{repo}" rel="noopener">github.com/LABHDUFBA/scholarskills</a>.</p></div>

<h2 class="sec-h">Histórico e transparência</h2>
<div class="prose">
<p>Decisões de implementação e depósito anteriores estão registradas no <code>DEPLOYMENT_LOG.md</code> do repositório; entradas antigas descrevem estados passados. O portal não usa rastreamento, cookies ou telemetria. O catálogo legível por máquina está em <a href="{registry}">registry.json</a>.</p>
</div>
""",
"en": """
<h2 class="sec-h">Scope</h2>
<div class="prose">
<p>ScholarSkills is an open academic repository of skills for AI agents, maintained by the Digital Humanities Laboratory of the Federal University of Bahia (LABHDUFBA) within the Métodos Digitais initiative. It gathers packages that operationalise research procedures or research-support activities, with explicit documentation, tests, limits and authorship.</p>
<p>The catalogue is neither a prompt directory nor a plugin store. Inclusion does not imply peer review, replication or institutional endorsement of a package's results.</p>
</div>

<h2 class="sec-h">Team</h2>
<div class="prose"><p>Coordination and co-authorship are named in the authorship section of the home page, with affiliation and ORCID when provided. Each package page states its own authorship; not every person in the project signs every skill.</p></div>

<h2 class="sec-h">Governance and editorial policy</h2>
<div class="prose">
<p>The <a href="{policy}">editorial policy</a> defines what a submission must contain, the evidence dimensions, the review criteria and the correction and withdrawal procedure. Two people review each submission and record a verdict; the current policy is preserved until the maintainers formally revise it. Human review is not replaced by an LLM.</p>
<p>DOI deposits require explicit authorisation from the maintainers. A change on the main branch does not update an archived Zenodo record.</p>
</div>

<h2 class="sec-h">How to cite</h2>
<div class="prose">
<p>For the catalogue, use the repository's <code>CITATION.cff</code> and the project's concept DOI. For a specific skill, use the version DOI shown on the package page where one exists. The concept DOI identifies the record that gathers the versions; the version DOI identifies the run you used.</p>
</div>

<h2 class="sec-h">Licences and rights</h2>
<div class="prose">
<p>The project's original code and documentation use MIT, per the root <code>LICENSE</code> and each package's licence file. Third-party fonts, logos, trademarks and images may carry their own terms; presence in this repository does not grant MIT rights over them. External data keeps its source licence.</p>
</div>

<h2 class="sec-h">Accessibility</h2>
<div class="prose">
<p>The portal targets WCAG 2.2 level AA as an engineering goal: contrast, visible focus, keyboard navigation, alternative text, reflow and respect for reduced motion. This is not a certification: no external accessibility audit has been carried out. Problems can be reported through the contact below.</p>
</div>

<h2 class="sec-h">Contact</h2>
<div class="prose"><p>To propose a skill, report a problem or ask for clarification: <a href="mailto:{email}">{email}</a>. The repository is at <a href="{repo}" rel="noopener">github.com/LABHDUFBA/scholarskills</a>.</p></div>

<h2 class="sec-h">History and transparency</h2>
<div class="prose">
<p>Earlier implementation and deposit decisions are recorded in the repository's <code>DEPLOYMENT_LOG.md</code>; older entries describe past states. The portal uses no tracking, cookies or telemetry. The machine-readable catalogue is at <a href="{registry}">registry.json</a>.</p>
</div>
""",
}


CONTRIBUTE = {
"pt": """
<h2 class="sec-h">Três caminhos para propor uma skill</h2>
<div class="prose">
<p>Você não precisa saber usar Git para começar, e não precisa escrever código sozinho. A preparação pode ser feita com um agente; a decisão editorial continua humana.</p>
</div>
<ol class="csteps">
  <li><div class="cstep"><span class="cnum">1</span><div>
    <b>Prepare o pacote com um agente</b>
    <p>Baixe o brief em Markdown e peça ao seu agente que preencha o que você sabe. Campo vazio é pergunta a fazer, não lacuna a inventar. O protocolo <a href="{skill_ss0000}">SS-0000</a> pode apoiar a preparação e a validação estrutural; ele não substitui a conferência humana nem a revisão editorial.</p>
  </div></div></li>
  <li><div class="cstep"><span class="cnum">2</span><div>
    <b>Abra um pull request</b>
    <p>Um pacote por pull request, com uma entrada nova em <code>registry/registry.json</code>. Proponha o identificador <code>SS-NNNN</code> na descrição; os mantenedores atribuem o definitivo. Rode o validador e os testes do pacote antes de enviar.</p>
    <p style="margin:8px 0 0"><a href="{guide}">Ler o guia de contribuição</a></p>
  </div></div></li>
  <li><div class="cstep"><span class="cnum">3</span><div>
    <b>Não usa Git? Peça orientação</b>
    <p>Escreva para o laboratório e descreva a skill que quer propor. A equipe orienta o formato e indica um caminho de envio; não há promessa de submissão por e-mail nem de aceitação automática.</p>
  </div></div></li>
</ol>

<h2 class="sec-h">O que a revisão verifica</h2>
<ul class="creqs">
  <li>O problema, a etapa da pesquisa e a disciplina a que a skill serve estão declarados.</li>
  <li>Todo requisito de execução está listado: credencial, variável de ambiente, software, rede.</li>
  <li>Existe seção de limites: o que a skill não faz e o que ela não prova.</li>
  <li>Os testes rodam offline e <code>tests/RESULTS.md</code> traz ambiente, comando e saída reais; integração com serviços reais, quando existir, é documentada à parte.</li>
  <li>Nenhuma credencial, caminho local ou dado pessoal no pacote.</li>
  <li>A licença e a autoria estão explícitas, e a citação corresponde ao registro real.</li>
</ul>

<h2 class="sec-h">Como a revisão acontece</h2>
<div class="prose">
<p>Primeiro, uma triagem estrutural: o pacote valida contra o esquema do catálogo e contra a especificação Agent Skills. Depois, duas pessoas aplicam os critérios da <a href="{policy}">política editorial</a> e registram um veredito por dimensão. A decisão pode ser aceitar, devolver com correções ou recusar; o parecer é registrado, e a resposta do autor fica no pull request.</p>
<p>Correções depois da publicação geram uma versão nova, com entrada no <code>CHANGELOG.md</code>. Depósitos em DOI exigem autorização explícita dos mantenedores. A revisão interna do projeto não é apresentada como avaliação por órgão externo.</p>
</div>

<h2 class="sec-h">Contato</h2>
<div class="prose"><p>Para propor uma skill, relatar um problema ou pedir orientação: <a href="mailto:{email}">{email}</a>.</p></div>
<p class="page-back"><a href="{catalogue}">Ver o catálogo</a></p>
""",
"en": """
<h2 class="sec-h">Three ways to propose a skill</h2>
<div class="prose">
<p>You do not need to know Git to start, and you do not need to write code alone. Preparation can be done with an agent; the editorial decision remains human.</p>
</div>
<ol class="csteps">
  <li><div class="cstep"><span class="cnum">1</span><div>
    <b>Prepare the package with an agent</b>
    <p>Download the Markdown brief and ask your agent to fill in what you know. An empty field is a question to ask, not a gap to invent. Protocol <a href="{skill_ss0000}">SS-0000</a> can support preparation and structural validation; it does not replace human checking or editorial review.</p>
  </div></div></li>
  <li><div class="cstep"><span class="cnum">2</span><div>
    <b>Open a pull request</b>
    <p>One package per pull request, with one new entry in <code>registry/registry.json</code>. Propose the <code>SS-NNNN</code> identifier in the description; maintainers assign the final one. Run the package validator and tests before submitting.</p>
    <p style="margin:8px 0 0"><a href="{guide}">Read the contribution guide</a></p>
  </div></div></li>
  <li><div class="cstep"><span class="cnum">3</span><div>
    <b>Do not use Git? Ask for guidance</b>
    <p>Write to the laboratory and describe the skill you want to propose. The team advises on the format and points to a submission route; there is no promise of email submission or automatic acceptance.</p>
  </div></div></li>
</ol>

<h2 class="sec-h">What review checks</h2>
<ul class="creqs">
  <li>The problem, the research stage and the discipline the skill serves are stated.</li>
  <li>Every execution requirement is listed: credential, environment variable, software, network.</li>
  <li>A limits section exists: what the skill does not do and does not prove.</li>
  <li>Tests run offline and <code>tests/RESULTS.md</code> carries the real environment, command and output; integration with real services, where it exists, is documented separately.</li>
  <li>No credential, local path or personal data in the package.</li>
  <li>Licence and authorship are explicit, and the citation matches the real record.</li>
</ul>

<h2 class="sec-h">How review happens</h2>
<div class="prose">
<p>First, a structural triage: the package validates against the catalogue schema and the Agent Skills specification. Then two people apply the <a href="{policy}">editorial policy</a> criteria and record a verdict per dimension. The decision can be accept, return for corrections or reject; the report is recorded, and the author's response stays in the pull request.</p>
<p>Corrections after publication produce a new version with a <code>CHANGELOG.md</code> entry. DOI deposits require explicit authorisation from the maintainers. The project's internal review is not presented as assessment by an external body.</p>
</div>

<h2 class="sec-h">Contact</h2>
<div class="prose"><p>To propose a skill, report a problem or ask for guidance: <a href="mailto:{email}">{email}</a>.</p></div>
<p class="page-back"><a href="{catalogue}">See the catalogue</a></p>
""",
}
