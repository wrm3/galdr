# Web Scraping Guide - Best Practices and Techniques

## Overview

This guide covers best practices, ethical considerations, and advanced techniques for web scraping using the Web Tools Skill.

## Ethical Web Scraping

### The Golden Rules

1. **Read and Respect robots.txt**
   - Always fetch and parse `/robots.txt`
   - Honor `Disallow` directives
   - Respect `Crawl-delay` settings
   - Follow `User-agent` specific rules

2. **Respect Rate Limits**
   - Minimum 0.5s delay between requests to same domain
   - Scale delay based on site size/resources
   - Implement exponential backoff on errors
   - Don't scrape during peak hours

3. **Identify Your Bot**
   - Use descriptive User-Agent string
   - Include contact information or URL
   - Example: `MyResearchBot/1.0 (+https://example.com/bot)`

4. **Cache Aggressively**
   - Don't re-scrape unchanged content
   - Use HTTP caching headers (ETags, Last-Modified)
   - Store results locally when possible

5. **Be A Good Citizen**
   - Use minimal resources
   - Don't DDOS accidentally
   - Contact site owner if scraping heavily
   - Offer to use API if available

### Legal Considerations

**Check Before Scraping:**
- Terms of Service (ToS)
- Copyright notices
- Privacy policies
- Local laws (GDPR, CCPA, etc.)

**Generally Acceptable:**
- Public information
- Data for personal research
- Price comparison
- Search engine indexing (with permission)

**Generally Problematic:**
- Private/gated content
- Copyrighted material
- Personal data
- Competitive intelligence (depends on ToS)
- Commercial use without permission

## robots.txt Deep Dive

### Checking robots.txt

```python
Example robots.txt:

User-agent: *
Disallow: /admin/
Disallow: /private/
Crawl-delay: 2

User-agent: MyBot
Disallow: /
```

**Interpretation:**
- General bots: Can access everything except /admin/ and /private/, wait 2s between requests
- MyBot: Disallowed from entire site

### Implementation

Before scraping any domain:
1. Fetch `https://example.com/robots.txt`
2. Parse rules for your user-agent
3. Check if target path is allowed
4. Get crawl-delay if specified
5. Proceed only if allowed

## Scraping Techniques

### Static HTML Scraping

**When to Use:**
- Simple HTML pages
- Server-side rendered content
- Fast extraction needed
- No JavaScript required

**Tools:**
- `web_scrape` MCP tool
- BeautifulSoup for parsing
- Requests for fetching

**Example Workflow:**
```
1. Fetch HTML with requests
2. Parse with BeautifulSoup
3. Select elements with CSS selectors
4. Extract text/attributes
5. Clean and structure data
```

**Advantages:**
- ✅ Very fast (< 1 second per page)
- ✅ Low resource usage
- ✅ Easy to parallelize
- ✅ Works without browser

**Limitations:**
- ❌ No JavaScript execution
- ❌ Can't handle SPAs
- ❌ No interaction possible

### Dynamic Scraping (Browser Automation)

**When to Use:**
- JavaScript-heavy sites
- Single Page Applications (SPAs)
- Content loaded via AJAX
- Requires user interaction
- Infinite scroll pages

**Tools:**
- `browser_navigate` + `browser_extract` MCP tools
- Playwright for automation
- Headless browser

**Example Workflow:**
```
1. Launch headless browser
2. Navigate to page
3. Wait for JavaScript to execute
4. Wait for specific elements
5. Extract rendered content
6. Close browser
```

**Advantages:**
- ✅ Handles any web technology
- ✅ Executes JavaScript
- ✅ Can interact with pages
- ✅ Sees exactly what users see

**Limitations:**
- ❌ Slower (3-10 seconds per page)
- ❌ High resource usage
- ❌ More complex error handling
- ❌ Can't parallelize easily

### Hybrid Approach

**Best Practice:**
1. Try static scraping first
2. If returns empty/incomplete: Switch to browser
3. Use browser only for pages that need it
4. Cache results aggressively

## Content Extraction

### CSS Selectors

**Basic Selectors:**
```css
/* Element */
div, p, a

/* Class */
.article, .product-card

/* ID */
#main-content, #header

/* Attribute */
[href], [data-id="123"]

/* Combination */
div.article p.content
article > h2
.container .item:first-child
```

**Advanced Selectors:**
```css
/* Nth child */
li:nth-child(2)
tr:nth-of-type(odd)

/* Contains text */
a:contains("Next")

/* Attribute starts with */
a[href^="https://"]

/* Multiple classes */
.class1.class2

/* Not */
div:not(.excluded)
```

