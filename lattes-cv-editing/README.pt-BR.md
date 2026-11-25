# Edição de currículo Lattes (pt-BR)

**Skills Métodos Digitais SS-0013** · versão 1.0.0 · maturidade `tested` · MIT (código e documentação originais)

## Objetivo

Preparar o item corretamente **antes** de abrir o formulário. O editor do Lattes não tem API nem
registro de transação: um ano errado ou uma entrada duplicada não é pego por nada e passa a integrar
um registro acadêmico público que outras pessoas citam.

## Descrição / como funciona

**Protocolo em cinco etapas:**

1. **Autorização e escopo.** Autorizar a edição não autoriza o envio ao CNPq. O envio publica versão
   nova e exige aceite de declaração legal — peça autorização específica e por escrito.
2. **Metadados em fonte primária.** DOI/Crossref, página da revista, ficha catalográfica ou PDF
   oficial antes de abrir o formulário. Resultado de buscador não comprova nada.
3. **Conferir o item e preencher um por chamada.** O editor perde modal não salvo entre chamadas.
4. **Portão de confirmação.** Tipo, seção, todos os campos, a fonte usada e screenshot; aguardar
   aprovação explícita.
5. **Envio é autorização separada.**

**Regras dos casos difíceis:**

| Situação | Regra |
|---|---|
| Preprint e artigo publicado | **Dois registros.** Nunca consolidar. |
| Anais e artigo em revista | **Dois registros.** |
| Capítulo e livro | **Dois registros.** |
| Duplicata confirmada | **Editar a existente**, mantendo a mais completa como base. |
| Título parecido mas diferente | **Não é duplicata.** |
| Campo sensível (cor/raça, deficiência) | **Perguntar ao titular.** Nunca inferir. |

## Autores

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## Como citar

> NASCIMENTO, Leonardo Fernandes; BRASIL, Eric; SODRÉ, Ricardo. **Edição de currículo Lattes**
> (Skills Métodos Digitais SS-0013), versão 1.0.0, 2026. Laboratório de Humanidades Digitais,
> Universidade Federal da Bahia.
> https://github.com/LABHDUFBA/scholarskills/tree/main/lattes-cv-editing

## Limites

- Sem raspagem de currículos de terceiros: opera apenas o registro do titular.
- Sem envio automatizado: o envio é ato jurídico do titular.
- Sem invenção: campo sem fonte primária fica vazio.
- Nenhuma credencial é armazenada; o titular autentica e a senha nunca passa pelo pacote.
