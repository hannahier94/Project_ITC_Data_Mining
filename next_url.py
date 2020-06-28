def next_url(url, soup, unfinished):
    try:
        next_button = soup.find('span', class_='next-button')  # keeping the next url for the next loop
        url = next_button.find('a').attrs['href']
        print('Next page')
    except Exception as e:
        print(f'inished {url}')
        unfinished = False

    return url, unfinished
