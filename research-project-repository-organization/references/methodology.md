# Methodological grounding

## 1. Character of the procedure

This package operationalizes established guidance on organizing research-computing projects. It is a practical workflow, not a new formal research method and not an empirical claim that a particular directory tree improves scientific quality. Its contribution is to turn recommendations about project boundaries, documentation, version control, and provenance into a sequence with explicit checks and stop conditions.

## 2. Sources and claims used

### Noble (2009)

Noble recommends organizing a computational biology project so that its files are easy to locate and the work can be rerun by others. His example separates documentation, data, results, source code, and external tools. He also discusses project-specific paths, reproducible scripts, and version control. The package uses these as adaptable design considerations, not as a mandatory folder schema. Noble's scope is computational biology; applying the principles to other fields is a transfer of practice, not evidence that every recommendation fits every discipline.

### Wilson et al. (2017)

Wilson and colleagues present "good enough" practices for scientific computing, including project organization, data management, collaboration, and change tracking. They explicitly recommend an overview, a shared to-do list, sensible project boundaries, clear filenames, and version control. The package draws on that checklist while avoiding a universal project split rule or rigid directory names. The paper is practical guidance, not a comparative trial demonstrating that one layout causes better research outcomes.

### The Turing Way Community

The Turing Way's repository guidance recommends documenting project goals and navigation, separating inputs, methods, and outputs where useful, recording the computational environment, and excluding sensitive or private material from version control. Its sensitive-data guidance also treats approved storage and access as project-specific responsibilities. This package adapts those recommendations as decision prompts; it does not replace the institution's data-management plan, ethics review, or security procedures.

## 3. Operationalization

| Principle | Procedure in this skill | Decision left to the researcher |
|---|---|---|
| Make files discoverable | Inventory current materials; propose directories around actual project functions | Which categories and names fit the discipline and team |
| Document project purpose and workflow | README, plan, progress record; optional protocol, findings, schema, or source inventory | Which documents are needed and who maintains them |
| Preserve change history | Inspect Git state and follow existing branch/review conventions | Whether Git is appropriate; hosting and release choices |
| Preserve provenance | Record source, unit, snapshot, filters, transformations, environment, and outputs when relevant | Which fields are necessary for the method and audience |
| Protect people and restricted material | Classify materials before staging; keep restricted originals in approved storage | Legal basis, consent, storage, access, retention, and release permissions |
| Avoid destructive restructuring | Inventory changes, preserve source, stop on unknown or conflicting files | Whether and when an authorized migration should occur |

## 4. Epistemic status and limits

- **Established from the cited guidance:** the sources recommend project organization, documentation, version control, explicit provenance, and care with sensitive materials.
- **Operational interpretation:** this package combines those recommendations into an eight-step repository setup and review procedure.
- **Not established here:** that this exact sequence or scaffold improves research quality, prevents all data exposure, or guarantees reproducibility.
- **Normative safeguard:** the skill refuses to infer rights, consent, institutional approval, or authorization to publish from public availability or repository visibility.

The skill applies to repository planning and documentation. It does not judge the validity of a research design, certify security, or determine compliance with law, funder rules, or institutional policy.

## 5. Alternatives considered

A single rigid directory template is easy to apply but can impose irrelevant folders and hide differences in data, governance, and outputs. This skill instead offers a minimal documentation scaffold and asks the researcher to adapt it.

A manual checklist works across tools but is easy to forget. The optional script creates only a blank, non-destructive starter scaffold. It does not automatically migrate files or initialize Git, because those actions require project-specific inspection and authorization.

## 6. Bibliography and resources

- Noble, William Stafford. “A Quick Guide to Organizing Computational Biology Projects.” *PLOS Computational Biology* 5, no. 7 (2009): e1000424. https://doi.org/10.1371/journal.pcbi.1000424.
- Wilson, Greg, Jennifer Bryan, Karen Cranston, Justin Kitzes, Lex Nederbragt, and Tracy K. Teal. “Good Enough Practices in Scientific Computing.” *PLOS Computational Biology* 13, no. 6 (2017): e1005510. https://doi.org/10.1371/journal.pcbi.1005510.
- The Turing Way Community. “Creating Project Repositories” and “Advanced Structure for Data Analysis.” *The Turing Way: A Handbook for Reproducible, Ethical and Collaborative Research*. https://book.the-turing-way.org/project-design/pd-overview/project-repo and https://book.the-turing-way.org/project-design/pd-overview/project-repo/project-repo-advanced. Accessed 2026-11-25.
- The Turing Way Community. “Sensitive Data Projects.” *The Turing Way*. https://book.the-turing-way.org/project-design/data-security/sdp. Accessed 2026-11-25.
