
def get_all_url(base_url):
    import requests
    from bs4 import BeautifulSoup

    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    list_content = soup.find_all('a', {'class': 'css-8hzhxf'})
    http_url = 'https://www.nytimes.com'

    url_date = []
    for content in list_content:
        url = f"{http_url}{content['href']}"
        url_date.append(url)

    filtered_url = set(url_date)
    return filtered_url

def get_article_attributes(filtered_url):
    import newspaper
    article_date = []
    for x in filtered_url:
        try:
            data = dict()
            article = newspaper.Article(url=x, language='en')
            article.download()
            article.parse()
            date = article.publish_date
            title = article.title
            text = article.text
            source = 'cnn'
            data['url'] = x
            data['date'] = date
            data['title'] = title
            data['text'] = text
            data['source'] = source
            article_date.append(data)
        except Exception as e:
            print(f"Error : {e}")
    return article_date

def main():
    base_url = 'https://www.nytimes.com/section/politics'
    urls = get_all_url(base_url)
    print(urls)
    print(len(urls))
    # articles = get_article_attributes(urls)
    # print(articles)

main()