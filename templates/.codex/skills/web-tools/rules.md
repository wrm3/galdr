# Web Tools Skill - Implementation Rules

## Skill Activation

Activate this skill when user requests involve:
- Web search queries
- Website scraping or content extraction
- Browser automation workflows
- Screenshot capture of web pages
- Multi-page data collection
- Website monitoring
- Web testing

**Do NOT activate for:**
- Desktop application automation (use computer-use-agent)
- Database operations (use database-tools)
- Local file operations (use file-operations)
- API direct calls (unless web scraping is specifically needed)

## Core Workflow

### Step 1: Understand the Request
Determine which web tool is needed:

**Web Search** - When user asks:
- "Search for...", "Find information about...", "Look up..."
- Needs current/recent information from the web

**Web Scraping** - When user asks:
- "Scrape this website", "Extract content from...", "Get data from..."
- Needs specific content from known URL(s)

**Browser Automation** - When user asks:
- "Fill out form on...", "Click button on...", "Navigate through..."
- Needs interaction with dynamic web pages

**Screenshot** - When user asks:
- "Take screenshot of...", "Capture image of...", "Show me what X looks like"
- Needs visual capture of web content

### Step 2: Choose the Right Approach

**Static Scraping (web_scrape)**
- ✅ Use when: Simple HTML pages, fast content extraction
- ✅ Advantages: Fast, low resource, concurrent-friendly
- ❌ Don't use: JavaScript-heavy sites, requires interaction

**Dynamic Scraping (browser automation)**
- ✅ Use when: JavaScript rendering needed, SPAs, infinite scroll
- ✅ Advantages: Handles any web technology, full rendering
- ❌ Don't use: Simple static pages (overkill), rate limiting concerns

**Concurrent Scraping (web_scrape_batch)**
- ✅ Use when: Multiple URLs, batch processing, data collection
- ✅ Advantages: Parallel processing, efficient for many URLs
- ❌ Don't use: Single URL, rate-limited sites

### Step 3: Execute with Appropriate Settings

Configure based on target website:
- **Rate Limit**: 1-2s for small sites, 0.5s for large sites
- **Concurrency**: 3-5 for small sites, 10+ for large sites
- **Timeout**: 10s static, 30s dynamic, 60s for slow sites
- **Retries**: 3 retries with exponential backoff

### Step 4: Process and Present Results

1. **Validate**: Check if scraping succeeded
2. **Clean**: Remove unwanted HTML, normalize text
3. **Structure**: Organize data logically
4. **Summarize**: Present findings clearly to user

## Web Search Workflows

### Basic Search
```
1. User provides search query
2. Use web_search with query
3. Get structured results (10-20 results)
4. Format: title, URL, snippet
5. Optionally: scrape top results for details
6. Present findings to user
```

### Advanced Search with Filters
```
1. Parse user query for filters:
   - Date range (past day, week, month, year)
   - Region (US, UK, etc.)
   - Safe search (on/off)
   - Language preference
2. Use web_search_advanced with filters
3. Process and rank results
4. Present with relevance scores
```

### Research Search (Deep Dive)
```
1. Perform initial search
2. Identify top 5 most relevant results
3. Scrape each result for detailed content
4. Extract key information
5. Synthesize findings
6. Provide comprehensive answer with sources
```

## Web Scraping Workflows

### Single Page Scraping
```
1. Validate URL format and accessibility
2. Choose scraping method:
   - Static: web_scrape for HTML pages
   - Dynamic: browser_navigate + browser_extract for JS sites
3. Extract content:
   - Text content (clean, readable)
   - Links (with context)
   - Metadata (title, description, keywords)
4. Clean and structure content
5. Return formatted result
```

### Multi-Page Scraping
```
1. Get list of URLs to scrape
2. Validate all URLs
3. Determine concurrency limit (5-10)
4. Use web_scrape_batch for parallel scraping
5. Configure:
   - max_concurrent: 5
   - timeout: 30
   - retry_max: 3
   - retry_delay: 2
6. Process each result
7. Combine into structured dataset
8. Handle any failures gracefully
```

### Paginated Content Scraping
```
1. Start with first page URL
2. Scrape current page content
3. Extract pagination links
4. For each subsequent page:
   a. Navigate to next page
   b. Scrape content
   c. Add to results
   d. Check for "next" link
5. Continue until no more pages
6. Compile all results
7. Deduplicate if needed
```

### Dynamic Content Scraping (Infinite Scroll)
```
1. browser_navigate to page
2. Initialize results array
3. Loop until no more content:
   a. browser_extract visible content
   b. Add to results
   c. browser_execute_js to scroll down
   d. browser_wait for new content (2-3 seconds)
   e. Check if new items loaded
4. Deduplicate results
5. Return structured data
```

