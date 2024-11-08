import requests
from bs4 import BeautifulSoup
import csv

# Base URL for the Amazon product listing (first page)
base_url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

# Define headers to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Function to scrape individual product data
def scrape_product_data(soup):
    products = soup.find_all('div', {'data-asin': True})
    product_details = []

    for product in products:
        # Get product name, removing first word and terminating at ',' or '|'
        product_name = product.find('span', {'class': 'a-text-normal'})
        price = product.find('span', {'class': 'a-price-whole'})
        rating = product.find('span', {'class': 'a-icon-alt'})
        seller_name = product.find('span', {'class': 'a-size-base-plus'})

        if product_name and price and rating:
            product_name = ' '.join(product_name.get_text(strip=True).split(' ')[1:]).split(',')[0].split('|')[0]
            price = price.get_text(strip=True)
            rating = rating.get_text(strip=True)
            seller_name = seller_name.get_text(strip=True).split(' ')[0] if seller_name else "Not Available"
        
            product_details.append([product_name, price, rating, seller_name])
    
    return product_details

# Function to get the next page URL
def get_next_page(soup):
    next_button = soup.find('a', {'class': 's-pagination-next'})
    if next_button:
        return 'https://www.amazon.in' + next_button['href']
    return None

# List to hold all scraped product data
all_product_data = []

# Start with the first page
current_url = base_url

# Loop through pages until no more next page exists
while current_url:
    print(f"Scraping {current_url}")
    response = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape product data from the current page
    product_data = scrape_product_data(soup)
    all_product_data.extend(product_data)

    # Find the next page URL
    current_url = get_next_page(soup)

# Save results to CSV
with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Rating', 'Seller Name'])
    writer.writerows(all_product_data)

print(f"Scraping complete. Found {len(all_product_data)} products.")
