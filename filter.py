# filter all the data from the json files after the h-indecies of their authors
import json
import os
from serpapi import GoogleSearch
import requests
from dotenv import load_dotenv

load_dotenv()

def get_articles_of_author(author_id):
    articles = []
    author_name = ''

    num_calls = 0

    isLastPage = False
    offset = 0
    while not isLastPage:
        if offset == 0:
            params = {
                "engine": "google_scholar_author",
                "author_id": author_id,
                "hl": "en",
                "api_key": os.getenv('SERP_API_KEY'),
                "start": offset * 20,
            }
            search = GoogleSearch(params)
            num_calls += 1
            results = search.get_dict()
        else:
            results = requests.get(results['serpapi_pagination']['next'])

        # if any articles do not have citations, prune them
        temp_articles = [article for article in results['articles']
                         if article['cited_by']['value'] != None]

        # if the search had uncited works, then it is the last page
        if len(temp_articles) != 20:
            isLastPage = True

        articles += temp_articles

        if offset == 0:
            author_name = results['author']['name']

        # increase offset
        offset += 1

    return articles, author_name, num_calls


def calculate_h_index(author_id):

    articles, author_name, num_calls = get_articles_of_author(author_id)

    # prune uncited articles
    articles = [
        article for article in articles if article['cited_by']['value'] != None]

    # sort articles by cited_by
    articles.sort(key=lambda x: x['cited_by']['value'], reverse=True)

    h_index = 0
    for article in articles:
        if article['cited_by']['value'] > h_index:
            h_index += 1
        else:
            break

    print(f'{author_name} has an h-index of {h_index} after {num_calls} calls')

    return h_index


def main():

    # find all files
    files = []
    for file in os.listdir():
        if file.startswith('results_'):
            files.append(file)

    articles = []
    # filter all the data from the json files after the h-indecies of their authors
    for file in files:
        with open(file) as item:
            data = json.load(item)
            articles += data['organic_results']


    with open('report.txt', 'w') as output:
        for idx, article in enumerate(articles):
            title = article['title']
            try:
                authors = article['publication_info']['authors']

                author_strings = []

                author_indices = []
                for author in authors:
                    name = author['name']
                    author_id = author['author_id']
                    h_index = calculate_h_index(author_id)
                    author_indices.append(h_index)

                    author_string = ' | '.join([name, author_id])
                    author_strings.append(author_string)

                authors = ', '.join(author_strings)
            except:
                authors = 'N/A'
                author_indices = [0]
            output.write(f'{idx+1}: {title}\n --- Authors: {authors} - max: {max(author_indices)} \n\n')

    return 0


if __name__ == '__main__':
    main()