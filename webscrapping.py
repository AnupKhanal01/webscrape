import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape data from the website
def scrape_juniper_data():
    # URL to scrape
    url = "https://www.myjuniper.com/juniper-vs-moshy"
    
    try:
        print("Starting the scraping process...")
        
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status
        
        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize lists to store extracted data
        comparison_features = []
        popularity_stats = []
        
        # Extract comparison features for "Weight Loss Program"
        comparison_section = soup.find('section', id="comparison-features")
        if comparison_section:
            features = comparison_section.find_all('li')
            for feature in features:
                comparison_features.append(feature.text.strip())
        else:
            print("Comparison features section not found.")
        
        # Extract popularity statistics
        popularity_section = soup.find('section', id="popularity-stats")
        if popularity_section:
            stats = popularity_section.find_all('li')
            for stat in stats:
                popularity_stats.append(stat.text.strip())
        else:
            print("Popularity statistics section not found.")
        
        # Ensure data alignment (fill missing entries if needed)
        max_length = max(len(comparison_features), len(popularity_stats))
        comparison_features.extend([""] * (max_length - len(comparison_features)))
        popularity_stats.extend([""] * (max_length - len(popularity_stats)))
        
        # Prepare the data as a DataFrame
        data = {
            "Comparison Features": comparison_features,
            "Popularity Statistics": popularity_stats
        }
        df = pd.DataFrame(data)
        
        # Save to CSV
        output_file = "juniper_vs_moshy_data.csv"
        df.to_csv(output_file, index=False)
        print(f"Data saved successfully to {output_file}")
    
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

# Function to schedule periodic scraping
def schedule_scraping(interval_hours=48):
    while True:
        scrape_juniper_data()
        print(f"Waiting {interval_hours} hours before the next scrape...")
        time.sleep(interval_hours * 3600)  # Convert hours to seconds

# Start scheduled scraping every 48 hours
if __name__ == "__main__":
    schedule_scraping(interval_hours=48)