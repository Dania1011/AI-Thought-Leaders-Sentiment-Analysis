from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json
from datetime import datetime, timedelta
import hashlib
import re
from langdetect import detect

# ---------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------

def hash_username(username):
    return hashlib.sha256(username.encode()).hexdigest()[:16]

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def parse_date(date_str):
    try:
        if "·" in date_str:
            date_part = date_str.split("·")[0].strip()
            time_part = date_str.split("·")[1].strip().replace(" UTC", "")
            full = f"{date_part} {time_part}"
            return datetime.strptime(full, "%b %d, %Y %I:%M %p")

        now = datetime.now()

        if "ago" in date_str:
            if "h ago" in date_str:
                return now - timedelta(hours=int(date_str.split("h")[0]))
            elif "m ago" in date_str:
                return now - timedelta(minutes=int(date_str.split("m")[0]))
            elif "d ago" in date_str:
                return now - timedelta(days=int(date_str.split("d")[0]))

        if "," in date_str:
            return datetime.strptime(date_str, "%b %d, %Y")

        date = datetime.strptime(date_str, "%b %d")
        result = date.replace(year=now.year)
        if result > now:
            result = result.replace(year=now.year - 1)
        return result
    except:
        return datetime.now()

def extract_tweet_id(url):
    match = re.search(r"/status/(\d+)", url)
    return match.group(1) if match else None

# ---------------------------------------
# PROFILE SCRAPER
# ---------------------------------------

def scrape_profile_info(driver, username):
    """Scrape profile header info from Nitter"""
    url = f"https://nitter.net/{username}"
    driver.get(url)
    time.sleep(4)

    profile = {
        "profile_name": "",
        "username": username,
        "bio": "",
        "location": "",
        "website": "",
        "join_date": "",
        "followers_count": 0,
        "following_count": 0,
        "tweets_count": 0,
        "profile_image_url": ""
    }

    try:
        profile["profile_name"] = driver.find_element(By.CSS_SELECTOR, ".profile-card-fullname").text
    except:
        pass

    try:
        bio_elem = driver.find_element(By.CSS_SELECTOR, ".profile-bio")
        profile["bio"] = bio_elem.text.strip()
    except:
        pass

    try:
        join_date = driver.find_element(By.CSS_SELECTOR, ".profile-join-date").text
        profile["join_date"] = join_date.replace("Joined", "").strip()
    except:
        pass

    try:
        loc = driver.find_element(By.CSS_SELECTOR, ".profile-location").text
        profile["location"] = loc.strip()
    except:
        pass

    try:
        website = driver.find_element(By.CSS_SELECTOR, ".profile-website a")
        profile["website"] = website.get_attribute("href")
    except:
        pass

    # Counts
    try:
        stats = driver.find_elements(By.CSS_SELECTOR, ".profile-stat-num")
        if len(stats) >= 3:
            profile["tweets_count"] = int(stats[2].text.replace(",", ""))
            profile["followers_count"] = int(stats[1].text.replace(",", ""))
            profile["following_count"] = int(stats[0].text.replace(",", ""))
    except:
        pass

    try:
        img = driver.find_element(By.CSS_SELECTOR, ".profile-card-avatar img")
        profile["profile_image_url"] = img.get_attribute("src")
    except:
        pass

    return profile

# ---------------------------------------
# TWEET SCRAPER
# ---------------------------------------

def scrape_x_posts(username, num_scrolls=5, tweet_type='original'):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    posts = []
    seen = set()

    try:
        # ✔️ FIRST: SCRAPE PROFILE
        profile = scrape_profile_info(driver, username)

        # ✔️ THEN LOAD TWEETS
        driver.get(f"https://nitter.net/{username}")
        time.sleep(4)

        scrolls = 0

        while scrolls < num_scrolls:
            tweet_cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".timeline-item"))
            )

            for card in tweet_cards:
                try:
                    # Tweet URL / ID
                    date_elem = card.find_element(By.CSS_SELECTOR, ".tweet-date a")
                    tweet_url = date_elem.get_attribute("href")
                    tweet_id = extract_tweet_id(tweet_url)
                    if not tweet_id or tweet_id in seen:
                        continue
                    seen.add(tweet_id)

                    # Basic text
                    text = card.find_element(By.CSS_SELECTOR, ".tweet-content").text.strip()

                    # Date
                    date_title = date_elem.get_attribute("title")
                    parsed = parse_date(date_title)

                    # Engagement
                    def get_stat(css):
                        try:
                            el = card.find_element(By.CSS_SELECTOR, css).find_element(By.XPATH, "..")
                            t = el.text.strip().lower()
                            if "k" in t:
                                return int(float(t.replace("k", "")) * 1000)
                            elif "m" in t:
                                return int(float(t.replace("m", "")) * 1_000_000)
                            return int(''.join(filter(str.isdigit, t)))
                        except:
                            return 0

                    stats = {
                        "comment_count": get_stat(".icon-comment"),
                        "retweet_count": get_stat(".icon-retweet"),
                        "like_count": get_stat(".icon-heart"),
                    }

                    # Tweet object
                    obj = {
                        **profile,  # ⬅️ ADD PROFILE FIELDS HERE
                        "tweet_id": tweet_id,
                        "text": text,
                        "created_at": parsed.strftime('%Y-%m-%d %H:%M:%S'),
                        "lang": detect_language(text),
                        "user_id_hashed": hash_username(username),
                        "comment_count": stats["comment_count"],
                        "retweet_count": stats["retweet_count"],
                        "like_count": stats["like_count"],
                        "is_reply": bool(card.find_elements(By.CSS_SELECTOR, ".replying-to")),
                        "is_retweet": bool(card.find_elements(By.CSS_SELECTOR, ".retweet-header")),
                        "is_quote": bool(card.find_elements(By.CSS_SELECTOR, ".quote")),
                        "urls": []
                    }

                    posts.append(obj)

                except:
                    continue

            # Scroll or click load more
            try:
                load_more = driver.find_element(By.XPATH, "//a[contains(text(),'Load more')]")
                driver.execute_script("arguments[0].scrollIntoView();", load_more)
                load_more.click()
                time.sleep(3)
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            scrolls += 1

        return posts

    finally:
        driver.quit()

# ---------------------------------------
# EXPORT TO CSV
# ---------------------------------------

def export_to_csv(tweets, username):
    filename = f"{username}_tweets.csv"

    if not tweets:
        print("No tweets scraped.")
        return

    fieldnames = list(tweets[0].keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in tweets:
            t["urls"] = json.dumps(t["urls"])
            writer.writerow(t)

    print(f"\nSaved to {filename}")

# ---------------------------------------
# MAIN
# ---------------------------------------

if __name__ == "__main__":
    user = input("Enter username to scrape: ").strip()
    tweet_type = input("Choose tweet type ('original','original_and_quotes','all'): ").strip()

    tweets = scrape_x_posts(user, num_scrolls=25, tweet_type=tweet_type)
    export_to_csv(tweets, user)
