---
name: digital-agency-dashboard-design
description: Design or review dashboards so they align with Japan Digital Agency dashboard guidance and reusable Power BI theme assets. Use when Codex needs to define dashboard requirements, structure a prototype, choose charts, apply accessible visual rules, adapt Digital Agency-style Power BI themes, or audit an existing dashboard for guideline compliance in public-sector or policy-reporting contexts.
---

# Digital Agency Dashboard Design

Follow this skill when a dashboard must match the style and working method behind the Digital Agency dashboard guidebook and compatible Power BI theme assets.

## Quick Start

1. Clarify the dashboard's purpose, audience, and expected action before touching layout or visuals.
2. Classify the dashboard as primarily `prompting/monitoring` or `exploratory`.
3. Inventory reusable assets in the current workspace.
4. Draft the information hierarchy and chart plan.
5. Apply the visual rules and accessibility checks in this skill.
6. Deliver a concrete artifact: design spec, implementation patch, review findings, or Power BI theme selection.

## Workflow

### 1. Define the decision to support

Capture:

- Primary audience
- Main decision or action after viewing
- Core questions the dashboard must answer
- Update cadence, freshness constraints, and source attribution
- Constraints such as screen size, Power BI use, publication medium, and accessibility requirements

If the user asks only for a visual redesign, still infer and state the intended audience and decision context before finalizing the structure.

### 2. Shape the dashboard before styling it

Prefer a layout that moves from high-signal summary to supporting detail.

- Put the key takeaway, KPI, or status summary first.
- Group related visuals so one section answers one question.
- Use comparison-friendly charts before decorative or dense alternatives.
- Remove elements that do not help interpretation or action.
- Keep filters and interactions minimal unless the task is explicitly exploratory.

### 3. Choose charts deliberately

Pick the chart type that best answers the user's question.

- Use bars for ranking and categorical comparison.
- Use lines for change over time.
- Use maps only when geography is essential to the decision.
- Use tables only when exact lookup matters.
- Avoid 3D effects, ornamental shapes, and color-heavy encodings that weaken comparison.

When uncertain, prefer the simplest chart that preserves the comparison the user needs.

### 4. Apply the shared visual system

If the workspace contains Digital Agency-compatible Power BI assets, inspect them first:

```bash
python3 <skill-path>/scripts/inspect_powerbi_assets.py .
```

Then align the design to the shared conventions documented in [digital-agency-assets.md](./references/digital-agency-assets.md).

Default conventions derived from the provided Power BI themes:

- Use a light neutral canvas with restrained accent color.
- Use bold left-aligned chart titles.
- Keep legend placement consistent; prefer bottom legends when the theme already does so.
- Keep spacing and card padding uniform.
- Keep gridlines subtle and light gray.
- Reserve red or warning accents for exceptions, negative change, or alert states.

Do not invent a new visual language when an existing palette or template already satisfies the request.

### 5. Check accessibility and interpretation risk

Always review:

- Contrast between text, marks, and background
- Distinction between `no data`, `zero`, `not started`, and `in progress`
- Reliance on labels or patterns in addition to color
- Plain-language titles, subtitles, and annotations
- Source, date, unit, and denominator clarity

If a design depends on color alone or lacks context for interpretation, treat that as a defect.

### 6. Produce an explicit output

Return one of these concrete outputs, depending on the task:

- Updated dashboard code or config
- Power BI theme recommendation with file paths
- Layout and content spec
- Review findings with prioritized issues
- Migration plan from an existing dashboard to the Digital Agency style

## Asset Discovery

Use the bundled script when the repository may or may not contain Power BI assets in known locations.

- Run `python3 <skill-path>/scripts/inspect_powerbi_assets.py .` from the workspace root.
- Read the JSON summary or Markdown output to locate `.json` themes and `.pbit` templates.
- If no assets are found, fall back to the official guidebook workflow and document the missing artifact explicitly.

## References

- Read [official-guidebook-summary.md](./references/official-guidebook-summary.md) for the workflow and source links distilled from the Digital Agency materials.
- Read [digital-agency-assets.md](./references/digital-agency-assets.md) when adapting or auditing the Power BI assets found in this repository or a copied equivalent.

Load only the reference file needed for the current task.
