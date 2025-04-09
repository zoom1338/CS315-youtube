import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from pandas.errors import DtypeWarning
warnings.filterwarnings("ignore", category=DtypeWarning)

import pandas as pd

filename = 'data/USvideos.csv'

# read total number of lines without skipping
# https://stackoverflow.com/questions/16108526/how-to-obtain-the-total-numbers-of-rows-from-a-csv-file-in-python
with open(filename) as f:
    total_lines = sum(1 for line in f)

# Load video data
# on_bad_lines - rows with too many columns or too few columns are skipped
df_us_video = pd.read_csv('data/USvideos.csv', on_bad_lines='skip')

# add 1 for the header row
parsed_lines = len(df_us_video) + 1

skipped = total_lines - parsed_lines
print(f"Skipped {skipped} bad lines while loading '{filename}")