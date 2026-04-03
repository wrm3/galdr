# Web Tools - Example Scraping Workflows

## Quick Reference Examples

### Example 1: Simple Web Search
```
User: "Search for latest Claude AI features"

web_search(query="Claude AI latest features 2025")
→ Returns 10 results with titles, URLs, snippets
```

### Example 2: Scrape Single Page
```
User: "Scrape the about page from anthropic.com"

web_scrape(url="https://www.anthropic.com/about")
→ Returns clean text, HTML, links, metadata
```

### Example 3: Scrape Multiple Pages
```
User: "Scrape these 5 product pages"

web_scrape_batch(
  urls=[...5 URLs...],
  max_concurrent=3,
  timeout=30
)
→ Returns array of scraped content
```

### Example 4: Browser Automation - Fill Form
```
User: "Fill out contact form on example.com"

1. browser_navigate("https://example.com/contact")
2. browser_type("#name", "John Doe")
3. browser_type("#email", "john@example.com")
4. browser_type("#message", "Hello!")
5. browser_click("button[type=submit]")
6. screenshot_webpage() to capture confirmation
```

### Example 5: Dynamic Content (Infinite Scroll)
```
User: "Extract all products from infinite scroll page"

1. browser_navigate(url)
2. Loop:
   - browser_extract(".product")
   - browser_execute_js("window.scrollTo(0, document.body.scrollHeight)")
   - browser_wait(2000)
   - Check for new products
3. Return all extracted products
```

### Example 6: Screenshot Capture
```
User: "Take screenshot of homepage"

screenshot_webpage("https://example.com")
→ Returns path to saved PNG screenshot
```

## Complete Workflows

See [reference/scraping_guide.md](../reference/scraping_guide.md) for detailed workflows and best practices.
