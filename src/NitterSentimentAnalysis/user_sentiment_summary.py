import pandas as pd

# Load sentiment results
df = pd.read_csv("sentiment_results.csv")

print("Loaded:", df.shape)

# Group by user and sentiment
user_summary = df.groupby(["profile_name", "sentiment_label"]).size().unstack(fill_value=0)

print("\nUser Sentiment Summary:")
print(user_summary)

# Save summary
output_path = "user_sentiment_summary.csv"
user_summary.to_csv(output_path)

print("\nSaved summary to:", output_path)
