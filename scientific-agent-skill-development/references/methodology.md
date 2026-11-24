# Writing the methodological section

The methodological section is what separates a scientific skill from a prompt library. It answers:
*which* method, *from where*, *operationalised how*, and *valid where*.

## 1. Name the method and its tradition

State the method, the field it comes from and the canonical reference. If the method has variants,
say which one is implemented and what the others do differently.

A citation is written only when it can be verified. When it cannot, write
`unverified — to be confirmed by ⟨author⟩`. An invented reference is a fabrication, and fabrication
invalidates the package more decisively than a missing citation.

## 2. Operationalisation

For each concept that becomes a variable, record:

| Concept | Variable | Decision | Alternative rejected | Reason |
|---|---|---|---|---|
| e.g. "engagement" | count of replies | replies only, no likes | weighted sum | likes are not comparable across platforms |

Every decision that could plausibly have gone the other way belongs in that table. The table is the
most useful part of the document for a reader deciding whether to trust the output.

## 3. Epistemic status of each statement

Separate the text into four registers, explicitly:

- **Established** — follows from the method when its assumptions hold.
- **Interpretation** — a reading of the result, defensible but not entailed.
- **Hypothesis** — plausible, untested here.
- **Normative** — a value judgement, labelled as such.

A skill that blurs these registers teaches its users to blur them too.

## 4. Assumptions and validity domain

For each assumption: what it is, how to check it on real data, and what breaks when it fails. The
validity domain is the set of inputs for which the output can be read as valid. Skills are commonly
used outside their domain because the domain was never written down.

## 5. Known alternatives

At least one competing method, with the trade-off. This is where reviewers look first, because a
method section with no alternative usually means the choice was not examined.

## 6. Bibliography

- Author, A. (Year). *Title*. Publisher. DOI/URL.
- Software: name, version, repository, and the specific function used.

## 7. Change log of methodological decisions

When the implementation changes in a way that alters results, record it here with the version in
which it happened. Silent changes to a method are indistinguishable, to a reader, from error.
