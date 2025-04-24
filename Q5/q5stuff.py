from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import os


df_comments_US = pd.read_csv("../data/UScomments_clean.csv", encoding='utf-8')
df_comments_GB = pd.read_csv("../data/GBcomments_clean.csv", encoding='utf-8')
df_us_videos = pd.read_csv("../data/USvideos_clean.csv",encoding='utf-8')
df_gb_videos = pd.read_csv("../data/GBvideos_clean.csv",encoding='utf-8')

pol_US = []
for i in df_comments_US['comment_text'].values:
    try:
        analysis = TextBlob(str(i))
        pol_US.append(analysis.sentiment.polarity)
    except:
        pol_US.append(0)

df_comments_US['pol'] = pol_US

df_comments_US['sentiment'] = df_comments_US['pol'].apply(
    lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
)

pol_GB = []
for i in df_comments_GB['comment_text'].values:
    try:
        analysis = TextBlob(str(i))
        pol_GB.append(analysis.sentiment.polarity)
    except:
        pol_GB.append(0)

df_comments_GB['pol'] = pol_GB

df_comments_GB['sentiment'] = df_comments_GB['pol'].apply(
    lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
)


def plotting(comments_df, title):
    plt.figure(figsize=(7, 4))
    comments_df['sentiment'].value_counts().plot(kind='bar', color=['green', 'gray', 'red'])
    plt.title(title)
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Comments')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.tight_layout()

plotting(df_comments_US, 'Comments sorted US by Sentiment Type')
print("Finished plotting US")
plotting(df_comments_GB, 'Comments sorted GB by Sentiment Type')

print("Finished plotting GB")


top_10_videos_likes_us= (
    df_us_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'likes': 'max'})  # Keep the first title and the max comments
    .nlargest(10, 'likes')  # Select the top 10 by comments
)

top_10_videos_likes_gb= (
    df_gb_videos.groupby('video_id', as_index=False)
    .agg({'title': 'first', 'likes': 'max'})  # Keep the first title and the max comments
    .nlargest(10, 'likes')  # Select the top 10 by comments
)

top_us_video_ids = top_10_videos_likes_us['video_id'].tolist()
top_us_likes = df_comments_US[df_comments_US['video_id'].isin(top_us_video_ids)]

top_gb_video_ids = top_10_videos_likes_gb['video_id'].tolist()
top_gb_likes = df_comments_GB[df_comments_GB['video_id'].isin(top_gb_video_ids)]

def classify_sentiment(text):
    try:
        polarity = TextBlob(str(text)).sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    except:
        return "Neutral"
    
def make_plot(top_likes, top10, title, filename):
    top_likes.loc[:, 'Sentiment'] = top_likes['comment_text'].apply(classify_sentiment)
    sentiment_by_video = top_likes.groupby(['video_id', 'Sentiment']).size().unstack(fill_value=0)
    merged = top10.merge(sentiment_by_video, on='video_id')
    merged['short_title'] = merged['title'].apply(lambda x: ' '.join(x.split()[:4]) + '...' if len(x.split()) > 4 else x)

    plt.figure(figsize=(12, 7))
    merged.set_index('short_title')[['Positive', 'Neutral', 'Negative']].plot(
        kind='bar', stacked=True, ax=plt.gca(), title=title
    )
    plt.xlabel("Video Title")
    plt.ylabel("Number of Comments")
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.yticks(fontsize=10)
    plt.title(title, fontsize=14)
    plt.grid(axis='y')
    plt.tight_layout()

    output_path = os.path.join(os.path.dirname(__file__), filename)
    plt.savefig(output_path)
    

make_plot(top_us_likes, top_10_videos_likes_us, "TOP 10 liked US Videos and their comment sentiment", "ustop10.png")
print("Finished plotting US top 10")
make_plot(top_gb_likes, top_10_videos_likes_gb, "TOP 10 liked GB Videos and their comment sentiment", "gbtop10.png")
print("Finished plotting GB top 10")