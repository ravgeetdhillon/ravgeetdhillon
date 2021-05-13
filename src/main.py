"""
Module to create README for Github Profile.
"""

import io
import json
import re
from datetime import datetime
import requests


def create_readme():
    """
    Creates the Readme.md from the Readme template.
    """

    readme = io.open('../readme.md', 'w+')
    for line in io.open('readme.template.md', 'r'):
        line = line.replace('{{age}}', get_age('1998-04-19'))
        line = line.replace('{{last_updated}}', get_last_updated())
        line = line.replace('{{blog_words_written}}',
                            get_number_of_words_written())
        readme.write(line)
    readme.close()


def get_number_of_words_written():
    """
    Returns the number of words written by scraping the feed.
    """

    feeds = ['https://www.ravsam.in/blog/feed.json',
             'https://www.ravgeet.in/blog/feed.json']

    word_count = 0

    for feed_url in feeds:
        feed = json.loads(requests.get(feed_url).content)
        for blog in feed['items']:
            content = re.sub(r'[^A-Za-z0-9 ]+', '', blog['content_html'])
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
