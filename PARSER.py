import time
import variables
import get_info
import next_url


def html_data(urls, keys):
    """
    This function, given an old.reddit.com thread, a list of users to randomly access, the number of pages and the
    fields to get, extracts the information required.
    :param urls: list of urls to consider
    :param user_agent_list: list of user agents to randomly rotate
    :param keys: list of keys to extract
    :return: dictionary with lists containing the information of each key
    """

    forums = []

    for url in urls:

        unfinished = True

        url = 'https://old.reddit.com/r/' + url + '/top/?sort=top&t=all'

        users = {word: [] for word in keys}  # dictionary initialization

        while unfinished:

            soup, posts = get_info.get_info(url)

            info = {key: [] for key in keys}  # inner dictionary to store each page information

            for post in posts:  # looping inside the information extracted in each page
                variables.variables(post, info)

            for key in keys:  # updating the users dictionary
                users[key] += info[key]

            url, unfinished = next_url.next_url(url, soup, unfinished)

            time.sleep(1)

        forums.append(users)

    return forums
