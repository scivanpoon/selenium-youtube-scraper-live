import requests
from bs4 import BeautifulSoup 
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

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  # which chromium-browser, which chromedriver to get path in shell
  # ChromiumPath = '/nix/store/58gnnsq47bm8zw871chaxm65zrnmnw53-ungoogled-chromium-108.0.5359.95/bin/chromium-browser'
  # ChromeDriverPath = '/nix/store/i85kwq4r351qb5m7mrkl2grv34689l6b-chromedriver-108.0.5359.71/bin/chromedriver'
  # driver = webdriver.Chrome() #path to chrome driver if on local machine
  driver = webdriver.Chrome(options=chrome_options)
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

if __name__ == "__main__":
  
  urls = ['https://finance.sina.com.cn/7x24/',
          'https://www.youtube.com/feed/trending',
          'https://www.bloomberg.com/asia',
          'https://www.wsj.com/?mod=nav_top_section',
          'https://www.ft.com/'
         ]
  
  response = requests.get(urls[1])
  print('Status Code', response.status_code)  
  with open('url.html', 'w') as f:
    f.write(response.text)
  doc = BeautifulSoup(response.text, 'html.parser')
  print('PageTitle by BeautifulSoup: ', doc.title.text)
  video_divs = doc.find_all('div', class_='ytd-video-renderer')
  print(f'Found {len(video_divs)} videos By BeautifulSoup')
  

  driver = get_driver()
  
  driver.get(urls[1])
  print('PageTitle by selenium: ', driver.title)
  aClassName = 'ytd-video-renderer'
  print(len(driver.find_element(By.CLASS_NAME, aClassName).text))
  #print(driver.find_element(By.CLASS_NAME, aClassName).text)

  videos = get_videos(driver)
  print(f'Found {len(videos)} videos with Selenium')

  
  print('Parsing the first video')
  # title, url thumbnail, channel, views, uploaded, description
  video = videos[0]
  title = video.find_element(By.ID, 'video-title')
  print(title)