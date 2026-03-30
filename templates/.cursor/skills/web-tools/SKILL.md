---
name: web-tools
description: Web search, scraping, Playwright automation, screenshots, and structured content extraction.
---

# Web Tools Skill

Comprehensive web interaction capabilities including search, scraping, browser automation, and screenshot capture for gathering information and automating web workflows.

## Overview

The Web Tools Skill provides:
- **Web Search**: Search engines with structured results
- **Web Scraping**: Extract content from static and dynamic pages
- **Browser Automation**: Control real browsers with Playwright
- **Screenshot Capture**: Capture web pages and specific elements
- **Concurrent Operations**: Parallel scraping and requests
- **Smart Extraction**: Clean, structured content extraction

## When to Use This Skill

Activate this skill when the user needs to:
- Search the web for information
- Extract content from websites
- Scrape multiple pages concurrently
- Automate browser interactions
- Take screenshots of web pages
- Monitor websites for changes
- Test web applications
- Gather data from web sources

## Capabilities

### Web Search
- **Search Engines**: Google, Bing, DuckDuckGo integration
- **Structured Results**: Title, URL, snippet, ranking
- **Query Options**: Safe search, region, language, date filters
- **Result Filtering**: Relevance scoring, deduplication
- **API Integration**: Direct search engine APIs when available

### Web Scraping
- **Static Pages**: Fast HTML parsing with BeautifulSoup/lxml
- **Dynamic Pages**: JavaScript rendering with headless browser
- **Content Extraction**: Text, HTML, links, images, metadata
- **Concurrent Scraping**: Multiple URLs in parallel
- **Smart Retry**: Automatic retry with exponential backoff
- **Rate Limiting**: Respect robots.txt and rate limits
- **User Agent Rotation**: Avoid detection and blocking
- **Proxy Support**: Rotate through proxy servers

### Browser Automation
- **Navigation**: Go to URLs, forward, back, refresh
- **Interaction**: Click, type, scroll, hover, drag
- **Extraction**: Text, links, attributes, computed styles
- **JavaScript**: Execute custom scripts in page context
- **Waiting**: Smart waits for elements, network, animations
- **Screenshots**: Full page, visible area, specific elements
- **File Handling**: Downloads, uploads, file choosers
- **Multi-Tab**: Manage multiple browser tabs/windows

### Screenshot Capture
- **Full Page**: Entire page including scrollable content
- **Viewport**: Visible area only
- **Element**: Specific DOM elements
- **Formats**: PNG, JPEG, PDF
- **Options**: Quality, dimensions, device emulation
- **Annotations**: Add markers, highlights, text overlays

## MCP Tools Available

This skill integrates with the `galdr_mcp_browser_use` MCP server:

### Search Tools
- `web_search`: Search the web with query and filters
- `web_search_advanced`: Advanced search with custom parameters

### Scraping Tools
- `web_scrape`: Scrape single URL with content extraction
- `web_scrape_batch`: Scrape multiple URLs concurrently
- `web_extract_links`: Extract all links from page
- `web_extract_text`: Extract clean text content
- `web_extract_metadata`: Extract page metadata (title, description, keywords)

### Browser Automation Tools
- `browser_navigate`: Navigate to URL in browser
- `browser_click`: Click element on page
- `browser_type`: Type text into input field
- `browser_extract`: Extract content from page
- `browser_execute_js`: Execute JavaScript in page
- `browser_wait`: Wait for element or condition
- `browser_screenshot`: Capture screenshot

### Screenshot Tools
- `screenshot_webpage`: Take screenshot of web page
- `screenshot_element`: Screenshot specific element
- `screenshot_fullpage`: Full scrollable page screenshot

## Usage Examples

### Example 1: Web Search
```
User: "Search for latest information about Claude AI skills"

Workflow:
1. Use web_search tool with query
2. Get structured results (10 results)
3. Format results with title, URL, snippet
4. Optionally scrape top results for details
5. Summarize findings
```

### Example 2: Web Scraping - Single Page
```
User: "Scrape the documentation from docs.anthropic.com/claude"

Workflow:
1. Use web_scrape with URL
2. Extract content (text, HTML, links)
3. Clean and structure content
4. Extract metadata (title, description)
5. Return formatted content
```

