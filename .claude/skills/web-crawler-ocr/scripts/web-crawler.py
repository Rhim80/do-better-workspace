#!/usr/bin/env python3
"""
Web Crawler + Gemini OCR v3.0

Scrapling (local) + trafilatura (content extraction) + Gemini OCR
Firecrawl 의존 완전 제거, 로컬 크롤링으로 전환

사용법:
  python web-crawler.py <URL> [output.md] [--wait ms] [--scroll] [--max-images N] [--no-ocr]

v3.0.1 (2026-03-15): 동적 사이트 이미지 추출 범용 개선
  - filter_product_images: thumbnail 패턴 정밀화 (한국 이커머스 호환)
  - extract_images_from_html: SPA fallback (article>main>body>soup 전체)
  - extract_images_from_regex: HTML 전체에서 이미지 URL 정규식 추출
  - 3소스 통합 (markdown + HTML img + regex) 으로 이미지 추출률 향상

v3.0.0 (2026-03-15): Scrapling + trafilatura로 전환
  - Firecrawl API 의존 제거 (완전 로컬)
  - 3단계 fetcher 에스컬레이션 (HTTP -> Stealth -> Dynamic)
  - trafilatura로 콘텐츠 정제 + markdown 변환
  - OCR 인라인 자동 삽입 (이미지 위치에 배치)
  - 비동기 이미지 다운로드 (aiohttp)
"""

import os
import sys
import re
import asyncio
import base64
import hashlib
import tempfile
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# SSL CA 번들 설정 (macOS Python 3.14 호환)
import certifi
os.environ.setdefault('SSL_CERT_FILE', certifi.where())
os.environ.setdefault('CURL_CA_BUNDLE', certifi.where())
os.environ.setdefault('REQUESTS_CA_BUNDLE', certifi.where())

# 환경변수 로드
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# 색상 출력
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'


def print_color(text, color):
    print(f"{color}{text}{Colors.NC}")


def check_api_keys(need_ocr=True):
    """API 키 확인 - OCR 사용시에만 GEMINI_API_KEY 필요"""
    if need_ocr and not GEMINI_API_KEY:
        print_color("Missing API key: GEMINI_API_KEY", Colors.RED)
        print("\n설정 방법:")
        print("1. .env 파일 생성 또는 환경변수 설정:")
        print("   GEMINI_API_KEY='your_key_here'")
        print("\n2. API 키 발급:")
        print("   - Gemini: https://aistudio.google.com/apikey")
        sys.exit(1)


def normalize_url(url):
    """URL 정규화 - 쿼리파라미터 제거, fragment 제거"""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))


def is_blocked_response(status_code, text):
    """차단된 응답인지 감지"""
    if status_code in (403, 503):
        return True
    block_indicators = [
        "just a moment", "checking your browser",
        "cloudflare", "captcha", "access denied",
        "please enable javascript", "ray id",
    ]
    text_lower = text.lower() if text else ""
    if any(indicator in text_lower for indicator in block_indicators):
        return True
    if len(text) < 1024 and status_code == 200:
        # 매우 짧은 응답은 차단 페이지일 수 있음
        if any(ind in text_lower for ind in ["just a moment", "checking"]):
            return True
    return False


# ============================================================
# Fetcher 에스컬레이션 엔진
# ============================================================

def _scrapling_available():
    """scrapling import 가능 여부 확인"""
    try:
        from scrapling import Fetcher
        return True
    except (ImportError, ModuleNotFoundError):
        return False


