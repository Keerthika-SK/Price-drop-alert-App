from scrapers import scrape_amazon, scrape_flipkart, scrape_myntra
import time
import random

def main():
    urls = [
        "https://www.flipkart.com/infinix-note-50x-5g-sea-breeze-green-128-gb/p/itm094fc01ad674b",
        "https://www.myntra.com/ethnic-dresses/varicos/varicos-ethnic-motifs-printed-fit--flare-tiered-cotton-maternity-maxi-dress/30403413/buy"
    ]
    
    for url in urls:
        print(f"\nScraping: {url}")
        
        # Random delay to avoid detection
        time.sleep(random.uniform(2, 5))
        
        try:
            if 'flipkart' in url:
                result = scrape_flipkart(url)
            elif 'myntra' in url:
                result = scrape_myntra(url)
            else:
                print(f"No scraper available for: {url}")
                continue
            
            # Handle result properly
            if isinstance(result, dict) and 'status' in result:
                if result['status']:
                    print("Successfully scraped:")
                    print(f"Product: {result['data']['product']}")
                    print(f"Price: {result['data']['price']}")
                    print(f"Image: {result['data']['image_url']}")
                else:
                    print(f"Failed to scrape: {result.get('error', 'Unknown error')}")
            else:
                print("Unexpected result format:", result)
                
        except Exception as e:
            print(f"Unexpected error processing {url}: {str(e)}")

if __name__ == "__main__":
    main()