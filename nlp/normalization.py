import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Sample text
text = "The striped bats are hanging on their feet for best"

# Tokenize words
words = word_tokenize(text)

# --- Stemming ---
stemmer = PorterStemmer()
stems = [stemmer.stem(word) for word in words]
print("🔹 Stemming Result:")
print(stems)

# --- Lemmatization ---
lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(word) for word in words]
print("\n🔹 Lemmatization Result (NLTK):")
print(lemmas)

# --- Lemmatization using spaCy ---
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
lemmas_spacy = [token.lemma_ for token in doc]
print("\n🔹 Lemmatization Result (spaCy):")
print(lemmas_spacy)