def fetch_with_scrapling(url, escalate=True, wait_for=None, scroll=False, force_stealth=False):
    """
    3단계 fetcher 에스컬레이션:
    Tier 1: Fetcher (HTTP + TLS impersonation) - 80%+ 사이트 커버
    Tier 2: StealthyFetcher (Cloudflare 우회) - 차단 감지시 자동 에스컬레이션
    Tier 3: DynamicFetcher (Playwright) - --wait/--scroll 사용시 또는 Tier 2 실패시

    scrapling 미설치시 requests fallback 자동 전환
    """
    # scrapling import 불가시 바로 fallback
    if not _scrapling_available():
        print_color(
            "scrapling 로드 실패. requests fallback 사용.\n"
            "scrapling 전체 설치: pip install 'scrapling[fetchers]' && scrapling install",
            Colors.YELLOW
        )
        html = _fetch_bs4_fallback(url)
        if html and is_blocked_response(200, html):
            print_color("차단 감지. --stealth 옵션과 scrapling[fetchers] 설치가 필요합니다.", Colors.YELLOW)
        return html

    from scrapling import Fetcher

    # --wait 또는 --scroll 사용시 바로 Tier 3로
    if wait_for or scroll:
        return _fetch_dynamic(url, wait_for=wait_for, scroll=scroll)

    # --stealth 플래그로 바로 Tier 2
    if force_stealth:
        return _fetch_stealthy(url)

    # Tier 1: 기본 HTTP fetcher
    print_color(f"[Tier 1] HTTP fetcher: {url}", Colors.BLUE)
    try:
        from curl_cffi import requests as curl_requests
        response = curl_requests.get(url, impersonate="chrome", timeout=30, verify=False)

        if is_blocked_response(response.status_code, response.text):
            print_color("[Tier 1] 차단 감지, Tier 2로 에스컬레이션", Colors.YELLOW)
            if escalate:
                return _fetch_stealthy(url)
            return None

        print_color(f"[Tier 1] 성공 ({len(response.text)} bytes)", Colors.GREEN)
        return response.text

    except Exception as e:
        print_color(f"[Tier 1] 실패: {e}", Colors.YELLOW)
        if escalate:
            return _fetch_stealthy(url)
        return None


def _fetch_stealthy(url):
    """Tier 2: StealthyFetcher (Camoufox 브라우저, Cloudflare 우회)"""
    try:
        from scrapling import StealthyFetcher
    except (ImportError, ModuleNotFoundError):
        print_color(
            "[Tier 2] StealthyFetcher 미설치. 설치하려면:\n"
            "  pip install 'scrapling[fetchers]'\n"
            "  scrapling install\n"
            "BS4 fallback으로 전환합니다.",
            Colors.YELLOW
        )
        return _fetch_bs4_fallback(url)

    print_color(f"[Tier 2] StealthyFetcher: {url}", Colors.BLUE)
    try:
        fetcher = StealthyFetcher()
        response = fetcher.fetch(url)

        status = getattr(response, 'status', 200)
        html = response.body if hasattr(response, 'body') else str(response)
        if isinstance(html, bytes):
            html = html.decode('utf-8', errors='replace')
        if is_blocked_response(status, html):
            print_color("[Tier 2] 여전히 차단됨, Tier 3으로 에스컬레이션", Colors.YELLOW)
            return _fetch_dynamic(url)

        print_color(f"[Tier 2] 성공 ({len(html)} bytes)", Colors.GREEN)
        return html

    except Exception as e:
        print_color(f"[Tier 2] 실패: {e}", Colors.YELLOW)
        return _fetch_dynamic(url)


def _fetch_dynamic(url, wait_for=None, scroll=False):
    """Tier 3: Playwright 직접 사용 (스크롤 + JS 대기 지원)"""
    try:
        from playwright.sync_api import sync_playwright
    except (ImportError, ModuleNotFoundError):
        print_color(
            "[Tier 3] Playwright 미설치. 설치하려면:\n"
            "  pip install playwright && playwright install chromium\n"
            "BS4 fallback으로 전환합니다.",
            Colors.YELLOW
        )
        return _fetch_bs4_fallback(url)

    print_color(f"[Tier 3] Playwright: {url}", Colors.BLUE)
    wait_ms = wait_for or 3000

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 800},
            )
            page = context.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            print_color(f"  JS 렌더링 대기: {wait_ms}ms", Colors.BLUE)
            page.wait_for_timeout(wait_ms)

            if scroll:
                print_color("  페이지 스크롤 중 (lazy-load 트리거)...", Colors.BLUE)
                _scroll_page(page)

            html = page.content()
            browser.close()

        print_color(f"[Tier 3] 성공 ({len(html)} bytes)", Colors.GREEN)
        return html

    except Exception as e:
        print_color(f"[Tier 3] 실패: {e}", Colors.YELLOW)
        return _fetch_bs4_fallback(url)


def _scroll_page(page, max_scrolls=15, scroll_delay=1000):
    """페이지를 점진적으로 스크롤하여 lazy-load 콘텐츠 트리거"""
    prev_height = 0
    for i in range(max_scrolls):
        page.evaluate('window.scrollBy(0, window.innerHeight)')
        page.wait_for_timeout(scroll_delay)

        cur_height = page.evaluate('document.body.scrollHeight')
        if cur_height == prev_height:
            # 더 이상 새 콘텐츠 없음
            break
        prev_height = cur_height

    # 맨 위로 복귀 (일부 사이트에서 상단 콘텐츠 로드 트리거)
    page.evaluate('window.scrollTo(0, 0)')
    page.wait_for_timeout(500)
    print_color(f"  스크롤 완료 ({i+1}회, 최종 높이: {cur_height}px)", Colors.GREEN)


