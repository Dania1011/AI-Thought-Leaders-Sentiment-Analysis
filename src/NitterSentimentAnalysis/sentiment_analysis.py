import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# Ensure NLTK VADER lexicon is available
nltk.download('vader_lexicon')

# -----------------------------
# Load CLEANED dataset
# -----------------------------
input_path = r"C:\Users\boban\OneDrive\Desktop\web_scraping_basics\src\NitterSentimentAnalysis\cleaned_combined_tweets.csv"

if not os.path.exists(input_path):
    raise FileNotFoundError("Cleaned dataset not found! Run the cleaning script first.")

df = pd.read_csv(input_path)
print("Loaded dataset with shape:", df.shape)

# ---------------------------------------------------
# Ensure clean_text exists and is not empty
# ---------------------------------------------------
df['clean_text'] = df['clean_text'].astype(str)
df = df[df['clean_text'].str.strip() != ""]

if df.empty:
    raise ValueError("All clean_text rows are empty. Cleaning script must be fixed.")

print("After removing empty clean_text rows:", df.shape)

# -----------------------------
# Initialize VADER
# -----------------------------
sia = SentimentIntensityAnalyzer()

# -----------------------------
# Apply sentiment scoring
# -----------------------------
def get_sentiment_label(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["neg"] = df["clean_text"].apply(lambda x: sia.polarity_scores(x)["neg"])
df["neu"] = df["clean_text"].apply(lambda x: sia.polarity_scores(x)["neu"])
df["pos"] = df["clean_text"].apply(lambda x: sia.polarity_scores(x)["pos"])
df["compound"] = df["clean_text"].apply(lambda x: sia.polarity_scores(x)["compound"])

df["sentiment_label"] = df["compound"].apply(get_sentiment_label)

# -----------------------------
# Save results
# -----------------------------
output_path = "sentiment_results.csv"
df.to_csv(output_path, index=False)

print("\nSaved sentiment analysis to:", output_path)

# -----------------------------
# Display statistics
# -----------------------------
print("\nSentiment Distribution:")
print(df["sentiment_label"].value_counts())

print("\nSample Results:")
print(df[["clean_text", "sentiment_label"]].head())
