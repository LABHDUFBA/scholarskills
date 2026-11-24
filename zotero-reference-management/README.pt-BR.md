# Zotero Reference Management (pt-BR)

**ScholarSkills SS-0001** · versão 1.0.0 · maturidade `tested` · MIT (código) / CC BY 4.0 (documentação)

## Objetivo

Transformar uma biblioteca Zotero em **fonte de dados confiável e citável para pipelines de
pesquisa**: enumerar, filtrar, exportar e gravar referências pela Web API v3, sem navegador, sem
raspagem e sem armazenar identificadores pessoais no pacote.

## Descrição / como funciona

**Princípio: a chave de API é o limite de acesso.** A skill nunca amplia o que a chave permite. Se o
escopo for somente leitura, ela lê e informa que a escrita não está disponível — não procura desvio.

1. **Resolver** — `GET /keys/{key}` devolve o `userID` numérico e o escopo de permissões. O nome de
   usuário não é parâmetro válido de path.
2. **Contar** — `Total-Results` é cabeçalho HTTP, não campo do corpo. Contar pelo tamanho do array
   devolvido é como bibliotecas são truncadas em silêncio.
3. **Paginar** — `limit` máximo 100; o cliente avança `start` e para na primeira página vazia.
4. **Filtrar** — `itemType=-attachment` exclui PDFs e notas, para que a contagem de referências seja
   contagem de referências.
5. **Exportar** — `format=bibtex|ris|csljson`. BibTeX no endpoint de itens ignora `limit`.
6. **Gravar** — `POST /users/{id}/items` com **array** JSON, mesmo para um item.

### O que não faz

- Não baixa PDFs ausentes do Zotero Storage (a API devolve 404 nesse caso, por projeto).
- Não contorna o escopo da chave e não aceita chave colada em conversa: lê variável de ambiente.
- Não decide o que a bibliografia *deve* conter — a seleção é decisão metodológica, documentada em
  `references/methodology.md`.

## Autores

| Autor | Afiliação | Contribuição |
|---|---|---|
| Leonardo Fernandes Nascimento | Laboratório de Humanidades Digitais (LABHDUFBA), UFBA | Concepção, implementação, testes |
| Eric Brasil | UNILAB | Revisão metodológica |
| Ricardo Sodré | UFBA | Revisão dos critérios bibliográficos |

## Como citar

Até o primeiro depósito autorizado, cite o repositório:

> Nascimento, L. F.; Brasil, E.; Sodré, R. (2026). *Zotero Reference Management* (ScholarSkills
> SS-0001, versão 1.0.0) [Software]. Laboratório de Humanidades Digitais, Universidade Federal da
> Bahia. https://github.com/LABHDUFBA/scholarskills/tree/main/zotero-reference-management

Após o depósito, o DOI de versão e o DOI conceitual são acrescentados aqui e no `CITATION.cff`,
separadamente: o conceitual resolve para a última versão; o de versão fixa este snapshot.