def _fetch_bs4_fallback(url):
    """최종 fallback: curl_cffi (TLS fingerprint + SSL 우회)"""
    print_color("[Fallback] curl_cffi로 크롤링", Colors.BLUE)
    try:
        from curl_cffi import requests as curl_requests
        response = curl_requests.get(url, impersonate="chrome", timeout=30, verify=False)
        response.raise_for_status()
        print_color(f"[Fallback] 성공 ({len(response.text)} bytes)", Colors.GREEN)
        return response.text
    except Exception as e:
        print_color(f"[Fallback] 실패: {e}", Colors.RED)
        return None


# ============================================================
# 콘텐츠 정제 (trafilatura)
# ============================================================

def extract_content(html_string, source_url):
    """trafilatura로 콘텐츠 정제 + markdown 변환. SPA fallback 포함."""
    import trafilatura

    print_color("trafilatura로 콘텐츠 정제 중...", Colors.BLUE)

    markdown = trafilatura.extract(
        html_string,
        output_format="markdown",
        include_formatting=True,
        include_links=True,
        include_images=True,
        include_tables=True,
        favor_recall=True,
        url=source_url,
    )

    if markdown and len(markdown) > 100:
        print_color(f"trafilatura 추출 완료 ({len(markdown)} chars)", Colors.GREEN)
    else:
        print_color(f"trafilatura 결과 부족 ({len(markdown or '')} chars)", Colors.YELLOW)

    # SPA 구조화 데이터 항상 시도 (보강용)
    spa_content = _extract_spa_structured_data(html_string, source_url)
    if spa_content and len(spa_content) > 100:
        print_color(f"SPA 구조화 데이터 추출 ({len(spa_content)} chars)", Colors.GREEN)

    # 결과 병합: SPA 데이터가 있으면 앞에 배치
    if spa_content and markdown:
        return f"## 구조화 데이터\n\n{spa_content}\n\n---\n\n## 페이지 콘텐츠\n\n{markdown}"
    if spa_content:
        return spa_content
    if markdown:
        return markdown

    # 최종 fallback: BS4 plain text
    print_color("BS4 fallback으로 전환", Colors.YELLOW)
    return _extract_bs4_fallback(html_string, source_url)


def _extract_spa_structured_data(html_string, source_url):
    """SPA 사이트에서 script 태그 내 구조화 데이터 추출 (범용)

    지원하는 데이터 소스:
    - JSON-LD (schema.org)
    - Next.js __NEXT_DATA__
    - Next.js RSC payload (self.__next_f.push)
    - Nuxt.js __NUXT__
    - 기타 인라인 JSON 데이터
    """
    import json
    soup = BeautifulSoup(html_string, 'html.parser')
    sections = []

    # 1. JSON-LD
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            text = _json_ld_to_text(data)
            if text:
                sections.append(text)
        except (json.JSONDecodeError, TypeError):
            pass

    # 2. __NEXT_DATA__ (Next.js SSR)
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        try:
            data = json.loads(next_data.string)
            props = data.get('props', {}).get('pageProps', {})
            text = _flatten_json_to_text(props, max_depth=4)
            if text:
                sections.append(text)
        except (json.JSONDecodeError, TypeError):
            pass

    # 3. Next.js RSC payload (self.__next_f.push) - 가장 복잡하지만 데이터가 풍부
    for script in soup.find_all('script'):
        text = script.string or ''
        if 'self.__next_f.push' not in text or len(text) < 300:
            continue
        rsc_text = _extract_rsc_payload(text)
        if rsc_text:
            sections.append(rsc_text)

    # 4. meta 태그 보강
    meta_section = _extract_meta_content(soup)
    if meta_section:
        sections.insert(0, meta_section)

    return '\n\n'.join(sections) if sections else None


def _json_ld_to_text(data):
    """JSON-LD를 읽기 가능한 텍스트로 변환"""
    if isinstance(data, list):
        return '\n'.join(_json_ld_to_text(item) for item in data if item)

    if not isinstance(data, dict):
        return ''

    lines = []
    type_name = data.get('@type', '')
    if type_name:
        lines.append(f"**{type_name}**")

    # 주요 필드 매핑
    field_labels = {
        'name': '상품명', 'description': '설명', 'brand': '브랜드',
        'price': '가격', 'priceCurrency': '통화',
        'sku': 'SKU', 'category': '카테고리',
        'aggregateRating': '평점', 'reviewCount': '리뷰수',
    }

    for key, label in field_labels.items():
        val = data.get(key)
        if val:
            if isinstance(val, dict):
                val = val.get('name', val.get('value', str(val)))
            lines.append(f"- {label}: {val}")

    # offers
    offers = data.get('offers')
    if offers:
        if isinstance(offers, dict):
            offers = [offers]
        if isinstance(offers, list):
            for offer in offers:
                if isinstance(offer, dict):
                    price = offer.get('price', '')
                    currency = offer.get('priceCurrency', '')
                    if price:
                        lines.append(f"- 가격: {price} {currency}")

    return '\n'.join(lines) if lines else ''


