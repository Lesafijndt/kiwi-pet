# Kiwi animated pet archive

Final authored Kiwi artwork and a reproducible preview helper for a v2 animated coding companion. This is an artwork project, not a standalone application or a service upload client.

## Contents

- `assets/spritesheet.png`: the single final atlas, 1536 x 2288 pixels; 8 columns x 11 rows; cells are 192 x 208 pixels.
- `assets/kiwi.gif`, `assets/kiwi.mp4`, `assets/contact-sheet.png`, `assets/four-stills.png`: final presentation previews.
- `pet_request.json`: sanitized name, description, atlas geometry and animation-row definitions.
- `validation/`: recorded artwork/atlas checks. These are historical results, not checks rerun during this backup.
- `scripts/finish_previews.py`: authored helper for regenerating per-state previews and direction-review notes from the final atlas.

Nine motion rows are followed by two rows containing sixteen look directions. Read the frame counts in `pet_request.json`; unused atlas cells are not animation frames.

## Preview setup

Use Python 3.10 or newer in an isolated environment. Install `requirements.txt`, then run `python scripts/finish_previews.py` from this repository. The script reads only `assets/spritesheet.png` and writes generated output below `qa/`. It creates GIF/MP4 previews; it does not regenerate the character or upload/activate a pet. FFmpeg is provided by the imageio-ffmpeg dependency.

The helper was adapted only to use this archive's directory layout. Dependencies are listed without frozen versions because the original environment lockfile was not retained.

## Provenance and exclusions

Source workspace: `Documents/Codex/2026-11-08/pets-plugin-work-pets-openai-curated`. The artwork was authored in that workspace using image generation and local assembly/validation. `SOURCE_MANIFEST.json` records selected original paths. The binary atlas is preserved unchanged; no duplicate final atlas or ZIP is included.

Excluded: service record IDs, creation timestamps, generation job IDs/paths, raw/intermediate artwork, downloaded layout guides, and duplicate final archives. The request contains only the descriptive fields needed to interpret the final atlas. This repository contains no service credentials or upload authorization.
