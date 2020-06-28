import random
import PROXIES
from bs4 import BeautifulSoup
import requests
import USER_AGENT


def get_info(url):

    proxy = random.choice(PROXIES.proxies_pool())
    user_agent = USER_AGENT.get_user_agent()
    headers = {'User-Agent': user_agent}
    proxies = {'proxies': proxy}
    attrs = {'class': 'thing'}
    html = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(html.text, 'html.parser')  # calling the url with beautiful soup
    posts = soup.find_all('div', attrs=attrs)

    return soup, posts
