#!/usr/bin/env python3
"""Look up a palette or calculate contrast for opaque sRGB colors. Standard library only."""
import argparse
import json
import re
from pathlib import Path


def luminance(color):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError("Colors must use #RRGGBB format")
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return sum(c * w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground, background):
    a, b = sorted((luminance(foreground), luminance(background)))
    return (b + 0.05) / (a + 0.05)


def catalog():
    return json.loads((Path(__file__).resolve().parents[1] / "references/palettes.json").read_text())


def self_test():
    assert abs(contrast("#000000", "#FFFFFF") - 21) < 1e-10
    assert contrast("#336699", "#336699") == 1
    assert contrast("#123456", "#ABCDEF") == contrast("#ABCDEF", "#123456")
    assert contrast("#777777", "#FFFFFF") < 4.5
    assert contrast("#767676", "#FFFFFF") > 4.5
    for invalid in ("red", "#fff", "#gg0000", "#12345678"):
        try:
            luminance(invalid)
        except ValueError:
            continue
        raise AssertionError(invalid)
    data = catalog()
    assert len(data["palettes"]) == 100
    assert len({p["id"] for p in data["palettes"]}) == 100
    for p in data["palettes"]:
        assert len(p["colors"]) == 3
        image_path = Path(__file__).resolve().parents[1] / p["image"]
        assert image_path.is_file() and image_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        assert p["method"] in ("printed_hex", "image_sample")
        assert p["family"] in {f["id"] for f in data["families"]}
        for color in p["colors"]:
            luminance(color)
    print("PASS: contrast edge cases, input validation, and 100 palette records")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("palette_id", nargs="?")
    action.add_argument("--list", action="store_true")
    action.add_argument("--contrast", nargs=2, metavar=("FOREGROUND", "BACKGROUND"))
    action.add_argument("--self-test", action="store_true")
    action.add_argument("--search", metavar="COLOR", help="Search a basic color name such as blue, pink, or any")
    parser.add_argument("--limit", type=int, default=5, help="Number of recommendations, default 5")
    parser.add_argument("--lightness", choices=("light", "dark"), help="Filter the whole palette by lightness")
    parser.add_argument("--saturation", choices=("muted", "vivid"), help="Filter the whole palette by saturation")
    args = parser.parse_args()
    if not args.search and (args.lightness or args.saturation or args.limit != 5):
        parser.error("Filters and count apply only to --search")
    if args.self_test:
        self_test()
    elif args.contrast:
        try:
            ratio = contrast(*args.contrast)
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps({"ratio": ratio, "normal_text_AA": ratio >= 4.5,
                          "large_text_or_required_nontext_AA": ratio >= 3}, ensure_ascii=False))
    elif args.search:
        from search import search
        try:
            result = search(catalog(), args.search, args.limit, args.lightness, args.saturation)
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.list:
        print(json.dumps(catalog()["families"], ensure_ascii=False, indent=2))
    else:
        palette = next((p for p in catalog()["palettes"] if p["id"] == args.palette_id), None)
        if palette is None:
            parser.error("Unknown palette ID; use --list for available ranges")
        print(json.dumps(palette, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
