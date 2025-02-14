# Install required libraries
!pip install beautifulsoup4 requests schedule

# Import necessary modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Function to scrape reviews
def scrape_reviews():
    base_url = "https://au.trustpilot.com/review/myjuniper.com?page="
    reviews = []
    
    # Loop through all 34 pages
    for page in range(1, 35):
        url = base_url + str(page)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract reviews within <p> tags
            for review in soup.find_all('p'):
                text = review.get_text(strip=True)
                if text:  # Ensure the review text is not empty
                    reviews.append({'Page': page, 'Review': text})
            print(f"Page {page} scraped successfully.")
        else:
            print(f"Failed to scrape page {page}. Status code: {response.status_code}")

    # Save data to a CSV file
    df = pd.DataFrame(reviews)
    output_path = '/content/drive/My Drive/reviews.csv'  # Change the path if needed
    df.to_csv(output_path, index=False)
    print(f"Reviews saved to {output_path}")

# Scheduler to run the function every 24 hours
import schedule

# Schedule the function
schedule.every(24).hours.do(scrape_reviews)

# Run the scheduler
print("Scheduler started. Press stop in Colab to end.")
scrape_reviews()  # Run once immediately
while True:
    schedule.run_pending()
    time.sleep(1)