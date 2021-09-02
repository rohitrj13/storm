from django.shortcuts import render, HttpResponse, redirect
import os
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import webbrowser
import ctypes

# Create your views here.

query = ""
response = ""


def index(request):
    return render(request,'info/index.html')





def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    newVoiceRate = 145
    engine.setProperty('rate', newVoiceRate)
    engine.say(audio)
    engine.runAndWait()


    
def listen(request):
    global query
    query = takecommand()
    query = query.lower()
    print(query)
    global response
    response = "Sorry I was unable to understand your command"
    if(query=='none'):
        query = "Please say that again"
        return redirect('listened',stage=10)
    elif "who are you" in query:
        response = "I am your Voice Assistant,STORM"
        return redirect('listened',stage=0)
    elif ("who" in query) and ("the" in query):
        response = "I am your fucking voice assistant,STORM" 
        return redirect('listened',stage=0)
    elif "stop listening" in query:
        speak('Listening stopped')
        return redirect('index')
    elif "play music" in query:
        speak('Playing Music')
        music_dir = 'R:\\songs'
        all_songs = os.listdir(music_dir)
        print(all_songs)
        os.startfile(os.path.join(music_dir , all_songs[0]))
        return redirect('index')
    elif "the time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The time is {current_time}"
        return redirect('listened',stage=1)
    elif "joke" in query:
        My_joke = pyjokes.get_joke(language="en", category="neutral") 
        response = My_joke
        return redirect('listened',stage=0)
    elif "wikipedia" in query:
        query = query.replace('wikipaedia',"")
        results = wikipedia.summary(query,sentences =2)
        speak("According to Wikipedia")
        print(results)
        response = results
        return redirect('listened',stage=0)
    elif "play" in query:
        query = query.replace('play','')
        query = query.replace('song','')
        query = query.replace(' ','+')
        
        print(query)
        
        opts = Options()
        opts.headless = False
        browser = Firefox(options=opts)
        browser.get("https://www.youtube.com/results?search_query="+query)
        time.sleep(2)
        box = browser.find_elements_by_class_name('style-scope ytd-thumbnail')
        box[0].click()
        tym = browser.find_elements_by_class_name('ytd-thumbnail-overlay-time-status-renderer')
        print(tym)
        time.sleep(20)
        browser.close()
        print('Done')
        print(len(tym))
        return redirect('listen')
    elif 'open youtube' in query:
        speak("Here you go to Youtube\n")
        webbrowser.open("youtube.com")
        return redirect('index')
 
    elif 'open google' in query:
        speak("Here you go to Google\n")
        webbrowser.open("google.com")
        return redirect('index')
 
    elif 'open stackoverflow' in query:
        speak("Here you go to Stack Over flow.Happy coding")
        webbrowser.open("stackoverflow.com")
        return redirect('index')
        
    elif "who made you" in query or "who created you" in query: 
        response = 'I have been created by the use of Python'
        
        return redirect('listened',stage=0)

    elif 'is love' in query:
        speak("It is 7th sense that destroy all other senses")
        return redirect('listen')

    elif 'search' in query:
             
        query = query.replace("search", "") 
        query = query.replace("play", "")          
        webbrowser.open(query) 
        return redirect('index')

    elif 'window' in query:
        speak("locking the device")
        ctypes.windll.user32.LockWorkStation()
        return redirect('index')
 
    return render(request,'info/listened.html',{'query':query,'stage':0})
    
    
def listened(request,stage):
    if(stage == 0):
        return render(request,'info/listened.html',{'query':query,'stage':0})
    elif(stage == 1):
        if(response!=""):
            speak(response)
        return render(request,'info/listened.html',{'query':'none','stage':1})
        
    return render(request,'info/listened.html',{'query':query,'stage':stage})


    

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source,duration=0.5)
        print('Listening...')
        audio_file = r.record(source,duration=3)
        print("___")
    try:
        query = r.recognize_google(audio_file,language='en-in')
        print(query)
        
    except Exception as e:
        print(e)
        print("Please say That Again..!!")
        return "None"
    return query

def phase2(request):
    #speak('Please say that again')
    return render(request,'info/base2.html',{'query':"Please say that again",'stage':2})

