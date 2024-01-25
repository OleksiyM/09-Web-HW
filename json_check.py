import json

need_write = False

with open('quotes.json') as quotes_file:
    quotes = json.load(quotes_file)

with open('authors.json') as authors_file:
    authors = json.load(authors_file)

for quote in quotes:
    author = quote['author']
    if author not in [a['fullname'] for a in authors]:
        quotes.remove(quote)
        need_write = True
        print(f"Error: Author {author} not found")

if need_write:
    with open('quotes.json', 'w') as quotes_file:
        json.dump(quotes, quotes_file, indent=2)
    print("Updated quotes.json with valid data")
else:
    print('Data valid, quotes.json not changed')
