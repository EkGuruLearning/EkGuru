# css/

Styles for the site.

- `tokens.css` is the source of design tokens (colours, spacing, type). Change
  a token here, not as a hard-coded value elsewhere. See `docs/DESIGN-SYSTEM.md`.
- `style.min.css` is a bundle. Do not hand-edit it; edit the source files and
  rebuild with the bundling tool in `tools/`.
- `themes/` holds theme variants.
- Check light and dark themes and a 360 px phone width after any change.
- Respect `prefers-reduced-motion`.
