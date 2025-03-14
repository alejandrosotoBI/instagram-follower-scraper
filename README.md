# Instagram Follower/Following Scraper

## Overview

This Python script automates the process of extracting follower and following lists from an Instagram profile using Selenium and BeautifulSoup. It scrolls through the list, extracts usernames, and saves them to an Excel file.

## Features

- Automatically scrolls through the followers/following list until all accounts are loaded
- Extracts followers or following from a specified profile
- Uses Selenium for web interaction and BeautifulSoup for parsing
- Saves extracted usernames to an Excel file


## Requirements

- Python 3.x
- Google Chrome & ChromeDriver
- Selenium
- BeautifulSoup4
- Pandas
- Tkinter (usually comes pre-installed with Python)

You can install the necessary Python packages with the following commands:

```bash
pip install selenium beautifulsoup4 pandas openpyxl
```
## How to Use

1. Clone this repository or download the Python script to your local machine.
2. Ensure you have the necessary dependencies installed as mentioned above.
3. Run the script using Python:

```bash
python instagram_scraper.py
```

4. The script will prompt you to enter the Instagram profile ID (the username of the profile you wish to extract data from).
5. Next, you will be asked whether you want to extract the followers or following list. Enter one of the two options: followers or following.
6. The script will open a new Chrome window for you to log in to your Instagram account. You will be prompted to confirm whether you've logged in, and once confirmed, it will proceed with extracting the usernames from the selected list (followers or following).
7. After the usernames are extracted, you will be prompted to select where to save the extracted data as an Excel file. The usernames will be saved in the .xlsx format.


## Notes

- You must manually log in to Instagram via the opened browser.
- Ensure Chrome and ChromeDriver versions match.
- Instagram may change its structure, requiring updates to the script.
- This script is for educational and research purposes only. Scraping Instagram data may violate their terms of service.


Disclaimer

- Use this script responsibly and ensure you comply with Instagram's terms of service when using it. The authors are not responsible for any misuse.

