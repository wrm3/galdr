# Search Engine Integration Guide

## Overview

Web search capabilities enable programmatic access to search engines for information retrieval, research, and content discovery. This guide covers search engine integration through the `galdr_mcp_browser_use` MCP server.

## Supported Search Engines

### 1. Google
- **Coverage**: Largest index, most comprehensive
- **Strengths**: Relevance, freshness, rich snippets
- **Best for**: General search, news, shopping

### 2. Bing
- **Coverage**: Large index, Microsoft integration
- **Strengths**: Image search, video search
- **Best for**: Visual content, Microsoft ecosystem

### 3. DuckDuckGo
- **Coverage**: Aggregates multiple sources
- **Strengths**: Privacy, no tracking, instant answers
- **Best for**: Privacy-focused search, quick facts

## Search API Integration

### Basic Search

```
web_search(query="Claude AI capabilities", engine="google", limit=10)
```

Parameters:
- `query`: Search terms
- `engine`: `google`, `bing`, `duckduckgo`
- `limit`: Number of results (default: 10)
- `safe_search`: Enable safe search filtering
- `region`: Geographic region code
- `language`: Language preference

### Advanced Search

```
web_search_advanced(
  query="machine learning frameworks",
  engine="google",
  limit=20,
  date_range="past_year",
  site="github.com",
  file_type="pdf"
)
```

Advanced parameters:
- `date_range`: `past_day`, `past_week`, `past_month`, `past_year`
- `site`: Restrict to specific domain
- `file_type`: Filter by file extension
- `exclude_terms`: Terms to exclude
- `exact_phrase`: Exact phrase matching

## Search Result Structure

### Result Object

```json
{
  "title": "Page Title",
  "url": "https://example.com/page",
  "snippet": "Description excerpt...",
  "rank": 1,
  "domain": "example.com",
  "published_date": "2025-01-15",
  "metadata": {
    "author": "John Doe",
    "site_name": "Example Site"
  }
}
```

### Rich Snippets

Some results include enhanced metadata:
- **Knowledge Graph**: Entity information
- **Featured Snippets**: Direct answers
- **People Also Ask**: Related questions
- **Related Searches**: Alternative queries

## Search Query Patterns

### 1. Basic Search

```
query: "Cursor AI features"
```

Returns general results about Cursor AI features.

### 2. Exact Phrase

```
query: '"Model Context Protocol"'
```

Matches exact phrase only.

### 3. Boolean Operators

```
query: "AI OR machine learning"
query: "Python AND data science"
query: "tutorial -video"
```

Combine terms with AND, OR, NOT operators.

### 4. Site-Specific

```
query: "site:anthropic.com Claude"
```

Search within specific domain only.

### 5. File Type

```
query: "machine learning filetype:pdf"
```

Find specific file types.

### 6. Wildcard

```
query: "Claude * Protocol"
```

Use * as placeholder for unknown terms.

### 7. Range

```
query: "laptop $500..$1000"
```

Search within numeric ranges.

### 8. Related Sites

```
query: "related:anthropic.com"
```

Find sites similar to given domain.

### 9. Title Search

```
query: "intitle:Cursor IDE"
```

Search page titles only.

### 10. URL Search

```
query: "inurl:documentation"
```

Search URLs only.

## Common Use Cases

### Research and Information Gathering

```python
# Example 1: Academic Research
results = web_search(
  query='"transformer architecture" filetype:pdf',
  engine="google",
  limit=20,
  date_range="past_year"
)

# Filter for high-quality sources
academic_sources = [r for r in results if any(
  domain in r['url'] for domain in
  ['arxiv.org', 'scholar.google.com', '.edu']
)]
```

### Competitive Analysis

```python
# Example 2: Competitor Research
competitors = ["competitor1.com", "competitor2.com", "competitor3.com"]

for competitor in competitors:
  results = web_search(
    query=f"site:{competitor} pricing",
    engine="google",
    limit=10
  )
  # Analyze pricing pages
```

### News Monitoring

```python
# Example 3: News Tracking
news_results = web_search(
  query="artificial intelligence breakthrough",
  engine="google",
  limit=20,
  date_range="past_week"
)

# Filter for news sites
news_sites = ['nytimes.com', 'reuters.com', 'bbc.com', 'techcrunch.com']
recent_news = [r for r in news_results if any(
  site in r['domain'] for site in news_sites
)]
```

### Product Research

```python
# Example 4: Product Reviews
product_reviews = web_search(
  query="MacBook Pro M3 review",
  engine="google",
  limit=30,
  date_range="past_month"
)

# Aggregate review sites
review_sites = [r for r in product_reviews if any(
  site in r['domain'] for site in
  ['theverge.com', 'arstechnica.com', 'anandtech.com']
)]
```

### Technical Documentation

```python
# Example 5: API Documentation
api_docs = web_search(
  query="site:docs.anthropic.com model context protocol",
  engine="google",
  limit=15
)

# Find relevant documentation pages
```

## Search Optimization Strategies

### 1. Query Refinement

Start broad, then narrow:
```python
# Iteration 1: Broad
results1 = web_search("machine learning")

# Iteration 2: More specific
results2 = web_search("machine learning python frameworks")

# Iteration 3: Very specific
results3 = web_search("PyTorch vs TensorFlow 2025 comparison")
```

### 2. Multi-Engine Search

Query multiple engines for comprehensive coverage:
```python
engines = ['google', 'bing', 'duckduckgo']
all_results = []

for engine in engines:
  results = web_search(query="Claude AI", engine=engine, limit=10)
  all_results.extend(results)

# Deduplicate by URL
unique_results = {r['url']: r for r in all_results}.values()
```

