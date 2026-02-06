# Zoom Docs Crawler

Crawl Zoom developer docs and API references to markdown files for building agent skills.

## Installation

```bash
cd tools/zoom-crawler

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows

# Install package
pip install -e .

# Install Playwright browsers
playwright install chromium
```

## Usage

### Crawl Developer Docs (Next.js sites)

```bash
# Crawl Windows Meeting SDK docs
zoom-crawler docs https://developers.zoom.us/docs/meeting-sdk/windows/

# Crawl Windows Video SDK docs
zoom-crawler docs https://developers.zoom.us/docs/video-sdk/windows/

# With custom settings
zoom-crawler docs https://developers.zoom.us/docs/meeting-sdk/windows/ \
  --depth 5 \
  --concurrency 10
```

### Crawl API Reference (Doxygen sites)

```bash
# Crawl Windows Meeting SDK API reference
zoom-crawler reference https://marketplacefront.zoom.us/sdk/meeting/windows/ \
  --start index.html

# Crawl Windows Video SDK API reference
# Note: "custom" in URL = Video SDK, automatically mapped to "video-sdk" folder
zoom-crawler reference https://marketplacefront.zoom.us/sdk/custom/windows/ \
  --start index.html

# With custom settings
zoom-crawler reference https://marketplacefront.zoom.us/sdk/meeting/windows/ \
  --start index.html \
  --depth 10 \
  --concurrency 10
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output, -o` | Output directory | `agent-skills/raw-docs/` |
| `--depth, -d` | Maximum crawl depth | 5 (docs), 10 (reference) |
| `--delay` | Delay between requests (seconds) | 0.5 |
| `--concurrency, -c` | Number of concurrent pages | 10 |
| `--start, -s` | Starting page (reference only) | None |
| `--include, -i` | URL patterns to include (comma-separated) | None |
| `--exclude, -e` | URL patterns to exclude (comma-separated) | None |

## Output Structure

Output mirrors the URL path structure with automatic path mappings:

```
raw-docs/
├── developers.zoom.us/
│   └── docs/
│       ├── meeting-sdk/
│       │   └── windows/
│       │       ├── windows.md
│       │       ├── get-started/
│       │       └── ...
│       └── video-sdk/
│           └── windows/
│               └── ...
└── marketplacefront.zoom.us/
    └── sdk/
        ├── meeting-sdk/         # Note: "meeting" URL mapped here
        │   └── windows/
        │       ├── index.md
        │       ├── class_i_auth_service.md
        │       └── ...
        └── video-sdk/           # Note: "custom" URL mapped here
            └── windows/
                └── ...
```

## Path Mappings

The crawler automatically maps certain URL paths to clearer folder names:

| URL Path | Output Folder | Reason |
|----------|---------------|--------|
| `sdk/meeting/` | `sdk/meeting-sdk/` | Consistent naming with docs |
| `sdk/custom/` | `sdk/video-sdk/` | "custom" in Zoom's URL refers to Video SDK |

## How It Works

### Concurrent Crawling
- Both crawlers use **asyncio** for concurrent page fetching
- Default: 10 pages crawled simultaneously
- Thread-safe URL tracking prevents duplicate crawls

### Docs Crawler
- Uses **Playwright** for full JavaScript rendering
- Handles React/Next.js dynamic content (Ant Design menus)
- Extracts main content area, removes nav/sidebar/footer
- Converts HTML to clean Markdown

### Reference Crawler
- Uses **Playwright** to bypass bot detection
- Designed for Doxygen-generated API docs
- Use `--start index.html` since base URL doesn't serve a page
- Preserves code blocks as C++

## Crawl Scope

The crawler **only** follows links that match the provided URL prefix:

```
Input URL: https://developers.zoom.us/docs/meeting-sdk/windows/

Crawled:
  ✅ .../meeting-sdk/windows/
  ✅ .../meeting-sdk/windows/get-started/
  ✅ .../meeting-sdk/windows/raw-data/

NOT crawled:
  ❌ .../meeting-sdk/linux/      (different platform)
  ❌ .../meeting-sdk/auth/       (parent level)
  ❌ .../video-sdk/...           (different product)
```

## Full Crawl Commands

To crawl all Windows SDK documentation:

```bash
# Meeting SDK
zoom-crawler docs https://developers.zoom.us/docs/meeting-sdk/windows/
zoom-crawler reference https://marketplacefront.zoom.us/sdk/meeting/windows/ --start index.html

# Video SDK
zoom-crawler docs https://developers.zoom.us/docs/video-sdk/windows/
zoom-crawler reference https://marketplacefront.zoom.us/sdk/custom/windows/ --start index.html
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black zoom_crawler/

# Lint
ruff check zoom_crawler/
```
