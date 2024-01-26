# Scraper and Parser

## Overview

This project scrapes quotes and author information from the website [https://quotes.toscrape.com](https://quotes.toscrape.com) and stores the collected data in separate JSON files. It utilizes the `requests` library for making HTTP requests and `BeautifulSoup4` for parsing HTML content.

## Features

* Scrapes quotes, tags, and author names from the website.
* Follows links to author pages to extract additional author details.
* Cleans and processes the extracted data.
* Stores the collected quotes in `quotes.json` and author information in `authors.json`.
* Employs multithreading to speed up the scraping process.
* Performs error handling to ensure data integrity.

## Installation

### Prerequisites

* Python 3.11 or newer
* Poetry (package manager)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/OleksiyM/09-web-hw.git
   ```

2. Navigate to the project directory:

   ```bash
   cd 09-web-hw
   ```

3. Install dependencies:

   ```bash
   poetry install --no-root
   ```

4. Activate the virtual environment (if using Poetry):

   ```bash
   poetry shell
   ```

## Usage

1. Run the main script:

   ```bash
   python main.py
   ```

2. The scraped data will be stored in the `quotes.json` and `authors.json` files.

## Project Structure

* `main.py`: The main script that runs the scraper.
* `poetry.toml` and `pyproject.toml`: Poetry configuration files.
* `quotes.json`: Output file containing scraped quotes.
* `authors.json`: Output file containing scraped author information.

## Technologies Used

* Python
* Requests
* Beautiful Soup 4 (bs4)
* Poetry
* Threading
* JSON

## Threading

This project leverages multithreading to enhance performance and efficiency during the scraping process. It employs the Python `threading` module to execute tasks concurrently:

- **Quotes Extraction:** The `page_spider` function, responsible for extracting quotes from individual pages, is run in separate threads. This allows multiple pages to be processed simultaneously, leading to faster overall scraping.
- **Author Information Retrieval:** The `fetch_author_data` function, which fetches author details from their respective pages, is also executed in parallel threads. This expedites the collection of author information.

By utilizing multithreading, the project optimizes resource utilization and achieves a more streamlined scraping workflow.