def _extract_rsc_payload(script_text):
    """Next.js RSC payload에서 구조화 데이터 추출 (범용)

    RSC payload는 깊이 중첩된 JSON이므로 key:value 패턴을 직접 추출.
    """
    # 전체 텍스트를 유니코드 디코딩 (\\uXXXX -> 실제 문자)
    try:
        decoded = script_text.encode('utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, ValueError):
        try:
            decoded = script_text.encode('utf-8').decode('unicode_escape')
        except (UnicodeDecodeError, ValueError):
            decoded = script_text

    # 관심 있는 key-value 패턴 직접 추출
    kv_patterns = {
        '상품명': r'"goodsName"\s*:\s*"([^"]+)"',
        '상품번호': r'"goodsNumber"\s*:\s*"([^"]+)"',
        '브랜드': r'"onlineBrandName"\s*:\s*"([^"]+)"',
        '공급사': r'"supplierName"\s*:\s*"([^"]+)"',
        '판매가': r'"salePrice"\s*:\s*(\d+)',
        '최종가': r'"finalPrice"\s*:\s*(\d+)',
        '상태': r'"statusName"\s*:\s*"([^"]+)"',
        '옵션': r'"optionName"\s*:\s*"([^"]+)"',
        '표준코드': r'"standardCode"\s*:\s*"([^"]+)"',
        '대분류': r'"upperCategoryName"\s*:\s*"([^"]+)"',
        '중분류': r'"middleCategoryName"\s*:\s*"([^"]+)"',
        '소분류': r'"lowerCategoryName"\s*:\s*"([^"]+)"',
        '품절여부': r'"soldOutFlag"\s*:\s*(true|false)',
        '배송유형': r'"deliveryType"\s*:\s*"([^"]+)"',
        '등록일': r'"registeredDate"\s*:\s*"([^"]+)"',
        # 범용 이커머스 패턴
        'productName': r'"productName"\s*:\s*"([^"]+)"',
        'brandName': r'"brandName"\s*:\s*"([^"]+)"',
        'price': r'"price"\s*:\s*(\d+)',
        'description': r'"description"\s*:\s*"([^"]{10,500})"',
        'category': r'"category"\s*:\s*"([^"]+)"',
    }

    lines = []
    seen_values = set()

    for label, pattern in kv_patterns.items():
        matches = re.findall(pattern, decoded)
        for val in matches:
            if val in seen_values or not val:
                continue
            seen_values.add(val)
            # 가격 포맷팅
            if label in ('판매가', '최종가', 'price'):
                try:
                    val = f"{int(val):,}원"
                except (ValueError, TypeError):
                    pass
            lines.append(f"- {label}: {val}")

    if lines:
        return '\n'.join(lines)

    # key-value 추출 실패시 한글 텍스트 직접 추출
    korean_texts = re.findall(r'[가-힣][가-힣\s\w/().,·\-]+', decoded)
    meaningful = [t.strip() for t in korean_texts if len(t.strip()) > 5]
    if meaningful:
        return '\n'.join(f"- {t}" for t in list(dict.fromkeys(meaningful))[:30])
    return ''


def _flatten_json_to_text(data, max_depth=3, prefix=''):
    """JSON 객체를 사람이 읽을 수 있는 key-value 텍스트로 변환"""
    if max_depth <= 0:
        return ''

    lines = []

    # 한글 라벨 매핑
    label_map = {
        'goodsName': '상품명', 'goodsNumber': '상품번호',
        'salePrice': '판매가', 'finalPrice': '최종가',
        'supplierName': '공급사', 'onlineBrandName': '브랜드',
        'brandName': '브랜드', 'statusName': '상태',
        'optionName': '옵션', 'standardCode': '표준코드',
        'upperCategoryName': '대분류', 'middleCategoryName': '중분류',
        'lowerCategoryName': '소분류', 'leafCategoryName': '세분류',
        'displayStartDatetime': '등록일', 'deliveryType': '배송유형',
        'soldOutFlag': '품절여부', 'description': '설명',
        'name': '이름', 'price': '가격', 'category': '카테고리',
    }

    if isinstance(data, dict):
        for key, val in data.items():
            if val is None or val == '' or val == []:
                continue
            label = label_map.get(key, key)
            full_label = f"{prefix}{label}" if prefix else label

            if isinstance(val, (str, int, float, bool)):
                # 가격은 포맷팅
                if 'price' in key.lower() or 'Price' in key:
                    try:
                        val = f"{int(val):,}원"
                    except (ValueError, TypeError):
                        pass
                lines.append(f"- {full_label}: {val}")
            elif isinstance(val, dict):
                sub = _flatten_json_to_text(val, max_depth - 1, f"{full_label} > ")
                if sub:
                    lines.append(sub)
            elif isinstance(val, list) and len(val) <= 5:
                for i, item in enumerate(val):
                    if isinstance(item, dict):
                        sub = _flatten_json_to_text(item, max_depth - 1, f"{full_label}[{i}] > ")
                        if sub:
                            lines.append(sub)
                    elif isinstance(item, (str, int, float)):
                        lines.append(f"- {full_label}: {item}")

    return '\n'.join(lines)


def _extract_meta_content(soup):
    """meta 태그에서 주요 콘텐츠 추출"""
    lines = []

    meta_fields = [
        ('og:title', '제목'),
        ('og:description', '설명'),
        ('og:site_name', '사이트'),
    ]

    for prop, label in meta_fields:
        tag = soup.find('meta', property=prop)
        if tag and tag.get('content'):
            lines.append(f"- {label}: {tag['content']}")

    # name 기반 meta
    desc = soup.find('meta', attrs={'name': 'description'})
    if desc and desc.get('content') and not any('설명' in l for l in lines):
        lines.append(f"- 설명: {desc['content']}")

    return '\n'.join(lines) if lines else ''


def _extract_bs4_fallback(html_string, source_url):
    """BS4 fallback 콘텐츠 추출 - SPA 범용"""
    soup = BeautifulSoup(html_string, 'html.parser')

    # 불필요한 태그 제거
    for tag in soup.find_all(['nav', 'footer', 'header', 'script', 'style', 'noscript']):
        tag.decompose()

    content = soup.find('article') or soup.find('main') or soup.body or soup
    text = content.get_text(separator='\n', strip=True)

    # 의미 있는 줄만 필터링 (3자 이상)
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 3]
    return '\n'.join(lines)


