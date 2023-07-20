# Artwork Scraper for Linux Desktop Backgrounds

![Desktop Background](https://example.com/desktop_background.jpg)

## Purpose

This Python script is designed to procure artwork from web pages hosted on "https://eternalisedofficial.com" to be used as visually appealing desktop backgrounds in a Linux environment. The script scrapes web pages containing artwork images and downloads them to a local directory. The artwork can then be fed into a Bash script that periodically changes the desktop background, providing users with a refreshing and dynamic visual experience.

## Features

- Scrapes web pages from "https://eternalisedofficial.com" to find artwork images.
- Downloads the artwork images and saves them in the "artwork" subdirectory.
- Uses the `feh` image viewer to periodically update the Linux desktop background.
- Identifies the artwork by its title and uses it as the image filename for proper attribution.
- Includes a customizable rate-limiting mechanism to avoid overloading the server.
- Sets a bot-like User-Agent header to identify the script and provide contact information for transparency and communication with website owners.

## Responsible Use

It is essential to emphasize that this script is intended solely for visual appreciation and desktop background rotation. The primary goal is to showcase and appreciate the artwork available on "https://eternalisedofficial.com" as part of the Linux desktop environment. There are no intentions to misuse or redistribute the artwork for any other purpose.

Please note that this script should be used responsibly and in compliance with the terms of use set by "https://eternalisedofficial.com". Be considerate of the website's resources and avoid any actions that may cause harm or disruption to their services.

## How to Use

1. Install the required Python packages: `beautifulsoup4` and `requests`.

```pip install beautifulsoup4 requests```

2. Install the `feh` image viewer on your Linux machine.

```sudo pacman -S feh # For Arch Linux```

3. Clone this repository and navigate to the project directory.

```git clone https://github.com/yourusername/artwork_scraper.git
cd artwork_scraper```

4. Run the Python script to start downloading the artwork.

```python scraper.py```

5. After the artwork has been downloaded to the "artwork" directory, run the Bash script to periodically change the desktop background. Adjust the frequency as desired.

```crontab -e```

Add the following line to the crontab (update every hour):

```0 * * * * /path/to/your/update_background.sh```

6. Enjoy the visually appealing artwork rotating on your Linux desktop background!

## License

This project is open-source and released under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code responsibly.
