# from selenium import webdriver

# website = 'https://www.adamchoi.co.uk/overs/detailed'
# driver = webdriver.Chrome()
# driver.get(website)

# input("Press Enter to exit...")  # Keeps the browser open
# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_quotes(url):
   # Set up the Selenium WebDriver
   driver = (
       webdriver.Chrome()
   )  # Make sure you have chromedriver installed and in your PATH
   driver.get(url)


   # Wait for the initial content to load
   WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, "quote"))
   )


   # Extract and print initial data
   initial_html = driver.page_source
   initial_soup = BeautifulSoup(initial_html, "html.parser")
   initial_quotes = initial_soup.find_all("div", class_="quote")
   extract_and_print_quotes(initial_quotes)


   # Simulate scroll events to load additional content
   for scroll_count in range(4):  # Assuming there are 5 scroll events in total
       # Scroll down using JavaScript
       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


       # Wait for the dynamically loaded content to appear
       WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.CLASS_NAME, "quote"))
       )


       # Extract and print the newly loaded quotes
       scroll_html = driver.page_source
       scroll_soup = BeautifulSoup(scroll_html, "html.parser")
       scroll_quotes = scroll_soup.find_all("div", class_="quote")
       extract_and_print_quotes(scroll_quotes)


   # Close the WebDriver
   driver.quit()

def extract_and_print_quotes(quotes):
 
   for quote in quotes:
       text = quote.find("span", class_="text").get_text(strip=True)
       author = quote.find("small", class_="author").get_text(strip=True)
       tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]


       print(f"Quote: {text}")
       print(f"Author: {author}")
       print(f"Tags: {', '.join(tags)}")
       print("----------")

if __name__ == "__main__":
   target_url = "http://quotes.toscrape.com/scroll"
   scrape_quotes(target_url)




website = 'https://www.nytimes.com/section/politics'
driver = webdriver.Chrome()
driver.get(website)

initial_html = driver.page_source
soup = BeautifulSoup(initial_html, 'html.parser')

for scroll_count in range(1, 5):  # Assuming there are 5 scroll events in total
    # Scroll down using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the dynamically loaded content to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1l4spti')))
    list_content = soup.find_all('a', {'class' : 'css-8hzhxf'})
    http_url = 'https://www.nytimes.com'
    url_date = []

    for content in list_content:
        data = dict()
        url = f"{http_url}{content['href']}"
        url_date.append(url)

    filtered_url = set(url_date)
    
    page = f'?page={scroll_count+1}'

    website = f'https://www.nytimes.com/section/politics{page}'
    driver = webdriver.Chrome()
    driver.get(website)

    initial_html = driver.page_source
    soup = BeautifulSoup(initial_html, 'html.parser')

print(filtered_url)
print(len(filtered_url))

input("Press Enter to exit...")  # Keeps the browser open
driver.quit()