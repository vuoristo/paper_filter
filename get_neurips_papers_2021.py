import requests
import collections
import string

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


YEAR = 2018
DEFAULT_KWS = [
    'meta','learning to learn','reinforcement','RL','few-shot','imitation',
    'transfer','lifelong','continual','partial observability','POMDP',
    'BAMDP','adaptation','generalization',
]

def parse_authors(text):
    authors = []
    for author in text.split('·'):
        authors.append(' '.join(author.strip().split()))
    authors = ', '.join(authors)
    return authors


def get_abstract(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.select_one('div.abstractContainer').text
    for ch in string.whitespace:
        text = text.replace(ch, ' ')
    return text


def get_papers_for_year(year, keywords):
    print('Getting all papers')
    r = requests.get(f'https://neurips.cc/Conferences/2021/Schedule?type=Poster')
    soup = BeautifulSoup(r.text, 'html.parser')
    paper_details = collections.defaultdict(list)
    print('Getting paper details')
    papercards = soup.select('div.maincard')
    failed_ids = []
    for card in tqdm(papercards):
        try:
            title = card.select_one('div.maincardBody').text
            authors = parse_authors(card.select_one('div.maincardFooter').text)
            paper_id = card.get('id')[9:]
            url = f'https://neurips.cc/Conferences/2021/Schedule?showEvent={paper_id}'
            abstract = get_abstract(url)
            paper_details['title'].append(title)
            paper_details['url'].append(url)
            paper_details['authors'].append(authors)
            paper_details['abstract'].append(abstract)
        except Exception as e:
            print("Failed getting details for")
            print(card)
            print(e)
            failed_ids.append(paper_id)
    print("Failed card ids")
    print(failed_ids)
    df = pd.DataFrame(paper_details)
    return df


df = get_papers_for_year(YEAR, DEFAULT_KWS)
df.to_csv(f'iclr_{YEAR}.csv')
