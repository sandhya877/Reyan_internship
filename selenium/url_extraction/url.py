from googlesearch import search

query = "TWDG"  # Your search query

# Define search parameters
search_params = {
    "num_results": 10,  # Total number of results to retrieve
    "pause": 2.0,  # Time to wait between HTTP requests (adjust as needed)
    "extra_params": {"hl": "en"}  # Additional search parameters
}

# Perform the Google search
results = list(search(query, tld='com', lang='en', stop=search_params["num_results"], num=10, pause=search_params["pause"]))

# Print the search results
for idx, result in enumerate(results):
    print(f"Result {idx + 1}: {result}")
