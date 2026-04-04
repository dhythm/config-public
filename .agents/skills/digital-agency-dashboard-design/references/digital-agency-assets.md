# Digital Agency Assets

Use this file when the workspace contains Power BI theme JSON files or `.pbit` templates that follow the Digital Agency distribution pattern.

## Repository patterns observed here

This repository exposes two reusable asset groups:

- `powerbi-templates/powerbi-theme-json/*.json`
- `powerbi-templates/powerbi-theme-pbit/*.pbit`

Observed palettes:

- Solid Gray
- Blue
- Light Blue
- Cyan
- Green
- Orange
- Red

## Shared theme conventions derived from the JSON files

These values were consistent across all seven theme JSON files in this repository.

- Canvas/background color: `#F8F8FB`
- Gridline color: `#E6E6E6`
- Chart title: `Arial`, `14`, bold, left aligned
- Subtitle font size: `10`
- Legend position: `Bottom`
- Legend font size: `10`
- Category axis font size: `8`
- Value axis font size: `8`
- Label font size: `12`
- Card padding: `12` on all sides
- Border radius: `12`
- Vertical spacing: `8`

## Palette guidance

Treat the first sequence in `dataColors` as the primary categorical palette.

- Blue and Light Blue themes include red accent values suitable for negative or warning emphasis.
- Solid Gray uses neutral grays with blue and red accents; use it when the dashboard should feel subdued or highly administrative.
- Orange, Green, Cyan, and Red are better when a single category color family should dominate the dashboard identity.

Preserve the palette order unless the user has a strong reason to change semantic meaning.

## Recommended use in implementation

- Prefer loading an existing `.json` theme rather than recreating styles by hand.
- If a `.pbit` template is available, use it as the starting point for layout and component structure.
- If the request is repo-agnostic, search for equivalent files first instead of assuming this exact path layout.
- If the user wants a new chart or page added, mirror the spacing, title sizing, and border treatment already present in the selected theme.

## File selection rule

Choose the asset in this order:

1. Existing `.pbit` template matching the desired palette
2. Theme JSON matching the palette
3. Manual implementation that mirrors the shared conventions in this file