def extract_title(html_string):
    """HTML에서 타이틀 추출"""
    soup = BeautifulSoup(html_string, 'html.parser')

    # og:title 우선
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        return og_title['content']

    # <title> 태그
    title_tag = soup.find('title')
    if title_tag and title_tag.text.strip():
        return title_tag.text.strip()

    # h1 태그
    h1 = soup.find('h1')
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)

    return 'Untitled'


# ============================================================
# 이미지 추출 + 필터링
# ============================================================

def extract_images_from_html(html_string, base_url):
    """HTML에서 이미지 URL 추출 - SPA/동적 사이트 범용"""
    soup = BeautifulSoup(html_string, 'html.parser')
    # article > main > body > soup 전체 순서로 탐색 (SPA fallback)
    content = soup.find('article') or soup.find('main') or soup.body or soup

    images = []
    seen = set()

    # data-* 속성에서 이미지 URL을 찾는 패턴 (동적 사이트 범용)
    data_attrs = ['src', 'data-src', 'data-lazy-src', 'data-original',
                  'data-img-src', 'data-image', 'data-full-src']

    for img_tag in content.find_all('img'):
        src = None
        for attr in data_attrs:
            src = img_tag.get(attr)
            if src and src.startswith(('http', '/')):
                break
        if not src:
            continue

        full_url = urljoin(base_url, src)
        normalized = normalize_url(full_url)

        if normalized not in seen:
            seen.add(normalized)
            alt = img_tag.get('alt', '')
            images.append({
                'url': full_url,
                'normalized_url': normalized,
                'alt': alt
            })

    return images


def extract_images_from_markdown(markdown_content, base_url):
    """Markdown에서 이미지 URL 추출"""
    patterns = [
        r'!\[([^\]]*)\]\(([^)\s]+)',  # ![alt](url)
        r'\[!\[([^\]]*)\]\(([^)\s]+)',  # [![alt](url)]
    ]

    images = []
    seen = set()

    for pattern in patterns:
        matches = re.findall(pattern, markdown_content)
        for match in matches:
            alt = match[0] if match[0] else ''
            url = match[1].rstrip(')')

            if not url.startswith(('http://', 'https://')):
                url = urljoin(base_url, url)

            normalized = normalize_url(url)
            if normalized not in seen:
                seen.add(normalized)
                images.append({
                    'url': url,
                    'normalized_url': normalized,
                    'alt': alt
                })

    return images


