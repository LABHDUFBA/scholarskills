# Operações acadêmicas no SIGAA

**Identificador ScholarSkills:** SS-0015 (proposto) · **Versão:** 0.1.0 · **Maturidade:** `tested` · **Licença:** MIT (código e documentação originais)

## Objetivo

Preparar e executar com segurança operações de ensino e pesquisa em portais acadêmicos da família SIGAA. A skill valida o escopo, prepara um resumo para aprovação humana, separa navegação de ações persistentes e verifica a leitura de retorno depois de salvar, publicar, aprovar ou submeter. Ela se destina ao próprio perfil institucional do titular e não armazena credenciais.

## O que cobre

- Turmas, contexto da disciplina e tópicos de aula.
- Planos de curso, aulas, notícias, materiais e atividades.
- Frequência e notas.
- Projetos de pesquisa, editais, planos de trabalho e frequências aguardando homologação.
- Submissões formais como PIBIC, PIBITI e programas institucionais equivalentes.

## Exemplo mínimo

```bash
python3 scripts/protocol.py examples/sample_operation.json
```

A saída é um resumo JSON para aprovação. O exemplo é sintético e não acessa nenhum portal.

## Limites

- O pacote não afirma compatibilidade com toda instalação do SIGAA.
- Versão, rótulos, permissões, módulos e fluxos locais variam entre instituições.
- O verificador valida formato do pedido e gates de aprovação, não a veracidade de notas, frequência, elegibilidade ou conteúdo científico.
- A skill não substitui o edital, os regulamentos institucionais nem o julgamento do pesquisador.
- Os testes não fazem login, upload, publicação, homologação ou submissão real.

## Dados e ética

Os exemplos usam identificadores e textos sintéticos. Não incluir senhas, tokens, cookies de sessão, listas de estudantes, notas, frequências, propostas privadas ou anexos restritos. Operar somente registros para os quais o titular esteja autorizado. Publicação, alteração de notas, homologação e submissão formal exigem confirmação humana explícita.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

Os resultados ficam registrados em `tests/RESULTS.md`.
