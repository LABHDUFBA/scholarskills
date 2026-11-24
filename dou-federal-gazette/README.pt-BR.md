# DOU e Convênios Federais (pt-BR)

**Skills Métodos Digitais SS-0010** · versão 1.0.0 · maturidade `tested` · MIT (código) / CC BY 4.0 (documentação)

## Objetivo

Coletar o que o governo federal publicou no Diário Oficial da União e o que transferiu por convênio,
usando as rotas que o próprio Estado publica para acesso por máquina — e não um contorno em torno
delas.

## Descrição / como funciona

**Princípio: a rota oficial primeiro, e o filtro precisa ser verificado.**

1. **Pergunte o mais estreito possível.** Um convenente, uma janela de datas, uma seção. Consulta
   ampla no DOU devolve milhares de páginas; a API responde a mesma pergunta em segundos.
2. **Leia o total antes de paginar.** `parse_total()` devolve a contagem anunciada, para o cliente
   saber se está diante de 3 ou de 3 000 resultados.
3. **Paginar até uma resposta vazia**, não até um limite adivinhado. `max_pages` é teto, nunca meta:
   parar no teto é truncamento e precisa ser reportado.
4. **Verificar o filtro nos primeiros registros.** A API ignora silenciosamente parâmetros
   desconhecidos — um nome de campo errado devolve registros de *qualquer* convenente.
   `verify_first_records()` recusa o lote quando os três primeiros não pertencem à instituição pedida.
5. **Respeitar a pausa.** Uma requisição por segundo por padrão, e recuar no 429 em vez de acelerar.
6. **Registrar o que a rota devolveu.** Cada linha carrega edição, seção, data e a URL canônica, para
   que o registro possa ser reconferido por uma pessoa.

## Autores

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## Como citar

Enquanto não houver DOI registrado, cite pelo identificador do pacote:

> NASCIMENTO, Leonardo Fernandes; BRASIL, Eric; SODRÉ, Ricardo. **DOU e Convênios Federais**
> (Skills Métodos Digitais SS-0010), versão 1.0.0, 2026. Laboratório de Humanidades Digitais,
> Universidade Federal da Bahia. https://github.com/LABHDUFBA/scholarskills/tree/main/dou-federal-gazette

Após o depósito no Zenodo, entram o DOI da versão e o DOI de conceito, separados.

## Limites

- Base legal: LAI (Lei 12.527/2011) e Decreto 7.724/2012 para o DOU; mesmo regime para o Portal da
  Transparência. Ambos oferecem acesso por máquina por desenho.
- Sem contorno: o cliente não troca identidade, não resolve desafio e não passa por proxy de terceiro
  para driblar bloqueio. Rota bloqueada vira `DouUnavailable`.
- Dados pessoais: atos que nomeiam pessoas são públicos, mas montar base de pessoas a partir deles é
  tratamento de dados sob a LGPD. Este pacote coleta atos sobre instituições e não extrai
  identificadores pessoais.
- Não é fonte autoritativa: o registro prova o que a rota devolveu no dia da consulta. Para efeito
  legal, vale a cópia certificada do Diário Oficial.
