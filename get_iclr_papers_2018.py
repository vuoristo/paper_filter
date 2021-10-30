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
    text = soup.select_one('span.note-content-value').text
    for ch in string.whitespace:
        text = text.replace(ch, ' ')
    return text


def get_papers_for_year(year, keywords):
    print('Getting all papers')
    r = requests.get(f'https://iclr.cc/Conferences/{year}/AcceptedPapersInitial')
    soup = BeautifulSoup(r.text, 'html.parser')
    paper_details = collections.defaultdict(list)
    print('Getting paper details')
    papercards = soup.select('div.maincard')
    for card in tqdm(papercards):
        title = card.select_one('div.maincardBody').text
        paper_details['title'].append(title)
        url = card.select_one('a.href_PDF')['href']
        paper_details['url'].append(url)
        authors = parse_authors(card.select_one('div.maincardFooter').text)
        paper_details['authors'].append(authors)
        abstract = get_abstract(url)
        paper_details['abstract'].append(abstract)
        for kw in keywords:
            normalized_kw = '_'.join(kw.split())
            paper_details[f'in_title_{normalized_kw}'].append(kw in title)
            paper_details[f'in_abstract_{normalized_kw}'].append(kw in abstract)
    df = pd.DataFrame(paper_details)
    return df


df = get_papers_for_year(YEAR, DEFAULT_KWS)
df.to_csv(f'iclr_{YEAR}.csv')
