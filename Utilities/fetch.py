from Crawler.fetcher import Fetcher

# one general fetcher
_fetcher = Fetcher()

async def fetch(url: str):
    return await _fetcher.fetch(url)
