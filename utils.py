import httpx
from bs4 import BeautifulSoup
from typing import List, Dict

def _fetch_html(query: str) -> str:
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = httpx.get(url, params=params, headers=headers, timeout=15.0, follow_redirects=True)
    resp.raise_for_status()
    return resp.text

def _parse_results(html: str, max_results: int = 5) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    results: List[Dict[str, str]] = []
    for r in soup.select("div.result")[:max_results]:
        a = r.select_one("a.result__a")
        if not a:
            continue
        snippet_tag = r.select_one("a.result__snippet") or r.select_one("div.result__snippet")
        results.append({
            "title": a.get_text(strip=True),
            "href": a.get("href", ""),
            "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
        })
    return results

def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    html = _fetch_html(query)
    return _parse_results(html, max_results=max_results)
