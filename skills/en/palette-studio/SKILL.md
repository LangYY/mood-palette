---
name: palette-studio
description: Recommend three-color palettes from everyday descriptions such as blue, pink, bright, or muted, or retrieve a theme or ID for image generation and UI recoloring. Use for palette selection, comparison, or explicit requests for this library; do not apply it to every design task.
---

# Palette Studio

Choose a complete three-color combination, then assign roles and area ratios. Preserve the user's subject, layout, and brand constraints. Respond in the user's language.

## Invocation and routing

Use `$palette-studio` with a task, for example:

- `Recommend five blue-themed palettes for me to choose from.`
- `$palette-studio Generate a landscape still-life illustration with cream-sky-01, without text.`
- `$palette-studio Recolor the current page with moss-tea-05; preserve its layout and interactions.`

When the user asks how to use the skill or supplies only its name, show usage examples. Read [usage examples](references/usage.md) for invocation help or batch conventions.

| Request | Deliverable |
|---|---|
| Recommend, compare, or browse palettes | Existing individual palette images with brief everyday color descriptions and suggested roles |
| Only HEX values | Copyable original HEX values and IDs |
| Generate an illustration, poster, packaging image, or UI mockup | Actual images using an available image tool; prefer imagegen when available |
| Only an image prompt | A copyable prompt |
| UI color variables | Semantic tokens in the project's format, with measured contrast |
| Recolor an existing page | Color changes preserving layout, content, interactions, and token naming; verify the rendered result |
| Audit colors or contrast | Measurements and findings; change colors only when a fix is requested |
| Batch examples or cross-use comparisons | A use case × palette × count checklist, followed by individual images and verification |

Infer optional mood, dimensions, theme, and format from the task when sufficient context exists. Brand constraints and explicit palette choices take priority. Other design workflows govern layout, typography, and components.

## Select and show palettes

For everyday descriptions, read [color search](references/search.md), map the request to the supported basic color, lightness, saturation, and count, and run the script. Retrieve real candidates rather than guessing from theme names. Recommend five by default; if fewer match after deduplication, report the actual count rather than inventing combinations.

Show the pre-rendered clean three-column card from each record’s `image` field, resolved relative to the skill folder. Cards are rendered only from catalog HEX values; reference images and their crops must not be used as skill assets. Embed images in image-capable chat; use an absolute path for local Markdown images. If embedding is unavailable, attach or link the image file. The image is the primary selection artifact: names or IDs alone do not fulfill a palette-browsing request. Reuse the existing image without drawing a replacement search chart or calling an image model. Under each image, add an everyday description such as “blue-gray + deep blue + light gray,” a suggested primary color, and a brief distinction. IDs and copyable HEX are supplementary. Return text alone when the user asks only for values.

If the user asks to choose, stop after showing candidates. Map a later “option 3” to the actual ID previously displayed, preserving its colors and image rather than rerunning and reordering the search. If explicitly asked to recommend and generate immediately, select and report an ID, then continue.

For named themes, consult the [theme index](references/index.md) and retrieve complete records from [the catalog](references/palettes.json). Use an explicit ID exactly. For a theme-only request, choose the required number of IDs based on the use case and report them. If an ID does not exist, explain and offer nearby candidates without silently substituting.

Commands run relative to the skill folder:

```bash
python3 scripts/palette.py --list
python3 scripts/palette.py moss-tea-01
python3 scripts/palette.py --search blue --limit 5
python3 scripts/palette.py --search pink --lightness light --saturation muted --limit 5
```

The library contains 12 themes and 100 records. Preserve the three original HEX values; stored order does not specify roles or area. Do not silently mix colors from different records. Mark a deliberate cross-record combination as new. `printed_hex` means transcribed labels; `image_sample` means approximate image sampling. Read [accuracy notes](references/accuracy.md) when precision, images, naming, or provenance matters. Mark added or adjusted colors as application-derived.

## Image generation

Put each selected color into the image prompt as an everyday name + HEX + intended location, such as background, subject, light, or small props. Assign area ratios to suit the scene; 60/30/10 is an optional starting point, not source metadata. Describe the important warm/cool, light/dark, saturation, and accent relationships.

For actual generation requests, call an available image-generation tool and deliver the resulting image. For prompt-only requests, deliver the prompt. Preserve the subject and composition requirements without binding the skill to a particular provider.

Example with `cream-sky-01`: cream `#FCF5D2` as roughly 60% open background, light sky blue `#C0E3F5` as roughly 30% subject, and soft yellow `#FFEC8E` as roughly 10% highlights or props; bright, airy, and low contrast. HEX communicates intent; verify generated pixel colors separately if exact fidelity matters.

## UI use

Map colors to existing semantic tokens. When new tokens are needed, identify background, surface, text, muted-text, primary, on-primary, accent, border, and focus uses. Add light/dark levels or neutrals as needed, marking each as application-derived. Mood colors do not automatically mean success, warning, or error; preserve existing state conventions.

Calculate actual foreground/background pairs: body text at least 4.5:1; large text (24px regular or about 18.67px bold) at least 3:1; required identifying control boundaries and graphics at least 3:1. See [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

```bash
python3 scripts/palette.py --contrast '#252A24' '#FCF5D2'
```

Report measured ratios only. An audit alone does not authorize changing colors. When selection, application, or repair is requested, adjust roles or derive colors as needed and recalculate. The script handles opaque, solid sRGB colors. For transparency, gradients, or image backgrounds, measure the composited colors first. Check hover, pressed, and focus pairs too. Pale palettes usually need a derived dark text color. Deliver tokens and key contrast measurements, and verify the rendered page.

## Batches and reuse

Track use case × palette × count. “Ten total” is a total; “ten each” applies per use case. State a reasonable allocation and proceed when the meaning is clear. Generate independent images individually; one contact sheet is not multiple image deliveries. Save requested outputs and their palette IDs; include generation prompts when requested. Count completed images against the checklist and explain failed items. An unavailable image tool is not a completed image deliverable.

Use the same ID and three original colors for cross-use comparisons. Mark derived text, material, or lighting shades. “Continue with this palette” reuses the current selected ID and tokens. Use existing project token files or DESIGN.md for cross-page reuse; update persistent project records when requested.

## Delivery and extension

Briefly identify the selected ID, mood, original colors, roles, and derived colors alongside the work. Explain approximations once. Keep commentary short when the user wants the finished artifact.

For new references, transcribe legible HEX exactly or mark sampled colors as `image_sample`. Distinguish invented combinations as new. Public records contain only the necessary ID, theme, colors, image path, and method. Render public palette assets only from final HEX values; exclude all reference images and crops. Keep sampling coordinates and private reference notes outside public distributions. Exclude personal identifiers and source links from public files. Add records incrementally rather than replacing existing values with guesses.
