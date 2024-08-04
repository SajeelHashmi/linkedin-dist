# from typing import Any
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time
# from langchain.chains import LLMChain
# from langchain_core.prompts import PromptTemplate
# from langchain_mistralai.chat_models import ChatMistralAI
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# import os
# from io import BytesIO
# import base64


# MISTRAL_API_KEY = 'c2pXa02xhfTrY6nZfjmOdzHjj4wKv7Mv'
# class ScrapeException(Exception):
#     """Custom exception for scrape errors"""
#     pass


# class Scrapper:
#     def __init__(self):
#         self.chrome_options = Options()
#         self.chrome_options.add_argument("--start-maximized")
#         # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
#         self.chrome_options.add_argument('--log-level 3') 
#         # self.chrome_options.add_argument("--headless")
#         self.chrome_options.add_argument("--no-sandbox")
#         self.chrome_options.add_argument("--disable-dev-shm-usage")
#         self.chrome_options.add_argument("--disable-gpu")

#     def scrape(self,url) -> str:
#         """Tries to scrape linkedin profile and returns about and headline throws if unsuccessful"""
#         service = ChromeService(ChromeDriverManager().install())
#         driver = webdriver.Chrome(options=self.chrome_options) 

#         print("here")
#         print(url)
#         driver.get(url)
#         print("sleeping")
#         time.sleep(2)
#         print("sleep over")
#         tries = 0
#         while driver.current_url != url:
#             if tries > 10:
#                 raise ScrapeException("Could not Scrape page")
            
#             print("redirected to signup page")
#             print(driver.current_url)
#             driver.get(url)
#             time.sleep(1)
#             tries += 1
            
#         time.sleep(1)
#         try:
#             driver.find_element(by=By.CSS_SELECTOR,value='#base-contextual-sign-in-modal > div > section > button').click()
#             print("clicked")
#         except:
#             print("could not find button ")
#             try:
#                 driver.find_element(by=By.CSS_SELECTOR,value='#public_profile_contextual-sign-in > div > section > button').click()
#                 print("clicked button 2")

#             except:
#                 print("could not find button")

#         time.sleep(1)
#         # with open('test.html', 'w', encoding='utf-8') as file:
#         #     file.write(driver.page_source)
#         print("writting page source for inspection")
#         about = driver.find_element(by=By.CSS_SELECTOR,value='section.core-section-container:nth-child(2) > div:nth-child(2) > p:nth-child(1)').text


#         headline = driver.find_element(by=By.CSS_SELECTOR,value ='.top-card-layout__headline').text



#         projectDetailsLi = driver.find_elements(by=By.CSS_SELECTOR,value ='.personal-project')



#         projDetails = ''
#         for project in projectDetailsLi:
#             projDetails += project.text.strip() + '\n'




#         experienceLi = driver.find_elements(by=By.CSS_SELECTOR,value ='.experience-item')
#         experience = ''
#         for exp in experienceLi:
#             experience += exp.text.strip() + '\n'



#         certificationLi = driver.find_elements(by=By.CSS_SELECTOR,value ='.experience-item')
#         certificationDetails = ''
#         for cert in certificationLi:
#             certificationDetails += cert.text.strip() + '\n'

        


    


#         educationDetailsLis = driver.find_elements(by=By.CSS_SELECTOR,value ='.education__list-item')
#         eduDetails = ''
#         for edu in educationDetailsLis:
#             eduDetails += edu.text.strip() + '\n'




#         screenshot = driver.get_screenshot_as_png()
#         screenshot = base64.b64encode(screenshot).decode('utf-8')
#         driver.quit()  
#         return{
#             'about':about,
#             'headline':headline,
#             'projects':projDetails,
#             'experience':experience,
#             'certifications':certificationDetails,
#             'education':eduDetails
#         } , screenshot








from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import time

class ScrapeException(Exception):
    """Custom exception for scrape errors"""
    pass

class Scrapper:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument('--log-level=3') 
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")

    def scrape(self, url) -> str:
        """Tries to scrape LinkedIn profile and returns about and headline, throws if unsuccessful"""
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.chrome_options)

        driver.get(url)
        time.sleep(2)

        tries = 0
        while driver.current_url != url and tries < 20:
            print("Redirected to signup page, retrying...")
            driver.get(url)
            time.sleep(2)
            tries += 1

        if driver.current_url != url:
            driver.quit()
            raise ScrapeException("Could not scrape page")

        # Click the dismiss button if it appears
        for _ in range(2):  # Retry up to 10 times
            try:
                driver.find_element(by=By.CSS_SELECTOR,value='#base-contextual-sign-in-modal > div > section > button').click()
                # dismiss_button = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.modal__dismiss'))
                # )
                # dismiss_button.click()
                print("Dismiss button clicked")
                time.sleep(1)
                break
            except Exception as e:
                print(f"Dismiss button not found, waiting... ({e})")
                time.sleep(1)  # Wait for 1 second before retrying

        try:
            about = driver.find_element(By.CSS_SELECTOR, 'section.core-section-container:nth-child(2) > div:nth-child(2) > p:nth-child(1)').text
            headline = driver.find_element(By.CSS_SELECTOR, '.top-card-layout__headline').text

            project_details = driver.find_elements(By.CSS_SELECTOR, '.personal-project')
            proj_details = '\n'.join([proj.text.strip() for proj in project_details])

            experience_list = driver.find_elements(By.CSS_SELECTOR, '.experience-item')
            experience = '\n'.join([exp.text.strip() for exp in experience_list])

            certification_list = driver.find_elements(By.CSS_SELECTOR, '.experience-item')
            certification_details = '\n'.join([cert.text.strip() for cert in certification_list])

            education_list = driver.find_elements(By.CSS_SELECTOR, '.education__list-item')
            edu_details = '\n'.join([edu.text.strip() for edu in education_list])
            time.sleep(2)

            screenshot = driver.get_screenshot_as_png()
            screenshot = base64.b64encode(screenshot).decode('utf-8')
            driver.quit()

        except Exception as e:
            driver.quit()
            raise ScrapeException(f"Error occurred while scraping: {e}")

        driver.quit()
        return {
            'about': about,
            'headline': headline,
            'projects': proj_details,
            'experience': experience,
            'certifications': certification_details,
            'education': edu_details
        }, screenshot

# Usage example
if __name__ == "__main__":
    scrapper = Scrapper()
    url = 'https://www.linkedin.com/in/malikzohaibmustafa/'  # Example URL
    try:
        profile_data, screenshot = scrapper.scrape(url)
        print(profile_data)
        # Save the screenshot for previewing
        with open('screenshot.png', 'wb') as f:
            f.write(base64.b64decode(screenshot))
    except ScrapeException as e:
        print(f"Scraping failed: {e}")
