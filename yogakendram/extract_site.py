#!/usr/bin/env python3
"""
Scrape a Google Site and convert content to Pelican-compatible Markdown files.
"""

import os
import re
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path
from bs4 import BeautifulSoup
import html2text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class GoogleSiteScraper:
    def __init__(self, base_url, output_dir='content'):
        """
        Initialize the scraper.
        
        Args:
            base_url: The base URL of the Google Site (e.g., www.zerobhikshu.org)
            output_dir: Directory to save Markdown files
        """
        self.base_url = base_url if base_url.startswith(('http://', 'https://')) else f'https://{base_url}'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure requests session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Configure html2text
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.body_width = 0  # Don't wrap text
        
        self.visited_urls = set()
        self.pages = []
    
    def fetch_page(self, url):
        """Fetch a page and return BeautifulSoup object."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_main_content(self, soup):
        """Extract main body content from the page."""
        # Try various common selectors for Google Sites
        selectors = [
            'div[role="main"]',
            'main',
            'article',
            'div.site-content',
            'div[data-content]',
            'div.goog-ws-edit-content',
            'div.sites-layout-tile'
        ]
        
        content_div = None
        for selector in selectors:
            content_div = soup.select_one(selector)
            if content_div and len(content_div.get_text(strip=True)) > 100:
                break
        
        if not content_div:
            # Fallback: get all main content from body, excluding navigation
            content_div = soup.find('body')
            if not content_div:
                return None
        
        # Remove script and style tags
        for tag in content_div.find_all(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        
        return content_div
    
    def sanitize_filename(self, title):
        """Convert title to a valid filename."""
        # Remove special characters and convert spaces to hyphens
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename.strip('-')
    
    def create_markdown_file(self, page_data):
        """Create a Pelican-compatible Markdown file."""
        title = page_data.get('title', 'Untitled')
        content = page_data.get('content', '')
        url = page_data.get('url', '')
        
        # Create filename from title
        filename = self.sanitize_filename(title)
        if not filename:
            filename = 'page'
        filepath = self.output_dir / f'{filename}.md'
        
        # Avoid duplicates
        counter = 1
        base_filepath = filepath
        while filepath.exists():
            filepath = self.output_dir / f'{filename}-{counter}.md'
            counter += 1
        
        # Create Pelican frontmatter
        frontmatter = f"""---
title: {title}
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
slug: {filename}
category: 
tags: 
source: {url}
---

"""
        
        # Combine frontmatter and content
        full_content = frontmatter + content
        
        # Write file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            logger.info(f"Created: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error writing {filepath}: {e}")
            return False
    
    def get_page_title(self, soup):
        """Extract page title."""
        # Try various title sources
        title = soup.find('h1')
        if title:
            return title.get_text(strip=True)
        
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True).split('|')[0].strip()
        
        return 'Untitled'
    
    def extract_links(self, soup, current_url):
        """Extract internal links from the page."""
        links = set()
        base_domain = urlparse(self.base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip anchors, javascript, and external links
            if href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(current_url, href)
            parsed = urlparse(absolute_url)
            
            # Only follow links on the same domain
            if parsed.netloc == base_domain and absolute_url not in self.visited_urls:
                # Remove query parameters and fragments for consistency
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                links.add(clean_url)
        
        return links
    
    def scrape(self, start_url=None, max_pages=None):
        """
        Recursively scrape the Google Site.
        
        Args:
            start_url: URL to start scraping from (defaults to base_url)
            max_pages: Maximum number of pages to scrape (None for unlimited)
        """
        if start_url is None:
            start_url = self.base_url
        
        if not start_url.startswith(('http://', 'https://')):
            start_url = urljoin(self.base_url, start_url)
        
        to_visit = [start_url]
        
        while to_visit and (max_pages is None or len(self.pages) < max_pages):
            current_url = to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
            
            self.visited_urls.add(current_url)
            logger.info(f"Scraping: {current_url}")
            
            soup = self.fetch_page(current_url)
            if not soup:
                continue
            
            # Extract content
            content_div = self.extract_main_content(soup)
            if content_div:
                # Convert HTML to Markdown
                html_content = str(content_div)
                markdown_content = self.h.handle(html_content)
                
                page_data = {
                    'url': current_url,
                    'title': self.get_page_title(soup),
                    'content': markdown_content.strip()
                }
                
                self.pages.append(page_data)
                logger.info(f"Extracted: {page_data['title']}")
            
            # Find more links to scrape
            new_links = self.extract_links(soup, current_url)
            to_visit.extend(new_links)
        
        return self.pages
    
    def save_all(self):
        """Save all scraped pages as Markdown files."""
        logger.info(f"Saving {len(self.pages)} pages to {self.output_dir}")
        
        for page_data in self.pages:
            self.create_markdown_file(page_data)
        
        logger.info("Done!")


def main():
    """Main execution function."""
    # Configuration
    SITE_URL = 'www.zerobhikshu.org'
    OUTPUT_DIR = 'content'  # Pelican content directory
    MAX_PAGES = None  # None for unlimited
    
    # Initialize scraper
    scraper = GoogleSiteScraper(SITE_URL, OUTPUT_DIR)
    
    # Scrape the site
    print(f"Starting scrape of {SITE_URL}...")
    scraper.scrape(max_pages=MAX_PAGES)
    
    # Save all pages
    scraper.save_all()
    
    print(f"\nScraping complete! {len(scraper.pages)} pages saved to '{OUTPUT_DIR}'")
    print("\nGenerated files:")
    for filepath in sorted(OUTPUT_DIR):
        print(f"  - {filepath}")


if __name__ == '__main__':
    main()
