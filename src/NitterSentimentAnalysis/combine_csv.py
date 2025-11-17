import pandas as pd
import glob

# Path to your CSVs
files = glob.glob("src/NitterSentimentAnalysis/*.csv")

dfs = [pd.read_csv(f) for f in files]

final_df = pd.concat(dfs, ignore_index=True)

# Save combined dataset
final_df.to_csv("src/NitterSentimentAnalysis/all_users_tweets.csv", index=False)

print("Merged CSV created!")
