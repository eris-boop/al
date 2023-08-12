import os
import json
import random
import re
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Load stopwords and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# file paths
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
USER_INTENT_PATH = os.path.join(DATA_DIR, "user_intents.json")

# Load user
user_intents = {}
if os.path.exists(USER_INTENT_PATH):
    with open(USER_INTENT_PATH, "r") as file:
        user_intents = json.load(file)

# Responses for general queries
general_responses = [
    "Tentu sajah.",
    "Saya pahamm.",
    "Silakan dilanjutkan.",
    "Bagaimana jika Anda menceritakan lebih banyak?",
    "Bisakah Anda menjelaskan lebih detail?"
]

# preprocess user input
def preprocess_input(text):
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# get information
def get_info_from_google(query):
    google_api_key = "api kau"
    search_engine_id = "api kau"

    if not google_api_key or not search_engine_id:
        return "Kunci API atau ID mesin pencari belum dikonfigurasi."

    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={search_engine_id}&q={query}"
    response = requests.get(url).json()

    if "items" in response and response["items"]:
        return response["items"]
    else:
        return []

# Main loop
while True:
    user_input = input("Anda: ")
    if user_input.lower() == "exit":
        # Simpan niat pengguna ke file sebelum keluar
        with open(USER_INTENT_PATH, "w") as file:
            json.dump(user_intents, file)
        break

    preprocessed_input = preprocess_input(user_input)

    if re.search(r"(info|informasi) tentang", preprocessed_input):
        query = re.sub(r"(info|informasi) tentang", "", preprocessed_input).strip()
        info = get_info_from_google(query)

        if info:
            for i, result in enumerate(info, start=1):
                print(f"AL Bot(beta): Hasil {i}:")
                print(f"Judul: {result['title']}")
                print(f"Snippet: {result['snippet']}")
                print(f"Link: {result['link']}")
                print("\n")
        else:
            print("AL Bot(beta): Tidak ditemukan hasil.")

    else:
        if preprocessed_input in user_intents:
            print("AL Bot(beta):", user_intents[preprocessed_input])
            ask_alternate = input(
                "Anda: Apakah Anda ingin mendengar jawaban lain untuk pertanyaan yang sama? (ya/tidak) ")
            if ask_alternate.lower() == "ya":
                alternate_responses = user_intents[preprocessed_input].get("alternate_responses", [])
                if alternate_responses:
                    random_alternate_response = random.choice(alternate_responses)
                    print("AL Bot(beta):", random_alternate_response)
                else:
                    print("AL Bot(beta): Tidak ada jawaban alternatif yang tersedia.")
        else:
            random_response = random.choice(general_responses)
            print("AL Bot(beta):", random_response)
            new_intent = get_info_from_google(preprocessed_input)
            user_intents[preprocessed_input] = {"response": random_response, "alternate_responses": []}
            if new_intent:
                user_intents[preprocessed_input]["alternate_responses"] = [result['snippet'] for result in new_intent]
                for i, result in enumerate(new_intent, start=1):
                    print(f"AL Bot(beta): Hasil {i}:")
                    print(f"Judul: {result['title']}")
                    print(f"Snippet: {result['snippet']}")
                    print(f"Link: {result['link']}")
                    print("\n")
            else:
                print("GoogleBot: Tidak menemukan hasil.")

#bukan sepuh masih banyak salah
#dapatin api key nya di Google Cloud Console.
