import asyncio
from fetcher import Fetcher
from parser import Parser

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

async def main():
    fetcher = Fetcher()
    parser = Parser()
    
    html = await fetcher.fetch(url)
    if not html:
        print("Failed to fetch page")
        return

    data = parser.parse_book_details(html)

    print("Parsed Data:")
    for key, value in data.items():
        print(f"{key}: {value}")

asyncio.run(main())