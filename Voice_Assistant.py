import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
import os
import time

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<API KEY>"

# Configure pyttsx3 voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use voices[1] for female (if available)
engine.setProperty('rate', 180)  # Speed of speech

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
        api_key="<API KEY>"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c[5:]  # Get everything after "play "
        link = musicLibrary.music.get(song.strip())
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the library.")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)

# Main loop
if __name__ == '__main__':
    speak("Initializing Jarvis...")
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.5
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibrated mic. Starting loop...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=1.5)
            word = recognizer.recognize_google(audio).strip().lower()

            if word == 'jarvis':
                speak('Yes?')
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                    command = recognizer.recognize_google(audio).strip()
                    processCommand(command)

        except sr.UnknownValueError:
            pass  # Nothing understood; retry loop
        except sr.WaitTimeoutError:
            pass  # No input; continue
        except Exception as e:
            print(f"Error: {e}")
