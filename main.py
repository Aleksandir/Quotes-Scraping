import json
import os

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

    count = 1

    # Get all quotes from all pages until there is no next page.
    while url:
        # Clear the terminal based on the OS.
        os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal
        print(f"Scraping page {count}...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        all_quotes.extend(get_quotes_from_page(soup))

        next_button = soup.find(class_="next")
        url = (
            f"http://quotes.toscrape.com{next_button.find('a')['href']}"
            if next_button
            else None
        )
        count += 1

    save_quotes(all_quotes)


def get_quotes_from_page(soup) -> list:
    """
    Extracts quotes from a BeautifulSoup object representing a web page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the web page.

    Returns:
        list: A list of Quote objects, each containing the quote text, author, and tags.
    """
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


def save_quotes(quotes: list) -> None:
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
