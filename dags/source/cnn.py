def get_all_url(base_url):
    import requests
    from bs4 import BeautifulSoup

    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    list_content = soup.find_all('a', {'class': 'container__link'})
    http_url = 'https://edition.cnn.com'

    url_date = []
    for content in list_content:
        data = dict()
        url = f"{http_url}{content['href']}"
        url_date.append(url)

    filtered_url = set(url_date)
    return filtered_url

def transform(url_article):
    # Transform datetime EST to UTC + 7
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    res = requests.get(url_article)
    soup = BeautifulSoup(res.text, 'html.parser')
    datetime_ = soup.find('div', {'class': 'timestamp'}).text
    datetime_ = datetime_.strip()
    datetime_ = datetime_.split("  ")
    date_new = datetime_[4]
    date_est = datetime.strptime(date_new, "%H:%M %p EST, %a %B %d, %Y")

    import pytz
    est = pytz.timezone("US/Eastern")
    jakarta = pytz.timezone("Asia/Jakarta")

    est_time = est.localize(date_est)
    jakarta_time = est_time.astimezone(jakarta)
    dt_wib = jakarta_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return dt_wib

def get_article_attributes(filtered_url):
    import newspaper
    article_date = []
    for x in filtered_url:
        try:
            data = dict()
            article = newspaper.Article(url=x, language='en')
            article.download()
            article.parse()
            date = transform(x)
            title = article.title
            text = article.text
            source = 'cnn'
            data['url'] = x
            data['datetime'] = date
            data['title'] = title
            data['text'] = text
            data['source'] = source
            article_date.append(data)
        except:
            pass
    return article_date

def main():
    from datetime import datetime, timedelta
    import pandas as pd

    list_category_url = ['https://edition.cnn.com/politics', 'https://edition.cnn.com/business', 'https://edition.cnn.com/business/investing']
    result = pd.DataFrame(columns=['url', 'datetime', 'title', 'text', 'source'])
    for base_url in list_category_url:

        urls = get_all_url(base_url)
        articles = get_article_attributes(urls)

        df = pd.DataFrame(articles)
        df['datetime'] = pd.to_datetime(df['datetime'])
        # print(df['date'])
        yesterday = datetime.now().date() - timedelta(days=7)
        new_df = df[df['datetime'].dt.date >= yesterday]
        # print(new_df)
        result = pd.concat([result, new_df], ignore_index=True)

    # Cleaning text column
    result["text"] = result["text"].str.replace("\n\n", "", regex=False) 
    result["text"] = result["text"].str.replace("\n", "", regex=False)
    result["text"] = result["text"].str.replace('CNN —', "", regex=False)
    print(result)
    print(result['datetime'])
    print(result['text'])
    return result