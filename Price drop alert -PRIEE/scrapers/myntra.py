from database.db import EcomDB
from playwright.sync_api import sync_playwright
import re
import time

def scrape_myntra(url):
    with sync_playwright() as p:
        # Configure browser with retry options
        browser = p.chromium.launch(
            headless=False,  # Set to True after testing
            channel="chrome",
            args=["--disable-http2"]  # Fix HTTP/2 error
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        page = context.new_page()
        
        try:
            # Navigate with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    page.goto(url, timeout=90000, wait_until="networkidle")
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(2)
            
            # Wait for critical elements
            page.wait_for_selector("h1.pdp-name", timeout=15000)
            
            # Product name with fallback
            try:
                product_name = page.locator("h1.pdp-name").inner_text()
            except:
                product_name = page.locator("h1").inner_text()
            
            # Price with fallback
            try:
                price = page.locator("span.pdp-price strong").inner_text()
            except:
                price = page.locator("span.pdp-price").inner_text()
            
            # Image extraction from background style
            try:
                image_container = page.locator("div.image-grid-image").first
                style = image_container.get_attribute("style")
                image_url = re.search(r'url\("?(.*?)"?\)', style).group(1)
            except:
                image_url = page.locator("img.img-responsive").first.get_attribute("src")
            
            # Store in database
            db = EcomDB()
            db.insert_product(
                site="myntra",
                product_name=product_name.strip(),
                price=price.strip(),
                image_url=image_url,
                product_url=url
            )
            
            return {
                "status": True,
                "data": {
                    "product": product_name.strip(),
                    "price": price.strip(),
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