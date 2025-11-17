from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

def scrape_infinite_scroll():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://quotes.toscrape.com/scroll")  # Demo page for infinite scroll
    time.sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")
    quotes_data = []

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("✅ No more content to load — infinite scroll complete!")
            break
        last_height = new_height

    # Extract all loaded quotes
    quotes = driver.find_elements(By.CLASS_NAME, "quote")
    for quote in quotes:
        try:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
            quotes_data.append({"text": text, "author": author, "tags": ", ".join(tags)})
        except Exception as e:
            print(f"⚠️ Skipped one quote due to error: {e}")

    driver.quit()

    # Save results
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "infinite_scroll_quotes.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(quotes_data)

    print(f"✅ Infinite scroll scraping complete! Data saved to: {output_path}")

if __name__ == "__main__":
    scrape_infinite_scroll()