## Browser Automation Workflows

### Navigate and Extract
```
1. browser_navigate to target URL
2. browser_wait for page load (selector or timeout)
3. browser_extract with appropriate selectors:
   - Text content: CSS selectors or XPath
   - Links: a[href]
   - Images: img[src]
   - Structured data: specific element selectors
4. Return extracted content
```

### Form Filling
```
1. browser_navigate to form page
2. browser_wait for form to load
3. For each form field:
   a. browser_type value into field selector
   b. Verify value was entered
   c. Handle special fields (dropdown, checkbox, radio)
4. browser_click submit button
5. browser_wait for response/confirmation
6. Capture result (success message or error)
```

### Multi-Step Interaction
```
1. browser_navigate to starting page
2. Step through workflow:
   a. browser_wait for element to be ready
   b. browser_click or browser_type as needed
   c. Wait for page response
   d. Verify expected state
   e. Extract intermediate data if needed
3. Continue until workflow complete
4. Capture final state
5. Return result with workflow trace
```

### Login and Authenticated Actions
```
1. browser_navigate to login page
2. browser_type username into username field
3. browser_type password into password field
4. browser_click login button
5. browser_wait for dashboard/home page
6. Verify login successful
7. Perform authenticated actions
8. Logout (optional)
```

**⚠️ Security Note:** Never handle real passwords. Use test accounts only.

## Screenshot Workflows

### Full Page Screenshot
```
1. browser_navigate to page
2. browser_wait for full page load
3. screenshot_fullpage with settings:
   - format: png (or jpeg for smaller size)
   - quality: 90
4. Save screenshot to designated path
5. Return path to user
```

### Element Screenshot
```
1. browser_navigate to page
2. browser_wait for target element
3. screenshot_element targeting specific selector
4. Optional: Add annotations/highlights
5. Save and return path
```

### Comparison Screenshots
```
For A/B testing or monitoring:
1. Take screenshot of version A
2. Take screenshot of version B
3. Optionally: Highlight differences
4. Save both with descriptive names
5. Return both paths for comparison
```

## Content Extraction Patterns

### Clean Text Extraction
```
1. Extract HTML content
2. Remove script and style tags
3. Remove navigation, header, footer
4. Extract main content area
5. Convert HTML to clean text
6. Normalize whitespace
7. Return readable text
```

### Structured Data Extraction
```
1. Identify data structure:
   - JSON-LD in script tags
   - Microdata in HTML attributes
   - RDFa attributes
   - Open Graph tags
2. Parse structured data
3. Validate and normalize
4. Return as JSON
```

### Link Extraction
```
1. Extract all <a href> elements
2. Get absolute URLs (resolve relative)
3. Filter by criteria:
   - Internal vs external links
   - File types (HTML, PDF, etc.)
   - URL patterns
4. Deduplicate
5. Return categorized links
```

### Metadata Extraction
```
Extract from <head>:
- <title>: Page title
- <meta name="description">: Description
- <meta name="keywords">: Keywords
- <meta property="og:*">: Open Graph data
- <link rel="canonical">: Canonical URL
- <script type="application/ld+json">: JSON-LD

Return as structured object
```

## Error Handling

### Network Errors
```
Error: Connection timeout, DNS failure, SSL error

Recovery:
1. Wait 2 seconds
2. Retry with increased timeout
3. If fails 3 times:
   - Check URL validity
   - Check network connectivity
   - Report error to user
```

### HTTP Errors
```
Error: 404, 500, 503, etc.

Recovery:
- 404: Report page not found, suggest alternatives
- 500: Wait 5s, retry up to 2 times
- 503: Service unavailable, wait longer (10s), retry
- 403: Blocked/forbidden, suggest different approach
- 429: Rate limited, increase delay, retry
```

### Content Extraction Errors
```
Error: Expected element not found, empty content

Recovery:
1. Verify page loaded completely
2. Check if page structure changed
3. Try alternative selectors
4. Switch to browser automation if static scraping failed
5. Report specific issue to user
```

### Browser Automation Errors
```
Error: Element not found, timeout, page crash

Recovery:
1. Increase timeout
2. Try alternative selector
3. Check if element is in iframe
4. Verify page actually loaded
5. Restart browser if needed
6. Report error with screenshot
```

## Performance Optimization

### Concurrent Scraping
```yaml
Small sites (< 1000 pages):
  max_concurrent: 3-5
  rate_limit: 1-2 seconds

Medium sites (1000-10000 pages):
  max_concurrent: 5-10
  rate_limit: 0.5-1 seconds

Large sites (10000+ pages):
  max_concurrent: 10-20
  rate_limit: 0.3-0.5 seconds
```

