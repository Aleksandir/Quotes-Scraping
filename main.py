import json

import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"


class Quote:
    """
    Represents a quote with its author and tags.
    """

    def __init__(self, quote, author, tags):
        self.quote = quote
        self.author = author
        self.tags = tags

    def __repr__(self):
        return f"{self.quote} - {self.author}"


def main():
    all_quotes = []
    url = "http://quotes.toscrape.com"

    while True:
        all_quotes.extend(get_quotes_from_page(url))
        next_button = BeautifulSoup(requests.get(url).text, "html.parser").find(
            class_="next"
        )
        if next_button is None:
            break
        url = f"http://quotes.toscrape.com{next_button.find('a')['href']}"

    save_quotes(all_quotes)


def get_quotes_from_page(url) -> list:
    """
    Get quotes from a page.

    Args:
        url (str): URL of the page.

    Returns:
        list: List of Quote objects.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    soup_quotes = soup.find_all(class_="quote")

    quotes = []
    for quote in soup_quotes:
        quote_text = (
            quote.find(class_="text").get_text().replace("“", "").replace("”", "")
        )
        quote_author = quote.find(class_="author").get_text()

        tags = quote.find(class_="tags")
        processed_tags = []
        for tag in tags:
            tag_text = tag.get_text().strip()
            if tag_text:
                processed_tags.append(tag_text)

        quote = Quote(quote_text, quote_author, processed_tags)
        quotes.append(quote)

    return quotes


def save_quotes(quotes):
    """
    Save quotes to a JSON file.

    Args:
        quotes (list): List of Quote objects.

    Returns:
        None
    """
    quotes_list = []
    for quote in quotes:
        quote_dict = {
            "quote": quote.quote,
            "author": quote.author,
            "tags": quote.tags,
        }
        quotes_list.append(quote_dict)

    with open("quotes.json", "w") as f:
        json.dump(quotes_list, f, indent=4)


if __name__ == "__main__":
    main()
