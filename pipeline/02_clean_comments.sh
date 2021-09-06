#!/bin/bash
cd ../data/

cat << EOF > clean_comments.py
#!/usr/bin/env python

import argparse
import emoji
import numpy as np
import pandas as pd


from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


def load_comments(filename):
    """
    Loads Comments from .feather / .parquet file
    """
    if filename.endswith('.feather'):
        df = pd.read_feather(filename)
    else:
        assert filename.endswith('.parquet')
        df = pd.read_parquet(filename)

    df['Updated At'] = pd.to_datetime(df['Updated At'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
    df.rename(columns={'Comments': 'comment_text'}, inplace=True)
    return df


def clean_comments(df):
    # 1. Remove emojis
    df['comments_cleaned'] = df['comment_text'].apply(emoji.demojize)

    # 2. Replace the colons, and \n with a space
    df['comments_cleaned'] = df['comments_cleaned'].str.replace('[\n:]', ' ', regex=True)
    df['comments_cleaned'] = df['comments_cleaned'].str.replace(r'\\n', ' ', regex=True)

    # 3. Change to lower case
    df['comments_cleaned'] = df['comments_cleaned'].str.lower()

    # 4. Remove special characters
    df['comments_cleaned'] = df['comments_cleaned'].str.replace('[^a-zA-Z0-9]', ' ', regex=True)

    # 5. Replace repeated white space with a single space
    df['comments_cleaned'] = df['comments_cleaned'].str.replace('\s+', ' ', regex=True)

    # 6. Remove starting / trailing white space
    df['comments_cleaned'] = df['comments_cleaned'].str.strip()

    # 7. Drop duplicates
    df.drop_duplicates(subset=['comments_cleaned'], inplace = True)
    return df


def show_df_info(df):
    print(f'The shape of the dataframe is: {df.shape}')
    print(f"The time range for the data is: {df['Updated At'].min():%Y-%m-%d %H%Mh} to {df['Updated At'].max():%Y-%m-%d %H%Mh}")
    print()
    print(df['comments_cleaned'].apply(len).sort_values(ascending=False).head(20))


def write_df(df, basename):
    # Save metadata in .tsv and .parquet formats
    df['comments_cleaned'].to_csv(f'{basename}.tsv', columns=['comments_cleaned'], index= False, header= False)
    df[['comments_cleaned']].to_parquet(f'{basename}.parquet', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Usage:\npython3 clean_comments.py [wW1lY5jFNcQ|bPiofmZGb8o]')
    parser.add_argument("video_id")
    args = parser.parse_args()

    filename = f'{args.video_id}_csv_final.parquet'
    df = load_comments(filename)
    df = clean_comments(df)
    write_df(df, f'meta_{args.video_id}')

    show_df_info(df)
EOF

for video_id in bPiofmZGb8o wW1lY5jFNcQ; do
    echo "----- Video ID: ${video_id} -----"
    python3 clean_comments.py wW1lY5jFNcQ
done
rm clean_comments.py
