import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


def get_rating_count(soup):
    try:
        rating = soup.find('span', attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except:
        rating = ""
    return rating


def get_title(soup):
    try:
        title = soup.find('span', attrs={"id": 'productTitle'}).text.strip()
    except:
        title = ""
    return title


def get_price(soup):
    try:
        price = soup.find('span', attrs={'class': 'a-price aok-align-center'}).find('span',
                                                                                    attrs={'class': 'a-offscreen'}).text
    except:
        price = ""

    return price


if __name__ == '__main__':
    # Header Request
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/122.0.0.0 Safari/537.36', 'Accept-Language': 'en-US en;q=0.5'})

    # Web URL
    URL = "https://www.amazon.com/s?k=smartphones&crid=3881WWLHKK3VQ&sprefix=smartph%2Caps%2C402&ref=nb_sb_ss_ts-doa" \
          "-p_2_7"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Beautiful Soup
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetching the links
    links = soup.find_all("a", attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    product_links = []
    for link in links:
        product_links.append("https://www.amazon.com" + link.get('href'))

    data = {'title': [], 'price': [], 'rating': []}

    for product in product_links:
        new_webpage = requests.get(product, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        data['title'].append(get_title(new_soup))
        data['price'].append(get_price(new_soup))
        data['rating'].append(get_rating_count(new_soup))

    product_df = pd.DataFrame.from_dict(data)
    product_df.replace({'title': np.nan}, inplace=True)
    product_df = product_df.dropna(subset=['title'])
    print(product_df)
