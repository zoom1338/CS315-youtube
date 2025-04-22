import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
#import seaborn as sns
import os
os.makedirs("figures", exist_ok=True)
import json


gb_videos='data/GBvideos_clean.csv'
gb_comments='data/GBcomments_clean.csv'

df_gb_videos = pd.read_csv(gb_videos, on_bad_lines='skip')
df_gb_comments = pd.read_csv(gb_comments, on_bad_lines='skip')

us_videos='data/USvideos_clean.csv'
us_comments='data/UScomments_clean.csv'

df_us_videos = pd.read_csv(us_videos, on_bad_lines='skip')
df_us_comments = pd.read_csv(us_comments, on_bad_lines='skip')

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

# Does the content's category, like games, news, or music, have a higher chance of trending?
print("-------------------------------------------------------------------")

# let's check the available categories and their frequencies
gb_category_counts = df_gb_videos['category_id'].value_counts().sort_values(ascending=False)
us_category_counts = df_us_videos['category_id'].value_counts().sort_values(ascending=False)

# function for visualizing category distribution
# https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
def plot_category_distribution(category_counts, title, filename):
    plt.figure(figsize=(10,6))
    category_counts.plot(kind='bar')
    plt.title(title)
    plt.xlabel('Category ID')
    plt.ylabel('Number of Trending Videos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"figures/{filename}", dpi=300)
    plt.close()

plot_category_distribution(gb_category_counts, "Trending Videos by Category (GB)", "gb_category_distribution.png")
plot_category_distribution(us_category_counts, "Trending Videos by Category (US)", "us_category_distribution.png")

gb_category_counts, us_category_counts

# let's map category_id to real category names like "Music", "News"
# load category mappings
with open("data/US_category_id.json") as f:
    us_categories_json = json.load(f)

# loop through all the items, extract category ID and category name, only include categories that are "assignable": true
us_categories = {
    int(item["id"]): item["snippet"]["title"]
    for item in us_categories_json["items"]
    if item["snippet"]["assignable"]
}

with open("data/GB_category_id.json") as f:
    gb_categories_json = json.load(f)

gb_categories = {
    int(item["id"]): item["snippet"]["title"]
    for item in gb_categories_json["items"]
    if item["snippet"]["assignable"]
}

# map category_id to category_name for each video
df_us_videos["category_name"] = df_us_videos["category_id"].map(us_categories)
df_gb_videos["category_name"] = df_gb_videos["category_id"].map(gb_categories)

# count how many videos per category name
us_category_counts = df_us_videos["category_name"].value_counts().sort_values(ascending=False)
gb_category_counts = df_gb_videos["category_name"].value_counts().sort_values(ascending=False)

# plot the new category distributions with names
plot_category_distribution(us_category_counts, "Trending Videos by Category (US)", "us_category_distribution_named.png")
plot_category_distribution(gb_category_counts, "Trending Videos by Category (GB)", "gb_category_distribution_named.png")

gb_category_counts, us_category_counts

# let's investigate if some categories get more views, likes, and comments. Let's also plot average view per category
# and average likes per category
# function to plot bar chart of average metric per category
def plot_avg_metric_by_category(df_us, df_gb, metric, title, filename):
    avg_us = df_us.groupby("category_name")[metric].mean().sort_values(ascending=False)

    # keep the same order as US categories
    avg_gb = df_gb.groupby("category_name")[metric].mean().reindex(avg_us.index)

    plt.figure(figsize=(12, 6))

    # create an array of evenly spaced values, one for each category
    x = np.arange(len(avg_us))
    plt.bar(x - 0.40/2, avg_us, 0.40, label="US", color="blue", zorder=3)
    plt.bar(x + 0.40/2, avg_gb, 0.40, label="GB", color="red", zorder=3)

    plt.xticks(x, avg_us.index, rotation=45, ha="right")
    plt.ylabel(f"Average {metric.capitalize()}")
    plt.xlabel("Category")
    plt.title(title)
    plt.legend(title="Region")

    #https://www.w3schools.com/python/matplotlib_grid.asp
    plt.grid(axis='y', linestyle="--", linewidth=0.5, zorder=0)

    plt.tight_layout()
    plt.savefig(f"figures/{filename}", dpi=300)
    plt.close()

plot_avg_metric_by_category(
    df_us_videos,
    df_gb_videos,
    metric="views",
    title="Average Views per Category (US vs GB)",
    filename="avg_views_by_category.png"
)

plot_avg_metric_by_category(
    df_us_videos,
    df_gb_videos,
    metric="likes",
    title="Average Likes per Category (US vs GB)",
    filename="avg_likes_by_category.png"
)