# Brief para uma nova skill — Skills Métodos Digitais

> **Como usar.** Preencha este arquivo e entregue ao seu agente de IA junto com o link do protocolo
> `SS-0000`: <https://labhdufba.github.io/scholarskills/skills/scientific-agent-skill-development.html>
> O agente tem o método completo; este arquivo diz **o que** construir. Campo em branco é campo a
> descobrir na conversa — não invente para preencher.
>
> O resultado esperado é um diretório de skill com `SKILL.md`, testes que rodam offline, `README.md`
> e `README.pt-BR.md`, `CITATION.cff`, `CHANGELOG.md` e `tests/RESULTS.md` com a saída real.

---

## 1. Identificação

- **Nome provisório:**
- **Área do conhecimento:**
- **Etapa da pesquisa que atende** (fundamentação · revisão · coleta · análise · simulação ·
  multimodal · escrita · verificação):
- **Quem usa** (perfil do pesquisador, não "qualquer pessoa"):

## 2. A tarefa

- **O que a skill faz, em uma frase:**
- **Entrada** (o que a pessoa fornece para começar):
- **Saída** (o que ela recebe no fim, com formato):
- **Como se sabe que funcionou** (critério observável, não "ficou bom"):

## 3. De onde vêm os dados

- **Rotas oficiais** (API pública, base aberta, repositório institucional — com URL):
- **Exige credencial?** (qual, como se obtém, nome da variável de ambiente):
- **Exige login de pessoa física?** (de quem, para quê):
- **Frequência máxima de requisição** que a fonte tolera:

## 4. Limites — a parte que quase todo mundo esquece

- **O que a skill NÃO faz:**
- **O que ela não prova** (o limite da evidência que ela produz):
- **Base legal do dado**, se houver dado pessoal (LAI, dado aberto por desenho, consentimento):
- **O que ela nunca deve fazer** (contornar autenticação, trocar identidade, resolver desafio,
  raspar dado protegido):

## 5. Evidência

- **Testes que devem existir**: caso positivo, caso negativo, caso de borda, falha da fonte,
  ausência de resultado.
- **O que conta como "testado"** neste caso: que comando roda, o que ele precisa devolver.
- **Ambiente onde foi executado de fato** (versão de Python, sistema, data):

## 6. Autoria e citação

- **Autores** (nome completo, instituição, ORCID — só se confirmado no registro do ORCID):
- **Licença** do código e da documentação:
- **Como esta skill deve ser citada:**

## 7. O que você já tem

- **Scripts, planilhas ou código que já funcionam** (cole ou aponte):
- **Documentação da fonte** que você já leu:
- **Tentativas que falharam** e por quê:

---

## Instruções ao agente

1. Siga o protocolo `SS-0000`: estrutura canônica, validador, testes que podem falhar.
2. Não invente método para preencher lacuna. Se um campo do brief estiver vazio, pergunte.
3. Toda credencial entra por variável de ambiente; nunca no código, no teste ou no exemplo.
4. Se a rota oficial for pior que um atalho, documente a oficial primeiro e o atalho como
   contingência nomeada, com a razão e o limite.
5. `tests/RESULTS.md` registra o ambiente real e a saída real — não uma promessa.
6. Ao terminar, liste o que ficou de fora e por quê.

---

*LABHDUFBA · Universidade Federal da Bahia · Skills Métodos Digitais*
