# Phone photos and wallpapers

Read for an uploaded base photo, recoloring that preserves photo content, or a phone wallpaper. Keep the name Mood Palette and skill identifier `mood-palette`. The desktop invocation remains `$mood-palette`; on mobile ChatGPT, use the host's `@` picker to select the plugin. Treat a typed `$mood-palette` as the same request when the skill is available. Respond in the user's language.

## Input and selection

Use photos attached to this chat directly, including photos uploaded from a phone. Do not require a desktop transfer, computer path, or separate storage service. If an edit is requested without the photo attached, ask for the photo in this chat. Palette recommendations may proceed independently, but text-to-image generation is not an edit of an unseen photo. For ambiguous multiple inputs, establish which image is the base and which is only a style reference.

- The base photo is the edit target: preserve subject identity, object count, pose, composition, and the user's important details.
- A three-column card supplies colors only: its swatches, HEX labels, ID, text, and borders do not belong in the wallpaper.
- For recommendations or “let me choose,” show five existing clean cards by default and wait.
- For an explicit palette ID or “pick one and make it,” report the chosen ID and continue without another selection approval.

Use the existing Python helper when execution is available. Otherwise read [the portable index](portable-search.json): keys are `color|lightness-or-any|saturation-or-any`, such as `blue|any|any` and `pink|light|muted`. Supported basic colors are blue, pink, yellow, red, orange, green, cyan, purple, brown, white, gray, black, and any. Normalize everyday language to these keys. Arrays are already ranked and deduplicated. Take the first N entries (default five), then retrieve each complete record, original colors, and image path by ID from [the catalog](palettes.json). Report empty or short results without padding or silently dropping filters. For moods, use [the theme index](index.md) to select real library IDs.

Image paths are relative to the skill resource directory provided by the host. Display the existing PNG using the host's actual file, attachment, or resource URL; resolve absolute computer paths only during local execution. Do not expose desktop paths as phone links, invent CDN URLs, or retrieve old reference artwork. If the host cannot display or deliver a resource image, explain the limitation and give the true HEX values as a temporary supplement without claiming that the card was shown.

Keep the displayed option number, actual ID, suggested primary, and selected photo associated in the current conversation. “Option 2” and “the same photo” reuse that mapping rather than rerunning a search and changing the choices.

## Edit and deliver

Use the host's available image-editing capability, passing the base photo as an actual image input and the palette card only as a color reference. If only text-to-image is available and the photo cannot be passed to an editing tool, report the limitation and provide an edit prompt without claiming an edit was performed. Specify the edit target, allowed changes to colors/light/mood, preserved subject and composition, whether new elements are allowed, and the intended role of each selected color.

For recoloring alone, preserve content and add no people, objects, text, or logos. Expand the scene creatively only when requested. Honor a supplied phone model or aspect ratio; otherwise default to a portrait 9:16 composition, protecting important subjects and leaving a quiet upper region. Explain any background extension needed to fit the format rather than stretching the subject. Do not promise exact device dimensions or pixel-identical preservation.

Inspect subject, composition, important details, color direction, and portrait framing before delivering the actual generated image. Briefly identify the palette ID and relevant editing deviations. Explain unavailable generation tools. HEX guides the result rather than guaranteeing exact pixels. If unchanged source pixels are required, explain that a deterministic color-grading workflow is needed rather than claiming generative editing is exact replacement.

Photos and outputs belong to the current chat. Unless requested, do not publish them to GitHub, plugin assets, public URLs, or third-party storage. Do not write photos back into the catalog or treat an attached image as authorization to expand the palette library. The plugin carries only generic instructions, original catalog values, and clean swatch cards.

## Examples

```text
Use Mood Palette to recommend five palettes for this photo; let me choose first.
Choose option 2 and turn the same photo into a phone wallpaper. Preserve the person and composition; no text.
Recolor this photo with rain-slate-06, keeping the scenery and camera angle, portrait 9:16.
Keep the photo content and show bright, muted pink options before generating anything.
```
