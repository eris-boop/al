import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import speech_recognition as sr
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os
import pygame
import time

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for Indonesian speech...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    print("Recognizing speech...")

    try:
        recognized_text = recognizer.recognize_google(audio, language="id-ID")
        print("Recognized: " + recognized_text)

        translator = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-id-en")
        tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-id-en")

        input_ids = tokenizer.encode(recognized_text, return_tensors="pt")
        translated_ids = translator.generate(input_ids)
        translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

        print("Translated: " + translated_text)

        # Convert translated text to speech using gTTS with a female voice
        tts = gTTS(text="The translated text is: " + translated_text, lang='en', tld='com')
        tts.save("translated_text.mp3")

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load("translated_text.mp3")
        pygame.mixer.music.play()

        # Wait for audio to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        # Clean up
        pygame.mixer.quit()
        os.remove("translated_text.mp3")

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Could not request results")

if __name__ == "__main__":
    main()