def extract_images_from_regex(html_string, base_url):
    """HTML 전체에서 이미지 URL 패턴을 정규식으로 추출 (SPA/동적 사이트 범용)

    <img> 태그 밖에 있는 이미지도 잡음:
    - og:image, twitter:image 메타 태그
    - JSON-LD/JS 데이터 내 이미지 URL
    - CSS background-image
    - data-* 속성 내 이미지 URL
    """
    pattern = r'https?://[^"\s\'<>\)]+\.(?:jpg|jpeg|png|webp)(?:\?[^"\s\'<>\)]*)?'
    matches = re.findall(pattern, html_string, re.IGNORECASE)

    base_domain = urlparse(base_url).netloc.replace('www.', '')
    images = []
    seen = set()

    # 같은 도메인 이미지 우선
    same_domain = []
    other_domain = []

    for url in matches:
        normalized = normalize_url(url)
        if normalized in seen:
            continue
        seen.add(normalized)

        img = {'url': url, 'normalized_url': normalized, 'alt': ''}
        url_domain = urlparse(url).netloc.replace('www.', '')
        if base_domain in url_domain or url_domain in base_domain:
            same_domain.append(img)
        else:
            other_domain.append(img)

    return same_domain + other_domain


def filter_product_images(image_list, max_images=15):
    """상품 상세 이미지만 필터링 - 썸네일/아이콘 제외"""
    exclude_patterns = [
        'thumb_', '_thumb.', '/thumb/',
        'icon', 'logo', 'banner',
        'btn', 'button', 'arrow', 'close', 'search',
        'profile', 'avatar', 'emoji', 'spinner', 'loading',
        'RS=64', 'RS=32', 'RS=48', 'RS=100',
        'reviewProfile', 'user_profile',
        '1x1.gif', 'spacer', 'pixel', 'blank.gif',
    ]

    priority_patterns = [
        'apglobal.com', 'asset/', 'goods/', 'product/',
        'detail', 'content', 'description', 'inline',
    ]

    priority_images = []
    normal_images = []

    for img in image_list:
        url_lower = img['url'].lower()

        if any(exc in url_lower for exc in exclude_patterns):
            continue

        if url_lower.endswith('.gif') or '.gif?' in url_lower:
            continue

        if any(inc in url_lower for inc in priority_patterns):
            priority_images.append(img)
        else:
            normal_images.append(img)

    return (priority_images + normal_images)[:max_images]


# ============================================================
# 비동기 이미지 다운로드
# ============================================================

