import requests
import collections
import string

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
import pdfplumber
import io
import os
# from pyPdf import PdfFileReader



# YEAR = 2020
KW_IN_ABS = [
    'meta','learning to learn','few-shot','imitation',
    'transfer','lifelong','continual','partial observability','POMDP',
    'BAMDP','adaptation','generalization',
]
# KW_IN_PAPER = ['reinforce', 'reinforcement','RL']

# def parse_authors(text):
#     authors = []
#     for author in text.split('·'):
#         authors.append(' '.join(author.strip().split()))
#     authors = ', '.join(authors)
#     return authors

def get_text(url):
    r = requests.get(url)
    f = io.BytesIO(r.content)
    file_dir = os.path.dirname(os.path.realpath(__file__))
    temp_path = os.path.join(file_dir, "temp")
    with open(temp_path, 'wb') as f:
        f.write(r.content)
    text =  ""
    with pdfplumber.open(temp_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

    # reader = PdfFileReader(f)
    # contents = reader.getPage(0).extractText()
    # return contents

def get_abstract(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # text = soup.select_one('span.note-content-value').text
    # for ch in string.whitespace:
    #     text = text.replace(ch, ' ')
    abstract = soup.text.split("Abstract")[1].split("Name Change Policy")[0]
    return abstract


def get_papers_for_year(keywords):
    print('Getting all papers')
    r = requests.get("https://papers.nips.cc/paper/2019")
    soup = BeautifulSoup(r.text, 'html.parser')
    # import pdb; pdb.set_trace()
    # paper_details = collections.defaultdict(list)
    print(soup)
    final_papers = {}
    print('Getting paper details')
    papers = soup.findAll("li")[2:]
    i = 0
    for paper in tqdm(papers):
        i += 1
        #
        if i <= 350:
            continue
        #
        url_suffix = paper.select("a[href]")[0]["href"]
        paper_url = "https://papers.nips.cc" + url_suffix
        authors = paper("i")[0].text
        # import pdb; pdb.set_trace()
        # print("here")
        # title = card.select_one('div.maincardBody').text
        # # paper_details['title'].append(title)
        # url = card.select_one('a.href_PDF')['href']
        # # paper_details['url'].append(url)
        # authors = parse_authors(card.select_one('div.maincardFooter').text)
        # # paper_details['authors'].append(authors)
        abstract = get_abstract(paper_url)
        pdf_url = paper_url.replace("hash", "file").replace("-Abstract.html", "-Paper.pdf")
        # paper_text = get_text(pdf_url)
        # kew_words = get_abstract(url)
        # paper_details['abstract'].append(abstract)
        kw_found = False
        for kw in KW_IN_ABS:
            normalized_kw = '_'.join(kw.split())
            if (normalized_kw.lower() in abstract.lower()):
                kw_found = True
                print(kw)
                # print(abstract)
                # exit()
                break
        if not kw_found:
            continue
            # print("skipped:", paper.text)
        # rl_paper = False
        # for second_kw in KW_IN_PAPER:
        #     normalized_kw = '_'.join(second_kw.split())
        #     if (normalized_kw.lower() in paper_text.lower()):
        #         rl_paper = True
        #         break
        # if not rl_paper:
        #     continue
        paper_text = get_text(pdf_url)
        if paper_text.count("reinforce")  < 2:
            # print("probably not RL:", paper.text)
            continue

        final_papers[paper_url] = paper.text
        print(paper.text)
        print(paper_url)
    return final_papers


final_papers = get_papers_for_year(KW_IN_ABS)
print(final_papers)
# df.to_csv(f'iclr_{YEAR}.csv')
