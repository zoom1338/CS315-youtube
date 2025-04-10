import warnings

# suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
from pandas.errors import DtypeWarning
warnings.filterwarnings("ignore", category=DtypeWarning)

import pandas as pd

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

print("\nShape of videos:", df_us_comments.shape) # (691400, 4) - this is good as there are 4 columns

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

# convert text to lower case
# https://stackoverflow.com/questions/42750551/converting-strings-to-a-lower-case-in-pandas
df_us_comments["comment_text"] = df_us_comments["comment_text"].str.lower()