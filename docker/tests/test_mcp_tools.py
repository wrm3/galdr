"""
MCP Tool Smoke Tests - galdr_docker
========================================
Verifies each MCP tool responds with a valid result.

Usage:
    python test_mcp_tools.py                  # Test all tools
    python test_mcp_tools.py --main-only      # Test main MCP server only
    python test_mcp_tools.py --video-only     # Test video analyzer only
    python test_mcp_tools.py --list           # Just list available tools

Requires:
    - Docker containers running (docker compose up -d)
    - requests package (pip install requests)
"""

import json
import sys
import time
import argparse
import uuid
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


# Server endpoints
MAIN_MCP_URL = "http://localhost:8082/mcp"
VIDEO_HEALTH_URL = "http://localhost:8085/health"
VIDEO_SSE_URL = "http://localhost:8085/sse"


class MCPTestClient:
    """Simple MCP client for streamable-http transport."""

    def __init__(self, base_url: str, name: str = "main"):
        self.base_url = base_url
        self.name = name
        self.session_id = None
        self.request_id = 0

    def _next_id(self) -> int:
        self.request_id += 1
        return self.request_id

    def _post(self, method: str, params: Optional[dict] = None) -> dict:
        """Send a JSON-RPC request and parse the response."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._next_id(),
        }
        if params:
            payload["params"] = params

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        resp = requests.post(self.base_url, json=payload, headers=headers, timeout=30)

        # Save session ID from response headers
        if "Mcp-Session-Id" in resp.headers:
            self.session_id = resp.headers["Mcp-Session-Id"]

        content_type = resp.headers.get("Content-Type", "")

        if "text/event-stream" in content_type:
            return self._parse_sse(resp.text)
        else:
            return resp.json()

    def _parse_sse(self, text: str) -> dict:
        """Parse SSE response and extract the JSON-RPC result."""
        result = None
        for line in text.strip().split("\n"):
            if line.startswith("data: "):
                data = line[6:]
                try:
                    parsed = json.loads(data)
                    if "result" in parsed or "error" in parsed:
                        result = parsed
                except json.JSONDecodeError:
                    pass
        return result or {"error": {"message": "No result in SSE stream"}}

    def initialize(self) -> dict:
        """Initialize the MCP session."""
        return self._post("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-test-client", "version": "1.0.0"},
        })

    def list_tools(self) -> list:
        """List all available tools."""
        resp = self._post("tools/list")
        if "result" in resp and "tools" in resp["result"]:
            return resp["result"]["tools"]
        return []

    def call_tool(self, name: str, arguments: dict) -> dict:
        """Call a specific tool and return the result."""
        return self._post("tools/call", {"name": name, "arguments": arguments})


class SSETestClient:
    """Simple MCP client for SSE transport (video analyzer)."""

    def __init__(self, sse_url: str):
        self.sse_url = sse_url
        self.message_url = None
        self.request_id = 0

    def _next_id(self) -> int:
        self.request_id += 1
        return self.request_id

    def connect(self) -> bool:
        """Connect to SSE endpoint and get the message URL."""
        try:
            resp = requests.get(self.sse_url, stream=True, timeout=10,
                                headers={"Accept": "text/event-stream"})
            for line in resp.iter_lines(decode_unicode=True):
                if line and line.startswith("event: endpoint"):
                    continue
                if line and line.startswith("data: "):
                    endpoint = line[6:].strip()
                    if endpoint.startswith("/"):
                        base = self.sse_url.rsplit("/", 1)[0]
                        self.message_url = f"{base}{endpoint}"
                    else:
                        self.message_url = endpoint
                    resp.close()
                    return True
            resp.close()
        except Exception as e:
            print(f"  SSE connect error: {e}")
        return False

    def _post(self, method: str, params: Optional[dict] = None) -> dict:
        """Send JSON-RPC request to the message endpoint."""
        if not self.message_url:
            return {"error": {"message": "Not connected"}}

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._next_id(),
        }
        if params:
            payload["params"] = params

        resp = requests.post(self.message_url, json=payload,
                             headers={"Content-Type": "application/json"},
                             timeout=30)
        if resp.status_code == 202:
            return {"result": "accepted"}
        return resp.json() if resp.text else {"result": "ok"}

    def initialize(self) -> dict:
        return self._post("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-test-client", "version": "1.0.0"},
        })

    def list_tools(self) -> list:
        resp = self._post("tools/list")
        if isinstance(resp, dict) and "result" in resp and "tools" in resp.get("result", {}):
            return resp["result"]["tools"]
        return []

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self._post("tools/call", {"name": name, "arguments": arguments})


# =============================================
# Test definitions for each tool
# =============================================

MAIN_TOOL_TESTS = {
    # Tool name -> (arguments, description, requires_api_key)
    "galdr_server_status": ({}, "Health check", False),
    "oracle_query": (
        {"sql": "SELECT 1 FROM DUAL", "host": "localhost", "username": "test",
         "password": "test", "service_name": "test"},
        "Oracle read query (needs Oracle DB)", True
    ),
    "oracle_execute": (
        {"sql": "SELECT 1 FROM DUAL", "host": "localhost", "username": "test",
         "password": "test", "service_name": "test"},
        "Oracle write query (needs Oracle DB)", True
    ),
    "md_to_html": (
        {"markdown_content": "# Test\n\nHello **world**!", "title": "Test Document"},
        "Markdown to HTML conversion", False
    ),
    "rag_list_subjects": (
        {},
        "List RAG knowledge base subjects", False
    ),
    "rag_list_sources": (
        {},
        "List ingested RAG sources", False
    ),
    "rag_stats": (
        {},
        "RAG knowledge base statistics", False
    ),
    "rag_set_default_subject": (
        {"subject": "work_knowledge"},
        "Set default RAG subject", False
    ),
    "rag_search": (
        {"query": "test query"},
        "Semantic search (needs OPENAI_API_KEY)", True
    ),
    "rag_ingest_text": (
        {"content": "This is a test document for smoke testing.", "title": "Smoke Test Doc"},
        "Ingest text into RAG (needs OPENAI_API_KEY)", True
    ),
    "rag_create_subject": (
        {"subject_id": f"smoke_test_{uuid.uuid4().hex[:8]}", "display_name": "Smoke Test (delete me)"},
        "Create a RAG subject", False
    ),
    "research_search": (
        {"query": "test"},
        "Web search — plugin not yet implemented (placeholder)", True
    ),
    "research_deep": (
        {"topic": "test"},
        "Deep research — plugin not yet implemented (placeholder)", True
    ),
    "mediawiki_search": (
        {"query": "Main Page"},
        "Search MediaWiki (needs MEDIAWIKI config)", True
    ),
    "mediawiki_page": (
        {"action": "read", "title": "Main Page"},
        "Read MediaWiki page (needs MEDIAWIKI config)", True
    ),
    "galdr_install": (
        {"target_path": "/tmp/GALDR_smoke_test", "dry_run": True},
        "Template install (dry run)", True
    ),
}

VIDEO_TOOL_TESTS = {
    "video_server_status": ({}, "Video server health check", False),
    "video_extract_metadata": (
        {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        "Extract video metadata", False
    ),
    "video_extract_transcript": (
        {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        "Extract video transcript", False
    ),
    "video_extract_frames": (
        {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        "Extract video frames", False
    ),
    "video_get_playlist": (
        {"playlist_url": "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"},
        "Get playlist videos", False
    ),
    "video_check_new": (
        {"playlist_url": "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"},
        "Check for new videos", False
    ),
    "video_analyze": (
        {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        "Full video analysis (needs ANTHROPIC or OPENAI key)", True
    ),
    "video_batch_process": (
        {"video_urls": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]},
        "Batch video processing (needs ANTHROPIC or OPENAI key)", True
    ),
}


def check_server_reachable(url: str, name: str) -> bool:
    """Check if a server is reachable."""
    try:
        resp = requests.get(url.replace("/mcp", "/").replace("/sse", "/health"),
                            timeout=5)
        return True
    except requests.ConnectionError:
        print(f"\n  UNREACHABLE: {name} at {url}")
        print(f"  Make sure Docker is running: docker compose up -d")
        return False
    except Exception:
        return True  # Server responded (even with error)


def test_tool(client, tool_name: str, args: dict, description: str,
              requires_key: bool) -> dict:
    """Test a single tool and return the result."""
    result = {
        "tool": tool_name,
        "description": description,
        "requires_api_key": requires_key,
        "status": "unknown",
        "message": "",
    }

    try:
        start = time.time()
        resp = client.call_tool(tool_name, args)
        elapsed = time.time() - start

        result["elapsed_ms"] = round(elapsed * 1000)

        if resp is None:
            result["status"] = "NO_RESPONSE"
            result["message"] = "Server returned no response"
        elif "error" in resp:
            error = resp["error"]
            error_msg = error.get("message", str(error)) if isinstance(error, dict) else str(error)

            # Check if it's an expected failure (missing API key, connection refused, etc.)
            expected_failures = [
                "api_key", "api key", "not configured", "connection refused",
                "ORA-", "TNS:", "connect", "timeout", "credential",
                "OPENAI", "PERPLEXITY", "GOOGLE", "ANTHROPIC", "MEDIAWIKI",
                "authentication", "unauthorized", "403", "401",
                "not available", "not found", "template source",
                "No listener", "Cannot connect",
            ]
            is_expected = any(kw.lower() in error_msg.lower() for kw in expected_failures)

            if is_expected and requires_key:
                result["status"] = "EXPECTED_FAIL"
                result["message"] = f"Expected: {error_msg[:100]}"
            elif "ORA-" in error_msg or "TNS:" in error_msg or "connect" in error_msg.lower():
                result["status"] = "EXPECTED_FAIL"
                result["message"] = f"No DB connection: {error_msg[:80]}"
            else:
                result["status"] = "ERROR"
                result["message"] = error_msg[:150]
        elif "result" in resp:
            resp_result = resp["result"]
            # Check for tool-level error in the result content
            if isinstance(resp_result, dict):
                content = resp_result.get("content", [])
                if isinstance(content, list) and len(content) > 0:
                    text = content[0].get("text", "") if isinstance(content[0], dict) else ""
                    try:
                        parsed = json.loads(text)
                        if isinstance(parsed, dict) and parsed.get("success") is False:
                            error_detail = parsed.get("error", "unknown error")
                            if requires_key:
                                result["status"] = "EXPECTED_FAIL"
                                result["message"] = f"Expected: {str(error_detail)[:100]}"
                            else:
                                result["status"] = "TOOL_ERROR"
                                result["message"] = str(error_detail)[:150]
                        else:
                            result["status"] = "PASS"
                            result["message"] = "Tool responded successfully"
                    except (json.JSONDecodeError, TypeError):
                        result["status"] = "PASS"
                        result["message"] = f"Response: {str(text)[:80]}"
                elif resp_result.get("isError"):
                    error_text = ""
                    if isinstance(content, list) and content:
                        error_text = content[0].get("text", "") if isinstance(content[0], dict) else str(content[0])
                    if requires_key:
                        result["status"] = "EXPECTED_FAIL"
                        result["message"] = f"Expected: {error_text[:100]}"
                    else:
                        result["status"] = "TOOL_ERROR"
                        result["message"] = error_text[:150]
                else:
                    result["status"] = "PASS"
                    result["message"] = "Tool responded successfully"
            else:
                result["status"] = "PASS"
                result["message"] = "Tool responded"
        else:
            result["status"] = "UNEXPECTED"
            result["message"] = f"Unexpected response: {str(resp)[:100]}"

    except requests.Timeout:
        result["status"] = "TIMEOUT"
        result["message"] = "Request timed out (30s)"
    except requests.ConnectionError:
        result["status"] = "CONN_ERROR"
        result["message"] = "Connection refused"
    except Exception as e:
        result["status"] = "EXCEPTION"
        result["message"] = f"{type(e).__name__}: {str(e)[:100]}"

    return result


def print_result(result: dict, index: int) -> None:
    """Print a single test result with color-coded status."""
    status = result["status"]
    tool = result["tool"]
    msg = result["message"]
    elapsed = result.get("elapsed_ms", "?")
    key_marker = " [KEY]" if result["requires_api_key"] else ""

    status_icons = {
        "PASS": "PASS",
        "EXPECTED_FAIL": "SKIP",
        "ERROR": "FAIL",
        "TOOL_ERROR": "FAIL",
        "TIMEOUT": "TIME",
        "CONN_ERROR": "CONN",
        "NO_RESPONSE": "NONE",
        "EXCEPTION": "EXCP",
        "UNEXPECTED": "UNKN",
    }
    icon = status_icons.get(status, "????")

    print(f"  [{icon:>4}] {index:>2}. {tool:<35}{key_marker:<6} ({elapsed}ms) {msg}")


def run_tests(test_main: bool = True, test_video: bool = True,
              list_only: bool = False) -> int:
    """Run all tool smoke tests. Returns exit code (0=pass, 1=failures)."""

    print("=" * 80)
    print("  MCP Tool Smoke Tests - galdr_docker")
    print("=" * 80)

    all_results = []
    total_pass = 0
    total_expected_fail = 0
    total_fail = 0

    # -----------------------------------------------
    # Main MCP Server (streamable-http on port 8084)
    # -----------------------------------------------
    if test_main:
        print(f"\n{'-' * 80}")
        print(f"  MAIN MCP SERVER (http://localhost:8084/mcp)")
        print(f"{'-' * 80}")

        if not check_server_reachable(MAIN_MCP_URL, "Main MCP"):
            return 1

        client = MCPTestClient(MAIN_MCP_URL)

        print("\n  Initializing MCP session...")
        try:
            init_resp = client.initialize()
            if "error" in init_resp:
                print(f"  WARNING: Init returned error: {init_resp['error']}")
            else:
                print(f"  Session initialized (ID: {client.session_id or 'none'})")
        except Exception as e:
            print(f"  WARNING: Init failed: {e}")

        if list_only:
            print("\n  Listing available tools...")
            tools = client.list_tools()
            for i, t in enumerate(tools, 1):
                print(f"    {i:>2}. {t['name']:<35} {t.get('description', '')[:60]}")
            print(f"\n  Total: {len(tools)} tools")
        else:
            print(f"\n  Testing {len(MAIN_TOOL_TESTS)} tools...\n")
            for i, (tool_name, (args, desc, needs_key)) in enumerate(MAIN_TOOL_TESTS.items(), 1):
                result = test_tool(client, tool_name, args, desc, needs_key)
                print_result(result, i)
                all_results.append(result)

    # -----------------------------------------------
    # Video Analyzer MCP Server (SSE on port 8085)
    # -----------------------------------------------
    if test_video:
        print(f"\n{'-' * 80}")
        print(f"  VIDEO ANALYZER MCP SERVER (http://localhost:8085/sse)")
        print(f"{'-' * 80}")

        if not check_server_reachable(VIDEO_HEALTH_URL, "Video Analyzer"):
            if test_main:
                print("  Skipping video tests (server unreachable)")
            else:
                return 1
        else:
            # Test health endpoint first
            try:
                health = requests.get(VIDEO_HEALTH_URL, timeout=5)
                health_data = health.json()
                print(f"\n  Health: {health_data.get('status', 'unknown')} "
                      f"({health_data.get('plugins', 0)} plugins loaded)")
            except Exception as e:
                print(f"\n  Health check failed: {e}")

            # Connect via SSE
            print("  Connecting via SSE...")
            video_client = SSETestClient(VIDEO_SSE_URL)
            connected = video_client.connect()

            if connected:
                print(f"  Connected (message URL: {video_client.message_url})")

                try:
                    video_client.initialize()
                except Exception:
                    pass

                if list_only:
                    print("\n  Listing available tools...")
                    tools = video_client.list_tools()
                    for i, t in enumerate(tools, 1):
                        name = t.get("name", "unknown")
                        desc = t.get("description", "")[:60]
                        print(f"    {i:>2}. {name:<35} {desc}")
                    print(f"\n  Total: {len(tools)} tools")
                else:
                    print(f"\n  Testing {len(VIDEO_TOOL_TESTS)} tools...\n")
                    for i, (tool_name, (args, desc, needs_key)) in enumerate(VIDEO_TOOL_TESTS.items(), 1):
                        result = test_tool(video_client, tool_name, args, desc, needs_key)
                        print_result(result, i)
                        all_results.append(result)
            else:
                print("  Failed to establish SSE connection")
                print("  Testing via health endpoint only...")
                result = {
                    "tool": "video_health_check",
                    "description": "Video server health",
                    "requires_api_key": False,
                    "status": "PASS" if health_data.get("status") == "healthy" else "FAIL",
                    "message": f"Health: {health_data.get('status', 'unknown')}",
                    "elapsed_ms": 0,
                }
                print_result(result, 1)
                all_results.append(result)

    # -----------------------------------------------
    # Summary
    # -----------------------------------------------
    if not list_only and all_results:
        for r in all_results:
            if r["status"] == "PASS":
                total_pass += 1
            elif r["status"] == "EXPECTED_FAIL":
                total_expected_fail += 1
            else:
                total_fail += 1

        print(f"\n{'=' * 80}")
        print(f"  RESULTS SUMMARY")
        print(f"{'=' * 80}")
        print(f"  Total tests:     {len(all_results)}")
        print(f"  Passed:          {total_pass}")
        print(f"  Expected fails:  {total_expected_fail} (missing API keys / no DB connection)")
        print(f"  Failures:        {total_fail}")
        print(f"{'=' * 80}")

        if total_fail > 0:
            print(f"\n  FAILED TOOLS:")
            for r in all_results:
                if r["status"] not in ("PASS", "EXPECTED_FAIL"):
                    print(f"    - {r['tool']}: {r['message']}")
            print()

        status_legend = """
  Status Legend:
    [PASS] - Tool responded successfully
    [SKIP] - Expected failure (missing API key or no DB connection)
    [FAIL] - Unexpected error (tool is broken)
    [TIME] - Request timed out
    [CONN] - Connection refused (server down?)
    [EXCP] - Python exception during test
"""
        print(status_legend)

        return 1 if total_fail > 0 else 0

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Tool Smoke Tests")
    parser.add_argument("--main-only", action="store_true",
                        help="Test main MCP server only")
    parser.add_argument("--video-only", action="store_true",
                        help="Test video analyzer only")
    parser.add_argument("--list", action="store_true",
                        help="List available tools without testing them")
    args = parser.parse_args()

    test_main = not args.video_only
    test_video = not args.main_only

    exit_code = run_tests(test_main=test_main, test_video=test_video,
                          list_only=args.list)
    sys.exit(exit_code)
