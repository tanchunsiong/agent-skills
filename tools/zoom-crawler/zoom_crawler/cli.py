"""CLI entry point for zoom-crawler."""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console

from .crawler import DocsCrawler, ReferenceCrawler

app = typer.Typer(
    name="zoom-crawler",
    help="Crawl Zoom developer docs and API references to markdown.",
    add_completion=False,
)
console = Console()


@app.command()
def docs(
    url: str = typer.Argument(..., help="Starting URL to crawl (e.g., https://developers.zoom.us/docs/meeting-sdk/windows/)"),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output directory. Defaults to agent-skills/raw-docs/ with URL path mirrored.",
    ),
    depth: int = typer.Option(5, "--depth", "-d", help="Maximum crawl depth (1-20)"),
    delay: float = typer.Option(0.5, "--delay", help="Delay between requests in seconds"),
    concurrency: int = typer.Option(10, "--concurrency", "-c", help="Number of concurrent pages to crawl"),
    include: Optional[str] = typer.Option(None, "--include", "-i", help="Comma-separated URL patterns to include"),
    exclude: Optional[str] = typer.Option(None, "--exclude", "-e", help="Comma-separated URL patterns to exclude"),
):
    """
    Crawl Zoom developer docs (Next.js sites) to markdown.
    
    Uses Playwright for JavaScript rendering. Crawls 10 pages concurrently by default.
    Only crawls URLs matching the provided URL prefix.
    
    Example:
        zoom-crawler docs https://developers.zoom.us/docs/meeting-sdk/windows/
    """
    if depth < 1 or depth > 20:
        console.print("[red]Error:[/red] Depth must be between 1 and 20")
        raise typer.Exit(1)
    
    include_patterns = [p.strip() for p in include.split(",")] if include else None
    exclude_patterns = [p.strip() for p in exclude.split(",")] if exclude else None
    
    crawler = DocsCrawler(
        base_url=url,
        output_dir=output,
        max_depth=depth,
        delay=delay,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        concurrency=concurrency,
    )
    
    try:
        crawler.crawl()
    except KeyboardInterrupt:
        console.print("\n[yellow]Crawl interrupted by user[/yellow]")
        raise typer.Exit(130)


@app.command()
def reference(
    url: str = typer.Argument(..., help="Base URL for scope (e.g., https://marketplacefront.zoom.us/sdk/meeting/windows/)"),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output directory. Defaults to agent-skills/raw-docs/ with URL path mirrored.",
    ),
    start: Optional[str] = typer.Option(
        None,
        "--start", "-s",
        help="Starting page (relative or absolute). Use when base URL doesn't serve a page directly.",
    ),
    depth: int = typer.Option(10, "--depth", "-d", help="Maximum crawl depth (1-20)"),
    delay: float = typer.Option(0.5, "--delay", help="Delay between requests in seconds"),
    concurrency: int = typer.Option(10, "--concurrency", "-c", help="Number of concurrent pages to crawl"),
    include: Optional[str] = typer.Option(None, "--include", "-i", help="Comma-separated URL patterns to include"),
    exclude: Optional[str] = typer.Option(None, "--exclude", "-e", help="Comma-separated URL patterns to exclude"),
):
    """
    Crawl Zoom API references (Doxygen sites) to markdown.
    
    Uses Playwright browser for bot bypass. Crawls 10 pages concurrently by default.
    Only crawls URLs matching the provided URL prefix.
    
    Example:
        zoom-crawler reference https://marketplacefront.zoom.us/sdk/meeting/windows/ --start index.html
    """
    if depth < 1 or depth > 20:
        console.print("[red]Error:[/red] Depth must be between 1 and 20")
        raise typer.Exit(1)
    
    include_patterns = [p.strip() for p in include.split(",")] if include else None
    exclude_patterns = [p.strip() for p in exclude.split(",")] if exclude else None
    
    # Determine start URL
    from urllib.parse import urljoin
    start_url = urljoin(url.rstrip("/") + "/", start) if start else url
    
    crawler = ReferenceCrawler(
        base_url=url,
        output_dir=output,
        max_depth=depth,
        delay=delay,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        start_url=start_url,
        concurrency=concurrency,
    )
    
    try:
        crawler.crawl()
    except KeyboardInterrupt:
        console.print("\n[yellow]Crawl interrupted by user[/yellow]")
        raise typer.Exit(130)


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"zoom-crawler version {__version__}")


if __name__ == "__main__":
    app()
