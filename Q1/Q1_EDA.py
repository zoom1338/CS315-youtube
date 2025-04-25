# EDA for Q1
# Which engagement metrics, like views, comments, dislikes, and likes, correlate strongly with a video’s trending status?
#contributions to code from Isabella Sunderman
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.plotting as table

#load in GB
gb_videos='data/GBvideos_clean.csv'
gb_comments='data/GBcomments_clean.csv'

#load in US
us_videos= 'data/USvideos_clean.csv'
us_comments='data/UScomments_clean.csv'

#GB dataframe
df_gb_videos = pd.read_csv(gb_videos, on_bad_lines='skip')
df_gb_comments = pd.read_csv(gb_comments, on_bad_lines='skip')
print(df_gb_videos.columns) # Display the columns of the videos dataframe
#print(df_gb_videos.head(5))# Display the first 5 rows of the videos dataframe

#US dataframe
df_us_videos=pd.read_csv(us_videos, on_bad_lines='skip')
df_us_comments=pd.read_csv(us_comments,on_bad_lines='skip')
print(df_us_videos.columns)

# TOP 10 VIDEOS BY VIEWS
print("TOP 10 VIDEOS BY VIEWS GB")
top_10_videos_views_gb = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'views': 'max'})  # Keep the first title and the max views
    .nlargest(10, 'views')  # Select the top 10 by views
)
print(top_10_videos_views_gb[['video_id', 'title', 'views']], '\n')  # Display the top 10 videos by views

# TOP 10 VIDEOS BY LIKES
print("TOP 10 VIDEOS BY LIKES GB")
top_10_videos_likes_gb = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'likes': 'max'})  # Keep the first title and the max likes
    .nlargest(10, 'likes')  # Select the top 10 by likes
)
print(top_10_videos_likes_gb[['video_id', 'title', 'likes']], '\n')  # Display the top 10 videos by likes

# TOP 10 VIDEOS BY DISLIKES
print("TOP 10 VIDEOS BY DISLIKES GB")
top_10_videos_dislikes_gb = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'dislikes': 'max'})  # Keep the first title and the max dislikes
    .nlargest(10, 'dislikes')  # Select the top 10 by dislikes
)
print(top_10_videos_dislikes_gb[['video_id', 'title', 'dislikes']], '\n')  # Display the top 10 videos by dislikes

# TOP 10 VIDEOS BY COMMENTS
print("TOP 10 VIDEOS BY COMMENTS GB")
top_10_videos_comments_gb = (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'comment_total': 'max'})  # Keep the first title and the max comments
    .nlargest(10, 'comment_total')  # Select the top 10 by comments
)
print(top_10_videos_comments_gb[['video_id', 'title', 'comment_total']], '\n')  # Display the top 10 videos by comments

# Correlation matrix
correlation_matrix = df_gb_videos[['views', 'likes', 'dislikes', 'comment_total']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Engagement Metrics of Videos GB')
filepath=f'Q1/{'correlation_matrix_gb'}'
plt.savefig(filepath)

#TOP 10 VIDEOS PNGS
def save_top_10_plot(data,metric,filename):
    plt.figure(figsize=(10, 6))
    data_sorted = data.sort_values(by=metric, ascending=True)
    plt.barh(data_sorted['title'].head(10), data_sorted[metric].head(10), color='skyblue')
    plt.xlabel(metric.capitalize())
    plt.title(f'Top 10 Videos by {metric.capitalize()}')
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate labels and align them to the right
    plt.tight_layout()
    filepath=f'Q1/{filename}'
    plt.savefig(filepath)
    plt.close()

save_top_10_plot(top_10_videos_views_gb, 'views', 'top_10_videos_views_GB.png')
save_top_10_plot(top_10_videos_likes_gb, 'likes', 'top_10_videos_likes_GB.png')
save_top_10_plot(top_10_videos_dislikes_gb, 'dislikes', 'top_10_videos_dislike_GB.png')
save_top_10_plot(top_10_videos_comments_gb, 'comment_total', 'top_10_videos_comments_GB.png')

# TOP 10 VIDEOS BY VIEWS
print("TOP 10 VIDEOS BY VIEWS US")
top_10_videos_views_us = (
    df_us_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'views': 'max'})  # Keep the first title and the max views
    .nlargest(10, 'views')  # Select the top 10 by views
)
print(top_10_videos_views_us[['video_id', 'title', 'views']], '\n')  # Display the top 10 videos by views

