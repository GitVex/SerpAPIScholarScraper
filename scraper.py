from serpapi import GoogleSearch
import json
import datetime
import sys
import os
from dotenv import load_dotenv

load_dotenv()

offset = int(sys.argv[1])
query = "+long-term-memory in artifical intelligence for natural language processing -isbn +doi",
num_results = 20

params = {
  "engine": "google_scholar",
  "q": query,
  "api_key": os.getenv('SERP_API_KEY'),
  "as_ylo": "2022",
  "start": offset * num_results,
  "num": num_results
}

search = GoogleSearch(params)
results = search.get_dict()
# get organic results as dict
organic_results = results['organic_results']

# write to json
with open(f'results_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json', 'w') as outfile:
    # prepend parameter info to organic_results
    search_results = {
        'search_parameters': params,
        'organic_results': organic_results
    }
    json.dump(search_results, outfile)