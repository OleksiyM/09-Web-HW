import json


with open('quotes.json', 'r') as file:
    quotes = json.load(file)

with open('authors.json', 'r') as f:
    authors = json.load(f)

# Create a set of all author fullnames for faster lookup
author_fullnames = {author['fullname'] for author in authors}

# Filter out quotes with authors not in authors.json
filtered_quotes = [quote for quote in quotes if quote['author'] in author_fullnames]

# If a quote was removed, print an error
if len(quotes) != len(filtered_quotes):
    print("Error: Some quotes were removed because their authors were not found in authors.json")
else:
    print("No errors found")

# Save the filtered quotes back to quotes.json
with open('quotes.json', 'w') as file:
    json.dump(filtered_quotes, file, indent=2)