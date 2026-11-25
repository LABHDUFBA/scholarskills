# Dados Fiscais Públicos Brasileiros (pt-BR)

**Skills Métodos Digitais SS-0011** · versão 1.0.0 · maturidade `tested` · MIT (código e documentação originais)

## Objetivo

Recuperar as contas fiscais que estados e municípios declaram ao Tesouro Nacional, em uma forma cuja
aritmética o leitor pode auditar.

## Descrição / como funciona

**Princípio: identificador, não nome; período explícito; total que se pode reconferir.**

1. **Identificar a entidade pelo código IBGE**, nunca pelo nome. `29` é a Bahia; `2927408` é Salvador.
   Nomes mudam com governos; códigos não.
2. **Declarar período e demonstrativo.** Todo registro carrega exercício, período e tipo — número
   fiscal sem isso é anedota.
3. **Somar da árvore de contas declarada** (`total(contas, "1.")`), e não de uma coluna pré-calculada
   que pode não existir para aquela entidade naquele período. A operação fica visível.
4. **Entrega vazia é achado, não falha.** SICONFI devolve lista vazia para entes que não entregaram;
   isso é informação sobre o ente e não se confunde com queda de rede.
5. **Linha sem valor é pulada.** Zero fabricado em tabela fiscal é pior que lacuna documentada.

## Autores

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## Como citar

> NASCIMENTO, Leonardo Fernandes; BRASIL, Eric; SODRÉ, Ricardo. **Dados Fiscais Públicos Brasileiros**
> (Skills Métodos Digitais SS-0011), versão 1.0.0, 2026. Laboratório de Humanidades Digitais,
> Universidade Federal da Bahia.
> https://github.com/LABHDUFBA/scholarskills/tree/main/brazilian-fiscal-data

## Limites

- Público por desenho: SICONFI é dado aberto do Tesouro Nacional. Sem credencial, sem contorno.
- Declarado ≠ executado: são os números que o ente declarou; auditá-los é outra operação.
- Não é ranking: comparar entes sem ajustar por população, base de arrecadação e qualidade do
  reporte produz tabela de campeonato, não análise.
