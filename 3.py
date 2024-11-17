import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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

# Read input CSV and scrape data
def scrape_from_csv(input_csv, output_csv):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Prepare for writing results
    results = []
    with open(input_csv, "r") as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip the header if present
        for row in reader:
            profile_url = row[0].strip()  # Assuming the URL is in the first column
            print(f"Scraping: {profile_url}")
            try:
                data = scrape_twitter_profile(driver, profile_url)
                results.append(data)
            except Exception as e:
                print(f"Error scraping {profile_url}: {e}")
    
    # Write results to output CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["url", "bio", "followers", "following"])
        writer.writeheader()
        writer.writerows(results)
    
    driver.quit()
    print(f"Scraping completed. Results saved to {output_csv}")

# File paths
input_csv = "twitter_links.csv"  # Input file with profile URLs
output_csv = "twitter_data3.csv"    # Output file for results

# Start scraping
scrape_from_csv(input_csv, output_csv)
