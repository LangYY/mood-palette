# Everyday color search

Extract the basic color, lightness, saturation, and count from the user's language, then retrieve candidates deterministically. Theme names and IDs remain valid direct lookups.

| User expression | Script condition |
|---|---|
| Mainly blue, blue-themed | `--search blue` |
| Pink, yellow, green, cyan, purple, brown, red, orange, black, white, gray | Corresponding basic color; query black, white, and gray separately |
| Light, bright, high lightness | `--lightness light` |
| Dark, deep, low lightness | `--lightness dark` |
| Muted, soft, low saturation | `--saturation muted` |
| Vivid, saturated, intense | `--saturation vivid` |
| Any hue, bright and muted | `--search any --lightness light --saturation muted` |
| Five options | `--limit 5`, also the default |

The agent maps natural language to these options; the CLI accepts basic color aliases rather than full sentences. Chinese basic color aliases are also supported. Explain contradictory conditions. For finer requirements, examine candidate features and state the additional reasoning; do not claim the script understands arbitrary adjectives.

```bash
python3 scripts/palette.py --search blue --limit 5
python3 scripts/palette.py --search pink --lightness light --saturation muted --limit 5
python3 scripts/palette.py --search any --lightness dark --saturation vivid --limit 5
```

## Retrieval contract

- Return only complete library combinations with original IDs, HEX, methods, and image paths.
- Everyday names are approximate RGB-based labels, including blue-gray and tinted whites, rather than standardized swatch names.
- Rank by the number of matching colors and chroma. Prefer different themes, then fill with distinct combinations from the same theme. An order-independent approximate RGB distance removes reordered and near-duplicate combinations.
- Lightness uses HSL lightness; saturation uses HSV saturation. Both the whole-palette mean and the suggested primary must satisfy the selected filters. These coarse measures are not perceptually uniform and do not replace contrast calculations.
- `suggested_primary` proposes the main color. `matching_colors` lists matching swatches. `color_details` contains names and numerical features. The original records do not specify roles or area ratios.
- `image` is a relative path to the existing individual palette image. Resolve it from the skill folder, not the current project's working directory.
- Status is `ok`, `fewer_matches`, or `no_matches`; use `returned` as the actual count. If too few match, explain and offer a relaxed condition without silently dropping filters.

## Presentation and selection

Show option number → actual existing palette image → everyday three-color description → suggested primary and short distinction. Embed each image directly when supported; use resolved absolute local paths in Markdown. Otherwise attach or link the image file. Names and IDs alone are insufficient for browsing; HEX and IDs are supplementary. A values-only request gets text.

Reuse the stored image; do not generate replacement search graphics. When the user wants to choose, stop after the options. Resolve a later “option 2” to its previously shown ID. Generate new illustrations, posters, or UI mockups only when those application images are requested.

```text
Recommend five blue-themed palettes for me to choose from.
Show me light, muted pink palettes.
Choose option 3 and generate a reading app homepage mockup with it.
Keep that palette and recolor my current page, preserving its layout.
```
