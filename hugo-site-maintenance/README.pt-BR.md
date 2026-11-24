# Manutenção de sites Hugo (pt-BR)

**Skills Métodos Digitais SS-0012** · versão 1.0.0 · maturidade `tested` · MIT (código) / CC BY 4.0 (documentação)

## Objetivo

Manter um site Hugo correto enquanto ele é editado: conferir o que existe antes de criar, conferir o
que está publicado antes de acreditar no clone, e ler o log do deploy antes de mexer no build.

## Descrição / como funciona

**Três regras que evitam a maior parte do dano:**

1. **Inspecionar antes de criar.** Antes de escrever página, shortcode, layout ou arquivo de dados,
   procure no `content/`, liste `layouts/` e `data/`, abra a página que a pessoa diz que já tem o
   recurso. Infraestrutura duplicada é o defeito mais comum e só aparece quando alguém edita a errada.
2. **O clone não é o site.** O publicado pode estar à frente da cópia local. Compare `last-modified`,
   `md5sum`, `git log origin/main` e `gh api .../pages` antes de editar.
3. **Ler o run, não o código.** Quando o deploy falha, a anotação diz a causa — e muitas vezes não é
   build: conta bloqueada, cota esgotada, permissão do workflow.

## Autores

Leonardo Fernandes Nascimento (LABHDUFBA/UFBA), Eric Brasil (UNILAB), Ricardo Sodré (UFBA).

## Como citar

> NASCIMENTO, Leonardo Fernandes; BRASIL, Eric; SODRÉ, Ricardo. **Manutenção de sites Hugo**
> (Skills Métodos Digitais SS-0012), versão 1.0.0, 2026. Laboratório de Humanidades Digitais,
> Universidade Federal da Bahia.
> https://github.com/LABHDUFBA/scholarskills/tree/main/hugo-site-maintenance

## Limites

- Nenhuma credencial no pacote: o deploy usa o token do próprio repositório nas Actions.
- A auditoria é estrutural, não editorial: ela não sabe se uma frase é verdadeira.
- Build verde não significa site correto: uma página pode compilar e apontar para um 404.
