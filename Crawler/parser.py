from bs4 import BeautifulSoup
from loguru import logger

class Parser:
    def parse_book_details(self, html: str) -> dict:

        try:
            soup = BeautifulSoup(html, "lxml")
            #title
            title = soup.find("h1").text.strip() if soup.find("h1") else None

            # Product description
            desc_tag = soup.find("div", id="product_description")
            description = None
            if desc_tag:
                next_p = desc_tag.find_next("p")
                description = next_p.text.strip() if next_p else None

            # Category
            category_tag = soup.select_one("ul.breadcrumb li:nth-of-type(3) a")
            category = category_tag.text.strip() if category_tag else None

            # Image
            img_tag = soup.find("img")
            image_url = img_tag["src"] if img_tag else None

            # Rating (stored in class attribute)
            rating_tag = soup.find("p", class_="star-rating")
            rating = None
            if rating_tag:
                rating_classes = rating_tag.get("class", [])
                for name in ["One", "Two", "Three", "Four", "Five"]:
                    if name in rating_classes:
                        rating = name

            # Table fields (price, availability, reviews)
            table = soup.find("table", class_="table table-striped")
            rows = {row.th.text.strip(): row.td.text.strip() for row in table.find_all("tr")} if table else {}

            price_excl_tax = rows.get("Price (excl. tax)")
            price_incl_tax = rows.get("Price (incl. tax)")
            availability = rows.get("Availability")
            num_reviews = rows.get("Number of reviews")

            return {
                "title": title,
                "description": description,
                "category": category,
                "image_url": image_url,
                "rating": rating,
                "price_excl_tax": price_excl_tax,
                "price_incl_tax": price_incl_tax,
                "availability": availability,
                "num_reviews": num_reviews,
            }

        except Exception as e:
            logger.error(f"Failed to parse book page: {e}")
            return None
        

    def extract_book_links(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        links = []

        products = soup.select("article.product_pod h3 a")

        for tag in products:
            relative = tag.get("href")

    
            # relative = relative.replace("../../../", "")

            full_url = f"https://books.toscrape.com/catalogue/{relative}"
            links.append(full_url)

        return links

