"""
Markdown to HTML Converter Plugin

Converts markdown content to a beautifully styled, self-contained HTML document.
All CSS is embedded so the HTML can be shared as a single file.
"""

import logging
import os
from datetime import datetime
from typing import Optional

# ============================================================
# PLUGIN METADATA
# ============================================================

TOOL_NAME = "md_to_html"

TOOL_DESCRIPTION = (
    "Convert markdown content to a beautifully styled, self-contained HTML document. "
    "All CSS is embedded inline so the resulting HTML can be shared as a single file. "
    "Supports tables, fenced code blocks, syntax highlighting, table of contents, "
    "blockquotes, and responsive design. "
    "IMPORTANT: This tool runs inside a Docker container and cannot write to host filesystem paths. "
    "Do NOT use output_path with host paths (e.g. C:\\, G:\\, /home/). "
    "Instead, use the returned 'html' field and save it yourself with your file-write tools."
)

TOOL_PARAMS = {
    "markdown_content": "The markdown text to convert to HTML (required)",
    "title": "Title for the HTML document. Auto-detected from first H1 heading if not provided",
    "output_path": (
        "Optional file path to save the generated HTML INSIDE the container. "
        "WARNING: This runs in Docker - host paths will NOT work. "
        "Prefer using the returned 'html' field and saving with your own file tools."
    ),
    "include_footer": "Whether to include a generation timestamp footer (default: true)",
    "source_label": "Label shown in the footer for the source (default: 'Markdown input')",
}

logger = logging.getLogger(__name__)

# ============================================================
# EMBEDDED CSS (Professional styling)
# ============================================================

EMBEDDED_CSS = """
:root {
    --bg: #ffffff;
    --text: #1a1a2e;
    --heading: #16213e;
    --link: #0f3460;
    --code-bg: #f4f4f8;
    --code-border: #ddd;
    --table-border: #ccc;
    --table-header-bg: #16213e;
    --table-header-text: #ffffff;
    --table-alt-row: #f8f9fa;
    --blockquote-bg: #fff3cd;
    --blockquote-border: #ffc107;
    --hr-color: #dee2e6;
    --shadow: rgba(0,0,0,0.08);
}
* { box-sizing: border-box; }
body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.7;
    color: var(--text);
    background: #f0f2f5;
    margin: 0;
    padding: 20px;
}
.container {
    max-width: 1100px;
    margin: 0 auto;
    background: var(--bg);
    padding: 40px 60px;
    border-radius: 8px;
    box-shadow: 0 2px 12px var(--shadow);
}
h1 {
    color: var(--heading);
    border-bottom: 3px solid var(--heading);
    padding-bottom: 12px;
    margin-top: 0;
    font-size: 2em;
}
h2 {
    color: var(--heading);
    border-bottom: 2px solid #dee2e6;
    padding-bottom: 8px;
    margin-top: 2em;
    font-size: 1.5em;
}
h3 {
    color: #2c3e50;
    margin-top: 1.5em;
    font-size: 1.2em;
}
h4 {
    color: #34495e;
    margin-top: 1.2em;
}
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
p { margin: 0.8em 0; }
code {
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 4px;
    padding: 2px 6px;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', 'Courier New', monospace;
    font-size: 0.9em;
    color: #c7254e;
}
pre {
    background: #1e1e2e;
    color: #cdd6f4;
    border-radius: 6px;
    padding: 16px 20px;
    overflow-x: auto;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', 'Courier New', monospace;
    font-size: 0.85em;
    line-height: 1.5;
    margin: 1em 0;
}
pre code {
    background: none;
    border: none;
    padding: 0;
    color: inherit;
    font-size: inherit;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.92em;
}
th {
    background: var(--table-header-bg);
    color: var(--table-header-text);
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}
td {
    padding: 8px 14px;
    border-bottom: 1px solid var(--table-border);
}
tr:nth-child(even) td {
    background: var(--table-alt-row);
}
tr:hover td {
    background: #e8f4f8;
}
blockquote {
    background: var(--blockquote-bg);
    border-left: 4px solid var(--blockquote-border);
    margin: 1em 0;
    padding: 12px 20px;
    border-radius: 0 6px 6px 0;
}
blockquote p { margin: 0.4em 0; }
blockquote strong { color: #856404; }
hr {
    border: none;
    border-top: 2px solid var(--hr-color);
    margin: 2em 0;
}
ul, ol {
    padding-left: 1.8em;
}
li {
    margin: 0.3em 0;
}
strong { color: #1a1a2e; }
em { color: #555; }
.toc-title {
    font-weight: bold;
    color: var(--heading);
    margin-bottom: 8px;
}
@media print {
    body { background: white; padding: 0; }
    .container { box-shadow: none; padding: 20px; max-width: 100%; }
    pre { background: #f4f4f4 !important; color: #333 !important; border: 1px solid #ccc; }
    a { color: #333; }
    h1, h2, h3 { page-break-after: avoid; }
    table, pre, blockquote { page-break-inside: avoid; }
}
@media (max-width: 768px) {
    .container { padding: 20px; }
    body { padding: 10px; }
    pre { font-size: 0.8em; }
    table { font-size: 0.85em; }
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="container">
{body}
{footer}
    </div>
</body>
</html>
"""

