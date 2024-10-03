from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import random_delay, infinite_scroll
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import io
from PIL import Image
import yt_dlp

import undetected_chromedriver as uc
# **** Note: Using selenium webdriver was invoking CAPTCHA. Using undetected_chromedrver solved the issue ***** 

def scrape_profile_data(username):
    """
    takes the Tiktok username and retrieves the basic info of a profile. returns the info in a dictionary.
    """
    url = f"https://www.tiktok.com/@{username}"

    driver = uc.Chrome()
    driver.get(url)

    random_delay()

    try:
        username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h1[@data-e2e='user-title']"))
        ).text

        name = driver.find_element(By.XPATH, "//h2[@data-e2e='user-subtitle']").text
        bio = driver.find_element(By.XPATH, "//h2[@data-e2e='user-bio']").text

        following = driver.find_element(By.XPATH, "//strong[@title='Following']").text
        follower = driver.find_element(By.XPATH, "//strong[@title='Followers']").text
        likes = driver.find_element(By.XPATH, "//strong[@title='Likes']").text

        # Store the scraped data in a dictionary
        profile_data = {
            "username": username,
            "name": name,
            "bio": bio,
            "following": following,
            "followers": follower,
            "likes": likes
        }

        # Output the dictionary
        print(profile_data)

    except Exception as e:
        print("Error scraping profile:", e)

    random_delay()

    driver.quit()


def scrape_profile_video_urls(username):
    """
    takes the Tiktok username of a profile as input and retrieves the Tiktok urls of all the videos of that profile. returns the video urls in a list.
    """
    url = f"https://www.tiktok.com/@{username}"

    driver = uc.Chrome()
    driver.get(url)

    random_delay()

    infinite_scroll(driver)

    try:
        video_url_tags = driver.find_elements(By.XPATH, f"//a[contains(@href, 'https://www.tiktok.com/@{username}/video/')]")

        video_urls = [tag.get_attribute('href') for tag in video_url_tags]

        print(video_urls)
        print(len(video_urls))

    except Exception as e:
        print("Error scraping profile:", e)

    random_delay()

    driver.quit()


def scrape_profile_photo_urls(username):
    """
    takes the Tiktok username of a profile as input and retrieves the Tiktok urls of all the photo post of that profile. returns the video urls in a list.
    """
    url = f"https://www.tiktok.com/@{username}"

    driver = uc.Chrome()
    driver.get(url)

    random_delay()

    infinite_scroll(driver)

    try:
        photo_url_tags = driver.find_elements(By.XPATH, f"//a[contains(@href, 'https://www.tiktok.com/@{username}/photo/')]")

        photo_urls = [tag.get_attribute('href') for tag in photo_url_tags]

        print(photo_urls)
        print(len(photo_urls))

    except Exception as e:
        print("Error scraping profile:", e)

    random_delay()

    driver.quit()


def scrape_single_video_data(url: str):

    driver = uc.Chrome()
    driver.get(url)

    random_delay()

    try:
        like_count = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//strong[@data-e2e='like-count']"))
        ).text
        comment_count = driver.find_element(By.XPATH, "//strong[@data-e2e='comment-count']").text
        bookmark_count = driver.find_element(By.XPATH, "//strong[@data-e2e='undefined-count']").text
        share_count = driver.find_element(By.XPATH, "//strong[@data-e2e='share-count']").text

        post_date = driver.find_element(By.XPATH, "//span[@data-e2e='browser-nickname']/span[last()]").text

        post_description = driver.find_element(By.XPATH, "//h1[@data-e2e='browse-video-desc']/span").text

        video_length = driver.find_element(By.XPATH, "//div[@class='css-1cuqcrm-DivSeekBarTimeContainer e1ya9dnw1']").text.split(" / ")[1]

        video_data = {
            "post_owner_username": url.split("/")[-3].replace("@", ""),
            "post_id": url.split("/")[-1],
            "like_count": like_count,
            "comment_count": comment_count,
            "bookmark_count": bookmark_count,
            "share_count": share_count,
            "post_date": post_date,
            "post_description": post_description,
            "video_length": video_length
        }

        print(video_data)
        
    except Exception as e:
        print("Error scraping profile:", e)

    random_delay()

    driver.quit()


## works well for all public videos
def download_video(video_url, save_path='tiktok_videos'):
    """
    Provide the link of the video post and it will download it in the path.
    """
    # Ensure the save directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path) # this creates nested directories, too

    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'), # instead of Id, title can be put as well
        'format': 'best',
    }

    try:
        # Create a yt-dlp object and download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Video successfully downloaded: {filename}")
    
    except Exception as e:
        print(f"Error downloading video: {str(e)}")


## This function works for Tiktok, Insta, Medium, LinkedIn, FB. Worked for jpg, webp. Didn't work for avif format.
def download_image(download_path, url, file_name):
    """
        takes download_path (folder path), url (image url) and file_name (new image file name with .jpg extension)

        saves the image in the path.
    """
    ### Works without adding header. In case of any issue, try adding header
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    #     "Referer": "https://www.tiktok.com/",
    #     "Accept-Language": "en-US,en;q=0.5",
    # }

    try:
        response = requests.get(url=url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            return
        
        # Check the Content-Type header
        content_type = response.headers.get('Content-Type')
        print(content_type)
        if 'image' not in content_type:
            print(f"Unexpected content type: {content_type}")
            return
        
        image_file = io.BytesIO(response.content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print("Error:", e)


download_video("https://www.tiktok.com/@d1asif/video/7179462609714810114?q=d1asif&t=1727966362497")