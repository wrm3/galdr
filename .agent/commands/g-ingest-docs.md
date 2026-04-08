# g-ingest-docs

Ingest a documentation URL into the vault with periodic revisit tracking.

Activates **g-skl-ingest-docs** → INGEST_DOC or REFRESH_STALE operation.

## Usage

```
@g-ingest-docs --url https://docs.example.com --name "ExampleDocs"
@g-ingest-docs REFRESH_STALE
```

## What it does (INGEST_DOC)

1. Checks if URL is already registered and fresh — skips unless stale or `--force`
2. Crawls URL via `g-skl-crawl` (crawl4ai) → clean Markdown
3. Writes note to `research/platforms/{slug}.md` with staleness frontmatter
4. Registers URL in `research/platforms/_index.yaml` with `next_refresh` date
5. Updates `vault/log.md`

## What it does (REFRESH_STALE)

Scans `_index.yaml`, finds all entries past their `refresh_days` deadline, re-crawls them.

## Notes

- Default `refresh_days: 30` — override with `--refresh-days N`
- Session start shows stale count: `📚 Vault Docs: 12 registered | 3 stale`
- Requires `g-skl-crawl` (crawl4ai) — run `@g-crawl SETUP` first
- Use `--dry-run` to list stale URLs without fetching

## Prerequisites

```bash
pip install crawl4ai pyyaml
python -m playwright install --with-deps chromium
```
