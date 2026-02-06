"""Crawler implementations for docs and API references."""

import asyncio
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Set
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.async_api import async_playwright, Browser, BrowserContext
from rich.console import Console

console = Console()

# Concurrency settings
MAX_CONCURRENT_PAGES = 10


def get_default_output_dir() -> Path:
    """Get the default output directory (agent-skills/raw-docs/)."""
    current = Path.cwd()
    
    for parent in [current] + list(current.parents):
        if (parent / "zoom-meeting-sdk").exists() and (parent / "zoom-video-sdk").exists():
            return parent / "raw-docs"
    
    return current / "raw-docs"


# Path mappings for clearer folder names
# Order matters - more specific paths should come first
PATH_MAPPINGS = {
    # === Docs (developers.zoom.us) ===
    # Web Meeting SDK docs - Component View
    "docs/meeting-sdk/web/component-view/": "docs/meeting-sdk/web/component-view/",
    # Web Meeting SDK docs - Client View
    "docs/meeting-sdk/web/client-view/": "docs/meeting-sdk/web/client-view/",
    
    # === API Reference (marketplacefront.zoom.us) ===
    # Web Meeting SDK - Component View (must be before generic web path)
    "sdk/meeting/web/components/": "sdk/meeting-sdk/web/component-view/",
    # Web Meeting SDK - Client View
    "sdk/meeting/web/": "sdk/meeting-sdk/web/client-view/",
    # "custom" in Zoom's URL actually refers to Video SDK
    "sdk/custom/": "sdk/video-sdk/",
    # Consistent naming for Meeting SDK reference (Windows, etc.)
    "sdk/meeting/": "sdk/meeting-sdk/",
}


