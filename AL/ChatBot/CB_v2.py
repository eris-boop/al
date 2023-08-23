import requests
from bs4 import BeautifulSoup
from transformers import pipeline


class GoogleSearchChatbot:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def search(self, query):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query
        }

        response = requests.get(url, params=params)
        results = response.json().get("items", [])

        return results


def scrape_and_summarize(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        page_text = soup.get_text()
        cleaned_text = preprocess_text(page_text)
        return cleaned_text
    else:
        return None

def preprocess_text(text):
    clean_text = ' '.join(BeautifulSoup(text, "html.parser").stripped_strings)
    clean_text = ' '.join(clean_text.split())
    return clean_text


if __name__ == "__main__":
    apiKey = 'API_KEY'
    customSearchEngineId = 'API_KEY'

    chatbot = GoogleSearchChatbot(apiKey, customSearchEngineId)

    while True:
        user_input = input("Kamu: ")

        if user_input.lower() == "exit":
            print("Chatbot: dadah!")
            break

        sources = []
        question_parts = user_input.split('(')

        for part in question_parts:
            if ')' in part:
                source_number = part.split(')')[0]
                sources.append(int(source_number))

        search_query = ' '.join([part for i, part in enumerate(question_parts) if i + 1 not in sources])

        search_results = chatbot.search(search_query)

        if search_results:
            for source_number, source in enumerate(search_results, start=1):
                title = source.get("title", "N/A")
                link = source.get("link", "N/A")

                print(f"Source {source_number}:")
                print(f"Title: {title}")
                print(f"Link: {link}")

                page_text = scrape_and_summarize(link)
                if page_text:
                    print("\nText from the Web Page:")
                    print(page_text)
                else:
                    print("\nFailed to scrape text from the web page.")

                response = input("\nDo you want more information from this source? (iya/tidak): ")
                if response.lower() == "tidak":
                    break
        else:
            print("Chatbot: I couldn't find any relevant information.")

"ai search masih bagian informsi dari google dan diekstrak belum bisa ai merangkum"