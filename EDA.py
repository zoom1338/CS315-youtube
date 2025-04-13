import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

gb_videos='data/GBvideos_clean.csv'
gb_comments='data/GBcomments_clean.csv'

df_gb_videos = pd.read_csv(gb_videos, on_bad_lines='skip')
df_gb_comments = pd.read_csv(gb_comments, on_bad_lines='skip')

#print(df_gb_videos.head(5))# Display the first 5 rows of the videos dataframe

print("TOP 10 VIDEOS BY VIEWS")
top_10_videos_views = df_gb_videos.nlargest(10, 'views')
print(top_10_videos_views[['video_id','title', 'views']],'\n') # Display the top 10 videos by views


print("TOP 10 VIDEOS BY LIKES")
top_10_videos_likes = df_gb_videos.nlargest(10, 'likes')
print(top_10_videos_likes[['video_id','title', 'likes']],'\n') # Display the top 10 videos by likes


print("\nTOP 10 CHANNELS BY VIEWS")
top_10_channels_views = df_gb_videos.groupby('channel_title')['views'].sum().nlargest(10)
print(top_10_channels_views,'\n') # Display the top 10 channels by total views

print("\nTOP 10 CHANNELS BY LIKES")
top_10_channels_likes = df_gb_videos.groupby('channel_title')['likes'].sum().nlargest(10)
print(top_10_channels_likes,'\n') # Display the top 10 channels by total likes

