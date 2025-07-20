import aiohttp
import asyncio
from newspaper import Article
from app.config import NEWS_SITES
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_article(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                article = Article(url)
                article.set_html(html)
                article.parse()
                return {
                    'title': article.title,
                    'text': article.text,
                    'date': article.publish_date or datetime.now(),
                    'url': url,
                    'source': url.split('/')[2]
                }
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

async def scrape_site(session, site, semaphore):
    async with semaphore:
        try:
            async with session.get(site, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
                    tasks = []
                    for link in links[:10]:  # Limit to 10 articles per site
                        tasks.append(fetch_article(session, link))
                        await asyncio.sleep(1)  # Rate limiting
                    articles = await asyncio.gather(*tasks, return_exceptions=True)
                    return [a for a in articles if a]
        except Exception as e:
            logger.error(f"Error scraping {site}: {e}")
            return []

async def scrape_articles():
    semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_site(session, site, semaphore) for site in NEWS_SITES]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        articles = []
        for result in results:
            if isinstance(result, list):
                articles.extend(result)
        return articles

def run_scraper():
    return asyncio.run(scrape_articles())
