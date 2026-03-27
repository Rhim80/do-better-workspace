# Web Crawler + Gemini OCR Skill

> **Claude Code Skill** for web page crawling + image OCR
> **Created**: 2025-10-29
> **Version**: v3.0.1 (2026-03-15)

## Quick Start

This skill **automatically activates** when you mention:
- "Analyze this URL: https://example.com"
- "Crawl this website"
- "Competitor site analysis"
- "Extract webpage with images"

## What It Does

1. **3-Tier Fetcher**: HTTP -> Stealth (Camoufox) -> Playwright (with scroll)
2. **trafilatura + SPA Fallback**: Content + RSC/JSON-LD/meta structured data
3. **3-Source Image Extraction**: markdown + HTML img + regex (SPA compatible)
4. **Gemini OCR**: Analyzes images up to 20MB (bypasses Claude's 5MB limit)
5. **OCR Inline**: OCR results auto-inserted at image positions

## Setup

```bash
cd ~/.claude/skills/web-crawler-ocr/scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install playwright && playwright install chromium
```

### API Key (OCR only)

Create `.env` file in `~/.claude/skills/web-crawler-ocr/scripts/`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional: Stealth Fetchers

For Cloudflare-protected sites:
```bash
pip install -r requirements-stealth.txt
scrapling install
```

## Usage

```bash
cd ~/.claude/skills/web-crawler-ocr/scripts && source venv/bin/activate

# Static sites
python3 web-crawler.py "https://example.com" /tmp/test.md --no-ocr

# Dynamic/SPA sites (Olive Young, Coupang, Musinsa etc.)
python3 web-crawler.py "https://oliveyoung.co.kr/..." /tmp/oy.md --wait 5000 --scroll --max-images 10
```

## Limitations

- **Gemini Free Tier**: 15 requests/minute
- **Image Limit**: Max 15 images per page (configurable)
- **Stealth**: Requires separate install

## Version History

- **v3.0.1** (2026-03-15): SPA/dynamic site support (Playwright scroll, RSC/JSON-LD extraction, 3-source image)
- **v3.0.0** (2026-03-15): Scrapling + trafilatura (Firecrawl removed)
- **v2.0.0** (2026-01-29): External CDN image OCR
- **v1.3.0** (2025-01-17): venv optimization
- **v1.0.0** (2025-10-29): Initial release

## Related Files

- **Skill Definition**: `~/.claude/skills/web-crawler-ocr/SKILL.md`
- **Scripts**: `~/.claude/skills/web-crawler-ocr/scripts/`
- **Config**: `~/.claude/skills/web-crawler-ocr/scripts/.env` (gitignored)
