import os
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from google.colab import drive
from datetime import datetime

# Mount Google Drive
drive.mount('/content/drive')

# Define the URLs to scrape
urls = [
    "https://youly.com.au/treatment/weight-loss/",
    "https://www.myjuniper.com/program",
    "https://www.getmoshy.com.au/weight-loss"
]

# Function to scrape price and money-back guarantee from a URL
def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract price (modify these selectors based on the website's HTML structure)
        price = soup.find(string=lambda t: "price" in t.lower() if t else False)
        if price:
            price = price.strip()
        else:
            price = "Not found"

        # Extract money-back guarantee (modify these selectors based on the website's HTML structure)
        guarantee = soup.find(string=lambda t: "money-back" in t.lower() if t else False)
        if guarantee:
            guarantee = guarantee.strip()
        else:
            guarantee = "Not found"

        return {"URL": url, "Price": price, "Money-Back Guarantee": guarantee}

    except Exception as e:
        return {"URL": url, "Price": "Error", "Money-Back Guarantee": "Error", "Error": str(e)}

# Main function to run the scraper and save the data
def run_scraper():
    data = []
    for url in urls:
        print(f"Scraping {url}...")
        data.append(scrape_data(url))

    # Save data to CSV
    df = pd.DataFrame(data)
    file_path = '/content/drive/My Drive/scraped_data.csv'  # Fixed file path
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

# Start the scraper manually
run_scraper()
