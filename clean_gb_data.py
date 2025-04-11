
import pandas as pd 
import matplotlib as plt

gb_videos='data/GBvideos.csv' 
gb_comments='data/GBcomments.csv'

df_gb_videos = pd.read_csv(gb_videos, on_bad_lines='skip')
df_gb_comments = pd.read_csv(gb_comments, on_bad_lines='skip')

print(f"Shape of videos: {df_gb_videos.shape}") # (4096, 11) - this is good as there are 11 columns
print(f"Shape of comments: {df_gb_comments.shape}") # (408000, 4) - this is good as there are 4 columns

print(f"\nNumber of nulls in {gb_videos}:\n{df_gb_videos.isnull().sum()}") # showing 0 for all columns, no nulls
print(f"\nNumber of nulls in {gb_comments}:\n{df_gb_comments.isnull().sum()}") # showing 0 for all columns, no nulls

