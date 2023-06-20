import pandas as pd
#import requests
#from bs4 import BeautifulSoup 
# pip install BeautifulSoup
# pip install selenium
# pip install --upgrade chromedriver==108.0.5359.71
# replit come with chromedriver
# in shell, 
# chromedriver --version
# chromium-browser --version (open version without google)
# check both versions are same at level of xxx.x.xxxx
from selenium import webdriver #pip install selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_driver():

  # Instantiate the WebDriver with options suitable for this environment
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)  
  # which chromium-browser, 
  # which chromedriver, to get path in shell
  # driver = webdriver.Chrome(path) if on local machine
  return driver

def get_videos(driver):
  aName = 'style-scope ytd-video-renderer'
  driver.get(urls[1])
  #videos = driver.find_elements(By.TAG_NAME, aName)
  #videos = driver.find_elements(By.CLASS_NAME, aName)

  videos = driver.find_elements(By.TAG_NAME, "video-title")
  
  # Iterate through the div_elements list and print the tag name and text content
  for video in videos:
      print("Tag Name:", video.tag_name)
      print("Text Content:", video.text)
      print("---------------")
  
  return videos

def find_elements_with_nested_tag(url, div_class_name, nested_class_names, max_scroll_count):
    # Instantiate the WebDriver (assuming you have the appropriate driver installed)
    driver = get_driver()

    # Navigate to the desired URL
    driver.get(url)

    try:
        print(div_class_name, nested_class_names)
        # Find the div elements by class name
        div_elements = driver.find_elements(By.CLASS_NAME, div_class_name)

        data = {'timestamp': [], 'news': []}

        # Scroll to the end of the page to load all the news elements
        scroll_count = 0
        while scroll_count < max_scroll_count:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)  # Adjust the sleep time based on your page's loading speed

            # Check if the "没有更多了" element is present
            end_of_content_element = driver.find_elements(By.ID, "liveList01_empty")
            if len(end_of_content_element) > 0 and end_of_content_element[0].is_displayed():
                break  # Exit the loop if the "没有更多了" element is displayed

            # Check if a "Load More" button is present
            #load_more_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'load-more')]")
            #if len(load_more_button) > 0:
                # Click the "Load More" button
            #    ActionChains(driver).move_to_element(load_more_button[0]).click().perform()
            #    time.sleep(20)  # Adjust the sleep time based on your page's loading speed
            #else:
            #    break  # Exit the loop if no more "Load More" button is found

            scroll_count += 1

        # Wait for the new content to load
        WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, div_class_name)))

        # Update the div elements list
        div_elements = driver.find_elements(By.CLASS_NAME, div_class_name)

        # Iterate over each div element
        for div_element in div_elements:
            # Find the nested tags under each div element by class name
            for nested_class_name in nested_class_names:
                # Use an explicit wait to wait until the nested elements are present
                nested_elements = WebDriverWait(div_element, 0.5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, nested_class_name))
                )

                # Append the text of each nested element to the corresponding list
                for nested_element in nested_elements:
                    if nested_class_name == nested_class_names[0]:
                        data['timestamp'].append(nested_element.text)
                    elif nested_class_name == nested_class_names[1]:
                        data['news'].append(nested_element.text)

    finally:
        # Close the WebDriver
        driver.quit()

    return pd.DataFrame(data)

def measure_runtime(func):
    start_time = time.time()
    func()  # Call the function to measure its runtime
    end_time = time.time()
    runtime = end_time - start_time
    print("Runtime:", runtime, "seconds")

if __name__ == "__main__":
  
  urls = ['https://finance.sina.com.cn/7x24/',
          'https://www.youtube.com/feed/trending',
          'https://www.bloomberg.com/asia',
          'https://www.wsj.com/?mod=nav_top_section',
          'https://www.ft.com/'
         ]

  sinaFinanceClasses = ['bd_c0', 'bd_i_time_c', 'bd_i_txt_c']  
  news_sinaFinance = find_elements_with_nested_tag(urls[0], sinaFinanceClasses[0], sinaFinanceClasses[1:], 0)
  # 9s for 20 news, 0 scroll
  # 20s for 100 news, 4 scrolls
  # 29s for 200 news, 9 scrolls
  print(news_sinaFinance)
  print(news_sinaFinance.shape)

