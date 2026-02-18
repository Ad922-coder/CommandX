import os  # Provides functions to interact with the operating system (like file paths, running commands)
import re  # Regular expressions module for pattern matching and text processing
from shlex import quote  # Safely quotes strings for shell commands to prevent injection issues
import subprocess  # Allows running external commands/programs from Python
from playsound import playsound  # Used to play audio files (like notification sounds)
import eel  # Library to create a web-based GUI (front-end) for Python applications
import pyautogui  # Automates keyboard and mouse actions (clicking, typing, screenshots)
from engine.command import speak  # Custom function to convert text to speech (assistant's voice)
from engine.config import ASSISTANT_NAME, LLM_KEY  # Custom configuration variables (assistant name, API key)
import pywhatkit as kit  # For sending WhatsApp messages, playing YouTube videos, etc.
import sqlite3  # Provides database functionality for storing and retrieving data locally
import webbrowser  # Opens URLs in the default web browser
from engine.helper import extract_yt_term, markdown_to_text, remove_words  # Custom helper functions for text processing
import pvporcupine  # Wake word detection library (to listen for trigger words like "Jarvis")
import pyaudio  # Access and stream audio from microphone or speakers
import struct  # Handles binary data (used with audio streams)
import time  # Provides time-related functions (sleep, timestamps)


conn=sqlite3.connect("jarvis.db")
cursor=conn.cursor()

#Playing assisatnt click sound function

@eel.expose    #This is uses to use this function in main.js

def playAssistantSound():
    music_dir="www\\assets\\vendore\\texllate\\audio\digital-click-357350.mp3"
    playsound(music_dir)

def openCommand(query):
    query=query.replace(ASSISTANT_NAME,"")
    query=query.replace("open","")
    query.lower()

    app_name=query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

            
        
        
                
        

def PlayYoutube(query):
    search_term=extract_yt_term(query)
    speak("Playing "+ search_term +" on Youtube")
    kit.playonyt(search_term)

def PlaySpotify(query):
    search_term=extract_yt_term(query)
    speak("Playing "+ search_term +"on Spotify")
    webbrowser.open("https://open.spotify.com/search/" + search_term.replace(" ", "%20"))


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0



def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 4
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 15
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 14
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)



import google.generativeai as genai
def geminai(query):
    try:
        query=query.replace(ASSISTANT_NAME,"")
        query=query.replace("search","")
        #set your api key
        genai.configure(api_key=LLM_KEY)

        #Select a model
        model=genai.GenerativeModel("gemini-2.0-flash")

        #Generate a response
        response=model.generate_content(query)
        filter_text=markdown_to_text(response.text)
        speak(filter_text)
    
    except Exception as e:
        print("Error:",e)


# To check the whether
# def getWeather(city):
#     try:
#         api_key = ''  # from config
#         base_url = "http://api.openweathermap.org/data/2.5/weather"

#         params = {
#             'q': city,
#             'appid': api_key,
#             'units': 'metric'
#         }

#         response = requests.get(base_url, params=params, headers={"Cache-Control": "no-cache"})
#         data = response.json()

#         if data.get('cod') == 200:
#             temp = data['main']['temp']
#             weather = data['weather'][0]['description']
#             humidity = data['main']['humidity']
#             result = f"The temperature in {city} is {temp}°C with {weather}. Humidity is {humidity}%."
#             speak(result)
#             return result
#         else:
#             speak("Sorry, I couldn't find that city.")
#             return "City not found."

#     except Exception as e:
#         print("Weather API error:", e)
#         speak("Sorry, I am unable to get the weather right now.")
