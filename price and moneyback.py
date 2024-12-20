# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from google.colab import drive
from datetime import datetime
import time

# Mount Google Drive
try:
    drive.mount('/content/drive', force_remount=True)
except Exception as e:
    print(f"Error mounting Google Drive: {e}")
    raise

# Define the function to scrape data
def scrape_data():
    # URLs to scrape
    urls = [
        "https://www.myjuniper.com/program",
        "https://www.getmoshy.com.au/weight-loss"
    ]

    # List to store scraped data
    data = []

    for url in urls:
        try:
            # Make a GET request
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Debug: Print raw HTML for inspection
            print(f"HTML content for {url}:
", soup.prettify())

            # Extract required information (customize as needed)
            if "myjuniper" in url:
                price = soup.select_one('.price')
                guarantee = soup.select_one('.guarantee')
                price = price.text.strip() if price else "N/A"
                guarantee = guarantee.text.strip() if guarantee else "N/A"
            elif "getmoshy" in url:
                price = soup.select_one('.price')
                guarantee = soup.select_one('.guarantee')
                price = price.text.strip() if price else "N/A"
                guarantee = guarantee.text.strip() if guarantee else "N/A"

            # Append the data
            data.append({
                'URL': url,
                'Price': price,
                'Money-Back Guarantee': guarantee,
                'Scraped At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Define the path to save the file on Google Drive
    output_path = '/content/drive/My Drive/scraped_data.csv'

    # Save the data to CSV
    if os.path.exists(output_path):
        df.to_csv(output_path, mode='a', header=False, index=False)  # Append mode
    else:
        df.to_csv(output_path, index=False)  # Create new file

    print(f"Data saved to {output_path}")

# Schedule the scraping to run every 24 hours
while True:
    scrape_data()
    print("Scraping completed. Sleeping for 24 hours.")
    time.sleep(86400)  # Sleep for 24 hours