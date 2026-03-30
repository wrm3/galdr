"""
install_rest.py — REST endpoint for galdr template downloads.

GET  /install/download           — stream templates/ as ZIP (first install)
POST /install/download           — stream templates/ as ZIP with merge/skip options

This endpoint is private (localhost or VPN only) — no auth required.

POST body (JSON, optional):
  existing_files  dict  {"agents.md": "<content>", ...}  merge instead of overwrite
  skip_files      list  ["GUARDRAILS.md"]                 omit from ZIP entirely
"""
import io
import logging
import zipfile
from pathlib import Path
from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

logger = logging.getLogger(__name__)

TEMPLATE_DIR = Path("/app/templates")


async def download(request: Request):
    """GET or POST /install/download — stream templates/ as a ZIP."""
    if not TEMPLATE_DIR.exists():
        return JSONResponse(
            {"error": f"template directory not found: {TEMPLATE_DIR}"},
            status_code=500,
        )

    # Parse optional POST body
    existing_files: dict[str, str] = {}
    skip_files: set[str] = set()

    if request.method == "POST":
        try:
            body = await request.json()
            existing_files = body.get("existing_files") or {}
            skip_files = {f.lower() for f in (body.get("skip_files") or [])}
        except Exception:
            pass

    # Import merge logic
    try:
        from .tools.plugins._galdr_shared import merge_markdown_file, MERGEABLE_FILES
    except ImportError:
        merge_markdown_file = None
        MERGEABLE_FILES = set()

    buf = io.BytesIO()
    files_included = []
    files_skipped = []
    files_merged = []

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(TEMPLATE_DIR.rglob("*")):
            if not path.is_file():
                continue

            arcname = str(path.relative_to(TEMPLATE_DIR))
            filename_lower = path.name.lower()

            if filename_lower in skip_files:
                files_skipped.append(arcname)
                continue

            content = path.read_bytes()

            if (
                merge_markdown_file is not None
                and filename_lower in MERGEABLE_FILES
                and path.name in existing_files
            ):
                source_text = content.decode("utf-8", errors="replace")
                dest_text = existing_files[path.name]
                merged_text = merge_markdown_file(source_text, dest_text, path.name)
                content = merged_text.encode("utf-8")
                files_merged.append(arcname)
            else:
                files_included.append(arcname)

            zf.writestr(arcname, content)

    buf.seek(0)
    zip_bytes = buf.read()

    logger.info(
        f"install_rest: serving ZIP — "
        f"{len(files_included) + len(files_merged)} files "
        f"({len(files_merged)} merged, {len(files_skipped)} skipped), "
        f"{len(zip_bytes):,} bytes"
    )

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=GALDR_template.zip"},
    )


INSTALL_ROUTES = [
    Route("/install/download", endpoint=download, methods=["GET", "POST"]),
]


def init_install_rest(config: Optional[dict] = None) -> None:
    logger.info(
        f"install_rest: initialized "
        f"(template_dir={TEMPLATE_DIR}, exists={TEMPLATE_DIR.exists()})"
    )