async def download_image_async(session, url, output_dir, min_size_kb=5):
    """단일 이미지 비동기 다운로드"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return None

            data = await response.read()

        # 컨텐츠 타입에서 확장자 결정
        content_type = response.headers.get('content-type', '')
        if 'jpeg' in content_type or 'jpg' in content_type:
            ext = '.jpg'
        elif 'png' in content_type:
            ext = '.png'
        elif 'webp' in content_type:
            ext = '.webp'
        else:
            path_ext = Path(urlparse(url).path).suffix.lower()
            ext = path_ext if path_ext in ['.jpg', '.jpeg', '.png', '.webp'] else '.jpg'

        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        filename = f"img_{url_hash}{ext}"
        filepath = output_dir / filename

        filepath.write_bytes(data)

        file_size_kb = filepath.stat().st_size / 1024
        if file_size_kb < min_size_kb:
            filepath.unlink()
            return None

        return filepath

    except Exception:
        return None


async def download_images_batch(image_list, output_dir):
    """이미지 배치 비동기 다운로드"""
    import aiohttp

    semaphore = asyncio.Semaphore(5)
    results = {}

    async def _download_with_sem(img):
        async with semaphore:
            filepath = await download_image_async(session, img['url'], output_dir)
            if filepath:
                results[img['url']] = filepath
                results[img.get('normalized_url', img['url'])] = filepath

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    connector = aiohttp.TCPConnector(limit=10, ssl=False, force_close=True)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers) as session:
        tasks = [_download_with_sem(img) for img in image_list]
        await asyncio.gather(*tasks, return_exceptions=True)

    return results


# ============================================================
# Gemini OCR
# ============================================================

def analyze_image_with_gemini(image_path):
    """Gemini REST API로 이미지 OCR"""
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()

        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{
                    "parts": [
                        {"text": "이 이미지의 모든 텍스트를 추출하고, 주요 내용을 설명해주세요. 한글로 답변해주세요."},
                        {"inline_data": {"mime_type": mime_type, "data": image_data}}
                    ]
                }]
            },
            timeout=60
        )

        if response.status_code != 200:
            raise Exception(f"API 오류: {response.status_code}")

        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print_color(f"  Gemini 분석 실패: {e}", Colors.YELLOW)
        return None


# ============================================================
# OCR 인라인 자동 삽입 (v3 핵심 신기능)
# ============================================================

def insert_ocr_inline(markdown_text, image_ocr_map):
    """
    markdown에서 이미지 참조를 찾아 바로 아래에 OCR 블록 삽입.

    image_ocr_map: {image_url: ocr_text} (normalized URL 포함)
    """
    lines = markdown_text.split('\n')
    result = []
    matched_urls = set()

    # 정규화된 URL -> OCR 텍스트 매핑도 생성
    normalized_map = {}
    for url, ocr_text in image_ocr_map.items():
        normalized_map[url] = ocr_text
        normalized_map[normalize_url(url)] = ocr_text

    for line in lines:
        result.append(line)

        # 이미지 마크다운 패턴 매칭: ![alt](url)
        img_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if img_match:
            img_url = img_match.group(2)
            img_url_normalized = normalize_url(img_url)

            # OCR 결과 매칭 시도
            ocr_text = normalized_map.get(img_url) or normalized_map.get(img_url_normalized)

            if ocr_text:
                matched_urls.add(img_url)
                matched_urls.add(img_url_normalized)
                result.append('')
                result.append('> **[OCR 추출]**')
                result.append('> ')
                for ocr_line in ocr_text.split('\n'):
                    result.append(f'> {ocr_line}')
                result.append('')

    # 매칭 실패한 OCR 결과는 끝에 추가
    unmatched = []
    seen_unmatched = set()
    for url, ocr_text in image_ocr_map.items():
        norm = normalize_url(url)
        if url not in matched_urls and norm not in matched_urls and norm not in seen_unmatched:
            seen_unmatched.add(norm)
            unmatched.append((url, ocr_text))

    if unmatched:
        result.append('')
        result.append('---')
        result.append('')
        result.append('## 추가 OCR 결과')
        result.append('')
        for i, (url, ocr_text) in enumerate(unmatched, 1):
            result.append(f'### 이미지 {i}')
            result.append(f'**URL**: `{url}`')
            result.append('')
            result.append('> **[OCR 추출]**')
            result.append('> ')
            for ocr_line in ocr_text.split('\n'):
                result.append(f'> {ocr_line}')
            result.append('')

    return '\n'.join(result)


# ============================================================
# 메인 파이프라인
# ============================================================

def process_url(url, output_file=None, wait_for=None, scroll=False,
                max_images=15, no_ocr=False, force_stealth=False):
    """URL 전체 처리 워크플로우 v3.0"""

    print_color(f"\n{'='*80}", Colors.BLUE)
    print_color(f"Web Crawler + OCR v3.0 (Scrapling + trafilatura)", Colors.BLUE)
    print_color(f"{'='*80}\n", Colors.BLUE)

    # 1. HTML 가져오기 (Scrapling 에스컬레이션)
    html_string = fetch_with_scrapling(
        url, escalate=True, wait_for=wait_for,
        scroll=scroll, force_stealth=force_stealth
    )

    if not html_string:
        print_color("크롤링 실패: HTML을 가져올 수 없습니다.", Colors.RED)
        sys.exit(1)

    # 2. 타이틀 추출
    title = extract_title(html_string)
    print_color(f"Title: {title}", Colors.CYAN)

    # 3. trafilatura로 콘텐츠 정제 + markdown 변환
    markdown_text = extract_content(html_string, url)

    if not markdown_text:
        print_color("콘텐츠 추출 실패", Colors.RED)
        sys.exit(1)

    # 4. 이미지 추출 + 필터링
    all_images = []
    seen_normalized = set()

    # markdown에서 이미지 추출
    md_images = extract_images_from_markdown(markdown_text, url)
    for img in md_images:
        if img['normalized_url'] not in seen_normalized:
            seen_normalized.add(img['normalized_url'])
            all_images.append(img)

    # HTML <img> 태그에서 추가 이미지 추출
    html_images = extract_images_from_html(html_string, url)
    for img in html_images:
        if img['normalized_url'] not in seen_normalized:
            seen_normalized.add(img['normalized_url'])
            all_images.append(img)

    # 정규식으로 HTML 전체에서 이미지 URL 추출 (SPA/동적 사이트 fallback)
    regex_images = extract_images_from_regex(html_string, url)
    for img in regex_images:
        if img['normalized_url'] not in seen_normalized:
            seen_normalized.add(img['normalized_url'])
            all_images.append(img)

    print_color(f"총 {len(all_images)}개 이미지 발견 (md:{len(md_images)} html:{len(html_images)} regex:{len(regex_images)})", Colors.CYAN)

    # 필터링
    filtered_images = filter_product_images(all_images, max_images=max_images)
    print_color(f"필터링 후 {len(filtered_images)}개 이미지 OCR 대상", Colors.GREEN)

    # 5. 이미지 다운로드 + OCR
    image_ocr_map = {}  # {url: ocr_text}

    if filtered_images and not no_ocr:
        print_color(f"\n이미지 다운로드 + Gemini OCR 처리 중...", Colors.BLUE)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # 비동기 배치 다운로드
            downloaded = asyncio.run(download_images_batch(filtered_images, temp_path))

            download_count = len(set(
                str(v) for v in downloaded.values()
            ))
            print_color(f"  {download_count}개 이미지 다운로드 완료", Colors.GREEN)

            # OCR 순차 실행 (Gemini 15 RPM 제한)
            processed = set()
            for img in filtered_images:
                filepath = downloaded.get(img['url']) or downloaded.get(img.get('normalized_url'))
                if not filepath or str(filepath) in processed:
                    continue

                processed.add(str(filepath))
                idx = len(image_ocr_map) + 1
                print_color(f"  [{idx}/{download_count}] OCR: {img['url'][:60]}...", Colors.NC)

                analysis = analyze_image_with_gemini(filepath)
                if analysis:
                    image_ocr_map[img['url']] = analysis
                    # normalized URL로도 매핑
                    image_ocr_map[img.get('normalized_url', img['url'])] = analysis
                    print_color(f"    {len(analysis)} chars extracted", Colors.GREEN)

    # 6. OCR 인라인 삽입
    if image_ocr_map:
        print_color("OCR 결과를 이미지 위치에 인라인 삽입 중...", Colors.BLUE)
        markdown_text = insert_ocr_inline(markdown_text, image_ocr_map)

    # 7. 최종 markdown 생성
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    final_markdown = f"""# {title}

