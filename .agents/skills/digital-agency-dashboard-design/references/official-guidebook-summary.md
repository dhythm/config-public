# Official Guidebook Summary

Use this file when the task needs the official basis for dashboard decisions.

## Sources

- Digital Agency, "ダッシュボードデザインの実践ガイドブックとデザインテンプレート"
  - Page updated: 2026-03-31
  - URL: https://www.digital.go.jp/resources/dashboard-guidebook
- Guidebook alternative text
  - Updated: 2026-03-31
  - URL: https://www.digital.go.jp/assets/contents/node/basic_page/field_ref_resources/1948e3cd-736a-4378-9e31-039b08d11106/e7f7ad2f/20260331_resources_dashboard-guidebook_guidebook_02.txt

## Official points to preserve

The Digital Agency page explicitly states that the guidebook is intended to improve dashboard quality and design efficiency and to help people build dashboards that are easy to understand.

The published workflow is:

1. Organize requirements
2. Prototype
3. Implement

The guidebook explicitly emphasizes:

- Purpose definition and constraint organization before design work
- Agreement-building through prototyping
- Information expression that helps people understand what they want to know
- Layout and chart expression that avoid misunderstanding
- Accessibility as part of implementation
- Template reuse for consistent, efficient Power BI delivery

The guidebook text distinguishes two dashboard types:

- `prompting/monitoring` dashboards for quick recognition against a baseline
- `exploratory` dashboards for deeper investigation and source tracing

This guidebook mainly targets the first type. When a request mixes both, keep the landing view in the simpler prompting style and isolate advanced exploration behind secondary interactions.

## Operational interpretation

The items below are implementation guidance inferred from the official workflow plus the published template system.

- Begin each design with the audience, decision, and action the dashboard should support.
- Prefer a visible top-level summary before detailed sections.
- Favor charts that make comparison and trend reading immediate.
- Avoid visual choices that add ambiguity, decoration, or excess cognitive load.
- Treat layout consistency, source/date labeling, and state labeling as quality requirements, not polish.
- Treat accessibility checks as required before delivery.

## How to cite this in work

If the user asks why a recommendation was made, ground it in one of these rationales:

- "The official workflow starts with requirements, then prototyping, then implementation."
- "The guidebook emphasizes information expression that helps interpretation and avoids misunderstanding."
- "The Digital Agency templates are meant to reduce fine-grained styling work by standardizing layout and formatting."

When presenting these rationales, prefer paraphrase over long quotation.
