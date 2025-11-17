import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ========================
# Create output folder
# ========================
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ========================
# Load sentiment results
# ========================
sentiment_file = r"C:\Users\boban\OneDrive\Desktop\web_scraping_basics\src\NitterSentimentAnalysis\sentiment_results.csv"
summary_file = r"C:\Users\boban\OneDrive\Desktop\web_scraping_basics\src\NitterSentimentAnalysis\user_sentiment_summary.csv"

df = pd.read_csv(sentiment_file)
summary_df = pd.read_csv(summary_file)

print("Loaded sentiment_results:", df.shape)
print("Loaded user_sentiment_summary:", summary_df.shape)

# =========================
# A. Overall Sentiment Distribution
# =========================

sentiment_counts = df["sentiment_label"].value_counts()

# Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
plt.title("Overall Sentiment Distribution")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "overall_sentiment_pie.png"))
plt.close()

# Bar Chart
plt.figure(figsize=(7, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
plt.title("Overall Sentiment Distribution")
plt.xlabel("Sentiment Label")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "overall_sentiment_bar.png"))
plt.close()


# =========================
# B. User-wise Sentiment Summary
# =========================

plt.figure(figsize=(10, 6))
sns.barplot(
    data=summary_df.melt(id_vars="profile_name",
                         var_name="Sentiment",
                         value_name="Count"),
    x="profile_name",
    y="Count",
    hue="Sentiment"
)

plt.title("User-wise Sentiment Comparison")
plt.xlabel("User")
plt.ylabel("Sentiment Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "user_wise_sentiment_comparison.png"))
plt.close()


# =========================
# C. Timeline Sentiment Trend (Optional but GOOD)
# =========================

if "created_at" in df.columns:
    try:
        df["created_at"] = pd.to_datetime(df["created_at"], errors='coerce')
        df_sorted = df.dropna(subset=["created_at"]).sort_values("created_at")

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_sorted, x="created_at", y="sentiment_label",
                     hue="sentiment_label", estimator=None, lw=1)

        plt.title("Sentiment Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Sentiment")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "sentiment_trend.png"))
        plt.close()
    except Exception as e:
        print("Could not generate trend chart:", e)

print("\nAll plots saved in:", PLOTS_DIR)