def url_to_filepath(url: str, base_url: str, output_dir: Path) -> Path:
    """Convert URL to a file path mirroring URL structure."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    
    # Apply path mappings for clearer folder names
    for old_path, new_path in PATH_MAPPINGS.items():
        if old_path in path:
            path = path.replace(old_path, new_path)
            break
    
    if not path or path.endswith("/"):
        path = path.rstrip("/") + "/index"
    
    if path.endswith(".html"):
        path = path[:-5]
    
    filepath = output_dir / parsed.netloc / (path + ".md")
    return filepath


class BaseCrawler(ABC):
    """Base crawler with concurrent crawling support."""
    
    def __init__(
        self,
        base_url: str,
        output_dir: Optional[Path] = None,
        max_depth: int = 4,
        delay: float = 0.5,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
        start_url: Optional[str] = None,
        concurrency: int = MAX_CONCURRENT_PAGES,
    ):
        self.base_url = base_url.rstrip("/")
        self.output_dir = output_dir or get_default_output_dir()
        self.max_depth = max_depth
        self.delay = delay
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.concurrency = concurrency
        
        initial_url = start_url if start_url else self.base_url
        self.visited: Set[str] = set()
        self.queued: Set[str] = {initial_url}  # Track queued URLs to avoid duplicates
        self.queue: asyncio.Queue = None  # Will be initialized in crawl()
        self.initial_url = initial_url
        self.stats = {"crawled": 0, "skipped": 0, "errors": 0}
        self.lock = None  # asyncio.Lock for thread-safe visited/queued access
        
        # Playwright resources
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
    
    def is_in_scope(self, url: str) -> bool:
        """Check if URL is within crawl scope."""
        if not url.startswith(self.base_url):
            return False
        
        if self.include_patterns:
            if not any(pattern in url for pattern in self.include_patterns):
                return False
        
        if self.exclude_patterns:
            if any(pattern in url for pattern in self.exclude_patterns):
                return False
        
        return True
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication."""
        url = url.split("#")[0]  # Remove fragment/anchor
        url = url.rstrip("/")
        return url
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> list[str]:
        """Extract all links from the page."""
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            
            if href.startswith(("javascript:", "mailto:", "tel:", "#")):
                continue
            
            absolute_url = urljoin(current_url, href)
            normalized = self.normalize_url(absolute_url)
            
            if self.is_in_scope(normalized):
                links.append(normalized)
        
        return list(set(links))  # Deduplicate
    
    def save_markdown(self, url: str, content: str, title: str = ""):
        """Save content as markdown file."""
        filepath = url_to_filepath(url, self.base_url, self.output_dir)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        frontmatter = f"---\nsource: {url}\n"
        if title:
            frontmatter += f"title: {title}\n"
        frontmatter += "---\n\n"
        
        filepath.write_text(frontmatter + content, encoding="utf-8")
    
    @abstractmethod
    async def fetch_page(self, url: str) -> tuple[str, BeautifulSoup]:
        """Fetch and parse a page. Returns (html_content, soup)."""
        pass
    
    @abstractmethod
    def extract_content(self, soup: BeautifulSoup, url: str) -> tuple[str, str]:
        """Extract main content from page. Returns (markdown_content, title)."""
        pass
    
    async def process_page(self, url: str, depth: int, semaphore: asyncio.Semaphore):
        """Process a single page with semaphore for concurrency control."""
        # Check and mark as visited atomically using lock
        async with self.lock:
            if url in self.visited:
                return  # Already processed by another worker
            self.visited.add(url)
            self.stats["crawled"] += 1
            crawl_num = self.stats["crawled"]
        
        console.print(f"[cyan]({crawl_num}) Crawling: {url}[/cyan]")
        
        async with semaphore:
            try:
                html, soup = await self.fetch_page(url)
                
                # Extract links first
                if depth < self.max_depth:
                    links = self.extract_links(soup, url)
                    
                    # Add new links atomically
                    async with self.lock:
                        new_links = [l for l in links if l not in self.visited and l not in self.queued]
                        for link in new_links:
                            self.queued.add(link)
                    
                    if new_links:
                        console.print(f"  [dim]Found {len(new_links)} new links[/dim]")
                        for link in new_links:
                            await self.queue.put((link, depth + 1))
                
                # Extract and save content
                content, title = self.extract_content(soup, url)
                
                if content.strip():
                    self.save_markdown(url, content, title)
                    console.print(f"  [green]Saved: {title or 'Untitled'}[/green]")
                
                # Small delay between requests
                await asyncio.sleep(self.delay)
                
            except Exception as e:
                console.print(f"[red]Error crawling {url}: {e}[/red]")
                async with self.lock:
                    self.stats["errors"] += 1
    
    async def worker(self, semaphore: asyncio.Semaphore):
        """Worker that processes pages from the queue."""
        while True:
            try:
                url, depth = await asyncio.wait_for(self.queue.get(), timeout=5.0)
                
                if depth > self.max_depth:
                    self.stats["skipped"] += 1
                    self.queue.task_done()
                    continue
                
                await self.process_page(url, depth, semaphore)
                self.queue.task_done()
                
            except asyncio.TimeoutError:
                # No more items, check if queue is empty and no pending tasks
                if self.queue.empty():
                    break
            except Exception as e:
                console.print(f"[red]Worker error: {e}[/red]")
                self.queue.task_done()
    
    async def _crawl_async(self):
        """Async crawl implementation."""
        console.print(f"\n[bold blue]Starting concurrent crawl[/bold blue]")
        console.print(f"  Base URL: {self.base_url}")
        console.print(f"  Output: {self.output_dir}")
        console.print(f"  Max depth: {self.max_depth}")
        console.print(f"  Concurrency: {self.concurrency}")
        console.print(f"  Delay: {self.delay}s\n")
        
        # Initialize queue and lock
        self.queue = asyncio.Queue()
        self.lock = asyncio.Lock()
        await self.queue.put((self.initial_url, 0))
        
        # Initialize browser
        await self._init_browser()
        
        try:
            semaphore = asyncio.Semaphore(self.concurrency)
            
            # Start workers
            workers = [asyncio.create_task(self.worker(semaphore)) for _ in range(self.concurrency)]
            
            # Wait for all workers to complete
            await asyncio.gather(*workers)
            
        finally:
            await self._close_browser()
        
        # Print summary
        console.print(f"\n[bold green]Crawl complete![/bold green]")
        console.print(f"  Pages crawled: {self.stats['crawled']}")
        console.print(f"  Pages skipped: {self.stats['skipped']}")
        console.print(f"  Errors: {self.stats['errors']}")
        console.print(f"  Output: {self.output_dir}\n")
    
    @abstractmethod
    async def _init_browser(self):
        """Initialize browser resources."""
        pass
    
    @abstractmethod
    async def _close_browser(self):
        """Close browser resources."""
        pass
    
    def crawl(self):
        """Main entry point - runs async crawl."""
        asyncio.run(self._crawl_async())


