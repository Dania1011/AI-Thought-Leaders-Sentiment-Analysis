# tokenization.py

import nltk
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize

# Download tokenizer data for nltk
nltk.download('punkt')

# Sample text
text = "Natural Language Processing (NLP) helps machines understand human language. Tokenization splits text into words or sentences."

# ---- NLTK Tokenization ----
print("🔹 NLTK Tokenization\n")

# Sentence Tokenization
sentences = sent_tokenize(text)
print("Sentences:", sentences)

# Word Tokenization
words = word_tokenize(text)
print("Words:", words)


# ---- spaCy Tokenization ----
print("\n🔹 spaCy Tokenization\n")

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Process text
doc = nlp(text)

# Tokens
tokens = [token.text for token in doc]
print("Tokens:", tokens)
