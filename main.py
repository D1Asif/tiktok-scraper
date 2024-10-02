import argparse
from config import config
from selenium import webdriver
from client import TikTokClient
from utils import random_delay
import time
import undetected_chromedriver as uc

def parse_args():
    parser = argparse.ArgumentParser(description="""
        Provide args for scraping
        """)
    
    parser.add_argument('--username', type=str, nargs="?", help="add the username of the profile you want to scrape")

    parser.add_argument('--keyword', type=str, default=config["keyword"], nargs="?", help="add the search keyword")

    return vars(parser.parse_args()) # returns the args in dictionary format

if __name__ == "__main__":
    args = parse_args()

    driver = uc.Chrome()

    url = "https://www.tiktok.com/"

    driver.get(url)

    random_delay()

    tiktokClient = TikTokClient(driver, **args)

    tiktokClient.login()

    random_delay()

    time.sleep(20)

    tiktokClient.driver_quit()



