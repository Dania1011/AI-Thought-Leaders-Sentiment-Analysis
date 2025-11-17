import re

# Sample text
text = """
Contact us at support@example.com or sales@company.org.
Visit https://www.example.com for more info.
Our Twitter: #DataScience #AI #MachineLearning
The total cost is $1200. Delivered by John Doe.
"""

# 1️⃣ Extract email addresses
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

# 2️⃣ Extract hashtags
hashtags = re.findall(r'#\w+', text)

# 3️⃣ Extract URLs
urls = re.findall(r'https?://[^\s]+', text)

# 4️⃣ Extract money values
money = re.findall(r'\$\d+', text)

# 5️⃣ Extract capitalized words (e.g., names)
capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)

print("📧 Emails:", emails)
print("🏷️ Hashtags:", hashtags)
print("🔗 URLs:", urls)
print("💰 Money Values:", money)
print("🧑‍💼 Capitalized Words:", capitalized)
