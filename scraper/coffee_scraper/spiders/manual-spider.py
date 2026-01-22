import scrapy
import re


class DakCoffeeSpider(scrapy.Spider):
    name = "manual"
    allowed_domains = ["dakcoffeeroasters.com"]
    start_urls = ["https://www.dakcoffeeroasters.com/shop"]

    MAX_PRODUCTS = 50

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"zyte_api": {"browserHtml": True}},
            )

    def slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text

    def parse(self, response):
        nodes = response.xpath(
            "//main//*[self::h1 or contains(@class,'snipcart-add-item')]"
        )

        current_roast_type = None
        count = 0

        for node in nodes:
            tag = node.root.tag

            if tag == "h1":
                header = node.xpath("normalize-space()").get()
                if header in {"Espresso", "Filter"}:
                    current_roast_type = header
                continue

            full_name = node.attrib.get("data-item-name")
            if not full_name:
                continue

            parts = [p.strip() for p in full_name.split(" - ", 1)]
            coffee_name = parts[0]
            origin = parts[1] if len(parts) > 1 else None

            slug = self.slugify(coffee_name)
            product_url = f"https://www.dakcoffeeroasters.com/shop/coffee/{slug}"

            yield scrapy.Request(
                product_url,
                callback=self.parse_product,
                meta={"zyte_api": {"browserHtml": True}},
                cb_kwargs={
                    "item": {
                        "coffee_name": coffee_name,
                        "origin": origin,
                        "roast_type": current_roast_type,
                        "url": product_url,
                    }
                },
            )

            count += 1
            if count >= self.MAX_PRODUCTS:
                break

    def parse_product(self, response, item):
        # ---------- ALTITUDE ----------
        altitude_m = None
        altitude_text = response.xpath(
            "//span[contains(normalize-space(),'Altitude')]/text()"
        ).get()

        if altitude_text:
            match = re.search(r"(\d{3,4})", altitude_text)
            if match:
                altitude_m = int(match.group(1))

        # ---------- PROCESSING METHOD ----------
        processing_method = None

        processing_text = response.xpath(
            "//span[contains(normalize-space(),'Altitude')]/preceding::span[1]/text()"
        ).get()

        if processing_text:
            processing_method = processing_text.strip()

        item["altitude_m"] = altitude_m
        item["processing_method"] = processing_method

        yield item

