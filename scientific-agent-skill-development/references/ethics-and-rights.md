# Ethics, privacy and copyright checklist

Run this before the package leaves the author's machine. It is a floor, not a substitute for
institutional review.

## 1. Personal data

- [ ] Does any input, example, fixture or test contain personal data?
- [ ] If yes: is there a legal basis (consent, legitimate interest, public interest) recorded?
- [ ] Are identifiers pseudonymised where the method does not require them?
- [ ] Is there a stated threshold below which a group is not reported (small-cell suppression)?
- [ ] Can an individual be re-identified by combining outputs with another dataset?

If the answer to the last question is yes and no mitigation exists, the skill must refuse that use
and say so in `SKILL.md`.

## 2. Consent and expectations

Public availability is not consent for every downstream use. Record what the people whose data is
used would reasonably expect, especially for quotes, images, and private-group content.

## 3. Copyright and database rights

- Source content: is it licensed for processing? (text and data mining exceptions vary by
  jurisdiction and do not always permit redistribution)
- Are examples redistributed? If so, under which licence?
- Third-party models and datasets: their licences travel with the skill.

## 4. Dual use

State plainly whether the method can be used to harm, surveil or de-anonymise, and what the skill
does to limit that (scope restriction, refusal path, aggregation).

## 5. Transparency about automation

If the skill produces text, classification or scores that a human will read as authored, say so in
the output. Simulated respondents, synthetic focus groups and generated annotations must be labelled
as synthetic wherever they appear.

## 6. Attribution

- Authors, contributors and data providers named.
- Prior methods cited, including those from outside the project's network.
- No claim of institutional endorsement that does not exist.

## 7. Sign-off

| Item | Responsible | Date |
|---|---|---|
| Data protection | | |
| Copyright | | |
| Institutional clearance | | |
