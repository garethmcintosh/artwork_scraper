import subprocess
import platform
import ctypes
import os
import requests
import uuid
import re
import time
from bs4 import BeautifulSoup

checked_urls = set()

def get_wallpaper(monitor=0):
    system = platform.system()

    if system == "Windows":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop") as key:
                wallpaper_path = winreg.QueryValueEx(key, "WallPaper")[0]
            return wallpaper_path
        except Exception as e:
            print(f"Error getting Windows wallpaper: {e}")
            return None

    elif system == "Linux":
        # Check for XFCE
        if 'XFCE' in os.environ.get('XDG_CURRENT_DESKTOP', ''):
            try:
                result = subprocess.run(
                    ['xfconf-query', '-c', 'xfce4-desktop', '-p', f'/backdrop/screen0/monitor{monitor}/last-image'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip()
            except subprocess.CalledProcessError:
                print("Error getting XFCE wallpaper")
                return None
        # Add checks for other Linux desktop environments here if needed
        else:
            print("Unsupported Linux desktop environment")
            return None

    else:
        print(f"Unsupported operating system: {system}")
        return None
    
def scrape_page(page_url, artwork):
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
                if image_url not in checked_urls:
                    checked_urls.add(image_url)
                    image_title = figure.find('img')['data-image-title']
                    cleaned_title = re.sub(r'[^A-Za-z0-9 ]+', '', image_title).lower()
                    cleaned_artwork = re.sub(r'[^A-Za-z0-9 ]+', '', artwork).lower()
                    if cleaned_title == cleaned_artwork:
                        print(f"Found a match: {image_url}")
                        return True;
    
    return False;
def main():
    base_url = "https://eternalisedofficial.com/latest-posts/"
    main_response = requests.get(base_url)
    if main_response.status_code != 200:
        print(f"Failed to fetch main page: {base_url}")
    else:
        wallpaper = get_wallpaper()
        if wallpaper:
            artwork = os.path.splitext(os.path.basename(wallpaper))[0]
            print(f"Current artwork: {artwork}")
            main_soup = BeautifulSoup(main_response.content, 'html.parser')
            articles = main_soup.find_all('article')

            for article in articles:
                link_tag = article.find('a', href=True)
                if link_tag:
                    page_url = link_tag['href']
                    print(f"Scraping page: {page_url}")
                    result = scrape_page(page_url, artwork)
                    if result:
                        print(f"Found a match: {page_url}")
                        break
        else:
            print("Failed to retrieve the artwork.")

if __name__ == "__main__":
    main()

