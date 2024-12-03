Technical Documentation for the Web Scraping Script

Overview
This script automates the extraction of data from three websites, processes it, and saves it as a CSV file on a local machine. It is designed to run periodically (every 24 hours) to update the data. The data of interest includes:
User reviews related to weight loss.
Details about money-back guarantees and prices.

How It Works
1. Imports and Libraries
os: Handles file paths and checks for the existence of directories.
requests: Sends HTTP GET requests to fetch HTML content of web pages.
BeautifulSoup: Parses the fetched HTML content and locates specific elements in the DOM using tags, classes, and attributes.
pandas: Structures the extracted data into a DataFrame and writes it to a CSV file.
time: Pauses the script for a set duration to implement periodic execution.

2. Script Functions
a. scrape_trustpilot_reviews
Purpose: Extracts reviews related to weight loss from Trustpilot.
Steps:
Sends a GET request to the Trustpilot URL.
Parses the HTML response using BeautifulSoup.
Identifies review sections by their specific CSS class (styles_reviewContent__0Q2Tg).
Filters reviews containing the keyword "weight loss".
Returns a list of relevant reviews.

b. scrape_getmoshy_details
Purpose: Extracts information about money-back guarantees and prices from Get Moshy.
Steps:
Sends a GET request to the Get Moshy URL.
Parses the HTML response using BeautifulSoup.
Searches the text of the page for phrases like "money back" and "price" using a find method with a lambda function.
Stores the extracted details in a dictionary and returns it.

c. scrape_youly_details
Purpose: Extracts reviews related to weight loss, money-back guarantees, and prices from Youly.
Steps:
Sends a GET request to the Youly URL.
Parses the HTML response using BeautifulSoup.
Identifies review sections by their class (review-text), filters for weight loss keywords, and stores them in a list.
Searches for guarantees and prices in the page text using the find method.
Returns a tuple containing the list of reviews and a dictionary of guarantee and price details.

3. Main Function: scrape_all_sites
Purpose: Orchestrates scraping and data saving.
Steps:
Calls the scraping functions for Trustpilot, Get Moshy, and Youly.
Combines their outputs into a single DataFrame.
Reviews are added along with their source (Trustpilot, Get Moshy, or Youly).
Money-back guarantee and price details are included if available.
Checks if the specified save directory exists; creates it if not.
Writes the DataFrame to a CSV file at the specified location.

4. Scheduler Function: schedule_scraping
Purpose: Repeats the scraping process at regular intervals (24 hours by default).
Steps:
Calls scrape_all_sites to fetch and save data.
Waits for the specified duration (interval_hours * 3600 seconds).
Repeats indefinitely.

Execution Workflow
Initialization:
The save directory (SAVE_DIRECTORY) and CSV file path (OUTPUT_FILE) are set.
Default interval for periodic scraping is 24 hours.
Scraping Cycle:
Calls scrape_all_sites:
Scrapes data from all three websites.
Saves the combined data to scraped_data.csv.
Periodic Execution:
Uses the schedule_scraping function to run the script every 24 hours.

Key Features
Error Handling:
Includes try-except blocks to handle HTTP and parsing errors without crashing the script.
Logs errors to the console for debugging.
Dynamic File Management:
Ensures the save directory exists before writing the CSV file.
Uses os.path.join to construct file paths dynamically, ensuring compatibility across operating systems.
Keyword-Based Filtering:
Filters reviews to only include those related to weight loss using case-insensitive keyword matching.
Scalability:
Designed to handle additional websites or data points with minimal changes.
Modular functions make it easy to extend or modify.
Outputs
A CSV file named scraped_data.csv is saved in the directory specified by SAVE_DIRECTORY.
The file contains:
Source: Website from which the data was scraped.
Reviews: User reviews mentioning weight loss.
Money Back Guarantee: Guarantee details (if available).
Price: Pricing details (if available).