### Example 3: Concurrent Scraping
```
User: "Scrape product info from these 10 URLs"

Workflow:
1. Validate all URLs
2. Use web_scrape_batch for parallel scraping
3. Set concurrency limit (5 concurrent)
4. Configure retry logic (3 retries, exponential backoff)
5. Extract structured data from each page
6. Combine and return results
```

### Example 4: Browser Automation - Form Filling
```
User: "Fill out the contact form on example.com"

Workflow:
1. browser_navigate to example.com/contact
2. browser_wait for form to load
3. browser_type name into #name field
4. browser_type email into #email field
5. browser_type message into #message textarea
6. browser_click submit button
7. browser_wait for confirmation
8. browser_screenshot to capture result
```

### Example 5: Dynamic Content Scraping
```
User: "Extract all products from this infinite scroll page"

Workflow:
1. browser_navigate to page
2. Loop:
   a. browser_extract current products
   b. browser_execute_js to scroll down
   c. browser_wait for new content to load
   d. Check if more products appeared
3. Combine all extracted products
4. Return structured data
```

### Example 6: Screenshot Capture
```
User: "Take screenshot of the hero section on landing page"

Workflow:
1. browser_navigate to landing page
2. browser_wait for hero section to load
3. screenshot_element targeting hero section
4. Save screenshot with annotation
5. Return screenshot path
```

### Example 7: Website Monitoring
```
User: "Monitor pricing page and alert if prices change"

Workflow:
1. web_scrape pricing page
2. Extract current prices
3. Compare with previous scrape
4. If changes detected:
   a. screenshot_webpage for evidence
   b. Extract specific changed elements
   c. Alert user with details
5. Store current state for next check
```

### Example 8: Multi-Page Data Collection
```
User: "Collect all article titles and dates from blog archive"

Workflow:
1. browser_navigate to blog archive
2. Extract pagination links
3. For each page:
   a. web_extract_metadata for articles
   b. Extract title, date, URL, excerpt
   c. Follow next page link
4. Compile all articles
5. Export as structured data (CSV/JSON)
```

## Configuration

### Scraping Settings
```yaml
# Concurrent scraping
max_concurrent: 5              # Max parallel requests
timeout: 30                    # Request timeout (seconds)
retry_max: 3                   # Max retry attempts
retry_delay: 2                 # Initial retry delay (seconds)

# Content extraction
extract_text: true             # Extract clean text
extract_html: false            # Include raw HTML
extract_links: true            # Extract all links
extract_metadata: true         # Extract page metadata

# Politeness
respect_robots_txt: true       # Honor robots.txt
rate_limit: 1.0                # Delay between requests (seconds)
user_agent: "Mozilla/5.0..."   # User agent string
```

### Browser Settings
```yaml
# Browser configuration
headless: true                 # Headless mode (no GUI)
browser: chromium              # chromium, firefox, webkit
viewport_width: 1920           # Viewport width
viewport_height: 1080          # Viewport height
device_emulation: null         # Desktop, mobile device name

# Performance
disable_images: false          # Disable images for speed
disable_javascript: false      # Disable JS (static only)
timeout: 30000                 # Navigation timeout (ms)

# Privacy
clear_cookies: true            # Clear cookies between sessions
disable_cache: false           # Disable browser cache
```

### Screenshot Settings
```yaml
# Screenshot options
format: png                    # png, jpeg, pdf
quality: 90                    # JPEG quality (0-100)
fullpage: false                # Capture full scrollable page
clip: null                     # Clip to specific region {x, y, width, height}
omit_background: false         # Transparent background
```

## Integration Requirements

