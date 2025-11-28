import aiohttp
import asyncio
from loguru import logger

class Fetcher:
    def __init__(self, max_retries: int = 3, timeout: int = 10):
        self.max_retries = max_retries
        self.timeout = timeout
        
    async def fetch(self, url:str) -> str:
        for attempt in range(1, self.max_retries + 1):
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        html = await response.text()
                        return html
                    
            except Exception as e:
                logger.error(f"[Attempt {attempt}] failed to fetch {url}: {e}")
                await asyncio.sleep(1* attempt)
                
        logger.error(f"Failed after {self.max_retries} attempt -> {url}")
        return None