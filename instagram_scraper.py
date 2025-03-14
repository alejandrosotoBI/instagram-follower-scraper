from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import time

def setup_driver():
    """
    Sets up the Chrome WebDriver with the necessary options.
    
    Returns:
        WebDriver: The configured Chrome WebDriver instance.
    """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def open_url(driver, url):
    """
    Opens the Instagram profile URL using the provided WebDriver.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL of the Instagram profile to open.    
    """
    driver.get(url)

def click_list_button(driver,list_type):
    """
    Clicks the 'following' button on the Instagram profile page.
    
    """
    button_xpath = f"//a[contains(@href, '/{list_type}/')]"
    following_link = driver.find_element(By.XPATH, button_xpath)
    driver.execute_script("arguments[0].click();", following_link)
    time.sleep(4)  # Wait for the modal to open

def get_accountlist_div_name(driver):
    """
    Identifies and retrieves the class name of the div containing the list of accounts in the 'following' modal.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        
    Returns:
        str: The class name of the div element that contains the list of accounts.
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    accountlist_div_name = None
    for div in soup.find_all('div', style=True):
        if div.get('style') == "height: auto; overflow: hidden auto;":
            accountlist_div_name = div.find_parent('div').get('class')[0]
            break
    return accountlist_div_name

def scroll_until_loaded(driver, account_list, scroll_pixels, scroll_delay):
    """
    Scrolls through the account list until all accounts have been loaded.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        account_list (WebElement): The account list WebElement.
        scroll_pixels (int): Number of pixels to scroll each time.
        scroll_delay (float): Time to wait between scrolls.
    """
    while True:
        try:
            loading_gif = account_list.find_element(By.XPATH, "./div[2]")
            driver.execute_script(f"arguments[0].scrollBy(0, {scroll_pixels});", account_list)
            time.sleep(scroll_delay)  # Allow time for loading
        except:
            break  # Exit loop when loading gif is not found
    # Additional scrolls for reliability
    time.sleep(scroll_delay)
    driver.execute_script(f"arguments[0].scrollBy(0, {scroll_pixels});", account_list)
    time.sleep(scroll_delay)
    driver.execute_script(f"arguments[0].scrollBy(0, {scroll_pixels});", account_list)
def extract_usernames(driver, accountlist_div_name, scroll_pixels, scroll_delay):
    """
    Extracts usernames from the account list after scrolling.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        accountlist_div_name (str): The class name of the account list div.
        scroll_pixels (int, optional): Number of pixels to scroll each time. 
        scroll_delay (float, optional): Time to wait between scrolls. .
    
    Returns:
        list: A list of unique Instagram usernames.
    """
    account_list = driver.find_element(By.CLASS_NAME, accountlist_div_name)
    scroll_until_loaded(driver, account_list, scroll_pixels, scroll_delay)

    # Get the page source of the account list and parse it with BeautifulSoup
    accountlist_html = account_list.get_attribute('outerHTML')
    soup = BeautifulSoup(accountlist_html, 'html.parser')

    # Find all accountline elements and extract the usernames
    account_links = soup.find_all('a', href=True)
    usernames = {link['href'].strip("/") for link in account_links}

    return list(usernames)

def save_to_excel(usernames):
    """
    Saves the list of usernames to an Excel file with a user-selected path.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
        title="Save Instagram Usernames"
    )
    if file_path:
        df = pd.DataFrame(usernames, columns=["Usernames"])
        df.to_excel(file_path, index=False)
        print(f"Usernames saved successfully to {file_path}")

def main():
    """
    Main function that orchestrates the process of scraping Instagram followers.
    """
    profile_id = input("Enter the Instagram profile ID: ")
    while True:
        list_type = input("Do you want to extract 'followers' or 'following'?: ").strip().lower()
        if list_type in ["followers", "following"]:
            break
        else:
            print("Invalid input. Please type 'followers' or 'following'.")
    driver = setup_driver()
    try:
        open_url(driver, "https://www.instagram.com/")
        print("Please log in to Instagram in the opened browser.")
        while True:
            logged_in = input("Have you already logged in? (yes/no): ").strip().lower()
            if logged_in == "yes":
                break
            elif logged_in == "no":
                print("Please log in and then type 'yes' to continue.")
            else:
                print("Invalid input. Please type 'yes' or 'no'.")		
		
        open_url(driver, f"https://www.instagram.com/{profile_id}/")
        time.sleep(5)
        click_list_button(driver,list_type)
        accountlist_div_name = get_accountlist_div_name(driver)
        scroll_pixels = 150  # Number of pixels to scroll each time
        scroll_delay = 2.0   # Time to wait (in seconds) between scrolls
        usernames = extract_usernames(driver, accountlist_div_name, scroll_pixels, scroll_delay)

        print("Extracted Usernames:")
        for username in usernames:
            print(username)
        save_to_excel(usernames)
    finally:
        driver.quit()
        
main()
