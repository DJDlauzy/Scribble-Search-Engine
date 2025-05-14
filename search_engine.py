from flask import Flask, request, render_template
from collections import defaultdict
import math
import re
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)

# Sample URLs to index
URLS = [
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/JavaScript",
    "https://en.wikipedia.org/wiki/HTML"
]

# In-memory index
index = defaultdict(list)
documents = {}

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

def build_index():
    global documents
    for doc_id, url in enumerate(URLS):
        for attempt in range(3):  # Retry up to 3 times
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find('div', {'id': 'mw-content-text'})
                text = content.get_text() if content else soup.get_text()
                words = clean_text(text)
                documents[doc_id] = {'url': url, 'title': soup.title.string if soup.title else url}
                tf = defaultdict(int)
                for word in words:
                    tf[word] += 1
                for word, freq in tf.items():
                    index[word].append((doc_id, freq / len(words)))
                print(f"Indexed {url}")
                break
            except Exception as e:
                print(f"Error indexing {url} (attempt {attempt + 1}): {e}")
                time.sleep(2)  # Wait before retrying
                if attempt == 2:
                    print(f"Failed to index {url} after 3 attempts")

def calculate_idf(word):
    docs_with_word = len(index.get(word, []))
    return math.log(len(documents) / (1 + docs_with_word)) if docs_with_word else 0

def search(query):
    print(query)
    query_words = clean_text(query)
    scores = defaultdict(float)
    for word in query_words:
        if word in index:
            idf = calculate_idf(word)
            for doc_id, tf in index[word]:
                scores[doc_id] += tf * idf
    results = [
        {'url': documents[doc_id]['url'], 
         'title': documents[doc_id]['title'], 
         'score': score}
        for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return results[:10]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_route():
    query = request.args.get('q', '')
    results = search(query) if query else []
    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    print("Building index...")
    build_index()
    print(f"Index built. {len(documents)} documents indexed.")
    port = int(os.getenv('PORT', 5000))  # Use Glitch's PORT or default to 5000
    app.run(host='0.0.0.0', port=port, debug=False)