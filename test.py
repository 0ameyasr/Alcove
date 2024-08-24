import requests
from bs4 import BeautifulSoup

def wiki_extract(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    if content_div is None:
        return "Content not found."
    paragraphs = content_div.find_all('p')
    text_content = '\n'.join(paragraph.text for paragraph in paragraphs)
    return text_content.strip()

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
print(wiki_extract(url))
