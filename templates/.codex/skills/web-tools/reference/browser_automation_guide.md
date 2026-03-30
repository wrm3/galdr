# Browser Automation Guide

## Overview

Browser automation provides powerful capabilities for interacting with web applications through programmatic control of real browsers. This guide covers browser automation patterns, best practices, and common workflows using the `galdr_mcp_browser_use` MCP server.

## Browser Automation Architecture

### Browser Control Flow
```
Cursor → MCP Server → Playwright → Browser (Chromium/Firefox/WebKit)
                                             ↓
                                         Web Page
```

### Available Browsers
- **Chromium**: Chrome/Edge-based browser (default, most compatible)
- **Firefox**: Mozilla Firefox engine
- **WebKit**: Safari engine (macOS native browser)

## Core Operations

### Navigation

#### browser_navigate
Navigate to a URL:
```
browser_navigate(url="https://example.com")
```

Options:
- Wait for page load events
- Handle redirects automatically
- Support JavaScript execution

#### Best Practices
- Always wait for navigation to complete
- Use explicit waits after navigation
- Handle navigation timeouts gracefully

### Element Interaction

#### browser_click
Click elements on the page:
```
browser_click(selector="#submit-button")
```

Selectors:
- CSS: `#id`, `.class`, `div > p`
- XPath: `//button[@type='submit']`
- Text content: `text=Submit`

#### browser_type
Type text into input fields:
```
browser_type(selector="#email", text="user@example.com")
```

Options:
- Clear existing text first
- Type with realistic delays
- Trigger input events

### Content Extraction

#### browser_extract
Extract content from the page:
```
browser_extract(selector=".product-title")
```

Extraction types:
- `text`: Inner text content
- `html`: Full HTML markup
- `value`: Form field values
- Attributes: `href`, `src`, `class`, etc.

### Waiting Strategies

#### browser_wait
Smart waits for elements and conditions:
```
browser_wait(selector="#dynamic-content", timeout=30000)
```

Wait types:
1. **Element visible**: Wait for element to appear
2. **Element hidden**: Wait for element to disappear
3. **Network idle**: Wait for network requests to complete
4. **Custom condition**: JavaScript-based conditions

### JavaScript Execution

#### browser_execute_js
Execute custom JavaScript in page context:
```javascript
browser_execute_js(`
  return document.querySelectorAll('.item').length;
`)
```

Use cases:
- Scroll to load infinite scroll
- Extract computed styles
- Manipulate page state
- Call page functions

### Screenshot Capture

#### browser_screenshot
Capture screenshots:
```
browser_screenshot(path="screenshot.png", fullpage=true)
```

Options:
- **Full page**: Entire scrollable content
- **Viewport**: Visible area only
- **Element**: Specific element screenshot
- **Format**: PNG, JPEG, PDF

## Common Patterns

### Pattern 1: Form Submission

```
# Navigate to form
browser_navigate("https://example.com/contact")

# Wait for form to load
browser_wait("#contact-form")

# Fill form fields
browser_type("#name", "John Doe")
browser_type("#email", "john@example.com")
browser_type("#message", "Hello from automation")

# Submit form
browser_click("button[type='submit']")

# Wait for confirmation
browser_wait(".success-message")

# Capture result
browser_screenshot("confirmation.png")
```

### Pattern 2: Infinite Scroll

```javascript
# Navigate to page
browser_navigate("https://example.com/products")

# Initialize
products = []
previous_count = 0

# Loop until no more content loads
while true:
  # Extract current products
  current = browser_extract(".product-item")
  products.extend(current)

  # Scroll down
  browser_execute_js("window.scrollTo(0, document.body.scrollHeight)")

  # Wait for new content
  browser_wait(timeout=2000)

  # Check if new items loaded
  new_count = browser_execute_js("return document.querySelectorAll('.product-item').length")
  if new_count == previous_count:
    break  # No more items
  previous_count = new_count

# Return all products
return products
```

### Pattern 3: Multi-Step Workflow

```
# Step 1: Login
browser_navigate("https://example.com/login")
browser_type("#username", "user")
browser_type("#password", "pass")
browser_click("#login-button")
browser_wait(".dashboard")

# Step 2: Navigate to settings
browser_click("a[href='/settings']")
browser_wait(".settings-page")

# Step 3: Update profile
browser_type("#bio", "New bio text")
browser_click("#save-button")
browser_wait(".success-toast")

# Step 4: Capture result
browser_screenshot("updated-profile.png")

# Step 5: Logout
browser_click("#logout-button")
```

### Pattern 4: Dynamic Content Extraction

```javascript
# Navigate to page
browser_navigate("https://example.com/dashboard")

# Wait for initial load
browser_wait(".data-loaded")

# Extract data with JavaScript
data = browser_execute_js(`
  const items = Array.from(document.querySelectorAll('.data-row'));
  return items.map(row => ({
    id: row.dataset.id,
    title: row.querySelector('.title').textContent,
    status: row.querySelector('.status').textContent,
    date: row.querySelector('.date').textContent
  }));
`)

return data
```

### Pattern 5: Handling Popups and Dialogs

```
# Navigate to page
browser_navigate("https://example.com")

# Close cookie banner if present
browser_wait(".cookie-banner", timeout=5000)
browser_click(".cookie-accept")

# Wait for modal to appear
browser_wait(".modal")

# Fill modal form
browser_type(".modal input[name='email']", "user@example.com")
browser_click(".modal button.submit")

# Wait for modal to close
browser_wait(".modal", wait_for="hidden")

# Continue with main workflow
browser_click("#main-action")
```

