from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import os

df_comments = pd.read_csv("../data/GBcomments_clean.csv", encoding='utf-8')

# getting the polarity of the comments
pol = []
for i in df_comments['comment_text'].values:
    try:
        analysis = TextBlob(str(i))
        pol.append(analysis.sentiment.polarity)
    except:
        pol.append(0)

df_comments['pol'] = pol

# Sentiment classification
df_comments['sentiment'] = df_comments['pol'].apply(
    lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
)

#plotting the graph
plt.figure(figsize=(7, 4))
df_comments['sentiment'].value_counts().plot(kind='bar', color=['green', 'gray', 'red'])
plt.title('Commets sorted GB by Sentiment Type')
plt.xlabel('Sentiment')
plt.ylabel('Number of Comments')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()

# Saving the file
output_path = os.path.join(os.path.dirname(__file__), "GBcomments.png")
plt.savefig(output_path)
plt.show()
