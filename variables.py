import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()


def variables(post, info):

    try:
        titles = post.find('p', class_='title')
        info['title'].append(post.find('div', class_='entry unvoted').div.p.text.split('(')[0])
    except Exception as e:
        info['title'].append('Unknown')
        #print(e)

    try:
        title_score = post.find('div', class_='entry unvoted').div.p.text.split('(')[0]
        pol_score = sia.polarity_scores(title_score)['compound']
        pol_score = 1 if pol_score > 0.2 else -1 if pol_score < -0.2 else 0
        info['titlescore'].append(pol_score)
    except Exception as e:
        info['titlescore'].append(0)
        #print(e)

    try:
        info['author'].append(post.find('a', class_='author').text)
    except Exception as e:
        info['author'].append('Unknown')
        #print(e)

    try:
        info['comments'].append(post.find('a', class_='comments').text.split()[0])
    except Exception as e:
        info['comments'].append('0')
        #print(e)

    try:
        info['scorelikes'].append(post.find('div', attrs={'class': 'score likes'}).text)
    except Exception as e:
        info['scorelikes'].append('0')
        #print(e)

    try:
        info['scoredislikes'].append(post.find('div', attrs={'class': 'score dislikes'}).text)
    except Exception as e:
        info['scoredislikes'].append('0')
        #print(e)

    try:
        info['dates'].append(re.findall(r'\d{4}-\d{2}-\w+:\d+:\d+\+\d+',
                                        post.find('p', attrs={'class': 'tagline'}).time.prettify())[0])
    except Exception as e:
        info['dates'].append('Unknown')
        #print(e)

    try:
        awards_i = post.find('span', class_='awardings-bar').prettify()
        award_count_list = [i.replace('data-count=', "").strip('"') for i in
                            re.findall(r'data-count="\d+\"', awards_i)]
        award_count_list = [int(i) for i in award_count_list]
        award_count = sum(award_count_list)
        info['awards'].append(award_count)
    except Exception as e:
        info['awards'].append(0)
        #print(e)

    try:
        if '(' not in titles.span.text:
            info['domain_tag'].append(titles.span.text)
        else:
            info['domain_tag'].append('Unknown')
    except Exception as e:
        info['domain_tag'].append('Unknown')
        #print(e)

    try:
        info['author_info'].append(post.find('span', class_='flair flair-seniorflair').text)
    except Exception as e:
        info['author_info'].append('Unknown')
        #print(e)

    try:
        info['thread'].append(post.find('div', class_='entry unvoted').div.p.text.split('(')[1]
                              .replace(')', ""))
    except Exception as e:
        info['thread'].append('Unknown')
        #print(e)

    try:
        info['spoilers'].append(re.findall('\W*(data-spoiler="\w+\")', post.prettify())[0]
                                .replace('data-spoiler="', "").replace('"', "").capitalize() == 'True')
    except Exception as e:
        info['spoilers'].append('Unknown')
        #print(e)

    try:
        info['promoted'].append(re.findall('\W*(data-promoted="\w+\")', post.prettify())[0]
                                .replace('data-promoted="', "").replace('"', "").capitalize() == 'True')
    except Exception as e:
        info['promoted'].append(False)
        #print(e)

    try:
        info['crossposts'].append(re.findall('\W*(data-num-crossposts="\w+\")', post.prettify())[0]
                                  .replace('data-num-crossposts=', "").replace('"', ""))
    except Exception as e:
        info['crossposts'].append(False)
        #print(e)

    try:
        info['postype'].append(re.findall('\W*(collapsed hide-when-pinned \S+\")', post.prettify())[0]
                               .replace('collapsed hide-when-pinned ', '').replace('"', ''))
    except Exception as e:
        info['postype'].append('Unknown')
        #print(e)
