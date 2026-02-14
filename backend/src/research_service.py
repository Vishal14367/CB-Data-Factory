
import logging
import json
import hashlib
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import feedparser
from pytrends.request import TrendReq
from duckduckgo_search import DDGS
from tavily import TavilyClient

from config import (
    NEWSDATA_API_KEY, NEWSAPI_KEY, TAVILY_API_KEY, 
    BASE_DIR
)
from models import ResearchSource

logger = logging.getLogger(__name__)

CACHE_DIR = BASE_DIR / "cache" / "research"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_VALIDITY_HOURS = 24

class ResearchFetcher(ABC):
    """Abstract base class for research fetchers."""
    
    @abstractmethod
    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class NewsDataFetcher(ResearchFetcher):
    """Fetcher for NewsData.io API."""
    
    def name(self) -> str:
        return "NewsData.io"

    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_API_KEY,
            "q": f"{domain} {function}",
            "language": "en",
            "prioritydomain": "top"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                sources = []
                for result in data.get("results", [])[:3]:
                    sources.append(ResearchSource(
                        title=result.get("title", ""),
                        url=result.get("link", ""),
                        relevance="high",
                        key_insights=[result.get("description", "")[:200] + "..."],
                        publication_date=result.get("pubDate")
                    ))
                return sources
            else:
                logger.warning(f"NewsData API error: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"NewsData fetch failed: {e}")
            return []


class NewsAPIFetcher(ResearchFetcher):
    """Fetcher for NewsAPI.org."""
    
    def name(self) -> str:
        return "NewsAPI.org"

    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": f"{domain} AND {function}",
            "sortBy": "relevance",
            "language": "en",
            "pageSize": 3
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                sources = []
                for article in data.get("articles", []):
                    sources.append(ResearchSource(
                        title=article.get("title", ""),
                        url=article.get("url", ""),
                        relevance="high",
                        key_insights=[article.get("description", "")[:200] + "..."],
                        publication_date=article.get("publishedAt")
                    ))
                return sources
            return []
        except Exception as e:
            logger.error(f"NewsAPI fetch failed: {e}")
            return []


class GoogleTrendsFetcher(ResearchFetcher):
    """Fetcher for Google Trends (via pytrends)."""
    
    def name(self) -> str:
        return "Google Trends"

    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        try:
            pytrends = TrendReq(hl='en-US', tz=360)
            kw_list = [domain]
            pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
            related_queries = pytrends.related_queries()
            
            check_key = domain
            if check_key not in related_queries:
                 # Fallback if the exact key mismatch
                 keys = list(related_queries.keys())
                 if keys:
                     check_key = keys[0]
                 else:
                     return []

            top_queries = related_queries[check_key]['top']
            
            if top_queries is not None and not top_queries.empty:
                insights = top_queries.head(5)['query'].tolist()
                return [ResearchSource(
                    title=f"Google Trends: {domain}",
                    url="https://trends.google.com/",
                    relevance="medium",
                    key_insights=[f"Trending topic: {q}" for q in insights],
                    publication_date=datetime.now().isoformat()
                )]
            return []
        except Exception as e:
            logger.error(f"Google Trends fetch failed: {e}")
            # Rate limits are common with pytrends, return empty gracefully
            return []


class MediumRSSFetcher(ResearchFetcher):
    """Fetcher for Medium RSS feeds."""
    
    def name(self) -> str:
        return "Medium RSS"

    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        # Clean domain for tag usage (e.g. "E-Commerce" -> "ecommerce")
        tag = domain.lower().replace(" ", "").replace("-", "")
        url = f"https://medium.com/feed/tag/{tag}"
        
        try:
            feed = feedparser.parse(url)
            sources = []
            for entry in feed.entries[:3]:
                # Extract text from summary (strip HTML tags broadly or just take raw)
                summary = entry.summary if 'summary' in entry else ""
                # Simple cleanup
                text_content = summary.replace("<p>", "").replace("</p>", "")[:200]
                
                sources.append(ResearchSource(
                    title=entry.title,
                    url=entry.link,
                    relevance="medium",
                    key_insights=[text_content + "..."],
                    publication_date=entry.get("published")
                ))
            return sources
        except Exception as e:
            logger.error(f"Medium fetch failed: {e}")
            return []


class DuckDuckGoFetcher(ResearchFetcher):
    """Fetcher for DuckDuckGo Search."""
    
    def name(self) -> str:
        return "DuckDuckGo"

    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        try:
            results = DDGS().text(f"{domain} industry {function} trends 2024 2025", max_results=3)
            sources = []
            for r in results:
                sources.append(ResearchSource(
                    title=r.get("title", ""),
                    url=r.get("href", ""),
                    relevance="high",
                    key_insights=[r.get("body", "")[:200] + "..."],
                    publication_date=None
                ))
            return sources
        except Exception as e:
            logger.error(f"DuckDuckGo fetch failed: {e}")
            return []


class TavilyFetcher(ResearchFetcher):
    """Fetcher for Tavily AI."""
    
    def name(self) -> str:
        return "Tavily AI"

    def fetch(self, domain: str, function: str) -> List[ResearchSource]:
        if not TAVILY_API_KEY:
            return []
            
        try:
            client = TavilyClient(api_key=TAVILY_API_KEY)
            response = client.search(
                query=f"latest {domain} industry challenges and KPIs for {function} 2024 2025",
                search_depth="advanced",
                max_results=3
            )
            
            sources = []
            for result in response.get("results", []):
                sources.append(ResearchSource(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    relevance="high",
                    key_insights=[result.get("content", "")[:300] + "..."],
                    publication_date=None
                ))
            return sources
        except Exception as e:
            logger.error(f"Tavily fetch failed: {e}")
            return []


class CacheManager:
    """Manages file-based caching for research results."""
    
    @staticmethod
    def _get_cache_key(domain: str, function: str) -> str:
        key_str = f"{domain.lower()}_{function.lower()}"
        return hashlib.md5(key_str.encode()).hexdigest()

    @staticmethod
    def get_cached_result(domain: str, function: str) -> Optional[List[Dict]]:
        key = CacheManager._get_cache_key(domain, function)
        cache_file = CACHE_DIR / f"{key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                
                cached_time = datetime.fromisoformat(data["timestamp"])
                if datetime.now() - cached_time < timedelta(hours=CACHE_VALIDITY_HOURS):
                    logger.info(f"Cache hit for {domain} - {function}")
                    return data["results"]
            except Exception as e:
                logger.warning(f"Cache read failed: {e}")
                
        return None

    @staticmethod
    def save_to_cache(domain: str, function: str, results: List[ResearchSource]):
        key = CacheManager._get_cache_key(domain, function)
        cache_file = CACHE_DIR / f"{key}.json"
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "results": [r.model_dump() for r in results]
            }
            with open(cache_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved results to cache: {cache_file}")
        except Exception as e:
            logger.error(f"Cache save failed: {e}")


class ResearchAggregator:
    """Aggregates research from multiple sources in parallel."""
    
    def __init__(self):
        self.fetchers = [
            NewsDataFetcher(),
            NewsAPIFetcher(),
            GoogleTrendsFetcher(),
            MediumRSSFetcher(),
            DuckDuckGoFetcher(),
            TavilyFetcher()
        ]

    def aggregate_research(self, domain: str, function: str) -> List[ResearchSource]:
        """Fetch research from all sources with caching and parallelism."""
        
        # Check cache first
        cached_data = CacheManager.get_cached_result(domain, function)
        if cached_data:
            return [ResearchSource(**item) for item in cached_data]

        logger.info(f"Starting parallel research for {domain} - {function}")
        all_sources = []
        
        with ThreadPoolExecutor(max_workers=len(self.fetchers)) as executor:
            future_to_fetcher = {
                executor.submit(fetcher.fetch, domain, function): fetcher 
                for fetcher in self.fetchers
            }
            
            for future in as_completed(future_to_fetcher):
                fetcher = future_to_fetcher[future]
                try:
                    sources = future.result()
                    logger.info(f"{fetcher.name()} returned {len(sources)} sources")
                    all_sources.extend(sources)
                except Exception as e:
                    logger.error(f"{fetcher.name()} failed: {e}")

        # Deduplicate by URL
        unique_sources = {}
        for source in all_sources:
            if source.url and source.url not in unique_sources:
                unique_sources[source.url] = source
        
        results = list(unique_sources.values())
        
        # Select Primary Case Study (Simulated Logic)
        if results:
            # Prioritize Tavily or highly relevant sources
            primary_set = False
            for source in results:
                if "tavily" in source.url.lower() or "newsdata" in source.url.lower():
                    source.is_primary = True
                    primary_set = True
                    break
            
            if not primary_set:
                results[0].is_primary = True

        # Save to cache
        if results:
            CacheManager.save_to_cache(domain, function, results)
            
        return results
