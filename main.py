import speech_recognition
import streamlit as st
import re
import random
import tgpt2
from youtube_transcript_api import YouTubeTranscriptApi
from translate import Translator
import easyocr
from kivy import platform


if platform == "android":
    from android.permissions import Permission, request_permissions


recognizer = speech_recognition.Recognizer()


st.title("General test")

# Sidebar with buttons
selected_option = st.sidebar.radio("Select an option", ["None",  "Speech", "Summarize", "Youtube", "Translate", "Image"])

# Text input
st.subheader("Url")
user_input = st.text_input("")

if selected_option == "Speech":
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.01)
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio, language="bg-BG")
                text = text.lower()

                st.write(f"{text}")

        except Exception as error:
            st.write(error)

elif selected_option == "Summarize":
    text = user_input
    user_prompt = f"Make a summary for this text: {text}"
    bot = tgpt2.TGPT()
    st.write(bot.chat(prompt=user_prompt))

elif selected_option == "Youtube":
    pattern = re.compile(
        r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})')
    match = pattern.search(user_input)
    video_id = match.group(1)

    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'fr', 'ru', 'es', 'pt', 'de'])
    full_text = " ".join(entry['text'] for entry in transcript)
    st.write(full_text)

elif selected_option == "Translate":
    dest_lang = random.choice(["en", "fr", "es", "pt", "de", "bg"])
    translator = Translator(to_lang=dest_lang)
    translation = translator.translate(user_input)
    st.write(translation)

elif selected_option == "Image":
    reader = easyocr.Reader(["en", "fr", "es", "pt"])
    path = user_input
    result = reader.readtext(path)

    for (bbox, text, prob) in result:
        st.write(text)
