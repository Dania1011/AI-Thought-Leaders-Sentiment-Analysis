# Installation Guide  
### AI Thought Leaders Sentiment Analysis Platform

This document provides **complete setup instructions** for installing and running the project, from environment creation to executing each module in the pipeline.

---

## 🔧 1. System Requirements

Before installation, ensure your system has:

- **Python 3.9+**
- **pip** or **conda**
- **Git**
- **Internet connection** (only for scraping)
- Windows, macOS, or Linux supported

---

## 🏗️ 2. Create the Virtual Environment

### Using `venv` (recommended)

```bash
python -m venv scraper_env

Activate:

Windows

scraper_env\Scripts\activate

Mac/Linux

source scraper_env/bin/activate

3. Install Required Dependencies

Run:

pip install -r requirements.txt


If you don't have a requirements.txt, use this instead:

pip install requests
pip install beautifulsoup4
pip install selenium
pip install webdriver-manager
pip install pandas
pip install numpy
pip install nltk
pip install matplotlib
pip install seaborn


You may also need to download NLTK lexicons:

import nltk
nltk.download('vader_lexicon')

4. Verifying Nitter Connections

Since you are scraping from Nitter:

Test access by opening in browser:

https://nitter.net/


If blocked, switch to a different mirror :
https://nitter.tiekoetter.com
https://nitter.privacydev.net
https://nitter.garudalinux.org