
import pandas as pd 
import matplotlib as plt
import string
import re

gb_videos='data/GBvideos.csv' 
gb_comments='data/GBcomments.csv'

df_gb_videos = pd.read_csv(gb_videos, on_bad_lines='skip')
df_gb_comments = pd.read_csv(gb_comments, on_bad_lines='skip')

print(f"Shape of videos: {df_gb_videos.shape}") # (4096, 11) - this is good as there are 11 columns
print(f"Shape of comments: {df_gb_comments.shape}") # (408000, 4) - this is good as there are 4 columns

print(f"\nNumber of nulls in {gb_videos}:\n{df_gb_videos.isnull().sum()}") # showing 0 for all columns, no nulls
print(f"\nNumber of nulls in {gb_comments}:\n{df_gb_comments.isnull().sum()}") # showing 0 for all columns, no nulls

#extra comment cleaning
df_gb_comments = df_gb_comments.dropna(subset=["comment_text"])
print("Remove null")

print(f"\nNumber of nulls in {gb_comments}:\n{df_gb_comments.isnull().sum()}") # no more nulls

#likes and replies to integers and additional cleaning
df_gb_comments['likes']=pd.to_numeric(df_gb_comments['likes'], errors='coerce')
df_gb_comments['replies']=pd.to_numeric(df_gb_comments['replies'], errors='coerce')
df_gb_comments = df_gb_comments.dropna(subset=["likes", "replies"])
print("Remove null likes and replies")
print(f"\nNumber of nulls in {gb_comments}:\n{df_gb_comments.isnull().sum()}") # no more nulls
# convert likes and replies to integers
df_gb_comments['likes'] = df_gb_comments['likes'].astype(int)
df_gb_comments['replies'] = df_gb_comments['replies'].astype(int)


sample_before = df_gb_comments.iloc[110]["comment_text"]
#fix encoding issues
def fix_encoding(text):
    if isinstance(text, str):
        return text.encode('utf-8', 'replace').decode('utf-8', 'replace')
    return text
df_gb_comments['comment_text'] = df_gb_comments['comment_text'].apply(fix_encoding)

#text to lower
df_gb_comments['comment_text'] = df_gb_comments['comment_text'].str.lower()

#remove punctuation and digits and emojis
def remove_punctuation(text):
    if isinstance(text, str):
        return ''.join(char for char in text if char.isalpha() or char.isspace())
    return text

def remove_digits(text):
    if isinstance(text, str):
        return ''.join(char for char in text if not char.isdigit())
    return text

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags = re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)
df_gb_comments['comment_text'] = df_gb_comments['comment_text'].apply(remove_punctuation)

# show after cleaning
sample_after = df_gb_comments.iloc[110]["comment_text"]
print("-------------------------------------------------------------------")

print("Example BEFORE cleaning:\n", sample_before)
print("\nExample AFTER cleaning:\n", sample_after)

print("-------------------------------------------------------------------")
# done :)
df_gb_comments.to_csv("data/GBcomments_clean.csv", index=False)
df_gb_videos.to_csv("data/GBvideos_clean.csv", index=False)