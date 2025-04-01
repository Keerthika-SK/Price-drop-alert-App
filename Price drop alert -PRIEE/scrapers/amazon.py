from database.db import EcomDB
from playwright.sync_api import sync_playwright

def scrape_amazon(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=60000)
            
            # More specific selector for product title
            product_name = page.locator("span#productTitle.a-size-large").first.inner_text().strip()
            
            # More robust price detection
            price = "Not found"
            price_elements = page.locator("span.a-price-whole").all()
            if price_elements:
                price = price_elements[0].inner_text().strip()
            
            # Image handling
            image_url = ""
            img_element = page.locator("#landingImage").first
            if img_element:
                image_url = img_element.get_attribute("src")
            
            # Database storage
            db = EcomDB()
            success = db.insert_product(
                site="amazon",
                product_name=product_name,
                price=price,
                image_url=image_url,
                product_url=url
            )
            
            return {
                "status": success,
                "data": {
                    "product": product_name,
                    "price": price,
                    "image_url": image_url
                }
            }
        except Exception as e:
            return {
                "status": False,
                "error": str(e),
                "url": url
            }
        finally:
            browser.close()