FOOTER_TEMPLATE = (
    '        <footer style="margin-top:3em; padding-top:1em; '
    'border-top:1px solid #ddd; color:#888; font-size:0.85em;">'
    "\n            <p>Generated from <code>{source_label}</code> "
    "on {gen_date}</p>\n        </footer>"
)


# ============================================================
# PLUGIN IMPLEMENTATION
# ============================================================


def _extract_title(md_text: str) -> str:
    """Extract title from the first H1 heading in markdown text."""
    for line in md_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            return stripped.lstrip("# ").strip()
    return "Document"


def _convert_markdown(md_text: str) -> str:
    """Convert markdown text to HTML body using the markdown library."""
    import markdown

    extensions = [
        "tables",
        "fenced_code",
        "codehilite",
        "toc",
        "nl2br",
        "sane_lists",
        "smarty",
    ]
    extension_configs = {
        "toc": {
            "permalink": False,
            "toc_depth": "2-4",
        },
        "codehilite": {
            "css_class": "highlight",
            "guess_lang": False,
            "noclasses": True,
        },
    }

    md = markdown.Markdown(
        extensions=extensions,
        extension_configs=extension_configs,
    )
    return md.convert(md_text)


async def execute(
    markdown_content: str,
    title: Optional[str] = None,
    output_path: Optional[str] = None,
    include_footer: bool = True,
    source_label: Optional[str] = None,
    context: dict = None,
) -> dict:
    """
    Convert markdown content to styled, self-contained HTML.

    Returns the HTML string and optionally saves to a file.
    """
    try:
        if not markdown_content or not markdown_content.strip():
            return {
                "success": False,
                "error": "markdown_content is required and cannot be empty",
            }

        # Auto-detect title from first H1 if not provided
        resolved_title = title if title else _extract_title(markdown_content)

        # Convert markdown to HTML body
        body_html = _convert_markdown(markdown_content)

        # Build footer
        footer_html = ""
        if include_footer:
            label = source_label or "Markdown input"
            gen_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            footer_html = FOOTER_TEMPLATE.format(
                source_label=label,
                gen_date=gen_date,
            )

        # Assemble final HTML
        html = HTML_TEMPLATE.format(
            title=resolved_title,
            css=EMBEDDED_CSS,
            body=body_html,
            footer=footer_html,
        )

        result = {
            "success": True,
            "title": resolved_title,
            "html": html,
            "html_length": len(html),
        }

        # Detect host filesystem paths (this runs inside Docker)
        if output_path:
            _is_host_path = (
                # Windows drive letters (C:\, G:\, etc.)
                (len(output_path) >= 2 and output_path[1] == ":")
                # Common host Linux/Mac paths
                or output_path.startswith("/home/")
                or output_path.startswith("/Users/")
                or output_path.startswith("/mnt/")
            )
            if _is_host_path:
                result["warning"] = (
                    f"output_path '{output_path}' looks like a host filesystem path. "
                    "This tool runs inside Docker and CANNOT write to host paths. "
                    "The file was NOT saved. Use the 'html' field in this response "
                    "and save it with your IDE's file-write tools instead."
                )
                logger.warning(
                    "Skipped saving to host path: %s (Docker cannot access host filesystem)",
                    output_path,
                )
            else:
                # Container-local path - safe to write
                output_path = os.path.expanduser(output_path)

                parent_dir = os.path.dirname(output_path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html)

                file_size = os.path.getsize(output_path)
                result["saved_to"] = output_path
                result["file_size_bytes"] = file_size
                logger.info(
                    "HTML saved to %s (%s bytes)", output_path, f"{file_size:,}"
                )

        return result

    except ImportError:
        return {
            "success": False,
            "error": (
                "The 'markdown' Python package is required but not installed. "
                "Add 'markdown>=3.5' to requirements.txt and rebuild."
            ),
        }
    except OSError as e:
        return {
            "success": False,
            "error": f"File I/O error: {e}",
        }
    except Exception as e:
        logger.exception("md_to_html conversion failed")
        return {
            "success": False,
            "error": f"Conversion failed: {e}",
        }
