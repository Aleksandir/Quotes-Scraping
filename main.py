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
    # get website page
    response = requests.get(url)

    # parse through html
    soup = BeautifulSoup(response.text, "html.parser")

    # get all quote elements
    soup_quotes = soup.find_all(class_="quote")

    # for each quote element, get quote text, author, and tags, and append to quotes list
    quotes = []
    for quote in soup_quotes:
        # get quote text and remove “ and ”
        quote_text = (
            quote.find(class_="text").get_text().replace("“", "").replace("”", "")
        )
        quote_author = quote.find(class_="author").get_text()

        # get tags, remove empty tags, and append to processed_tags
        tags = quote.find(class_="tags")
        processed_tags = []
        for tag in tags:
            tag_text = tag.get_text().strip()
            if tag_text:  # if tag_text is not empty
                processed_tags.append(tag_text)

        quote = Quote(quote_text, quote_author, processed_tags)
        quotes.append(quote)

    save_quotes(quotes)


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
