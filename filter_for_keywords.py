import os
import argparse
import collections

import pandas as pd

DEFAULT_KWS = [
    'meta','learning to learn','reinforcement','RL','few-shot','imitation',
    'transfer','lifelong','continual','partial observability','POMDP',
    'BAMDP','adaptation','generalization',
]


def match_keywords(df):
    for kw in DEFAULT_KWS:
        normalized_kw = '_'.join(kw.split())
        df[f"{normalized_kw}_in_title"] = df.apply(
            lambda x: kw.lower() in x.title.lower(), axis=1)
        df[f"{normalized_kw}_in_abstract"] = df.apply(
            lambda x: kw.lower() in x.abstract.lower(), axis=1)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    df = pd.read_csv(args.file, index_col=0)
    match_df = match_keywords(df)
    filename = os.path.splitext(os.path.basename(args.file))
    match_df.to_csv(f"{filename[0]}_with_keywords.csv")
