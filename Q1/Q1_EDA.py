# EDA for Q1
# Which engagement metrics, like views, comments, dislikes, and likes, correlate strongly with a video’s trending status?
#contributions to code from Isabella Sunderman
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


# Analysis conducted on Great Brittian data

gb_videos='data/GBvideos_clean.csv'
gb_comments='data/GBcomments_clean.csv'

df_gb_videos = pd.read_csv(gb_videos, on_bad_lines='skip')
df_gb_comments = pd.read_csv(gb_comments, on_bad_lines='skip')

print(df_gb_videos.columns) # Display the columns of the videos dataframe
#print(df_gb_videos.head(5))# Display the first 5 rows of the videos dataframe

# TOP 10 VIDEOS BY VIEWS
print("TOP 10 VIDEOS BY VIEWS")
top_10_videos_views = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'views': 'max'})  # Keep the first title and the max views
    .nlargest(10, 'views')  # Select the top 10 by views
)
print(top_10_videos_views[['video_id', 'title', 'views']], '\n')  # Display the top 10 videos by views

# TOP 10 VIDEOS BY LIKES
print("TOP 10 VIDEOS BY LIKES")
top_10_videos_likes = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'likes': 'max'})  # Keep the first title and the max likes
    .nlargest(10, 'likes')  # Select the top 10 by likes
)
print(top_10_videos_likes[['video_id', 'title', 'likes']], '\n')  # Display the top 10 videos by likes

# TOP 10 VIDEOS BY DISLIKES
print("TOP 10 VIDEOS BY DISLIKES")
top_10_videos_dislikes = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'dislikes': 'max'})  # Keep the first title and the max dislikes
    .nlargest(10, 'dislikes')  # Select the top 10 by dislikes
)
print(top_10_videos_dislikes[['video_id', 'title', 'dislikes']], '\n')  # Display the top 10 videos by dislikes

# TOP 10 VIDEOS BY COMMENTS
print("TOP 10 VIDEOS BY COMMENTS")
top_10_videos_comments = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'comment_total': 'max'})  # Keep the first title and the max comments
    .nlargest(10, 'comment_total')  # Select the top 10 by comments
)
print(top_10_videos_comments[['video_id', 'title', 'comment_total']], '\n')  # Display the top 10 videos by comments

# Correlation matrix
correlation_matrix = df_gb_videos[['views', 'likes', 'dislikes', 'comment_total']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Engagement Metrics of Videos')
filepath=f'Q1/{'correlation_matrix'}'
plt.savefig(filepath)

#TOP 10 VIDEOS PNGS
def save_top_10_plot(data,metric,filename):
    plt.figure(figsize=(10, 6))
    data_sorted = data.sort_values(by=metric, ascending=True)
    plt.barh(data_sorted['title'].head(10), data_sorted[metric].head(10), color='skyblue')
    plt.xlabel(metric.capitalize())
    plt.title(f'Top 10 Videos by {metric.capitalize()}')
    plt.tight_layout()
    filepath=f'Q1/{filename}'
    plt.savefig(filepath)
    plt.close()

save_top_10_plot(top_10_videos_views, 'views', 'top_10_videos_views_GB.png')
save_top_10_plot(top_10_videos_likes, 'likes', 'top_10_videos_likes_GB.png')
save_top_10_plot(top_10_videos_dislikes, 'dislikes', 'top_10_videos_dislike_GB.png')
save_top_10_plot(top_10_videos_comments, 'comment_total', 'top_10_videos_comments_GB.png')

 #TOP 10 CHANNELS
print("\nTOP 10 CHANNELS BY VIEWS")
top_10_channels_views = df_gb_videos.groupby('channel_title')['views'].sum().nlargest(10)
print(top_10_channels_views,'\n') # Display the top 10 channels by total views

print("\nTOP 10 CHANNELS BY LIKES")
top_10_channels_likes = df_gb_videos.groupby('channel_title')['likes'].sum().nlargest(10)
print(top_10_channels_likes,'\n') # Display the top 10 channels by total likes

print("\nTOP 10 CHANNELS BY DISLIKES")
top_10_channels_dislikes = df_gb_videos.groupby('channel_title')['dislikes'].sum().nlargest(10)
print(top_10_channels_dislikes,'\n') # Display the top 10 channels by total dislikes

print("\nTOP 10 CHANNELS BY COMMENTS")
top_10_channels_comments = df_gb_videos.groupby('channel_title')['comment_total'].sum().nlargest(10)
print(top_10_channels_comments,'\n') # Display the top 10 channels by total comments

# Correlation between likes and views
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_gb_videos, x='views', y='likes')
plt.title('Scatter Plot of Likes vs. Views')
plt.xlabel('Views')
plt.ylabel('Likes')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
filepath=f'Q1/{'likes_vs_views.png'}'
plt.savefig(filepath)
