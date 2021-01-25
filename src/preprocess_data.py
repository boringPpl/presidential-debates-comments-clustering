#!/usr/bin/env python

import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


def load_comments(video_id):
    filename = f'data/{video_id}_csv_final.csv'
    df = pd.read_csv(filename, index_col=0)
    return df


if __name__ == '__main__':
    print('Loading comments...')
    df1 = load_comments('bPiofmZGb8o')['Comments']
    print(df1.head())

    print('Loading bert-base-nli-mean-tokens')
    embedder = SentenceTransformer('bert-base-nli-mean-tokens')