### Caching Strategy
```
1. Cache successful scrapes for 1 hour (configurable)
2. Use URL as cache key
3. Include timestamp in cache
4. Return cached result if fresh
5. Re-scrape if stale or force refresh
```

### Resource Management
```
1. Close browser tabs when done
2. Clear cookies/storage between sessions
3. Limit memory usage per browser instance
4. Kill hung processes after timeout
5. Clean up temporary files
```

## Ethical Guidelines

### Required Checks Before Scraping

**1. Check robots.txt**
```
1. Fetch /robots.txt from domain
2. Parse User-agent rules
3. Check if path is disallowed
4. If disallowed: Stop and inform user
5. If allowed: Proceed with scraping
```

**2. Respect Rate Limits**
```
Minimum delays:
- 0.5s between requests to same domain
- 1.0s for sites without clear ToS
- Follow Crawl-delay if specified in robots.txt
```

**3. Use Appropriate User Agent**
```
Include contact information:
"MyBot/1.0 (+http://example.com/bot-info)"

Not just generic browser user agent
```

### What NOT to Scrape

**❌ Never Scrape:**
- Authentication credentials
- Personal identifiable information (PII)
- Credit card or payment information
- Medical/health records
- Private messages or communications
- Copyrighted content without permission

**⚠️ Scrape with Caution:**
- Social media content (respect privacy)
- News articles (respect copyright)
- Product reviews (respect ToS)
- Pricing data (check ToS)

## MCP Tool Selection

### When to Use Each Tool

**web_search / web_search_advanced**
- User wants to find information
- Need current web results
- Research questions
- Fact-finding missions

**web_scrape**
- Single URL to scrape
- Static HTML page
- Fast extraction needed
- Known page structure

**web_scrape_batch**
- Multiple URLs (5+)
- Batch data collection
- Product catalogs
- Directory listings

**browser_navigate + browser_extract**
- JavaScript-heavy site
- Dynamic content loading
- SPA (Single Page Application)
- Requires rendering

**browser_click / browser_type**
- Form submission needed
- Button clicks required
- Interactive elements
- Multi-step workflows

**screenshot_webpage / screenshot_element**
- Visual capture needed
- Monitoring/comparison
- Documentation
- Bug reports

## User Communication

### Initial Response Template
```
I'll help you [search/scrape/automate] [target].

Approach:
- Method: [Static scraping / Browser automation / Search]
- Expected time: [~X seconds]
- Number of pages: [X]

Settings:
- Rate limit: [X]s between requests
- Timeout: [X]s per page
- Retries: [X] attempts

Ready to proceed?
```

### Progress Updates
```
For long-running scrapes (> 10s):

Progress: [X/Y pages] ([Z]%)
- Completed: [list of successful URLs]
- In progress: [current URL]
- Failed: [count] (will retry)

Estimated time remaining: [X seconds]
```

### Completion Report
```
Scraping completed!

Summary:
- Pages processed: [X]
- Successful: [Y]
- Failed: [Z]
- Time elapsed: [X]s
- Data extracted: [size/count]

Results:
[Formatted extracted data or summary]

Failed URLs (if any):
[List with error reasons]
```

### Error Report
```
Scraping encountered errors:

Failed: [URL]
Error: [Error message]
Cause: [Rate limit / Page not found / Timeout / etc.]

Attempted recovery:
- [What was tried]
- [Result of recovery]

Recommendations:
1. [Suggestion 1]
2. [Suggestion 2]

Would you like me to:
- Retry with different settings
- Try alternative approach
- Continue with available data
```

## Integration with Other Skills

### With computer-use-agent
- Use web-tools for browser-based automation
- Use computer-use-agent for desktop apps
- Combine for workflows spanning web and desktop

### With database-tools
- Scrape data from web
- Store in database via database-tools
- Query and analyze stored data

### With data-processing
- Scrape raw data via web-tools
- Process and clean via data-processing
- Export formatted results

## Best Practices Summary

1. **Always check robots.txt** - Respect website rules
2. **Use appropriate delays** - Don't overwhelm servers
3. **Start with static scraping** - Use browser only if needed
4. **Implement retries** - Handle transient failures gracefully
5. **Validate URLs** - Check before scraping
6. **Clean extracted content** - Remove noise and formatting
7. **Handle errors gracefully** - Inform user, suggest alternatives
8. **Cache when possible** - Reduce redundant requests
9. **Close resources** - Clean up browsers, connections
10. **Document sources** - Track where data came from

---

**Remember:** Always scrape ethically and legally. Respect website ToS, robots.txt, and rate limits.
