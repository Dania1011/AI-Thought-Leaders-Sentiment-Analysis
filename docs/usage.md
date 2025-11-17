Usage Guide — AI Thought Leaders Sentiment Analysis Platform
⭐ 1. Overview

This guide explains how to run the full scraping → cleaning → sentiment analysis → summary pipeline of your project.
It is written so that any user (even without prior experience) can use your project successfully.

Your project contains three main modules:

Data Collection (Scraping using Nitter)

Data Cleaning & Combination

Sentiment Analysis & Summary Generation

🧩 2. Prerequisites

Before running anything, ensure:

✔️ You have installed all dependencies

(Already explained in installation.md)

✔️ You are inside your virtual environment:
scraper_env\Scripts\activate

✔️ Folder structure:
src/
  NitterSentimentAnalysis/
      scraper_nt.py
      combine_csv.py
      sentiment_analysis.py
      user_sentiment_summary.py
      ...
docs/

🕸️ 3. How to Scrape Tweets (Data Collection)
Script: scraper_nt.py
Purpose:

Scrapes tweets for a given username from Nitter using Selenium and saves the result into a CSV file.

▶ Run the scraper

Example:

python src/NitterSentimentAnalysis/scraper_nt.py username_here


Replace username_here with the profile you want to scrape, such as:

python src/NitterSentimentAnalysis/scraper_nt.py geoffreyhinton
python src/NitterSentimentAnalysis/scraper_nt.py karpathy
python src/NitterSentimentAnalysis/scraper_nt.py ilyasutskever

Output:

A CSV file such as:

data_raw/geoffreyhinton.csv

🧹 4. Combine & Clean Tweets (Text Preprocessing)
Script: combine_csv.py
Purpose:

Loads all user CSV files

Removes duplicates

Cleans text (URLs, emojis, mentions, punctuation)

Creates a new clean_text column

Saves a final combined cleaned dataset

▶ Run the cleaning script
python src/NitterSentimentAnalysis/combine_csv.py

Output:
data_processed/cleaned_combined_tweets.csv


This file is REQUIRED for sentiment analysis.

😊 5. Sentiment Analysis (VADER)
Script: sentiment_analysis.py
Purpose:

Performs sentiment analysis using NLTK VADER on clean_text and assigns:

Positive

Negative

Neutral

▶ Run the script
python src/NitterSentimentAnalysis/sentiment_analysis.py

Output:
outputs/sentiment_results.csv


This file contains:

clean_text

sentiment scores

sentiment label

profile_name

username

👥 6. User-wise Sentiment Summary
Script: user_sentiment_summary.py
Purpose:

Creates an aggregated table of sentiment counts per user.

▶ Run the script:
python src/NitterSentimentAnalysis/user_sentiment_summary.py

Output:
outputs/user_sentiment_summary.csv


This file contains:

profile_name	Positive	Negative	Neutral
Andrej Karpathy	218	44	47
Geoffrey Hinton	32	13	6
Ilya Sutskever	104	51	48
📊 7. How to Use the Results
After running all scripts, you will have:
A. Cleaned dataset

cleaned_combined_tweets.csv
✔ Text cleaned
✔ Duplicates removed
✔ Ready for analysis

B. Sentiment results

sentiment_results.csv
✔ Clean text
✔ Sentiment scores
✔ Sentiment labels

C. User sentiment summary

user_sentiment_summary.csv
✔ Used in your PDF analysis report
✔ Helps identify tone differences among AI leaders

📈 8. Optional: Generate Visualizations

If you want to create plots for your PDF report (bar charts, pie charts, trend lines), you can write additional scripts inside:

src/NitterSentimentAnalysis/visualizations/


Example visualizations:

Sentiment distribution bar chart

User-wise sentiment comparison

Word clouds

Emotion timelines

🧪 9. Reproducibility Checklist

Before delivering the project, verify:

✔ All CSVs exist in correct folders
✔ Scripts run without errors
✔ No missing columns
✔ Python environment exports (pip freeze)
✔ Documentation package complete