# TOP 10 VIDEOS BY LIKES
print("TOP 10 VIDEOS BY LIKES US")
top_10_videos_likes_us = (
    df_us_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'likes': 'max'})  # Keep the first title and the max likes
    .nlargest(10, 'likes')  # Select the top 10 by likes
)
print(top_10_videos_likes_us[['video_id', 'title', 'likes']], '\n')  # Display the top 10 videos by likes

# TOP 10 VIDEOS BY DISLIKES
print("TOP 10 VIDEOS BY DISLIKES us")
top_10_videos_dislikes_us = (
    df_us_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'dislikes': 'max'})  # Keep the first title and the max dislikes
    .nlargest(10, 'dislikes')  # Select the top 10 by dislikes
)
print(top_10_videos_dislikes_us[['video_id', 'title', 'dislikes']], '\n')  # Display the top 10 videos by dislikes

# TOP 10 VIDEOS BY COMMENTS
print("TOP 10 VIDEOS BY COMMENTS us")
top_10_videos_comments_us = (
    df_us_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'comment_total': 'max'})  # Keep the first title and the max comments
    .nlargest(10, 'comment_total')  # Select the top 10 by comments
)
print(top_10_videos_comments_us[['video_id', 'title', 'comment_total']], '\n')  # Display the top 10 videos by comments

# Correlation matrix
correlation_matrix = df_us_videos[['views', 'likes', 'dislikes', 'comment_total']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Engagement Metrics of Videos US')
filepath=f'Q1/{'correlation_matrix_us'}'
plt.savefig(filepath)


save_top_10_plot(top_10_videos_views_us, 'views', 'top_10_videos_views_us.png')
save_top_10_plot(top_10_videos_likes_us, 'likes', 'top_10_videos_likes_us.png')
save_top_10_plot(top_10_videos_dislikes_us, 'dislikes', 'top_10_videos_dislike_us.png')
save_top_10_plot(top_10_videos_comments_us, 'comment_total', 'top_10_videos_comments_us.png')


import matplotlib.pyplot as plt
from pandas.plotting import table

# Function to combine and save top 10 videos for US and GB in a table as PNG
def combined_top_10_table(data_us, data_gb, metric, filename):
    # Add a region column to distinguish between US and GB
    data_us['region'] = 'US'
    data_gb['region'] = 'GB'
    
    # Combine the two datasets
    combined_data = pd.concat([data_us[['video_id', 'title', metric, 'region']], 
                               data_gb[['video_id', 'title', metric, 'region']]])
    
    # Sort by metric in descending order
    combined_data = combined_data.sort_values(by=metric, ascending=False)
    
    # Reset index for better readability
    combined_data.reset_index(drop=True, inplace=True)
    
    # Create a figure for the table
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust size as needed
    ax.axis('off')  # Turn off the axis
    ax.axis('tight')  # Adjust layout to fit the table
    
    # Render the table
    tbl = table(ax, combined_data, loc='center', colWidths=[0.5] * len(combined_data.columns))
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1.2, 1.2)  # Adjust scale for better readability
    
    # Save the table as a PNG file
    filepath = f'Q1/{filename}'
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()

# Save combined tables for each category as PNG
combined_top_10_table(top_10_videos_views_us, top_10_videos_views_gb, 'views', 'combined_top_10_videos_views.png')
combined_top_10_table(top_10_videos_likes_us, top_10_videos_likes_gb, 'likes', 'combined_top_10_videos_likes.png')
combined_top_10_table(top_10_videos_dislikes_us, top_10_videos_dislikes_gb, 'dislikes', 'combined_top_10_videos_dislikes.png')
combined_top_10_table(top_10_videos_comments_us, top_10_videos_comments_gb, 'comment_total', 'combined_top_10_videos_comments.png')
#############################################################################################################################################
#CHANNEL ANALYISIS 

#TOP 10 CHANNELS GB
print("\nTOP 10 CHANNELS BY VIEWS GB")
top_10_channels_views_gb = df_gb_videos.groupby('channel_title')['views'].sum().nlargest(10)
print(top_10_channels_views_gb,'\n') # Display the top 10 channels by total views

print("\nTOP 10 CHANNELS BY LIKES GB")
top_10_channels_likes_gb = df_gb_videos.groupby('channel_title')['likes'].sum().nlargest(10)
print(top_10_channels_likes_gb,'\n') # Display the top 10 channels by total likes

print("\nTOP 10 CHANNELS BY DISLIKES GB")
top_10_channels_dislikes_gb = df_gb_videos.groupby('channel_title')['dislikes'].sum().nlargest(10)
print(top_10_channels_dislikes_gb,'\n') # Display the top 10 channels by total dislikes

