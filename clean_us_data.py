import warnings

# suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
from pandas.errors import DtypeWarning
warnings.filterwarnings("ignore", category=DtypeWarning)

import pandas as pd
import string
import re

# filenames
filename_videos = 'data/USvideos.csv'
filename_comments = 'data/UScomments.csv'

# count total number of lines before reading with pandas including the header
# https://stackoverflow.com/questions/16108526/how-to-obtain-the-total-numbers-of-rows-from-a-csv-file-in-python
with open(filename_videos) as f:
    total_lines = sum(1 for line in f)
print(f"Total number of lines in raw file ({filename_videos}): {total_lines}")

# Load video data, skipping bad lines
# on_bad_lines - rows with too many columns or too few columns are skipped
print(f"Loading and skipping bad lines in {filename_videos}...")
df_us_videos = pd.read_csv(filename_videos, on_bad_lines='skip')

# add 1 for the header row
parsed_lines = len(df_us_videos) + 1

# print out number of bad lines skipped
skipped = total_lines - parsed_lines
print(f"Parsed lines (after skipping): {parsed_lines}")
print(f"Skipped {skipped} bad lines")

# shape returns a tuple representing the dimensions of the data (rows, columns)
print("\nShape of videos:", df_us_videos.shape) # (7992, 11) - this is good as there are 11 columns

# any nulls in the csv file?
print(f"\nNumber of nulls in {filename_videos}:\n{df_us_videos.isnull().sum()}") # showing 0 for all columns, no nulls

# let's do the same for us comments csv file
print("-------------------------------------------------------------------")

with open(filename_comments) as f:
    total_lines = sum(1 for line in f)
print(f"Total number of lines in raw file ({filename_comments}): {total_lines}")

print(f"Loading and skipping bad lines in {filename_comments}...")
df_us_comments = pd.read_csv(filename_comments, on_bad_lines='skip')

parsed_lines = len(df_us_comments) + 1

skipped = total_lines - parsed_lines
print(f"Parsed lines (after skipping): {parsed_lines}")
print(f"Skipped {skipped} bad lines")

print("\nShape of comments:", df_us_comments.shape) # (691400, 4) - this is good as there are 4 columns

print(f"\nNumber of nulls in {filename_comments}:\n{df_us_comments.isnull().sum()}")

# there are 4 nulls for comment_text, let's remove them
df_us_comments = df_us_comments.dropna(subset=["comment_text"])
print("Removing nulls...")

# now let's check the number of nulls
print(f"\nNumber of nulls in {filename_comments}:\n{df_us_comments.isnull().sum()}") # no more nulls

# let's convert the likes and replies to integers
# column header row is included many times so we need to convert only valid integers
df_us_comments["likes"] = pd.to_numeric(df_us_comments["likes"], errors='coerce')
df_us_comments["replies"] = pd.to_numeric(df_us_comments["replies"], errors='coerce')

# then we drop rows where the conversion failed
df_us_comments.dropna(subset=["likes", "replies"], inplace=True)

# finally convert likes/replies to integers
df_us_comments["likes"] = df_us_comments["likes"].astype(int)
df_us_comments["replies"] = df_us_comments["replies"].astype(int)

# show before and after cleaning for one example
sample_before = df_us_comments.iloc[110]["comment_text"]

# fixing encoding, ex: ðŸ¤”how will girls unlock their iphone x after taking off their makeup
# https://stackoverflow.com/questions/26491448/how-to-fix-broken-utf-8-encoding-in-python
def fix_encoding(text):
    if isinstance(text, str):
        try:
            return text.encode('latin1').decode('utf-8')
        except:
            return text  # if decoding fails, return original
    return text

df_us_comments["comment_text"] = df_us_comments["comment_text"].apply(fix_encoding)

# convert text to lower case
# https://stackoverflow.com/questions/42750551/converting-strings-to-a-lower-case-in-pandas
df_us_comments["comment_text"] = df_us_comments["comment_text"].str.lower()

# Let's remove punctuation and digits
# https://www.tutorialspoint.com/How-to-strip-down-all-the-punctuation-from-a-string-in-Python
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_digits(text):
    return text.translate(str.maketrans('', '', string.digits))

df_us_comments["comment_text"] = df_us_comments["comment_text"].apply(remove_punctuation)
df_us_comments["comment_text"] = df_us_comments["comment_text"].apply(remove_digits)

# last cleaning, removing emojis
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags = re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

df_us_comments["comment_text"] = df_us_comments["comment_text"].apply(remove_emojis)

# removing out non-ASCII junk
# https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces
def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

df_us_comments["comment_text"] = df_us_comments["comment_text"].apply(remove_non_ascii)

# show after cleaning
sample_after = df_us_comments.iloc[110]["comment_text"]
print("-------------------------------------------------------------------")

print("Example BEFORE cleaning:\n", sample_before)
print("\nExample AFTER cleaning:\n", sample_after)

print("-------------------------------------------------------------------")
# done :)
#df_us_comments.to_csv("data/UScomments_clean.csv", index=False)
#df_us_videos.to_csv("data/USvideos_clean.csv", index=False)