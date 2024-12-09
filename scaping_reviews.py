# -*- coding: utf-8 -*-
"""scaping-reviews.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HK3TsCIpxfclFmuj6C7b-djbOIeyBtEl
"""

# Install required libraries
!pip install selenium pandas bs4 schedule
!apt-get update -y
!apt-get install -y chromium-chromedriver

# Import necessary modules
import os
import time
import schedule
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')
SAVE_DIRECTORY = "/content/drive/My Drive/Colab Notebooks/Scraped Data/"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# Configure Selenium
def get_webdriver():
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')  # Ensure compatibility in Colab
        return webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
    except Exception as e:
        print(f"Error configuring WebDriver: {e}")
        return None

# Scraping Trustpilot reviews for MyJuniper
def scrape_juniper_reviews():
    print("Scraping reviews for MyJuniper...")
    base_url = "https://au.trustpilot.com/review/myjuniper.com?page="
    reviews = []
    driver = get_webdriver()
    if not driver:
        print("WebDriver failed to initialize.")
        return
    try:
        for page in range(1, 35):  # 34 pages
            url = f"{base_url}{page}"
            driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_elements = soup.find_all('div', class_='styles_reviewContent__0Q2Tg')
            for element in review_elements:
                reviews.append(element.text.strip())
    except Exception as e:
        print(f"Error scraping MyJuniper reviews: {e}")
    finally:
        driver.quit()

    output_file = os.path.join(SAVE_DIRECTORY, "juniper_reviews.csv")
    pd.DataFrame({"Review": reviews}).to_csv(output_file, index=False)
    print(f"MyJuniper reviews saved to {output_file}")

# Scraping Trustpilot reviews for GetMosh
def scrape_getmosh_reviews():
    print("Scraping reviews for GetMosh...")
    base_url = "https://www.trustpilot.com/review/getmosh.com.au?page="
    reviews = []
    driver = get_webdriver()
    if not driver:
        print("WebDriver failed to initialize.")
        return
    try:
        for page in range(1, 11):  # 10 pages
            url = f"{base_url}{page}"
            driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_elements = soup.find_all('div', class_='styles_reviewContent__0Q2Tg')
            for element in review_elements:
                reviews.append(element.text.strip())
    except Exception as e:
        print(f"Error scraping GetMosh reviews: {e}")
    finally:
        driver.quit()

    output_file = os.path.join(SAVE_DIRECTORY, "getmosh_reviews.csv")
    pd.DataFrame({"Review": reviews}).to_csv(output_file, index=False)
    print(f"GetMosh reviews saved to {output_file}")

# Scraping Facebook data
def scrape_facebook_data():
    print("Scraping Facebook data...")
    pages = {
        "Youly": "https://www.facebook.com/youlyau",
        "GetMosh": "https://www.facebook.com/moshy.health",
        "MyJuniper": "https://www.facebook.com/profile.php?id=100076447984459",
    }
    data = []
    for name, url in pages.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            likes = soup.find(string=lambda x: x and "like this" in x.lower())
            followers = soup.find(string=lambda x: x and "follow this" in x.lower())
            data.append({"Page Name": name, "URL": url, "Likes": likes or "N/A", "Followers": followers or "N/A"})
        except Exception as e:
            print(f"Error scraping Facebook data for {name}: {e}")
            data.append({"Page Name": name, "URL": url, "Likes": "N/A", "Followers": "N/A"})

    output_file = os.path.join(SAVE_DIRECTORY, "facebook_data.csv")
    pd.DataFrame(data).to_csv(output_file, index=False)
    print(f"Facebook data saved to {output_file}")

# Scraping Instagram data
def scrape_instagram_data():
    print("Scraping Instagram data...")
    pages = {
        "MyJuniper": "https://www.instagram.com/my.juniper?igsh=MWxiOGZuamlrdHRwdQ==",
        "GetMosh": "https://www.instagram.com/moshyhealth?igsh=dGg5dHMxZThtOGFw",
    }
    data = []
    driver = get_webdriver()
    if not driver:
        print("WebDriver failed to initialize.")
        return
    try:
        for name, url in pages.items():
            driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            followers = soup.find('span', {'class': 'g47SY'}).text
            data.append({"Page Name": name, "URL": url, "Followers": followers})
    except Exception as e:
        print(f"Error scraping Instagram data for {name}: {e}")
        data.append({"Page Name": name, "URL": url, "Followers": "N/A"})
    finally:
        driver.quit()

    output_file = os.path.join(SAVE_DIRECTORY, "instagram_data.csv")
    pd.DataFrame(data).to_csv(output_file, index=False)
    print(f"Instagram data saved to {output_file}")

# Main function to run all scrapers
def run_all_scrapers():
    print("Starting all scraping tasks...")
    scrape_juniper_reviews()
    scrape_getmosh_reviews()
    scrape_facebook_data()
    scrape_instagram_data()
    print("All scraping tasks completed successfully.")

# Scheduler function
def schedule_scraping():
    schedule.every(24).hours.do(run_all_scrapers)
    print("Scheduler started. Scraping tasks will run every 24 hours.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run scheduler
if __name__ == "__main__":
    run_all_scrapers()  # First-time execution
    schedule_scraping()