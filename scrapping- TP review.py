# Install necessary dependencies
!pip install selenium
!apt-get update # Update the package lists
!apt install -y chromium-chromedriver

# Import necessary libraries
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from google.colab import files

# Set up the Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

# Initialize the WebDriver correctly with the path to chromedriver
driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', options=chrome_options)

# Function to scrape reviews from a given Trustpilot page URL using Selenium
def scrape_reviews(url, total_pages):
    reviews = []
    
    for page in range(1, total_pages + 1):
        # Construct the URL for the specific page
        page_url = f"{url}?page={page}"
        driver.get(page_url)
        time.sleep(3)  # Wait for the page to load
        
        # Find all review elements on the page
        review_containers = driver.find_elements(By.CSS_SELECTOR, 'div.review')
        
        for review in review_containers:
            try:
                review_text = review.find_element(By.CSS_SELECTOR, 'p.review-content__text').text
            except:
                review_text = ''
            
            try:
                rating = review.find_element(By.CSS_SELECTOR, 'div.star-rating')['title']
            except:
                rating = 'No rating'
                
            try:
                reviewer_name = review.find_element(By.CSS_SELECTOR, 'div.consumer-information__name').text
            except:
                reviewer_name = 'Anonymous'
            
            try:
                date = review.find_element(By.CSS_SELECTOR, 'time.review-content__header__date').get_attribute('datetime')
            except:
                date = 'No date'
            
            reviews.append({
                'reviewer_name': reviewer_name,
                'review_text': review_text,
                'rating': rating,
                'date': date
            })
        
        print(f"Scraped {len(review_containers)} reviews from page {page}")
    
    return reviews

# Function to scrape data for both Get Mosh and Juniper
def scrape_all_reviews():
    # URLs to scrape
    get_mosh_url = "https://www.trustpilot.com/review/getmosh.com.au"
    juniper_url = "https://au.trustpilot.com/review/myjuniper.com"
    
    # Get Mosh: Total pages = 10
    get_mosh_reviews = scrape_reviews(get_mosh_url, 10)
    
    # Juniper: Total pages = 34
    juniper_reviews = scrape_reviews(juniper_url, 34)
    
    # Combine the reviews from both sources
    all_reviews = get_mosh_reviews + juniper_reviews
    
    # Convert the reviews into a DataFrame
    df = pd.DataFrame(all_reviews)
    
    # Save the DataFrame to a CSV file
    df.to_csv('trustpilot_reviews.csv', index=False)
    
    print("Scraping completed and data saved to 'trustpilot_reviews.csv'.")

# Run the function to scrape reviews and save the CSV file
scrape_all_reviews()

# Download the CSV file
files.download('trustpilot_reviews.csv')