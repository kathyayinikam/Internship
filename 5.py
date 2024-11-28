import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Database configuration
DB_CONFIG = {
    "host": "localhost",  # XAMPP default host
    "user": "root",       # Default user for XAMPP
    "password": "",       # Leave blank if no password is set
    "database": "twitter_data"  # Replace with your database name
}

# Function to scrape Twitter profile data
def scrape_twitter_profile(driver, profile_url):
    driver.get(profile_url)
    time.sleep(20)  # Adjust sleep time if necessary
    
    try:
        bio = driver.find_element(By.XPATH, "//div[@data-testid='UserDescription']").text
    except:
        bio = "Bio not available"
        
    try:
        followers = driver.find_element(By.XPATH, "//a[contains(@href, '/followers')]").text
    except:
        followers = "Followers count not available"
        
    try:
        following = driver.find_element(By.XPATH, "//a[contains(@href, '/following')]").text
    except:
        following = "Following count not available"
    
    return {"url": profile_url, "bio": bio, "followers": followers, "following": following}

# Save data to database
def save_to_database(connection, data):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO profiles (url, bio, followers, following)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (data['url'], data['bio'], data['followers'], data['following']))
        connection.commit()
        print(f"Data for {data['url']} saved successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Read input CSV and scrape data
def scrape_from_csv(input_csv):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Connect to the database
    connection = mysql.connector.connect(**DB_CONFIG)
    
    with open(input_csv, "r") as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip the header if present
        for row in reader:
            profile_url = row[0].strip()  # Assuming the URL is in the first column
            print(f"Scraping: {profile_url}")
            try:
                data = scrape_twitter_profile(driver, profile_url)
                save_to_database(connection, data)
            except Exception as e:
                print(f"Error scraping {profile_url}: {e}")
    
    driver.quit()
    connection.close()
    print("Scraping and database update completed.")

# File paths
input_csv = "twitter_links.csv"  # Input file with profile URLs

# Start scraping
scrape_from_csv(input_csv)