### XPath

**When to Use XPath:**
- Complex hierarchical selection
- Text content matching
- Attribute value matching
- Multiple conditions

**Examples:**
```xpath
/* All links */
//a

/* Links with specific text */
//a[contains(text(), "Next")]

/* Parent of element */
//div[@class="child"]/parent::div

/* Following sibling */
//h2[@class="title"]/following-sibling::p

/* Attribute contains */
//div[contains(@class, "product")]
```

### Text Cleaning

**Remove Unwanted Elements:**
```
1. Script tags: <script>...</script>
2. Style tags: <style>...</style>
3. Comments: <!-- ... -->
4. Navigation: <nav>, .sidebar
5. Footer: <footer>, .footer
6. Ads: .ad, .advertisement
```

**Normalize Text:**
```
1. Replace multiple spaces with single space
2. Replace multiple newlines with \n\n
3. Trim leading/trailing whitespace
4. Decode HTML entities (&amp; → &)
5. Remove zero-width characters
```

**Extract Main Content:**
```
Look for:
- <main> tag
- <article> tag
- .content, .main-content classes
- Largest text block
- High text-to-HTML ratio area
```

## Common Scraping Patterns

### Pattern 1: Product Catalog

```
Target: E-commerce product listings

Steps:
1. Get category page URL
2. Extract product cards:
   - Title: h2.product-title
   - Price: span.price
   - Image: img.product-image
   - Link: a.product-link
3. Follow pagination links
4. For each product:
   - Navigate to detail page
   - Extract full details
5. Compile catalog
```

### Pattern 2: News Articles

```
Target: News website articles

Steps:
1. Get article list/feed
2. For each article URL:
   - Title: h1.headline or <title>
   - Date: time.published-date or meta[property="article:published_time"]
   - Author: span.author-name
   - Content: article.content or .article-body
   - Extract paragraphs, remove ads
3. Clean and structure
4. Store with metadata
```

### Pattern 3: Table Data

```
Target: HTML tables

Steps:
1. Find table: table.data-table
2. Extract headers: thead th
3. For each row:
   - Get cells: td
   - Map to headers
   - Create row object
4. Return as array of objects
```

### Pattern 4: Infinite Scroll

```
Target: Social media feeds, image galleries

Steps:
1. Load initial page
2. Extract visible items
3. Scroll down
4. Wait for new items to load
5. Extract new items
6. Deduplicate
7. Repeat until no new items
8. Return all items
```

## Error Handling

### HTTP Status Codes

**2xx Success:**
- 200 OK: Success, process content
- 204 No Content: Success, but empty

**3xx Redirection:**
- 301 Moved Permanently: Update URL, follow
- 302 Found: Temporary redirect, follow
- 304 Not Modified: Use cached version

**4xx Client Errors:**
- 400 Bad Request: Check URL format
- 401 Unauthorized: Authentication required
- 403 Forbidden: Access denied, respect it
- 404 Not Found: Page doesn't exist
- 429 Too Many Requests: Rate limited, slow down

**5xx Server Errors:**
- 500 Internal Server Error: Retry after delay
- 502 Bad Gateway: Temporary, retry
- 503 Service Unavailable: Server overloaded, retry later
- 504 Gateway Timeout: Retry with longer timeout

### Retry Strategy

**Exponential Backoff:**
```
Attempt 1: Wait 1 second
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds
Max attempts: 4
```

**When to Retry:**
- ✅ Network timeouts
- ✅ 500-level errors
- ✅ 429 Rate Limit
- ✅ Connection errors

**When NOT to Retry:**
- ❌ 404 Not Found
- ❌ 403 Forbidden
- ❌ 401 Unauthorized
- ❌ 400 Bad Request

### Handling Dynamic Content Failures

**Problem: Content not loading**

**Solutions:**
1. Increase wait time
2. Wait for specific selector
3. Check network requests
4. Disable unnecessary resources (images, fonts)
5. Try different viewport size
6. Check for CAPTCHAs

## Performance Optimization

### Concurrent Scraping

**Benefits:**
- Faster overall completion
- Better resource utilization
- Efficient for many URLs

**Configuration:**
```python
# Good settings for most sites
max_concurrent = 5
timeout = 30
retry_max = 3
rate_limit = 1.0  # seconds between requests
```

**Caution:**
- Don't overwhelm small sites
- Respect server resources
- Monitor for rate limiting
- Scale based on site capacity

### Caching

**What to Cache:**
- robots.txt (24 hours)
- Scraped pages (1-24 hours depending on update frequency)
- Search results (1 hour)
- Static resources (indefinitely)

