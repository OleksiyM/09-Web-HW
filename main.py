import json
import re
import threading
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://quotes.toscrape.com'

authors = []

quotes = []

authors_url_list = []


def fetch_author_data(author_url):
    author_data = get_author(author_url)
    authors.append(author_data)


def check_quotes_integrity():
    for quote in quotes:
        author = quote['author']
        if author not in [a['fullname'] for a in authors]:
            quotes.remove(quote)
            print(f'    Error: Author "{author}" not found in quote:\n    {quote["quote"]}\n    This quote was removed')


def clean_text(text):
    text = text.strip()
    text = re.sub(r"\n", " ", text)  # Replace newlines with spaces
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # Remove control characters
    text = re.sub(r"[^\w\-.,\s]", "", text)  # Remove special characters except those allowed
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    return text


def get_url_list(start_url):
    urls_list = [BASE_URL]
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_page = soup.find('li', class_='next')

    while next_page:
        next_page_url = BASE_URL + next_page.a['href']
        urls_list.append(next_page_url)
        # print(url_list, next_page_url)
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.find('li', class_='next')
    return urls_list


def get_quote(data):
    container = data
    quote = container.span.text
    quote = clean_text(quote)
    author = container.find('small', class_='author').text
    author = clean_text(author)
    all_tags = container.find_all('a', class_='tag')
    tags = [tag.text for tag in all_tags]
    # clean tags
    tags = [clean_text(tag) for tag in tags if tag]  # Remove empty tags
    tags = list(set(tags))  # Remove duplicate tags
    tags.sort()  # Sort tags alphabetically
    return {"tags": tags, "author": author, "quote": quote}


def get_author_url(data):
    container = data
    # author = container.find('small', class_='author').text
    current_author_url = BASE_URL + container.find('a')['href']
    return current_author_url


def get_author(current_author_url):
    response = requests.get(current_author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fullname = soup.find('h3', class_='author-title').text
    fullname = clean_text(fullname)
    born_date = soup.find('span', class_='author-born-date').text
    born_date = clean_text(born_date)
    born_location = soup.find('span', class_='author-born-location').text
    born_location = clean_text(born_location)
    born_location = born_location[3:] if born_location.startswith('in') else born_location
    description = soup.find('div', class_='author-description').text
    description = clean_text(description)

    return {"fullname": fullname, "born_date": born_date, "born_location": born_location, "description": description}


def page_spider(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    containers = soup.find_all("div", attrs={"class": "quote"})
    for container in containers:
        quotes.append(get_quote(container))
        current_author_url = get_author_url(container)
        if current_author_url not in authors_url_list:
            authors_url_list.append(current_author_url)


def main():
    print(f'Getting url list from {BASE_URL}')
    url_list = get_url_list(BASE_URL)
    print('Getting quotes')
    q_threads = []
    for url in url_list:
        # page_spider(url)
        q_thread = threading.Thread(target=page_spider, args=(url,))
        q_threads.append(q_thread)
        q_thread.start()

    for q_thread in q_threads:
        q_thread.join()

    print('Getting authors')
    threads = []
    for author_url in authors_url_list:
        thread = threading.Thread(target=fetch_author_data, args=(author_url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # for author_url in authors_url_list:
    #    authors.append(get_author(author_url))

    print('Checking quotes integrity')
    check_quotes_integrity()

    print(f'Writing data to the files: \n- quotes: {len(quotes)}\n- authors: {len(authors)}')

    with open('quotes.json', 'w') as f:
        json.dump(quotes, f, indent=2)

    with open('authors.json', 'w') as f:
        json.dump(authors, f, indent=2)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f'Done in {end - start:.2f} sec')
