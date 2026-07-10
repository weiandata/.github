# WeianData Engineering Handbook Style Guide

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData |
| Effective date | 2026-07-10 |

## 1. Purpose

This guide makes handbook writing consistent, concise, reviewable, and executable by humans and AI agents.

## 2. Language and tone

- Write in English.
- Use a professional, objective, engineering-oriented tone.
- Prefer short sentences and concrete verbs.
- State the rule before the rationale.
- Avoid promotional language, slogans outside the manifesto, and unnecessary adjectives.
- Use active voice unless the actor is genuinely unknown or irrelevant.

## 3. Normative statements

Use the normative keywords defined in the [authoring constitution](handbook-authoring-rules.md#4-normative-language). Each requirement should state who acts, what they do, and when it is complete.

Good:

> The release owner MUST attach the validation report before creating the release tag.

Avoid:

> Releases should be high quality and thoroughly checked.

## 4. Headings and section order

- Use one `#` heading for the document title.
- Use `##` for required chapter sections.
- Use `###` for subsections.
- Do not skip heading levels.
- Use sentence case for headings.
- Keep the standard chapter sections in constitutional order.

## 5. Paragraphs, lists, and tables

- Keep paragraphs focused on one idea.
- Use bullets for unordered conditions and numbered lists for sequences.
- Use tables only for repeated, comparable fields.
- Do not place paragraph-length policy in tables.
- Introduce every table or list with enough context to interpret it independently.

## 6. Code and commands

Every fenced code block MUST declare a language such as `python`, `r`, `yaml`, `bash`, `json`, `text`, or `mermaid`. Examples MUST be safe, minimal, and free of real credentials or client data.

Use placeholders that cannot be mistaken for real secrets:

```bash
export SERVICE_TOKEN="<provided-by-secret-manager>"
```

Do not present an illustrative command as a universal standard unless the owning chapter requires it.

## 7. Diagrams

Prefer Mermaid for workflows, state machines, and architecture. A diagram MUST have meaningful node labels and MUST not be the sole expression of a normative rule. Keep diagrams small enough to render on GitHub without horizontal scrolling.

## 8. Links and references

- Use descriptive link text.
- Use relative links for handbook files.
- Link to the owning section, not only the document, when practical.
- Prefer primary sources for external technical or scientific references.
- Do not use bare local filesystem paths.

## 9. Terminology

Use one term for one concept. Definitions belong in the [glossary](../chapters/35-glossary.md). Use:

- **AI agent** for an AI system that performs a bounded task with tools;
- **accountable human** for the person who approves risk-bearing output;
- **restricted client data** for raw or directly identifying client information;
- **evidence artifact** for a durable record supporting a decision or validation;
- **repository** rather than repo in normative prose.

Define a new acronym on first use. Avoid invented abbreviations when the full term is short.

## 10. Examples and checklists

Examples SHOULD demonstrate the smallest correct pattern and MUST NOT introduce unowned policy. Label non-normative examples with "Example".

Checklist items MUST be observable and phrased as completed assertions, for example:

- [ ] Required tests pass in the controlled environment.
- [ ] Statistical assumptions and limitations are recorded.

## 11. Metadata and versions

Use an opening metadata table. Dates use ISO 8601 (`YYYY-MM-DD`). Versions use semantic versioning without a leading `v` in metadata and with `v` in release names, such as handbook release `v1.0.0`.

## 12. Accessibility and portability

- Provide text labels for links and diagrams.
- Do not rely on color alone to communicate meaning.
- Use plain Unicode conservatively and avoid decorative symbols in normative content.
- Keep lines and tables readable on narrow screens.
- Ensure the document remains understandable as plain text.

## 13. Editorial checklist

- [ ] The document is fully English.
- [ ] The title, metadata, and headings follow this guide.
- [ ] Normative keywords are used intentionally.
- [ ] Each rule has a clear actor and outcome.
- [ ] Examples are safe and labeled.
- [ ] Links are relative and descriptive.
- [ ] Terms match the glossary.
- [ ] No marketing language, secrets, placeholders, or duplicated standards remain.

