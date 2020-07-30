URLS = ['MachineLearning']

POST_KEYS = ['postid','domain_tag', 'title', 'awards', 'author', 'comments', 'scorelikes', 'scoredislikes', 'dates',
        'thread', 'spoilers', 'promoted', 'crossposts', 'postype', 'titlescore']

USER_KEYS = ['username', 'total_posts', 'total_comments', 'user_since', 'trophies']


CREATE_TABLE_STATEMENTS = [
"""
CREATE TABLE `search` (
  `search_id` int PRIMARY KEY,
  `date` timestamp,
  `tag` varchar(255)
);
""",
"""
CREATE TABLE `posts` (
  `post_id` varchar(255) PRIMARY KEY,
  `author_id` int,
  `search_id` int,
  `domain_tag` varchar(255),
  `title` text,
  `awards` int,
  `comments` varchar(255),
  `scorelikes` varchar(255),
  `scoredislikes` varchar(255),
  `post_date` timestamp,
  `thread` varchar(255),
  `topic` varchar(255),
  `promoted` boolean,
  `crossposts` boolean,
  `postype` varchar(255),
  `scrape_date` timestamp
);
""",
"""

CREATE TABLE `authors` (
  `author_id` varchar(255) PRIMARY KEY,
  `user_since` timestamp,
  `total_posts` int,
  `total_comments` int,
  `trophies` int
);

ALTER TABLE `posts` ADD FOREIGN KEY (`search_id`) REFERENCES `search` (`search_id`);

ALTER TABLE `posts` ADD FOREIGN KEY (`author_id`) REFERENCES `authors` (`author_id`);
"""]

MAGIC_ZERO = 0
MAGIC_ONE = 1
MAGIC_TWO = 2
