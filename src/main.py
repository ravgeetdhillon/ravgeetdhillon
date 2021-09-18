"""
Module to create README for Github Profile.
"""

import io
import json
import re
from datetime import datetime

import atoma
import requests


def create_readme():
    """
    Creates the Readme.md from the Readme template.
    """

    age = get_age('1998-04-19')
    last_updated_at = get_last_updated()
    number_of_words = get_number_of_words_written()

    readme = io.open('readme.md', 'w+')
    for line in io.open('src/readme.template.md', 'r'):
        line = line.replace('{{age}}', age)
        line = line.replace('{{last_updated}}', last_updated_at)
        line = line.replace('{{blog_words_written}}', number_of_words)
        readme.write(line)
    readme.close()


def get_number_of_words_written():
    """
    Returns the number of words written by scraping the feed.
    """

    feeds = ['https://blog.ravgeet.in/rss.xml']

    word_count = 0

    for feed_url in feeds:
        response = requests.get(feed_url)
        feed = atoma.parse_rss_bytes(response.content)
        for blog in feed.items:
            content = re.sub(r'[^A-Za-z0-9 ]+', '', blog.description)
            content = content.split(' ')
            word_count += len(content)

    return str(word_count)


def get_age(dob):
    """
    Returns the age of the entity.
    """

    now = datetime.now()
    dob = datetime.strptime(dob, '%Y-%m-%d')
    age = (now - dob).days
    return str(age)


def get_last_updated():
    """
    Returns the last updated date.
    """

    now = datetime.now()
    return datetime.strftime(now, '%d %b, %Y')


def main():
    """
    Main function for the Module.
    """

    create_readme()


if __name__ == '__main__':
    main()