### MCP Server Setup
Ensure `galdr_mcp_browser_use` is configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "galdr_mcp_browser_use": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\.ai\\mcps\\galdr_mcp_browser_use",
        "run",
        "galdr_mcp_browser_use"
      ]
    }
  }
}
```

### Required Dependencies
The MCP server handles all dependencies including:
- Playwright (browser automation)
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP client)
- lxml (fast XML/HTML parsing)

No additional setup required.

## Best Practices

### Web Scraping Ethics
1. **Respect robots.txt**: Always check and honor robots.txt rules
2. **Rate Limiting**: Don't overwhelm servers with requests
3. **Attribution**: Credit sources when using scraped content
4. **Terms of Service**: Review and comply with website ToS
5. **Personal Data**: Be careful with personal/sensitive information
6. **Load**: Minimize server load, use caching when possible

### Efficient Scraping
1. **Use Static Scraping First**: Faster and lighter than browser automation
2. **Browser Only When Needed**: Use browser for JavaScript-heavy sites
3. **Concurrent Wisely**: Balance speed vs server load (5-10 concurrent max)
4. **Cache Results**: Store results to avoid re-scraping
5. **Incremental Updates**: Only scrape changed content
6. **Error Handling**: Implement robust retry logic

### Browser Automation
1. **Wait Properly**: Use smart waits, not fixed delays
2. **Target Stable Selectors**: Use IDs or stable classes
3. **Handle Popups**: Close cookie notices, ads, modals
4. **Stealth Mode**: Rotate user agents, disable automation flags
5. **Resource Management**: Close browsers properly, clean up

## Troubleshooting

### Common Issues

**Scraping Returns Empty Content**
- Check if site requires JavaScript (use browser automation)
- Verify user agent isn't blocked
- Check if IP is rate-limited
- Inspect robots.txt restrictions

**Browser Automation Timing Out**
- Increase timeout values
- Use explicit waits for elements
- Check network connectivity
- Verify selectors are correct

**Screenshots Are Blank**
- Wait for page to fully load
- Check if content is dynamically loaded
- Verify viewport size is adequate
- Ensure element is visible

**Rate Limiting / IP Blocking**
- Reduce concurrent requests
- Increase delay between requests
- Rotate user agents
- Use proxy rotation
- Check robots.txt compliance

**Content Extraction Issues**
- Verify page structure hasn't changed
- Check if site uses anti-scraping measures
- Try different extraction methods
- Inspect raw HTML for clues

## Comparison to Other Tools

### Web Tools vs Computer Use Agent
- **Web Tools**: Browser and web page automation only
- **Computer Use**: Entire desktop control, any application
- **Use Web Tools For**: Web scraping, search, web testing
- **Use Computer Use For**: Desktop apps, system operations

### Static vs Dynamic Scraping
- **Static (web_scrape)**: Fast, low resource, simple HTML
- **Dynamic (browser_*)**: Handles JavaScript, slower, full rendering
- **Choose Static**: Static pages, APIs, simple content
- **Choose Dynamic**: SPAs, infinite scroll, complex interactions

## Advanced Features

### Proxy Rotation
```yaml
proxies:
  - http://proxy1:8080
  - http://proxy2:8080
  - http://proxy3:8080
proxy_strategy: rotate        # rotate, random, failover
```

### Custom Headers
```yaml
headers:
  User-Agent: "Custom User Agent"
  Accept-Language: "en-US,en;q=0.9"
  Referer: "https://google.com"
  Cookie: "session=abc123"
```

### JavaScript Execution
```javascript
// Execute custom JavaScript in page context
const result = await browser_execute_js(`
  return {
    title: document.title,
    links: Array.from(document.querySelectorAll('a'))
      .map(a => ({href: a.href, text: a.textContent}))
  };
`);
```

### Content Cleaning
- Remove HTML tags, keep text
- Extract structured data (JSON-LD, microdata)
- Normalize whitespace and formatting
- Remove ads, nav, footer elements
- Extract main content only

## Security Considerations

### Safe Scraping
- **Validate URLs**: Check domain, protocol before scraping
- **Sanitize Content**: Clean scraped HTML before processing
- **Timeout Limits**: Prevent infinite loops and hangs
- **Resource Limits**: Cap memory, disk usage
- **Sandboxing**: Use browser in isolated environment

### Data Privacy
- **Don't Scrape PII**: Avoid personal identifiable information
- **Respect Privacy**: Honor privacy policies
- **Secure Storage**: Encrypt stored credentials, cookies
- **Audit Logging**: Log all web interactions for audit trail

## Reference Materials

For detailed implementation information, see:
- [reference/scraping_guide.md](reference/scraping_guide.md) - Web scraping best practices
- [reference/browser_automation_guide.md](reference/browser_automation_guide.md) - Browser automation patterns
- [reference/search_engines.md](reference/search_engines.md) - Search engine integration
- [examples/scraping_workflows.md](examples/scraping_workflows.md) - Example workflows

## Related Skills

- **computer-use-agent**: For desktop application automation
- **database-tools**: For storing scraped data
- **data-processing**: For processing scraped content

---

**Note:** Always respect website terms of service, robots.txt, and rate limits. Web scraping should be done ethically and legally.
