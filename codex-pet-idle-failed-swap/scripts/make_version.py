#!/usr/bin/env python3
"""Create a new installable pet version with idle and failed visuals swapped."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "codex-pet-foot-forward"
OUTPUT = ROOT / "codex-pet-idle-failed-swap"
CELL_W, CELL_H = 192, 208
COLUMNS, ROWS = 8, 9
ROW_BY_STATE = {
    "idle": 0,
    "running-right": 1,
    "running-left": 2,
    "waving": 3,
    "jumping": 4,
    "failed": 5,
    "waiting": 6,
    "running": 7,
    "review": 8,
}
FRAME_COUNTS = {
    "idle": 6,
    "running-right": 8,
    "running-left": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
}
FRAME_MAP = {
    "idle": [("failed", i) for i in (0, 1, 3, 4, 6, 7)],
    "failed": [("idle", i) for i in (0, 1, 1, 2, 3, 4, 4, 5)],
}
NATIVE_DURATIONS = {
    "idle": [280, 110, 110, 140, 140, 320],
    "failed": [140, 140, 140, 140, 140, 140, 140, 240],
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def crop_cell(image: Image.Image, row: int, column: int) -> Image.Image:
    x, y = column * CELL_W, row * CELL_H
    return image.crop((x, y, x + CELL_W, y + CELL_H))


def crop_row(image: Image.Image, row: int) -> Image.Image:
    y = row * CELL_H
    return image.crop((0, y, CELL_W * COLUMNS, y + CELL_H))


def transparent_checker(size: tuple[int, int], square: int = 16) -> Image.Image:
    canvas = Image.new("RGBA", size, (238, 238, 238, 255))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if (x // square + y // square) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill=(216, 216, 216, 255))
    return canvas


def save_gif(frames: list[Image.Image], durations: list[int], path: Path) -> None:
    checker = transparent_checker((CELL_W, CELL_H))
    rendered = []
    for frame in frames:
        rgba = checker.copy()
        rgba.alpha_composite(frame.convert("RGBA"))
        rendered.append(rgba.convert("P", palette=Image.Palette.ADAPTIVE, colors=256))
    rendered[0].save(
        path,
        format="GIF",
        save_all=True,
        append_images=rendered[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def make_contact_sheet(atlas: Image.Image, output_path: Path) -> None:
    thumb_w, thumb_h = 96, 104
    top_pad, state_header, frame_header = 28, 20, 12
    width = COLUMNS * thumb_w
    height = top_pad + ROWS * (state_header + frame_header + thumb_h)
    sheet = Image.new("RGB", (width, height), (25, 29, 31))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((8, 8), "SUNYU BAOBAO | IDLE AND FAILED SWAPPED", fill=(255, 255, 255), font=font)

    for state, row in ROW_BY_STATE.items():
        y = top_pad + row * (state_header + frame_header + thumb_h)
        draw.rectangle((0, y, width - 1, y + state_header - 1), fill=(35, 54, 44))
        draw.text((7, y + 5), f"row {row}  {state}  {FRAME_COUNTS[state]} frames", fill=(250, 250, 250), font=font)
        y += state_header
        checker = transparent_checker((thumb_w, thumb_h), square=12)
        for column in range(COLUMNS):
            x = column * thumb_w
            draw.rectangle((x, y, x + thumb_w - 1, y + frame_header - 1), fill=(42, 46, 48))
            draw.text((x + 4, y + 2), str(column), fill=(220, 225, 222), font=font)
            if column < FRAME_COUNTS[state]:
                frame = crop_cell(atlas, row, column).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                tile = checker.copy()
                tile.alpha_composite(frame.convert("RGBA"))
                sheet.paste(tile.convert("RGB"), (x, y + frame_header))
    sheet.save(output_path, format="PNG", optimize=True)


def main() -> None:
    allowed_files = {OUTPUT / "scripts" / "make_version.py", OUTPUT / "使用说明.md"}
    if OUTPUT.exists() and any(path.is_file() and path not in allowed_files for path in OUTPUT.rglob("*")):
        raise SystemExit(f"Refusing to overwrite generated version data: {OUTPUT}")

    source_png = SOURCE / "final" / "spritesheet.png"
    source_webp = SOURCE / "final" / "spritesheet.webp"
    with Image.open(source_png) as opened:
        original = opened.convert("RGBA")
    if original.size != (CELL_W * COLUMNS, CELL_H * ROWS):
        raise SystemExit(f"Unexpected source atlas size: {original.size}")

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "final").mkdir(exist_ok=True)
    (OUTPUT / "qa" / "previews").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "frames" / "idle").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "frames" / "failed").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "scripts").mkdir(exist_ok=True)

    result = original.copy()
    blank = Image.new("RGBA", (CELL_W * COLUMNS, CELL_H), (0, 0, 0, 0))
    for state in ("idle", "failed"):
        row = ROW_BY_STATE[state]
        result.paste(blank, (0, row * CELL_H))
        frames = []
        for index, (source_state, source_index) in enumerate(FRAME_MAP[state]):
            source_row = ROW_BY_STATE[source_state]
            frame = crop_cell(original, source_row, source_index)
            frames.append(frame)
            result.paste(frame, (index * CELL_W, row * CELL_H))
            frame.save(OUTPUT / "frames" / state / f"{index:02d}.png", format="PNG", optimize=True)
        save_gif(frames, NATIVE_DURATIONS[state], OUTPUT / "qa" / "previews" / f"{state}.gif")

    result.save(OUTPUT / "final" / "spritesheet.png", format="PNG", optimize=True)
    result.save(
        OUTPUT / "final" / "spritesheet.webp",
        format="WEBP",
        lossless=True,
        quality=100,
        method=6,
        exact=True,
    )

    pet = {
        "id": "sunyu-baobao",
        "displayName": "孙煜宝宝",
        "description": "孙煜宝宝：待机与失落动作画面互换版。",
        "spriteVersionNumber": 1,
        "spritesheetPath": "spritesheet.webp",
    }
    (OUTPUT / "final" / "pet.json").write_text(json.dumps(pet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    errors: list[str] = []
    row_checks = []
    for row in range(ROWS):
        changed = row in (ROW_BY_STATE["idle"], ROW_BY_STATE["failed"])
        identical = crop_row(original, row).tobytes() == crop_row(result, row).tobytes()
        if identical == changed:
            errors.append(f"Unexpected pixel identity result for row {row}")
        row_checks.append({"row": row, "state": next(name for name, index in ROW_BY_STATE.items() if index == row), "changed": not identical, "pixel_identical": identical})

    cells = []
    for state, row in ROW_BY_STATE.items():
        for column in range(COLUMNS):
            cell = crop_cell(result, row, column)
            alpha_histogram = cell.getchannel("A").histogram()
            nontransparent = sum(alpha_histogram[1:])
            used = column < FRAME_COUNTS[state]
            if used and nontransparent == 0:
                errors.append(f"Empty used cell: {state} column {column}")
            if not used and nontransparent != 0:
                errors.append(f"Unexpected artwork in unused cell: {state} column {column}")
            cells.append({
                "state": state,
                "row": row,
                "column": column,
                "used": used,
                "nontransparent_pixels": nontransparent,
            })

    with Image.open(OUTPUT / "final" / "spritesheet.webp") as webp:
        webp.load()
        webp_matches_png = result.tobytes() == webp.convert("RGBA").tobytes()
    if not webp_matches_png:
        errors.append("Lossless WebP pixels differ from the PNG master")

    validation = {
        "ok": not errors,
        "version": "idle-failed-swap",
        "source_version": "codex-pet-foot-forward",
        "operation": "Swap idle and failed animation visuals while preserving native frame counts",
        "format": "WEBP",
        "mode": "RGBA",
        "columns": COLUMNS,
        "rows": ROWS,
        "sprite_version_number": 1,
        "width": result.width,
        "height": result.height,
        "native_frame_counts": FRAME_COUNTS,
        "lossless_webp_matches_png": webp_matches_png,
        "errors": errors,
        "warnings": [],
        "cells": cells,
    }
    (OUTPUT / "final" / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    row_preservation = {
        "source": "codex-pet-foot-forward/final/spritesheet.png",
        "changed_rows": [0, 5],
        "preserved_rows": [1, 2, 3, 4, 6, 7, 8],
        "all_preserved_rows_pixel_identical": all(check["pixel_identical"] for check in row_checks if check["row"] not in (0, 5)),
        "rows": row_checks,
        "frame_mapping": {
            "idle_row_0_from_failed_row_5_columns": [0, 1, 3, 4, 6, 7],
            "failed_row_5_from_idle_row_0_columns": [0, 1, 1, 2, 3, 4, 4, 5],
            "reason": "The native idle slot has 6 frames and failed slot has 8; source poses are sampled or held to fill each fixed slot without blank frames.",
        },
    }
    (OUTPUT / "qa" / "row-preservation.json").write_text(json.dumps(row_preservation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    make_contact_sheet(result, OUTPUT / "qa" / "contact-sheet.png")

    zip_path = OUTPUT / "孙煜宝宝-待机失落互换版.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(OUTPUT / "final" / "pet.json", "sunyu-baobao/pet.json")
        archive.write(OUTPUT / "final" / "spritesheet.webp", "sunyu-baobao/spritesheet.webp")
    with zipfile.ZipFile(zip_path) as archive:
        if sorted(archive.namelist()) != ["sunyu-baobao/pet.json", "sunyu-baobao/spritesheet.webp"]:
            errors.append("Package contents do not match the install contract")
        else:
            packaged_sheet = Image.open(archive.open("sunyu-baobao/spritesheet.webp"))
            if result.tobytes() != packaged_sheet.convert("RGBA").tobytes():
                errors.append("Packaged spritesheet differs from the final master")

    summary = {
        "ok": not errors,
        "version": "codex-pet-idle-failed-swap",
        "source_version": "codex-pet-foot-forward",
        "changed_states": ["idle", "failed"],
        "preserved_states": ["running-right", "running-left", "waving", "jumping", "waiting", "running", "review"],
        "frame_mapping": row_preservation["frame_mapping"],
        "installed_pet_changed": False,
        "package": zip_path.name,
        "contact_sheet": "qa/contact-sheet.png",
        "validation": "final/validation.json",
        "row_preservation": "qa/row-preservation.json",
        "sha256": {
            "source_spritesheet_webp": sha256(source_webp),
            "spritesheet_webp": sha256(OUTPUT / "final" / "spritesheet.webp"),
            "package_zip": sha256(zip_path),
        },
        "errors": errors,
    }
    (OUTPUT / "qa" / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        raise SystemExit("Version generated with errors: " + "; ".join(errors))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
