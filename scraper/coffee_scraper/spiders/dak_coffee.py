import scrapy
import re

class DakCoffeeSpider(scrapy.Spider):
    name = "dak_coffee"
    allowed_domains = ["dakcoffeeroasters.com"]
    start_urls = ["https://www.dakcoffeeroasters.com/shop"]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse_shop,
                meta={
                    "zyte_api": {
                        "browserHtml": True
                    }
                },
            )

    def slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text

    # ----------------------------
    # Shop page → product URLs
    # ----------------------------
    def parse_shop(self, response):
        product_nodes = response.css("div.snipcart-add-item")

        for node in product_nodes:
            full_name = node.attrib.get("data-item-name")
            if not full_name:
                continue

            coffee_name = full_name.split(" - ", 1)[0].strip()
            slug = self.slugify(coffee_name)
            product_url = f"https://www.dakcoffeeroasters.com/shop/coffee/{slug}"

            yield scrapy.Request(
                product_url,
                callback=self.parse_product,
                meta={
                    "zyte_api": {
                        "browserHtml": True,
                        "pageContent": True,
                        "pageContentOptions": {
                            "extractFrom": "browserHtml"
                        }
                    }
                },
                cb_kwargs={
                    "product_url": product_url
                },
            )

    # ----------------------------
    # Product page → Zyte Auto Extract
    # ----------------------------
    def parse_product(self, response, product_url):
        api_response = response.raw_api_response or {}
        page_content = api_response.get("pageContent", {})
        item_main = page_content.get("itemMain")

        yield {
            "product_url": product_url,
            "item_main": item_main,
        }
