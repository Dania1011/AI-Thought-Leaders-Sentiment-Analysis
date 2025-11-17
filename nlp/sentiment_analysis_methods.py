# ============================================
# MODULE 5: SENTIMENT ANALYSIS METHODOLOGIES
# ============================================

# STEP 1: IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from flair.models import TextClassifier
from flair.data import Sentence
import re

# STEP 2: SAMPLE OR DATASET
data = {
    'text': [
        "I love this product! It's absolutely fantastic.",
        "The service was terrible and I’m disappointed.",
        "This is an average experience, nothing special.",
        "I hate the delay in delivery.",
        "The new update is awesome and super fast!"
    ],
    'label': ['positive', 'negative', 'neutral', 'negative', 'positive']
}

df = pd.DataFrame(data)

# STEP 3: VADER SENTIMENT ANALYSIS
vader = SentimentIntensityAnalyzer()
def get_vader_sentiment(text):
    score = vader.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'
df['VADER'] = df['text'].apply(get_vader_sentiment)

# STEP 4: TEXTBLOB SENTIMENT ANALYSIS
def get_textblob_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'
df['TextBlob'] = df['text'].apply(get_textblob_sentiment)

# STEP 5: FLAIR SENTIMENT ANALYSIS
classifier = TextClassifier.load('en-sentiment')
def get_flair_sentiment(text):
    sentence = Sentence(text)
    classifier.predict(sentence)
    label = sentence.labels[0].value.lower()
    return 'positive' if label == 'positive' else 'negative'
df['Flair'] = df['text'].apply(get_flair_sentiment)

# STEP 6: VISUALIZE SENTIMENT COUNTS FOR EACH METHOD
methods = ['VADER', 'TextBlob', 'Flair']
for method in methods:
    plt.figure(figsize=(5,3))
    sns.countplot(x=df[method], palette='coolwarm')
    plt.title(f'Sentiment Distribution - {method}')
    plt.show()

# STEP 7: EVALUATION (if labels exist)
for method in methods:
    print(f"\n=== {method} Evaluation ===")
    print("Accuracy:", accuracy_score(df['label'], df[method]))
    print(classification_report(df['label'], df[method]))

# STEP 8: DOMAIN-SPECIFIC HANDLING EXAMPLE
def clean_text(text):
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+|#', '', text)
    return text.strip()
df['clean_text'] = df['text'].apply(clean_text)

# STEP 9: COMPARISON TABLE
print("\n--- Sentiment Comparison ---")
print(df[['text', 'label', 'VADER', 'TextBlob', 'Flair']])

# STEP 10: COMBINED VISUALIZATION
sentiment_counts = df[['VADER', 'TextBlob', 'Flair']].melt(var_name='Method', value_name='Sentiment')
plt.figure(figsize=(8,4))
sns.countplot(data=sentiment_counts, x='Method', hue='Sentiment', palette='Set2')
plt.title('Sentiment Comparison Across Methods')
plt.show()
