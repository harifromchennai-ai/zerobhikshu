# Google Site to Pelican Scraper

Convert content from your public Google Site into Markdown files compatible with the Pelican static site generator.

## Features

- **Recursive crawling**: Automatically discovers and scrapes all pages on your site
- **HTML to Markdown conversion**: Preserves formatting while converting to Markdown
- **Pelican-compatible**: Generates files with YAML frontmatter (title, date, slug, source URL)
- **Deduplication**: Avoids processing the same page twice
- **Error handling**: Gracefully handles network errors and invalid pages
- **Logging**: Detailed logging of the scraping process

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Edit the `main()` function in `extract_site.py` to configure:

```python
SITE_URL = 'www.zerobhikshu.org'      # Your site URL
OUTPUT_DIR = 'content'                 # Output directory for Markdown files
MAX_PAGES = None                       # Max pages to scrape (None = unlimited)
```

Then run:

```bash
python extract_site.py
```

### Output

The script creates Markdown files in the `content/` directory with this structure:

```markdown
---
title: Page Title
date: 2024-01-15 10:30:00
slug: page-title
category: 
tags: 
source: https://www.zerobhikshu.org/page
---

# Page content in Markdown format

Your content here...
```

### Pelican Integration

1. Place the generated `content/` directory in your Pelican project
2. Or merge with existing content files
3. Configure `pelicanconf.py` as needed
4. Generate your static site: `pelican content`

## Customization

### Limiting Scrape Depth

To scrape only the first 10 pages:

```python
scraper.scrape(max_pages=10)
```

### Custom Content Selectors

If the script doesn't detect your main content correctly, edit the `extract_main_content()` method to add your site's content div selector.

### Adjusting the Output Format

Modify the frontmatter in the `create_markdown_file()` method to add custom fields like:

```python
category: My Category
tags: tag1, tag2
```

## Troubleshooting

### Issue: Empty content files

**Solution**: Google Sites may require JavaScript rendering. Install `selenium` and update the `fetch_page()` method:

```bash
pip install selenium
```

Then modify to use Selenium with Chrome WebDriver for JavaScript support.

### Issue: Navigation/footer in content

**Solution**: Adjust the selectors in `extract_main_content()` to better target your main content area, or add more exclusion rules for navigation elements.

### Issue: Special characters in filenames

The script automatically sanitizes filenames, but you can customize this in the `sanitize_filename()` method.

## Requirements

- `requests`: HTTP library for fetching pages
- `beautifulsoup4`: HTML parsing
- `html2text`: HTML to Markdown conversion

## Notes

- The script respects `robots.txt` conventions by checking same-domain links
- Each page is fetched only once (deduplication)
- Original source URL is preserved in the frontmatter
- Timestamps are set to the current date/time when scraped

## Advanced: JavaScript-Heavy Sites

If your Google Site relies heavily on JavaScript, use the `selenium` branch approach:

```bash
pip install selenium
# Download ChromeDriver from https://chromedriver.chromium.org/
```

Then modify `fetch_page()` to use Selenium instead of requests.

## License

Use freely for your own content migration purposes.
