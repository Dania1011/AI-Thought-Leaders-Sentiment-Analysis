import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # run browser in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Target URL (Quotes website with pagination)
base_url = "https://quotes.toscrape.com/js/"

# Storage for scraped data
all_quotes = []

try:
    driver.get(base_url)
    time.sleep(2)

    while True:
        # Extract quotes on current page
        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        for quote in quotes:
            try:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
                all_quotes.append({"text": text, "author": author, "tags": ", ".join(tags)})
            except Exception as e:
                print("⚠️ Skipped a quote due to:", e)
                continue

        # Check for "Next" button (pagination)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
            next_button.click()
            time.sleep(2)
        except Exception:
            print("✅ No more pages left — scraping complete!")
            break

except Exception as e:
    print("❌ Error during scraping:", e)

finally:
    driver.quit()

# Save results to CSV
df = pd.DataFrame(all_quotes)
output_path = "data/processed/dynamic_quotes_pagination.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
print(f"✅ Scraping complete! Data saved to: {output_path}")