print("\nTOP 10 CHANNELS BY COMMENTS GB")
top_10_channels_comments_gb = df_gb_videos.groupby('channel_title')['comment_total'].sum().nlargest(10)
print(top_10_channels_comments_gb,'\n') # Display the top 10 channels by total comments

#TOP 10 CHANNEL US
print("\nTOP 10 CHANNELS BY VIEWS US")
top_10_channels_views_us = df_us_videos.groupby('channel_title')['views'].sum().nlargest(10)
print(top_10_channels_views_gb,'\n') # Display the top 10 channels by total views

print("\nTOP 10 CHANNELS BY LIKES US")
top_10_channels_likes_us = df_us_videos.groupby('channel_title')['likes'].sum().nlargest(10)
print(top_10_channels_likes_us,'\n') # Display the top 10 channels by total likes

print("\nTOP 10 CHANNELS BY DISLIKES US")
top_10_channels_dislikes_us = df_us_videos.groupby('channel_title')['dislikes'].sum().nlargest(10)
print(top_10_channels_dislikes_us,'\n') # Display the top 10 channels by total dislikes

print("\nTOP 10 CHANNELS BY COMMENTS US")
top_10_channels_comments_us = df_us_videos.groupby('channel_title')['comment_total'].sum().nlargest(10)
print(top_10_channels_comments_us,'\n') # Display the top 10 channels by total comments

# Convert Series to DataFrame for US and GB
top_10_channels_views_us = top_10_channels_views_us.reset_index().rename(columns={'index': 'channel_title', 'views': 'views'})
top_10_channels_views_gb = top_10_channels_views_gb.reset_index().rename(columns={'index': 'channel_title', 'views': 'views'})

top_10_channels_likes_us = top_10_channels_likes_us.reset_index().rename(columns={'index': 'channel_title', 'likes': 'likes'})
top_10_channels_likes_gb = top_10_channels_likes_gb.reset_index().rename(columns={'index': 'channel_title', 'likes': 'likes'})

top_10_channels_dislikes_us = top_10_channels_dislikes_us.reset_index().rename(columns={'index': 'channel_title', 'dislikes': 'dislikes'})
top_10_channels_dislikes_gb = top_10_channels_dislikes_gb.reset_index().rename(columns={'index': 'channel_title', 'dislikes': 'dislikes'})

top_10_channels_comments_us = top_10_channels_comments_us.reset_index().rename(columns={'index': 'channel_title', 'comment_total': 'comment_total'})
top_10_channels_comments_gb = top_10_channels_comments_gb.reset_index().rename(columns={'index': 'channel_title', 'comment_total': 'comment_total'})

def combined_top_10_channel(data_us, data_gb, metric, filename):
    # Add a region column to distinguish between US and GB
    data_us['region'] = 'US'
    data_gb['region'] = 'GB'
    
    # Combine the two datasets
    combined_data = pd.concat([data_us[['channel_title', metric, 'region']], 
                               data_gb[['channel_title', metric, 'region']]])
    
    # Sort by metric in descending order
    combined_data = combined_data.sort_values(by=metric, ascending=False)
    
    # Reset index for better readability
    combined_data.reset_index(drop=True, inplace=True)
    
    # Create a figure for the table
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust size as needed
    ax.axis('off')  # Turn off the axis
    ax.axis('tight')  # Adjust layout to fit the table
    
    # Render the table
    tbl = table(ax, combined_data, loc='center', colWidths=[0.5] * len(combined_data.columns))
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1.2, 1.2)  # Adjust scale for better readability
    
    # Save the table as a PNG file
    filepath = f'Q1/{filename}'
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()

combined_top_10_channel(top_10_channels_views_us, top_10_channels_views_gb, 'views', 'combined_top_10_channels_views.png')
combined_top_10_channel(top_10_channels_likes_us, top_10_channels_likes_gb, 'likes', 'combined_top_10_channels_likes.png')
combined_top_10_channel(top_10_channels_dislikes_us, top_10_channels_dislikes_gb, 'dislikes', 'combined_top_10_channels_dislikes.png')
combined_top_10_channel(top_10_channels_comments_us, top_10_channels_comments_gb, 'comment_total', 'combined_top_10_channels_comments.png')

# Scatter plot of Likes vs. Views
plt.figure(figsize=(10, 6))
plt.scatter(df_gb_videos['views'], df_gb_videos['likes'], alpha=0.5)
plt.xscale('log')  # Use logarithmic scale for better visualization
plt.yscale('log')  # Use logarithmic scale for better visualization
plt.xlabel('Views')
plt.ylabel('Likes')
plt.title('Scatter Plot of Likes vs. Views')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('Q1/likes_vs_views.png')  # Save the plot as a PNG file
plt.show()