### 3. Date-Aware Search

Prioritize recent content:
```python
# Latest information only
recent = web_search(
  query="Cursor AI updates",
  date_range="past_month"
)

# Historical context
historical = web_search(
  query="Cursor AI updates",
  date_range="past_year"
)
```

### 4. Domain Filtering

Focus on authoritative sources:
```python
# Academic sources
academic = web_search(
  query="AI safety research",
  site="arxiv.org OR site:scholar.google.com"
)

# Official documentation
official = web_search(
  query="Claude API",
  site="anthropic.com"
)
```

### 5. Result Ranking

Re-rank results by custom criteria:
```python
results = web_search(query="AI frameworks", limit=50)

# Rank by domain authority
authority_domains = ['github.com', 'arxiv.org', '.edu', 'official_sites']
scored_results = sorted(results, key=lambda r: (
  sum(domain in r['url'] for domain in authority_domains),
  -r['rank']
), reverse=True)
```

## Search Result Processing

### Extract Key Information

```python
def process_search_results(results):
  """Extract and structure search results."""
  processed = []

  for result in results:
    processed.append({
      'title': result['title'],
      'url': result['url'],
      'snippet': result['snippet'],
      'domain': result['domain'],
      'rank': result['rank'],
      'relevance_score': calculate_relevance(result)
    })

  return processed

def calculate_relevance(result):
  """Calculate custom relevance score."""
  score = 100 - result['rank']  # Base score

  # Boost for authoritative domains
  if any(domain in result['url'] for domain in ['.edu', '.gov', 'arxiv.org']):
    score += 20

  # Boost for recent content
  if result.get('published_date'):
    days_old = (datetime.now() - result['published_date']).days
    if days_old < 30:
      score += 10

  return score
```

### Content Extraction

```python
# Search + Scrape workflow
search_results = web_search(query="Claude AI documentation", limit=10)

# Scrape top results for detailed content
detailed_results = []
for result in search_results[:5]:  # Top 5 only
  content = web_scrape(url=result['url'])
  detailed_results.append({
    'title': result['title'],
    'url': result['url'],
    'content': content['text'],
    'links': content['links']
  })
```

## Rate Limiting and Ethics

### Best Practices

1. **Respect Rate Limits**: Don't overwhelm search engines
   ```python
   import time

   results = []
   for query in queries:
     result = web_search(query=query)
     results.append(result)
     time.sleep(1)  # 1 second delay between searches
   ```

2. **Cache Results**: Store search results to avoid redundant queries
   ```python
   cache = {}

   def cached_search(query):
     if query in cache:
       return cache[query]

     result = web_search(query=query)
     cache[query] = result
     return result
   ```

3. **User-Agent**: Use appropriate user-agent strings
   ```
   User-Agent: Cursor AI Web Search/1.0 (+https://example.com/bot)
   ```

4. **Attribution**: Credit sources when using search results

## Advanced Features

### Search Suggestions

```python
# Get autocomplete suggestions
suggestions = web_search_suggestions(query="machine lear")
# Returns: ["machine learning", "machine learning python", ...]
```

### Related Searches

```python
# Find related queries
related = web_search_related(query="Claude AI")
# Returns related search terms
```

### Trend Analysis

```python
# Track search trends over time
trends = []
for month in past_12_months:
  results = web_search(
    query="AI adoption",
    date_range=month
  )
  trends.append({
    'month': month,
    'result_count': len(results)
  })
```

## Troubleshooting

### No Results Returned

**Problem**: Search returns empty results

**Solutions**:
- Verify query spelling
- Remove overly restrictive filters
- Try different search engines
- Broaden search terms

### Poor Result Quality

**Problem**: Results not relevant

**Solutions**:
- Refine query with more specific terms
- Use advanced operators (quotes, site:, filetype:)
- Filter by date for fresh content
- Exclude irrelevant domains with -site:

### Rate Limiting

**Problem**: Search blocked or limited

**Solutions**:
- Implement delays between requests
- Reduce search frequency
- Use caching to avoid redundant searches
- Distribute searches across multiple engines

## Integration with Other Tools

### Search + Scrape

```python
# Search for relevant pages
search_results = web_search(query="API documentation", limit=10)

# Scrape top results
content = []
for result in search_results[:5]:
  page_content = web_scrape(url=result['url'])
  content.append(page_content)
```

### Search + Browser Automation

```python
# Search for page
results = web_search(query="login page example.com")

# Navigate to top result
browser_navigate(url=results[0]['url'])
browser_wait(selector="#login-form")
```

## Performance Optimization

1. **Parallel Searches**: Run multiple searches concurrently
2. **Result Caching**: Store and reuse search results
3. **Pagination**: Request only needed number of results
4. **Filtering**: Apply filters server-side when possible

## Search Quality Metrics

Track search effectiveness:
```python
def evaluate_search_quality(query, results):
  """Evaluate search result quality."""
  metrics = {
    'result_count': len(results),
    'avg_rank': sum(r['rank'] for r in results) / len(results),
    'domain_diversity': len(set(r['domain'] for r in results)),
    'fresh_content': sum(1 for r in results if is_recent(r))
  }
  return metrics
```

## Related Skills

- **web-tools**: General web interaction
- **research-methodology**: Research workflows
- **data-processing**: Result analysis

---

**Note**: Always respect search engine terms of service and robots.txt. Use search APIs responsibly and ethically.
