from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Open the Twitter profile page
    twitter_url = "https://twitter.com/GTNUK1"  # Replace with the desired Twitter URL
    driver.get(twitter_url)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 20)
    
    # Scroll to ensure content is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Allow time for content to load
    
    # Fetch Bio
    try:
        bio_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="UserDescription"]')))
        bio = bio_element.text
    except Exception:
        bio = "Bio not available"
    
    # Fetch Following Count
    try:
        following_element = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/following")]/span[1]/span')))
        following_count = following_element.text
    except Exception:
        following_count = "Following count not available"
    
    # Fetch Followers Count
    try:
        followers_element = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/followers")]/span[1]/span')))
        followers_count = followers_element.text
    except Exception:
        followers_count = "Followers count not available"
    
    # Fetch Location
    try:
        location_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]/span')))
        location = location_element.text
    except Exception:
        location = "Location not available"
    
    # Fetch Website
    try:
        website_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]/a')))
        website = website_element.get_attribute("href")
    except Exception:
        website = "Website not available"
    
    # Print the details
    print(f"Bio: {bio}")
    print(f"Following Count: {following_count}")
    print(f"Followers Count: {followers_count}")
    print(f"Location: {location}")
    print(f"Website: {website}")
    
finally:
    # Quit the browser
    driver.quit()
