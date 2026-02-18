from email.mime import audio  # Used to create audio MIME objects for sending audio via email (less common, only for email attachments)
import pyttsx3  # Text-to-speech library to convert text into spoken voice (offline, no internet needed)
import speech_recognition as sr  # For recognizing and converting spoken words from microphone into text
import eel  # Library to create a web-based GUI for Python applications (front-end interface)
import time  # Provides time-related functions like sleep, timestamps, and delays


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    engine.setProperty('rate', 140)
    if text:
        eel.DisplayMessage(text)
        engine.say(text)
        eel.receiverText(audio)
        engine.runAndWait()

@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('listening')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
            print('Recognizing...')
            eel.DisplayMessage('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            eel.DisplayMessage(query)
            time.sleep(2)

            
        except sr.WaitTimeoutError:
            print("Error: Listening timed out waiting for phrase to start.")
            return ""
        except sr.RequestError as e:
            print(f"Error: Could not request results from Google. {e}")
            return ""
        except sr.UnknownValueError:
            print("Error: Google Speech Recognition could not understand audio.")
            return ""
        return query.lower()
# if __name__ == "__main__":
#     text = takecommand()
#     if text:
#         speak(text)
#     else:
#         print("No valid input detected. Please try again.")
@eel.expose
def allCommands(message=1):

    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query)
    
    else:
        query=message
        eel.senderText(query)

    try:
        # query=takecommand()
        # print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "on spotify" in query:
            from engine.features import PlaySpotify
            PlaySpotify(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact,whatsApp
            flag=""
            contact_no,name=findContact(query)
            if(contact_no!=0):

                if "send message" in query:
                    flag='message'
                    speak("What message to send")
                    query=takecommand()
                elif "phone call" in query:
                    flag='call'
                else:
                    flag='video call'
                
                whatsApp(contact_no,query,flag,name)
        elif "weather" in query or "temperature" in query:
            speak("Which city do you want the weather for?")
            city = takecommand()
            from engine.features import getWeather
            getWeather(city)

        else:
            from engine.features import geminai
            geminai(query)
    except:
        print("Error")
    eel.ShowHood()