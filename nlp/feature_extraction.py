from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Sample text corpus
corpus = [
    "Natural Language Processing is amazing",
    "Machine Learning makes NLP powerful",
    "Text preprocessing is an important NLP step"
]

# 1️⃣ Bag of Words
bow_vectorizer = CountVectorizer()
bow_matrix = bow_vectorizer.fit_transform(corpus)
print("🧩 Bag of Words (BOW) Feature Names:")
print(bow_vectorizer.get_feature_names_out())
print("\nBOW Matrix:\n", bow_matrix.toarray())

# 2️⃣ TF-IDF Features
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
print("\n🔍 TF-IDF Feature Names:")
print(tfidf_vectorizer.get_feature_names_out())
print("\nTF-IDF Matrix:\n", tfidf_matrix.toarray())
