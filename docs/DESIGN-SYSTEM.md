# Design system

**Idea.** A dark engineering interface whose recurring motif is a small network of agent nodes. It appears in the hero as the one memorable element; project cards use quieter diagrams (pipeline, contribution bars, browser wireframe, terminal).

## Tokens
| Role | Value |
| :-- | :-- |
| Ink (card inner, banners) | `#080B17` |
| Navy (card surface) | `#0D1117` |
| Line (borders) | `#232A45` |
| Violet / Purple / Cyan | `#8B5CF6` / `#A78BFA` / `#22D3EE` |
| Text / Secondary text | `#F8FAFC` / `#94A3B8` |
| Chip category dots | languages `#8B5CF6`, frontend `#22D3EE`, backend `#A78BFA`, AI `#E879F9`, databases `#38BDF8`, automation `#2DD4BF`, infrastructure `#6366F1`, e-commerce `#F59E0B` |

## Type
System stacks only, because SVGs shown through `<img>` cannot load web fonts: sans `Segoe UI, Helvetica Neue, Arial`, mono `SFMono-Regular, Consolas, Menlo`. Wordmark 156 px/800; card title 46 px/800; subtitle 21 px; status 16 px/600.

## Geometry and rules
- Cards 960×260, radius 20, 1 px border, illustration panel 376×212 at 24 px inset, text column at x=440.
- Banner radius 24. Chips radius 16 (pill). Link buttons radius 19 with gradient border.
- Gradient is violet to cyan, 135°. Do not use `url(#g)` strokes on perfectly horizontal or vertical lines (zero-size bounding box renders nothing); use a solid colour there.
- Motion: only the hero pulses, the APRS pulse and the lab cursor. All are SMIL, class `anim`, hidden under reduced motion.
- Mobile: GitHub scales images to the viewport. Large text lives in the SVGs; small descriptive text lives in README text so it stays readable. Tech chips are separate inline images so they wrap.
