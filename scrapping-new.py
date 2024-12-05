# Import necessary libraries
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from google.colab import drive

# Mount Google Drive to save the output CSV file
drive.mount('/content/drive')

# Define the directory where the CSV file will be saved
SAVE_DIRECTORY = "/content/drive/My Drive/Colab Notebooks/Scraped Data"
OUTPUT_FILE = os.path.join(SAVE_DIRECTORY, "juniper_vs_moshy_data.csv")

# Function to scrape Trustpilot reviews
def scrape_trustpilot_reviews():
    url = "https://au.trustpilot.com/review/myjuniper.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    reviews = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate review sections
        review_sections = soup.find_all('div', class_='styles_reviewContent__0Q2Tg')
        for section in review_sections:
            review_text = section.find('p').text.strip()
            if "weight loss" in review_text.lower():
                reviews.append(review_text)
    except Exception as e:
        print(f"Error scraping Trustpilot: {e}")
    return reviews

# Function to scrape details from Get Moshy
def scrape_getmoshy_details():
    url = "https://www.getmoshy.com.au/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    data = {"Money Back Guarantee": "", "Price": ""}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant information
        guarantee_section = soup.find(string=lambda t: t and "money back" in t.lower())
        if guarantee_section:
            data["Money Back Guarantee"] = guarantee_section.strip()
        
        price_section = soup.find(string=lambda t: t and "price" in t.lower())
        if price_section:
            data["Price"] = price_section.strip()
    except Exception as e:
        print(f"Error scraping Get Moshy: {e}")
    return data

# Function to scrape details from Youly
def scrape_youly_details():
    url = "https://youly.com.au/treatment/weight-loss/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    reviews = []
    data = {"Money Back Guarantee": "", "Price": ""}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract reviews related to weight loss
        review_sections = soup.find_all('div', class_='review-text')
        for section in review_sections:
            review_text = section.text.strip()
            if "weight loss" in review_text.lower():
                reviews.append(review_text)
        
        # Extract guarantee and price
        guarantee_section = soup.find(string=lambda t: t and "money back" in t.lower())
        if guarantee_section:
            data["Money Back Guarantee"] = guarantee_section.strip()
        
        price_section = soup.find(string=lambda t: t and "price" in t.lower())
        if price_section:
            data["Price"] = price_section.strip()
    except Exception as e:
        print(f"Error scraping Youly: {e}")
    return reviews, data

# Main function to scrape all websites and save to CSV
def scrape_all_sites():
    print("Starting scraping...")
    
    # Scrape data from Trustpilot
    trustpilot_reviews = scrape_trustpilot_reviews()
    
    # Scrape data from Get Moshy
    getmoshy_data = scrape_getmoshy_details()
    
    # Scrape data from Youly
    youly_reviews, youly_data = scrape_youly_details()
    
    # Combine data into a DataFrame
    data = {
        "Source": ["Trustpilot"] * len(trustpilot_reviews) + ["Youly"] * len(youly_reviews),
        "Reviews": trustpilot_reviews + youly_reviews,
        "Money Back Guarantee": [""] * len(trustpilot_reviews) + [youly_data["Money Back Guarantee"]] * len(youly_reviews),
        "Price": [""] * len(trustpilot_reviews) + [youly_data["Price"]] * len(youly_reviews)
    }
    df = pd.DataFrame(data)
    
    # Add Get Moshy details to the DataFrame
    moshy_row = pd.DataFrame({
        "Source": ["Get Moshy"],
        "Reviews": [""],
        "Money Back Guarantee": [getmoshy_data["Money Back Guarantee"]],
        "Price": [getmoshy_data["Price"]]
    })
    df = pd.concat([df, moshy_row], ignore_index=True)
    
    # Ensure the directory exists
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)
    
    # Save DataFrame to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data saved successfully to {OUTPUT_FILE}")

# Function to schedule periodic scraping
def schedule_scraping(interval_hours=24, run_once=False):
    while True:
        scrape_all_sites()
        if run_once:
            break  # Exit after one iteration
        print(f"Waiting {interval_hours} hours before the next scrape...")
        time.sleep(interval_hours * 3600)

# Start scraping (use run_once=True for one-time execution in Colab)
if __name__ == "__main__":
    schedule_scraping(interval_hours=24, run_once=True)