## Advanced Techniques

### Device Emulation

Emulate mobile devices:
```yaml
device_emulation: "iPhone 12"
viewport_width: 390
viewport_height: 844
user_agent: "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
```

### Network Interception

Monitor network requests:
```javascript
# Listen for network events
browser_execute_js(`
  window.networkRequests = [];
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    window.networkRequests.push({url: args[0], method: args[1]?.method || 'GET'});
    return originalFetch.apply(this, args);
  };
`)

# Perform actions
browser_click("#load-data")
browser_wait(timeout=2000)

# Get captured requests
requests = browser_execute_js("return window.networkRequests")
```

### File Downloads

Handle file downloads:
```
# Set download path
browser_execute_js(`
  window.downloads = [];
`)

# Click download button
browser_click("#download-button")

# Wait for download to complete
browser_wait(timeout=10000)

# Verify file exists
# (Download handling requires browser configuration)
```

### Multi-Tab Management

Work with multiple tabs:
```
# Open new tab
browser_execute_js("window.open('https://example.com/page2', '_blank')")

# Switch between tabs
# (Tab management requires browser context API)

# Close tab
browser_execute_js("window.close()")
```

## Performance Optimization

### 1. Disable Unnecessary Resources

```yaml
disable_images: true      # Skip image loading
disable_javascript: false # Keep JS for SPAs
disable_cache: false      # Use cache for speed
```

### 2. Use Headless Mode

```yaml
headless: true  # No GUI, faster execution
```

### 3. Reduce Timeouts

```yaml
timeout: 15000  # Shorter timeout for fast sites
```

### 4. Reuse Browser Context

```
# Reuse same browser session for multiple operations
# Avoid creating new browser for each request
```

### 5. Minimize Screenshots

```
# Only capture screenshots when needed
# Use viewport screenshots instead of fullpage
```

## Error Handling

### Common Errors

**Element Not Found**
```
Error: Element not found: #submit-button

Solution:
- Verify selector is correct
- Add explicit wait before interacting
- Check if element is in iframe
- Ensure page is fully loaded
```

**Timeout**
```
Error: Navigation timeout exceeded

Solution:
- Increase timeout value
- Check network connectivity
- Verify URL is accessible
- Look for slow-loading resources
```

**Element Not Clickable**
```
Error: Element is not clickable

Solution:
- Wait for element to be visible
- Scroll element into view
- Close overlaying popups/modals
- Ensure element is not disabled
```

### Retry Logic

```
# Retry pattern for flaky operations
max_retries = 3
for attempt in range(max_retries):
  try:
    browser_click("#submit")
    break
  except:
    if attempt < max_retries - 1:
      browser_wait(timeout=2000)
    else:
      raise
```

## Security Considerations

### 1. Credential Management

```
# NEVER hardcode credentials
# Use environment variables or secure storage
browser_type("#password", os.getenv("PASSWORD"))
```

### 2. Sanitize Inputs

```
# Validate and sanitize user inputs
# Prevent injection attacks
```

### 3. Verify SSL Certificates

```
# Ensure HTTPS connections are verified
# Avoid ignoring SSL errors
```

### 4. Limit Permissions

```
# Run browser with minimal permissions
# Sandbox browser execution
```

## Debugging

### 1. Enable Screenshots

```
# Take screenshots at each step
browser_screenshot("step1_after_login.png")
browser_screenshot("step2_after_form_fill.png")
```

### 2. Console Logging

```javascript
# Capture console logs
browser_execute_js(`
  window.capturedLogs = [];
  ['log', 'error', 'warn'].forEach(method => {
    const original = console[method];
    console[method] = function(...args) {
      window.capturedLogs.push({type: method, message: args.join(' ')});
      original.apply(console, args);
    };
  });
`)

# Later retrieve logs
logs = browser_execute_js("return window.capturedLogs")
```

### 3. Page Source Inspection

```
# Extract full HTML for debugging
html = browser_execute_js("return document.documentElement.outerHTML")
```

### 4. Network Inspection

```
# Monitor network activity
# Check for failed requests
# Verify API responses
```

## Best Practices

1. **Use Explicit Waits**: Always wait for elements before interacting
2. **Stable Selectors**: Use IDs or stable data attributes
3. **Error Handling**: Implement retry logic for flaky operations
4. **Resource Cleanup**: Close browsers properly
5. **Stealth Mode**: Rotate user agents, avoid detection
6. **Rate Limiting**: Respect server load
7. **Documentation**: Comment complex automation logic
8. **Testing**: Test automation scripts regularly

## Comparison: Static vs Dynamic Scraping

| Feature | Static (web_scrape) | Dynamic (browser_*) |
|---------|---------------------|---------------------|
| Speed | Fast | Slower |
| Resource Usage | Low | High |
| JavaScript | No | Yes |
| Interaction | No | Yes |
| Cost | Cheap | Expensive |
| Use Case | Static pages | SPAs, forms |

## Related Tools

- **web_scrape**: For static HTML scraping
- **web_search**: For web search
- **computer-use-agent**: For desktop automation

## Troubleshooting

### Browser Won't Start
- Check Playwright installation
- Verify browser binary exists
- Check system permissions

### Elements Not Interactive
- Wait for page load
- Scroll into view
- Remove overlays
- Check z-index

### Screenshots Blank
- Wait for content to load
- Increase viewport size
- Check element visibility
- Verify page rendering

---

**Note**: Browser automation should be used ethically and in compliance with website terms of service.