class DocsCrawler(BaseCrawler):
    """Crawler for Next.js documentation sites using Playwright."""
    
    async def _init_browser(self):
        """Initialize Playwright browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
    
    async def _close_browser(self):
        """Close Playwright browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def fetch_page(self, url: str) -> tuple[str, BeautifulSoup]:
        """Fetch page using Playwright for JS rendering."""
        page = await self.context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Expand all collapsed menu items
            try:
                await page.evaluate("""
                    () => {
                        document.querySelectorAll('.ant-menu-submenu:not(.ant-menu-submenu-open) .ant-menu-submenu-title').forEach(el => {
                            el.click();
                        });
                    }
                """)
                await page.wait_for_timeout(500)
            except Exception:
                pass
            
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            return html, soup
        finally:
            await page.close()
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> list[str]:
        """Extract links from Next.js docs page, including Ant Design menu items."""
        links = []
        parsed = urlparse(current_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        # Standard anchor links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith(("javascript:", "mailto:", "tel:", "#")):
                continue
            absolute_url = urljoin(current_url, href)
            normalized = self.normalize_url(absolute_url)
            if self.is_in_scope(normalized):
                links.append(normalized)
        
        # Ant Design menu items with data-menu-id containing paths
        for el in soup.find_all(attrs={"data-menu-id": True}):
            menu_id = el.get("data-menu-id", "")
            if "/docs/" in menu_id:
                path_match = re.search(r'(/docs/[^\s]+)', menu_id)
                if path_match:
                    path = path_match.group(1)
                    absolute_url = base + path
                    normalized = self.normalize_url(absolute_url)
                    if self.is_in_scope(normalized):
                        links.append(normalized)
            elif "/changelog/" in menu_id:
                path_match = re.search(r'(/changelog/[^\s]+)', menu_id)
                if path_match:
                    path = path_match.group(1)
                    absolute_url = base + path
                    normalized = self.normalize_url(absolute_url)
                    if self.is_in_scope(normalized):
                        links.append(normalized)
        
        return list(set(links))
    
    def extract_content(self, soup: BeautifulSoup, url: str) -> tuple[str, str]:
        """Extract main content from Next.js docs page."""
        title = ""
        title_el = soup.find("h1") or soup.find("title")
        if title_el:
            title = title_el.get_text(strip=True)
        
        # Remove unwanted elements
        unwanted_selectors = [
            "header", "footer", "nav", "script", "style", "noscript",
            "[class*='sider']", "[class*='sidenav']", "[class*='sidebar']",
            ".ant-menu", "[class*='menu']",
            "[class*='toc']", "[class*='TableOfContents']",
            "[class*='breadcrumb']",
        ]
        for selector in unwanted_selectors:
            for el in soup.select(selector):
                el.decompose()
        
        # Find main content
        main_content = None
        zoom_selectors = [".zva-content", "[class*='content_children']", "[class*='docs_content']"]
        for selector in zoom_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            for selector in ["main", "article", '[role="main"]', ".content", "#content"]:
                main_content = soup.select_one(selector)
                if main_content:
                    break
        
        if not main_content:
            main_content = soup.find("body")
        
        if not main_content:
            return "", title
        
        markdown = md(str(main_content), heading_style="ATX", code_language_callback=lambda el: "")
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        markdown = markdown.strip()
        
        return markdown, title


class ReferenceCrawler(BaseCrawler):
    """Crawler for Doxygen API reference sites using Playwright."""
    
    async def _init_browser(self):
        """Initialize Playwright browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
    
    async def _close_browser(self):
        """Close Playwright browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def fetch_page(self, url: str) -> tuple[str, BeautifulSoup]:
        """Fetch page using Playwright."""
        page = await self.context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            return html, soup
        finally:
            await page.close()
    
    def extract_content(self, soup: BeautifulSoup, url: str) -> tuple[str, str]:
        """Extract main content from Doxygen page."""
        title = ""
        title_el = soup.find("div", class_="title") or soup.find("h1") or soup.find("title")
        if title_el:
            title = title_el.get_text(strip=True)
        
        # Remove unwanted elements
        for selector in ["script", "style", "noscript", "#nav-tree", ".nav-path", "#MSearchBox"]:
            for el in soup.select(selector):
                el.decompose()
        
        # Find main content
        main_content = None
        for selector in ["#doc-content", ".contents", "main", "article"]:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find("body")
        
        if not main_content:
            return "", title
        
        markdown = md(str(main_content), heading_style="ATX", code_language_callback=lambda el: "cpp")
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        markdown = markdown.strip()
        
        return markdown, title
