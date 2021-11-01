import requests
import collections
import string

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


YEAR = 2017


def parse_authors(text):
    authors = []
    for author in text.split('·'):
        authors.append(' '.join(author.strip().split()))
    authors = ', '.join(authors)
    return authors


def get_abstract(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.select_one('div.abstract').text
    for ch in string.whitespace:
        text = text.replace(ch, ' ')
    return text


def get_papers_for_year():
    print('Getting all papers')
    r = requests.get(f'https://icml.cc/Conferences/{YEAR}/Schedule?type=Poster')
    soup = BeautifulSoup(r.text, 'html.parser')
    paper_details = collections.defaultdict(list)
    print('Getting paper details')
    papercards = soup.select('div.maincard')
    for card in tqdm(papercards):
        try:
            title = card.select_one('div.maincardBody').text
            url = card.select_one('a.href_PDF')['href']
            authors = parse_authors(card.select_one('div.maincardFooter').text)
            abstract = get_abstract(url)
            paper_details['title'].append(title)
            paper_details['url'].append(url)
            paper_details['authors'].append(authors)
            paper_details['abstract'].append(abstract)
        except Exception as e:
            print("Failed getting details for")
            print(card)
            print(e)
    df = pd.DataFrame(paper_details)
    return df

df = get_papers_for_year()
df.to_csv(f'icml_{YEAR}.csv')
