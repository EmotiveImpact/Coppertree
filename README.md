# Copper Tree universe: development source pack
Version 0.3 | 9 November 2026 | Working internal project name

Start with PROJECT_STATE.md, then bible/WORLD_BIBLE.md and decisions/DECISIONS.md.
This repository records the Copper Tree world, the first three story manuscripts and their production sources. See PROJECT_STATE.md for the current artwork and PDF completion status. Canonical repository: https://github.com/EmotiveImpact/Coppertree (public, as directed by the owner).

## Source of truth
- User-confirmed decisions take precedence over proposals.
- Preserve stable entity IDs when renaming characters or places.
- graph/universe.json records relationships and their development status.
- Timeline events describe proposed story events, not published history.
- assets/ASSET_REGISTER.md identifies existing artwork and name discrepancies.
- Update the decision log, graph and project state together after a canon change.
- Never silently turn an assistant suggestion into confirmed canon.

## Repository
EmotiveImpact/Coppertree is public with the owner’s explicit approval. The name is an internal project label, not a cleared publishing brand. Keep account-specific links, credentials and personal information out of repository files.

## Contents
bible/: creative foundations, characters and places
books/: complete story manuscripts, series plan and collection continuity
graph/: machine-readable information graph
decisions/: decisions, proposals and unresolved questions
production/: continuity workflow and reproducible PDF builder
assets/: artwork provenance and reference links
PROJECT_STATE.md: current position and next actions

## First three books

| Book | Manuscript |
|---|---|
| The Map Beneath the Sunflowers | [Book 1](books/book1.json) |
| Zuri and the Footprints After Rain | [Book 2](books/book2.json) |
| Kofi and the Almost-Perfect Machine | [Book 3](books/book3.json) |

Read [collection continuity](books/COLLECTION_CONTINUITY.md) before writing further adventures. The existing neighbourhood map is a rough reference awaiting redesign.

To rebuild the PDFs after all scene assets are present, run python3 production/build_books.py. The builder requires Python, ReportLab, Pillow and DejaVu fonts. It reads the twelve story sections and six colouring scenes for each book and writes A4 PDFs under output/pdf/.

## Printable editions

- [The Map Beneath the Sunflowers](output/pdf/Copper-Tree-Book-1.pdf)
- [Zuri and the Footprints After Rain](output/pdf/Copper-Tree-Book-2.pdf)
- [Kofi and the Almost-Perfect Machine](output/pdf/Copper-Tree-Book-3.pdf)

Each first printable edition has 22 A4 pages. Physical print proof is pending.
