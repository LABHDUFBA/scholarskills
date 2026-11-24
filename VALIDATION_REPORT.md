# Relatório de implantação — ScholarSkills

**Data:** 24/11/2026 · **Responsável técnico:** Hermes Bot (agente) · **Operador:** Leonardo Fernandes Nascimento
**Repositório:** https://github.com/leofn/scholarskills (privado) · **Registro de ações:** `DEPLOYMENT_LOG.md`

---

## 1. Etapas concluídas

| # | Etapa | Estado | Evidência |
|---|---|---|---|
| 1 | Inspeção do ambiente (git, gh, Python, credenciais) | ✅ | `DEPLOYMENT_LOG.md` §001 |
| 2 | Leitura da documentação oficial vigente | ✅ | §002 — especificação Agent Skills, Zenodo API, CFF 1.2.0 |
| 3 | Verificação de disponibilidade de nomes | ✅ | `scholarskills` livre no GitHub (HTTP 404); comunidade Zenodo inexistente (404) |
| 4 | Estrutura local (`registry/`, `skill-template/`, `scientific-agent-skill-development/`) | ✅ | 52 arquivos versionados |
| 5 | Catálogo `registry.json` + esquema JSON + política editorial | ✅ | 9 entradas (1 `available`, 8 `planned`) |
| 6 | Template oficial (SKILL.md, README, CITATION.cff, LICENSE, CHANGELOG, .zenodo.json, references/) | ✅ | `skill-template/` |
| 7 | Meta-skill SS-0000 implementada | ✅ | `scientific-agent-skill-development/` |
| 8 | Quatro scripts operacionais | ✅ | `validate_skill.py`, `build_package.py`, `generate_metadata.py`, `run_checks.py` |
| 9 | Exemplo sintético completo (análise descritiva) | ✅ | `examples/descriptive-analysis/` |
| 10 | Testes positivos, negativos, de borda e de falha de ferramenta | ✅ | 21 testes (protocolo) + 8 (exemplo) |
| 11 | GitHub Actions com permissões mínimas | ✅ | run [45357118018](https://github.com/leofn/scholarskills/actions/runs/45357118018) — **success** em Python 3.10 e 3.12 |
| 12 | Repositório criado e conteúdo publicado (privado) | ✅ | `leofn/scholarskills`, branch `main`, commit `dbd5369` |
| 13 | Compartilhamento com coautor | ✅ parcial | convite enviado a `ericbrasiln` (write), pendente de aceite |
| 14 | Pacote de depósito preparado (ZIP + SHA-256 + metadados + checklist) | ✅ | `84957b5b…c73c8` |
| 15 | Registro persistente de ações | ✅ | `DEPLOYMENT_LOG.md` (8 entradas) |

## 2. Etapas pendentes ou bloqueadas

| # | Etapa | Bloqueio | Ação necessária |
|---|---|---|---|
| 1 | Convite a Ricardo Sodré | conta GitHub não identificada com segurança | informar o *username* |
| 2 | Repositório público | exige autorização; destino institucional não decidido | autorizar e escolher entre `leofn`, organização `ScholarSkills` ou `LABHDUFBA` |
| 3 | Licença definitiva | aguarda revisão institucional de direitos | aprovação formal |
| 4 | ORCIDs e grafia de afiliação | declarações de identidade | confirmação de cada autor |
| 5 | Comunidade Zenodo | **não há endpoint de criação de comunidades na API**; criação é pela interface | ação manual do operador |
| 6 | Depósito em sandbox | `ZENODO_SANDBOX_TOKEN` ausente no ambiente | fornecer credencial (sem enviar pelo chat) |
| 7 | Depósito em produção e DOI | irreversível; exige clareza de autoria e direitos | autorização final |

## 3. Evidências dos testes

```
validate_skill.py scientific-agent-skill-development          → PASS, 0 warnings
validate_skill.py .../examples/descriptive-analysis           → PASS, 0 warnings
validate_skill.py skill-template --allow-template
                 --allow-placeholders                         → PASS, 5 warnings (esperados)
python3 -m unittest discover -s tests                         → 21 testes, OK
python3 -m unittest discover -s examples/.../tests            → 8 testes, OK
GitHub Actions (3.10 e 3.12)                                  → success
```

Detalhamento em `scientific-agent-skill-development/tests/RESULTS.md`.

## 4. Arquivos produzidos

- **Governança:** `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, `CITATION.cff`
- **Catálogo:** `registry/registry.json`, `registry/metadata-schema.json`, `registry/EDITORIAL_POLICY.md`
- **Template:** `skill-template/` (11 arquivos)
- **SS-0000:** `SKILL.md`, `README.md`, `CITATION.cff`, `.zenodo.json`, `CHANGELOG.md`, 4 referências, 4 scripts, 1 exemplo completo, 1 suíte de testes
- **CI:** `.github/workflows/validate.yml`
- **Registro:** `DEPLOYMENT_LOG.md`

## 5. Decisões que exigem aprovação humana

1. Tornar o repositório público e sob qual titularidade.
2. Licença definitiva (proposta: MIT para código, CC BY 4.0 para documentação).
3. Rota única de depósito: integração GitHub–Zenodo **ou** manual/API — nunca ambas.
4. Autoria final, ordem e afiliações.

## 6. Como reproduzir

```bash
git clone https://github.com/leofn/scholarskills.git
cd scholarskills
pip install pyyaml

python3 scientific-agent-skill-development/scripts/validate_skill.py \
    scientific-agent-skill-development
python3 scientific-agent-skill-development/scripts/validate_skill.py \
    scientific-agent-skill-development/examples/descriptive-analysis

cd scientific-agent-skill-development && python3 -m unittest discover -s tests
cd examples/descriptive-analysis && python3 -m unittest discover -s tests
```

## 7. Nota metodológica

A validação implementada é **estrutural**. Ela verifica conformidade com a especificação Agent
Skills, presença de documentação, marcadores não resolvidos, links locais, padrões de credencial e
consistência de metadados. Não verifica se o método implementado é o método correto, nem confere se
uma citação sustenta a afirmação atribuída a ela. Revisão por pares e replicação permanecem
processos sociais, com evidência documental própria (`EDITORIAL_POLICY.md`).
