# g-ingest-url

One-time URL ingestion into vault `research/articles/`.

Activates **g-skl-ingest-url** → INGEST_URL or INGEST_URL_BATCH operation.

## Usage

```
@g-ingest-url https://example.com/article
@g-ingest-url https://example.com/article --title "Custom Title" --topics "ai,benchmarks"
@g-ingest-url --urls-file my_urls.txt
```

## What it does

1. Checks if URL is already captured (dedup via `_index.yaml`) — skips duplicates unless `--force`
2. Crawls URL via `g-skl-crawl` (crawl4ai) → clean Markdown
3. Writes vault note to `research/articles/{date}_{slug}.md`
4. Registers URL in `research/articles/_index.yaml`
5. Updates `vault/log.md`

## Notes

- No revisit schedule — these are one-shot snapshots
- Use `@g-ingest-docs` for documentation that should be refreshed periodically
- Use `--force` to re-capture an already-indexed URL
- Requires `g-skl-crawl` (crawl4ai) — run `@g-crawl SETUP` first

## Prerequisites

```bash
pip install crawl4ai pyyaml
python -m playwright install --with-deps chromium
```
