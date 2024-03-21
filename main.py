from dotenv import load_dotenv
from gtts import gTTS
import os
import random
from terms import unit_6_terms
from playsound import playsound
from openai import OpenAI
import speech_recognition as sr

load_dotenv()
api_key = os.getenv("api_key")  
if api_key is None:
    raise ValueError("API key is not set. Please set the 'api_key' environment variable.")

client = OpenAI(api_key=api_key)

def get_user_voice_input(language=None):
    '''Gets user input'''
    r = sr.Recognizer()
    text = "default"
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio, language)
        except:
            pass
    if text.lower() == "pause":
        print("Pause command detected. Pausing...")
        print("Say resume to resume...")
        while True:
            r = sr.Recognizer()
            text = "default"

            with sr.Microphone() as source:
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio, language)
                except:
                    pass
            if text.lower() == "resume":
                print("Resuming...")
                break
            else:
                print("Invalid command. Say resume to resume...")

        return "resume"
    else:
        return text
    
def text_to_speech(text, lang):
    '''Converts text to speech'''
    tts = gTTS(text=text, lang=lang)
    tts.save("current.mp3")
    playsound("current.mp3")
    os.remove("current.mp3")

#Loop to randomly select a term, get user input, and interact with GPT-3
while unit_6_terms:
    random_term = random.choice(unit_6_terms)
    print(random_term)
    text_to_speech(random_term, "en")
    user_input = get_user_voice_input()
    print(user_input)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert on information pertaining to the class AP Human Geography. A user will try and explain certain concepts. Tell them if they are right or wrong, and give VERY VERY CONCISE AND SHORT REASONING as to why that is the case."},
            {"role": "user", "content": f"{user_input}"}
        ]
    )
    output = str(completion.choices[0].message.content)
    print(output)
    text_to_speech(output, "en")

    # Remove the selected term from the list to prevent repetition
    unit_6_terms.remove(random_term)