**Cache Invalidation:**
- Time-based (expires after X hours)
- Manual refresh
- Check Last-Modified header
- Use ETags

### Resource Management

**Reduce Resource Usage:**
1. Disable images when not needed
2. Disable CSS (if extracting text only)
3. Block ads and trackers
4. Use minimal browser features
5. Close browsers promptly
6. Clear cache periodically

## Anti-Scraping Measures

### Common Techniques

**1. Rate Limiting**
- Detection: 429 errors, temporary blocks
- Countermeasure: Respect limits, slow down

**2. User Agent Blocking**
- Detection: 403 for bot user agents
- Countermeasure: Use realistic user agent

**3. IP Blocking**
- Detection: Consistent 403 from same IP
- Countermeasure: Rotate proxies, reduce rate

**4. JavaScript Challenges**
- Detection: Requires browser execution
- Countermeasure: Use browser automation

**5. CAPTCHAs**
- Detection: CAPTCHA page appears
- Countermeasure: Manual solving, CAPTCHA services (carefully)

**6. Honeypot Links**
- Detection: Hidden links that bots follow
- Countermeasure: Check if link is hidden (CSS)

**7. Session Tracking**
- Detection: Requires cookies/session
- Countermeasure: Maintain session, handle cookies

### Respectful Workarounds

**If site blocks scraping:**
1. Check if API is available
2. Contact site owner
3. Reduce scraping frequency
4. Scrape only public data
5. Consider alternative sources

**Don't:**
- ❌ Circumvent CAPTCHAs aggressively
- ❌ Spoof headers extensively
- ❌ Use residential proxies without permission
- ❌ Scrape after explicit blocking

## Advanced Techniques

### JavaScript Execution

**Execute in Page Context:**
```javascript
// Extract data via custom JavaScript
const data = await browser_execute_js(`
  return {
    products: Array.from(document.querySelectorAll('.product')).map(el => ({
      title: el.querySelector('h2').textContent,
      price: el.querySelector('.price').textContent,
      link: el.querySelector('a').href
    }))
  };
`);
```

### Waiting Strategies

**Wait for Element:**
```javascript
// Wait up to 10s for element to appear
await browser_wait('.content', {timeout: 10000});
```

**Wait for Network Idle:**
```javascript
// Wait for no network activity for 2s
await browser_wait_for_network_idle({idle: 2000});
```

**Wait for Function:**
```javascript
// Wait for custom condition
await browser_execute_js(`
  await new Promise(resolve => {
    const check = () => {
      if (document.querySelectorAll('.item').length >= 10) {
        resolve();
      } else {
        setTimeout(check, 100);
      }
    };
    check();
  });
`);
```

### Handling Pagination

**Next Button:**
```
1. While "Next" button exists:
   a. Extract current page data
   b. Click "Next" button
   c. Wait for new page to load
   d. Continue
```

**Page Numbers:**
```
1. Find max page number
2. For each page 1 to max:
   a. Navigate to ?page=N
   b. Extract data
   c. Add to results
```

**Load More:**
```
1. While "Load More" button exists:
   a. Click button
   b. Wait for content to load
   c. Extract new content
   d. Check if button still present
```

## Troubleshooting

### Empty Results

**Possible Causes:**
1. Page requires JavaScript → Use browser automation
2. Content in iframe → Extract from iframe
3. Content lazy-loaded → Wait longer or scroll
4. Incorrect selectors → Inspect page, verify selectors
5. Content behind auth → Provide authentication

### Incomplete Data

**Possible Causes:**
1. Pagination not followed → Implement pagination
2. Content loaded dynamically → Wait for load
3. Timeout too short → Increase timeout
4. Rate limited → Reduce request frequency

### Blocked Requests

**Possible Causes:**
1. Bot user agent → Use realistic user agent
2. Too fast requests → Increase delays
3. IP blocked → Rotate IPs or proxy
4. robots.txt violation → Respect robots.txt

## Summary Checklist

Before Scraping:
- [ ] Check robots.txt
- [ ] Review site ToS
- [ ] Confirm legal/ethical
- [ ] Plan rate limits
- [ ] Test on small scale

During Scraping:
- [ ] Monitor for errors
- [ ] Respect rate limits
- [ ] Handle failures gracefully
- [ ] Log progress
- [ ] Cache results

After Scraping:
- [ ] Close resources
- [ ] Clean data
- [ ] Store results securely
- [ ] Document sources
- [ ] Review for quality

---

**Remember:** Ethical scraping is respectful scraping. Always prioritize being a good web citizen.
