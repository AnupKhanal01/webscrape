# Install necessary dependencies
!pip install requests beautifulsoup4

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape price and money back guarantee information
def scrape_price_and_guarantee(url):
    # Send HTTP request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize data dictionary
    data = {
        'url': url,
        'money_back_guarantee': None,
        'price': None
    }

    # Scrape "Money Back Guarantee" text (Assumed element, can be changed based on actual page structure)
    try:
        money_back_element = soup.find(text=lambda text: text and "Money Back Guarantee" in text)
        data['money_back_guarantee'] = money_back_element.strip() if money_back_element else "Not found"
    except:
        data['money_back_guarantee'] = "Not found"

    # Scrape "Price" text (Assumed element, can be changed based on actual page structure)
    try:
        price_element = soup.find(text=lambda text: text and "Price" in text)
        data['price'] = price_element.strip() if price_element else "Not found"
    except:
        data['price'] = "Not found"
    
    return data

# URLs for Get Mosh and Juniper
get_mosh_url = "https://www.getmoshy.com.au/weight-loss"
juniper_url = "https://www.myjuniper.com/"

# Scrape data for both websites
get_mosh_data = scrape_price_and_guarantee(get_mosh_url)
juniper_data = scrape_price_and_guarantee(juniper_url)

# Combine results into a DataFrame
all_data = [get_mosh_data, juniper_data]
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
df.to_csv('price_and_guarantee_data.csv', index=False)

# Print out the DataFrame
print(df)

# Download the CSV file
from google.colab import files
files.download('price_and_guarantee_data.csv')
