# Usage examples

Use `$mood-palette` plus an ordinary task description. These are natural-language examples, not extra slash commands or script subcommands.

## Browse and choose

```text
$mood-palette Recommend palettes for my tea brand.
Recommend five blue-themed palettes for me to choose from.
Show me five light, muted pink combinations.
Choose option 3 and use it for a poster.
```

Show clean three-column palette cards rendered from HEX values, five by default, with short everyday descriptions and suggested primary colors. IDs and HEX supplement the images. Resolve each record's `image` path relative to the skill directory. Reuse images rather than drawing a new search chart. Wait for a choice when requested; report the actual count when fewer match. Read [color search](search.md) for filter and result conventions. For values alone, ask “only give me the HEX values.” “List palette themes” lists the catalog without generating images.

## Compare

```text
$mood-palette Compare two calm palettes for a reading website; show the cards and explain background, text, and accent roles. Do not edit files yet.
$mood-palette Compare Cream Sky and Rain Slate for a weather utility.
```

Recommendations reuse existing images without calling an image-generation tool or modifying a project. A named theme resolves to concrete IDs according to the requested count; use an ID for exact reproduction.

## Generate images or only prompts

```text
$mood-palette Use cream-sky-01 to generate a ceramic still-life illustration, landscape 4:3, without text, using imagegen.
$mood-palette Use Rain Slate for a portrait photography exhibition poster titled RAIN STUDIES.
$mood-palette Write a tea-set product-image prompt with Moss Tea; do not generate yet.
```

The first two deliver actual images; the third delivers a prompt. Include prompts when requested. HEX guides relationships rather than promising exact pixel colors. Explain when the image tool is unavailable.

## UI tokens, mockups, and code changes

```text
$mood-palette Output CSS color variables and contrast measurements for moss-tea-05; no page implementation yet.
$mood-palette Generate a desktop landscape flower-shop homepage mockup with Mint Candy using imagegen.
$mood-palette Recolor the current dashboard with rain-slate-01. Preserve layout, content, interactions, and token naming.
```

These respectively deliver tokens, a static mockup image, and code changes. A static mockup is not a working page. An audit-only request can say “Check text and button contrast without changing colors.”

Token example for `moss-tea-05`: background `#D6C78C`, primary button `#684936`, decorative accent `#86A126`; derived text `#302B20`, derived surface and button text `#F7F0DA`. For opaque solids: text/background about 8.32:1, button text/button about 7.10:1, button/background about 4.78:1. These values apply only to those pairs; recalculate for the actual project.

## Batch images and reuse

```text
$mood-palette Use ten different palette IDs to generate ten illustrations, ten UI mockups, and ten posters: thirty separate images total, using imagegen. Reuse each ID across the three use cases and provide originals, prompts, and a gallery.
$mood-palette Generate three landscape tea-set product images with Cream Sky. Use different compositions but keep one palette ID; no text.
```

The first means ten IDs × three use cases × one image. The second means one ID × one use case × three compositions. Count independent images; a gallery is only a browsing aid. If use cases are omitted, state a context-appropriate allocation and proceed.

```text
Use $mood-palette moss-tea-05 with the project's current design system to implement a tea-brand homepage.
Continue with that palette on the settings page, reusing the selected semantic tokens.
```

The library provides colors and roles; the project and relevant design workflow govern typography, components, layout, and product behavior. No additional skill installation is required.

## Phone photos

In mobile ChatGPT select the installed Mood Palette plugin and attach a photo directly from your phone. The desktop invocation remains `$mood-palette`. The standalone GitHub skill does not automatically install on a phone; a plugin must be created and installed separately.

```text
Use Mood Palette to recommend five palettes for this photo; let me choose.
Choose option 2 and make a portrait wallpaper from the same photo, preserving subject and composition; no text.
```

An explicit ID can be applied directly. Ask for missing photos in the current chat rather than a desktop transfer. Photos do not belong in plugin assets or GitHub. Read [the photo workflow](mobile.md).

## Optional CLI

Run in the directory containing `SKILL.md`:

```bash
python3 scripts/palette.py --list
python3 scripts/palette.py moss-tea-05
python3 scripts/palette.py --search blue --limit 5
python3 scripts/palette.py --search pink --lightness light --saturation muted --limit 5
python3 scripts/palette.py --contrast '#302B20' '#D6C78C'
```

`--list` returns 12 themes. ID lookup returns colors, image path, and method. `--search` returns real deduplicated candidates and image paths. `--contrast` calculates opaque solid sRGB contrast. The agent runs these helpers; users need not type CLI commands for normal requests.