> Source: {url}
> Crawled: {timestamp}
> Tool: Scrapling + Gemini OCR v3.0

---

{markdown_text}
"""

    # 8. 파일 저장
    if not output_file:
        domain = urlparse(url).netloc.replace('www.', '')
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"{domain}_{ts}.md"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_markdown, encoding='utf-8')

    print_color(f"\n{'='*80}", Colors.GREEN)
    print_color(f"완료: {output_path.absolute()}", Colors.GREEN)
    print_color(f"{'='*80}\n", Colors.GREEN)

    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Web Crawler + Gemini OCR v3.0 (Scrapling + trafilatura)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 기본 크롤링
  python web-crawler.py https://example.com/article

  # 출력 파일 지정
  python web-crawler.py https://example.com output.md

  # 동적 페이지 (JS 렌더링 대기 3초)
  python web-crawler.py https://spa-site.com --wait 3000

  # 무한 스크롤 페이지
  python web-crawler.py https://infinite-scroll.com --scroll

  # Stealth 모드 강제 사용
  python web-crawler.py https://protected-site.com --stealth

  # OCR 없이 텍스트만
  python web-crawler.py https://example.com --no-ocr
        """
    )

    parser.add_argument('url', help='크롤링할 URL')
    parser.add_argument('output', nargs='?', help='출력 파일 경로 (선택)')
    parser.add_argument('--wait', type=int, help='JS 렌더링 대기 시간 (ms), 예: --wait 3000')
    parser.add_argument('--scroll', action='store_true', help='무한 스크롤 페이지 처리')
    parser.add_argument('--max-images', type=int, default=15, help='최대 OCR 처리 이미지 수 (기본: 15)')
    parser.add_argument('--no-ocr', action='store_true', help='OCR 처리 건너뛰기')
    parser.add_argument('--stealth', action='store_true', help='StealthyFetcher 강제 사용')

    args = parser.parse_args()

    # API 키 확인 (OCR 사용시에만)
    check_api_keys(need_ocr=not args.no_ocr)

    process_url(
        url=args.url,
        output_file=args.output,
        wait_for=args.wait,
        scroll=args.scroll,
        max_images=args.max_images,
        no_ocr=args.no_ocr,
        force_stealth=args.stealth,
    )


if __name__ == "__main__":
    main()
