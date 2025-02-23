from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import newspaper
import pandas as pd
from datetime import datetime, timedelta

def setup_driver():
    # Initialize webdriver
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_page_source(driver, url):
    # get page_source
    driver.get(url)
    return driver.page_source

def extract_urls(soup, base_url):
    # Extract all urls
    list_content = soup.find_all('a', {'class': 'css-8hzhxf'})
    return {f"{base_url}{content['href']}" for content in list_content}

def scroll_and_scrape(driver, base_url, section_url, scroll_limit=10):
    # Scroll page and scraping
    all_urls = set()
    
    for scroll_count in range(1, scroll_limit + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1l4spti')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_urls.update(extract_urls(soup, base_url))
        
        next_page = f"{section_url}?page={scroll_count+1}"
        driver.get(next_page)
        
    return all_urls

def get_attribute_newspaper(all_articles):
    article_date = []
    for x in all_articles:
        try:
            data = dict()
            article = newspaper.Article(url=x, language='en')
            article.download()
            article.parse()
            data['url'] = x
            data['datetime'] = article.publish_date
            data['title'] = article.title
            data['text'] = article.text
            data['source'] = "New York Times"
            article_date.append(data)
        except:
            pass
    return article_date

def transform(articles, result):
    df = pd.DataFrame(articles)
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    # print(df['date'])
    yesterday = datetime.now().date() - timedelta(days=1)
    new_df = df[df['datetime'].dt.date == yesterday]
    # print(new_df)
    result = pd.concat([result, new_df], ignore_index=True)
    return result

def main():
    base_url = 'https://www.nytimes.com'
    all_section_url = ['https://www.nytimes.com/news-event/economy-business-us', 'https://www.nytimes.com/section/politics', 'https://www.nytimes.com/international/section/business', 'https://www.nytimes.com/section/opinion/international-world']
    # section_url = f'{base_url}/section/politics'
    driver = setup_driver()
    
    try:
        result = pd.DataFrame(columns=['url', 'datetime', 'title', 'text', 'source'])
        for section_url in all_section_url:
            driver.get(section_url)
            scraped_urls = scroll_and_scrape(driver, base_url, section_url)
            print(f"Total scraped: {len(scraped_urls)}")

            articles = get_attribute_newspaper(scraped_urls)

            result = transform(articles, result)
        result["text"] = result["text"].str.replace("\n\n", "", regex=False) 
        result["text"] = result["text"].str.replace("\n", "", regex=False)
        print(result)
        return result
    finally:
        # input("Press Enter to exit...")  # Keeps the browser open for review
        driver.quit()

if __name__ == "__main__":
    main()
