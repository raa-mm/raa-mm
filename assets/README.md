# Assets

All artwork in this folder was created for this profile. No third-party artwork, logos or fonts are embedded.

| File | Used for |
| :-- | :-- |
| `ram-hero.svg` | Hero banner (1000×360) |
| `ram-footer.svg` | Footer banner (1000×120) |
| `project-aprs.svg`, `project-skilllens.svg`, `project-sprkk.svg`, `project-lab.svg` | Project cards (960×260), identical frame, different illustration |
| `icons/chip-*.svg` | Technology chips, one per technology (height 32) |
| `icons/link-*.svg` | Contact link buttons (height 40) |

Conventions: every SVG has `<title>`, a `viewBox`, system font stacks only, no scripts, no external references. Animation uses SMIL and is hidden under `prefers-reduced-motion`. Palette and type rules are in `docs/DESIGN-SYSTEM.md`.

To add a technology chip, copy an existing `chip-*.svg`, change the label, the `textLength` (about 7.6 × number of characters) and the width values so they stay consistent, then reference it from `README.md`.
