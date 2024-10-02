from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from utils import random_delay

load_dotenv()

class TikTokClient:
    def __init__(self, driver: WebDriver, **args):
        self.driver = driver 
        self.email = os.getenv("TIKTOK_EMAIL")
        self.password = os.getenv("TIKTOK_PASSWORD")

    def login(self):
        random_delay()

        # target and click the header login button
        element = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "header-login-button"))
        )
        element.click()

        random_delay()

        # Click the Use phone / email / username button
        element = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Use phone / email / username']"))
        )
        element.click()

        random_delay()

        # click on the Login with email or username button
        element = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in with email or username']"))
        )
        element.click()

        random_delay()

        # target the email and password input, fill in the values and press the login button
        email_input = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))
        )
        password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")

        email_input.clear()
        email_input.send_keys(self.email)
        random_delay()
        password_input.clear()
        password_input.send_keys(self.password)

        random_delay()

        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' and text()='Log in']")
        submit_button.click()

        random_delay()

    def driver_quit(self):
        self.driver.quit()