import os
import requests
import uuid
import re
import time
from bs4 import BeautifulSoup

downloaded_urls = set()

def clean_filename(title):
    # Remove any special characters from the title
    cleaned_title = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores and convert to lowercase
    return cleaned_title.strip().replace(' ', '_').replace('\n', '_').lower()

def download_image(image_url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; artwork_scraper_bot/1.0; +https://www.github.com/garethmcintosh/artwork_scraper)'
    }
    response = requests.get(image_url, headers=headers)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded: {save_path}")
    else:
        print(f"Failed to download image: {image_url}")

def scrape_page(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {page_url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    header_tag = soup.find('h2', string='Artwork used in the video')
    if header_tag:
        gallery_block = header_tag.find_next_sibling('figure', class_='wp-block-gallery')
        if gallery_block:
            for i, figure in enumerate(gallery_block.find_all('figure')):
                image_url = figure.find('img')['src']
                if image_url not in downloaded_urls:
                    downloaded_urls.add(image_url)
                    image_title = figure.find('img')['data-image-title']
                    cleaned_title = clean_filename(image_title)
                    image_filename = f"{cleaned_title}_{uuid.uuid4().hex[:8]}.jpg"
                    download_path = os.path.join('artwork', image_filename)
                    download_image(image_url, download_path)
                    time.sleep(2)  # Introduce a 2-second delay between requests

if __name__ == "__main__":
    base_url = "https://eternalisedofficial.com/latest-posts/"
    main_response = requests.get(base_url)
    if main_response.status_code != 200:
        print(f"Failed to fetch main page: {base_url}")
    else:
        if not os.path.exists('artwork'):
            os.makedirs('artwork')
            
        # clear the artwork folder
        for file in os.listdir('artwork'):
            os.remove(os.path.join('artwork', file))

        main_soup = BeautifulSoup(main_response.content, 'html.parser')
        articles = main_soup.find_all('article')

        for article in articles:
            link_tag = article.find('a', href=True)
            if link_tag:
                page_url = link_tag['href']
                print(f"Scraping page: {page_url}")
                scrape_page(page_url)
