# Reddit Web Scraper 

> An ITC Adventure : By Hanna Hier & Sebastian Kleiner

> What is **Israel Tech Challenge**? ITC opens the door for talented professionals from Israel and abroad to develop their careers in technology while focusing on the most in-demand skills in tech. Located in a beautiful campus in Tel Aviv, we offer our students intensive tech training in English, inspired by the IDF’s 8200 unit, and job placement assistance to our graduates. To date, we’ve introduced over 500 alumni to the Israeli hi-tech industry.

> This project will scrape, clean, and analyze this year's top Reddit posts pertaining to data science. 



## Table of Contents

- [Flowchart](#Flowchart)
- [Overview](#Overview)
- [Introduction](#Introduction)
- [GettingStarted](#GettingStarted)
- [Clone](#Clone)
- [Requirements](#Requirements)
- [Usage](#Usage)
- [UserInputs](#UserInputs)
- [Badges] (#Badges)
- [Team](#Team)
- [FAQ](#FAQ)

## Flowchart

![alt text](https://github.com/SebKleiner/Project_ITC_Data_Mining/blob/master/flowchart_webscraper.png?raw=true)

## Overview 

- The data is pulled from Reddit via a custom-Python crawler 
- Raw data is then cleaned and structured in Python
- Next, the data is written to a MySQL database 
- Basic exploration is implemented in Python using a PyMySQL connection
- The data is deployed on an EC2 instance in AWS
- Finally, the data is placed in ReDash for BI Analysis

---

## Introduction

This is a Reddit scraper that can scrape Subreddits. 

Written in Python and utilizes the official Reddit API `PRAW`.

Run `pip install -r requirements.txt` to get all project dependencies (see requirements). 

You will need your own Reddit account and API credentials for PRAW. See the [Getting Started](#getting-started) section for more information. 

***NOTE:*** `PRAW` is currently supported on Python 3.5+. This project was tested with Python 3.6.1. 

**Whether you are using URS for enterprise or personal use, I am very interested in hearing about your use cases and how it has helped you achieve a goal. Please send us an email or leave a note by clicking on the Email! badge. I look forward to hearing from you!**

---

## GettingStarted

It is very quick and easy to get Reddit API credentials. Refer to https://www.reddit.com/wiki/api to get your credentials, then update the configuration dictionary located in `config.json`

---
## Clone

Clone this repo to your local machine using `https://github.com/SebKleiner/Project_ITC_Data_Mining`

---

## Requirements

beautifulsoup4==4.9.1 \
logger==1.4 \
mysql==0.0.2 \
nltk==3.5 \
pandas==1.0.3 \
requests==2.24.0 \
pip~=20.1.1 \
setuptools~=46.1.3 \
fake_useragent==0.1.11 \
praw~=7.1.0

---

## Usage

Welcome to the Reddit Web Scraper! The default list to scrape is: ['DataScience', 'MachineLearning']

Go to your python command line inside the cloned folder and type: python main.py default --console=INFO as a default run.

For new reddit information added to the default list search, change 'default' for 'add' as a single word (ex: datascience instead of data science).

'custom' option let the user define which topics he wants to scrape avoiding default ones.

For details, please type -help in the argparse.

---

## UserInputs

param1=default : default , add , custom (option to add or customize topics to parse)
--topics=None : (each topic to be added / customized should be added seperately)
--c / --console=False : 'False', 'DEBUG', 'INFO', 'WARNING', 'ERROR' (option to set console logger level)
--s / --sleep=1 : 0, 1, 2 (option to set sleep time between URLs)

---


## Badges
> Warning: The following badges are for display purposes only and may be considered fake news as they do not reflect actual information about this page. 

[![Fake Coverage](https://camo.githubusercontent.com/3eff610e3559385c77a9b6d87cbe1252cab79a4d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f7665726167652d38302532352d79656c6c6f77677265656e)](https://travis-ci.org/badges/badgerbadgerbadger)  [![A Fake Rating](https://camo.githubusercontent.com/d5cd29c0e2930c3c4026ba87ff427e2e340f461b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f726174696e672d2545322539382538352545322539382538352545322539382538352545322539382538352545322539382538362d627269676874677265656e)](https://travis-ci.org/badges/badgerbadgerbadger)  [![A Fake 3rd Thing](https://camo.githubusercontent.com/b3fc74878a0d5fcca5a78b288aa4b489f65fd7eb/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f757074696d652d3130302532352d627269676874677265656e)](https://travis-ci.org/badges/badgerbadgerbadger)

---

## Team
 

Seb Kleiner: A fresh off the boat Argentinian pursing his life long dream of becoming a Data Scientist in Israel.

Hanna Hier: An aspiring ML Engineer trying to model some sense out of this crazy world.

YOU : The most important part of any project is the receiver! 

---

## FAQ

- **How do I know this project is going to be awesome?**
    - Here at Hanna & Seb, we take our user's satisfaction very seriously. We take great pride in our work, so you can rest assured that we will bring 100% to this project.


