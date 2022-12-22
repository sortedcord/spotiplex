# # import requests
# # import json

# # send a GET request to 'https://api.deezer.com/search/artist/?q=eminem&index=0&limit=2&output=xml'

# url = 'https://api.deezer.com/search/track?q=willow&output=json'

# response = requests.get(url)

# # pretty print the JSON response
# print(json.dumps(response.json(), indent=4))

# from deezer.client import Client

# client = Client(access_token="frPi5RdI5xCzlQcZhXC8jjSvDnS3OhLo6NQzX8zB607bQG0o7B")

# print(client.search("mizuoto to curtain", artist="MIMI"))


from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

print(similar("ryos", "ryol"))