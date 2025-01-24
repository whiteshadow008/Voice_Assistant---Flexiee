import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import psutil
import datetime
import random

from bs4 import BeautifulSoup
import requests
engine = pyttsx3.init()

voices=engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input and return the recognized command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except sr.RequestError:
            speak("There seems to be a network error. Please check your connection.")
        return None

def open_application(app_name):
    """Open the application specified by the user."""
   
    apps = {
    # System Utilities
    "notepad": "notepad.exe",  # Notepad
    "calculator": "calc.exe",  # Calculator

    # Browsers
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",  # Google Chrome
    "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",  # Mozilla Firefox
    "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",  # Microsoft Edge

    # Media Players
    "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",  # VLC Media Player
    "media player": "C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe",  # Windows Media Player

    # Office Applications
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",  # Microsoft Word
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",  # Microsoft Excel
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",  # Microsoft PowerPoint
    "wps": "C:\\Users\\Dhanush\\OneDrive\\Desktop\\WPS Office.lnk",  # WPS Office (custom path)

    # Music and Streaming
    "spotify": "C:\\Users\\Dhanush\\Spotify\\Spotify.exe",  # Spotify

    # Developers Tools
    "vs code": "C:\\Users\\Dhanush\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",  # Visual Studio Code

    # File Explorers
    "music":"C:\\Users\\Dhanush\\Music",
    "downloads": "C:\\Users\\Dhanush\\Downloads",  # Downloads Folder
    "documents": "C:\\Users\\Dhanush\\Documents",  # Documents Folder
    "pictures": "C:\\Users\\Dhanush\\Pictures",  # Pictures Folder
    "record": "D:\\RECORD",  # Custom Folder Path
    "task manager":" C:\\Windows\\System32\\Taskmgr.exe",
    "command prompt": "C:\\Windows\\System32\\cmd.exe",
    "power shell": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
    "snipping Tool": "C:\\Windows\\System32\\SnippingTool.exe",
    "whatsapp":"https://www.microsoft.com/store/productId/9NKSQGP7F2NH?ocid=libraryshare",
    # Web Search (Placeholder for browser)
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "control panel":" C:\\Windows\\System32\\control.exe",
   
  # Replace with any other app or file path
}
    for key, path in apps.items():
        if key in app_name:
            try:
                os.startfile(path)
                speak(f"Opening {key}")
                return
            except Exception as e:
                speak(f"Sorry, I couldn't open {key}.")
                print(f"Error: {e}")
                return
    speak("Sorry, I don't know how to open that application.")

def search_web(query):
    """Perform a web search for the given query."""
    if "google" in query:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    elif "fire fox" in query:
        firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # Update this if Firefox is installed elsewhere
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
    else:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    webbrowser.open(search_url)
    speak(f"Searching for {query} on the web.") 


def tell(command):
    """Responds to specific commands like time, date, and day."""
    now = datetime.datetime.now()
    
    if "time" in command:
        current_time = now.strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        print(f"The current time is {current_time}.")
    
    elif "date" in command:
        current_date = now.strftime("%B %d, %Y")  # Example: January 6, 2025
        speak(f"Today's date is {current_date}.")
        print(f"Today's date is {current_date}.")
    
    elif "day" in command:
        current_day = now.strftime("%A")  # Example: Monday
        speak(f"Today is {current_day}.")
        print(f"Today is {current_day}.")
    
    elif "joke" in command:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "Why was the math book sad? Because it had too many problems.",
            "Why did the bicycle fall over? It was two-tired!"
        ]
        joke = random.choice(jokes)
        speak(joke)
        print(joke)
    
    else:
        speak("I don't have a response for that. Please try asking something else.")

def provide_help(command=None):
    """Provides help and support information."""
    general_help = """
    Here are some things I can do:
    1. Open applications (e.g., "Open Chrome").
    2. Close applications (e.g., "Close Notepad").
    3. Search the web (e.g., "Search for the weather in New York").
    4. Perform system tasks (e.g., "Shut down the computer" or "Open Wi-Fi settings").
    5. Play music (e.g., "Play [song name]").
    6. Tell the time or date (e.g., "What time is it?" or "What's today's date?").
    7. Tell jokes or fun facts (e.g., "Tell me a joke").
    8. Provide weather updates (e.g., "What's the weather like today?").
    
    You can ask "How do I [task]?" for detailed instructions.
    """
    if not command:
        print(general_help)
        speak(general_help)
    else:
        # Explain specific command
        if "open" in command:
            speak("To open an application, say 'Open' followed by the application's name. For example, 'Open Chrome'.")
        elif "close" in command:
            speak("To close an application, say 'Close' followed by the application's name. For example, 'Close Notepad'.")
        elif "search" in command:
            speak("To search the web, say 'Search for' followed by your query. For example, 'Search for the weather in New York'.")
        elif "time" in command or "date" in command:
            speak("To know the time or date, just ask 'What time is it?' or 'What's today's date?'.")
        else:
            speak("I'm sorry, I don't have detailed instructions for that command yet.")

def get_user_confirmation(action_name, action_command):
    """General function to get user confirmation for system actions like restart or hibernate."""
    speak(f"Are you sure you want to {action_name} the system? Please say 'yes' to confirm or 'no' to cancel.")
    
    max_attempts = 2
    attempts = 0
    
    while attempts < max_attempts:
        user_response = listen()
        if user_response:
            print(f"User said: {user_response}")
            
            if "command" in user_response or action_name in user_response:
                speak(f"{action_name.capitalize()} the system. Please wait.")
                os.system(action_command)  # Execute the system action
                return
            elif "no" in user_response or "cancel" in user_response:
                speak(f"{action_name.capitalize()} operation canceled.")
                return
            else:
                speak("I didn't understand that. Please say 'yes' to confirm or 'no' to cancel.")
        else:
            speak("I didn't hear anything. Please try again.")
        
        attempts += 1

    speak(f"I couldn't understand your response. Aborting {action_name} operation.")

def sleep_system():
    get_user_confirmation("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def restart_system():
    """Restarts the system after user voice confirmation."""
    get_user_confirmation("restart", "shutdown /r /t 5")

def hibernate_system():
    """Hibernates the system after user voice confirmation."""
    get_user_confirmation("hibernate", "shutdown /h")

def lock_system():
    get_user_confirmation("lock","rundll32.exe user32.dll,LockWorkStation")

def shutdown_system():
   get_user_confirmation("shutdown", "shutdown /s /t 5 ")

def get_definition(term):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return definition
    else:
        return None

def get_wikipedia_info(term):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        extract = data.get('extract', 'Sorry, no description available.')
        return extract
    else:
        return None

def master():
    speak("you are my Master Dhanush Nataraj ; you created me ;")
    speak(" i am your voice assistant flexiee!")

def close_application(app_name):

    for process in psutil.process_iter(['name', 'pid']):
        if process.info['name'] and app_name.lower() in process.info['name'].lower():
            try:
                process.terminate() 
                process.wait(timeout=5) 
                print(f"{app_name} has been closed gracefully.")
                return
            except psutil.NoSuchProcess:
                print(f"{app_name} process no longer exists.")
                return
            except psutil.AccessDenied:
                print(f"Permission denied to close {app_name}.")
                return
    print(f"No app named {app_name} found running.")
import openai

# Initialize OpenAI API key
openai.api_key = "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"
def generate_fun_response(user_input):
    """Generate a fun response using GPT-3."""
    try:
        prompt = f"Give me a fun response to the following: {user_input} (Make it entertaining and lighthearted)"
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # Use GPT-3's Davinci engine for creative responses
            prompt=prompt,
            max_tokens=50,  # Limit the length of the response to make it short and sweet
            temperature=0.8  # Set temperature to make the response more creative and fun
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error in AI response generation: {e}")
        return "Oops! Something went wrong. Let's try again!"

# Function for interactive fun chat mode
def chat():
    """Activate AI fun chat interface with voice response."""
    speak("Hello! I'm ready to chat with you. Ask me anything fun!")

    while True:
        user_input = listen()
        
        if user_input:
            if "exit chat" in user_input:
                speak("Exiting chat. I'm ready to hear another command.")
                break  # Exit chat mode and return to the main command listener

            # Generate fun response
            fun_response = generate_fun_response(user_input)

            # Speak out the AI's fun response
            speak(fun_response)
# Example usage in the main function
def main():
    speak("Hi, I am Flexiee, your voice assistant.")
    silence_count = 0 
    while True:
        command = listen()
        if command:
            silence_count = 0 
            if any(keyword in command for keyword in ("joke", "time", "day", "date")):
                tell(command)
            elif any(keyword in command for keyword in ("exit", "quit", "bye")):
                speak("Goodbye!")
                break
            elif "shutdown" in command:
                shutdown_system()
            elif "restart" in command:
                restart_system()
            elif "hibernate" in command:
                hibernate_system()
            elif "sleep" in command:
                sleep_system()
            elif "lock" in command:
                lock_system()
            elif "help" in command:
                if "how do i" in command or "tell me " in command:
                    specific_command = command.replace("help", "").replace("how do i", "").strip()                            
                    provide_help(specific_command)
                else:
                    provide_help()
            elif "who am i" in command:
                master()
            elif "hi" in command:
                chat()
            elif "open" in command:
                app_name = command.replace("open", "").strip()
                open_application(app_name)
            elif "close" in command:
                app_name = command.replace("close", "").strip()
                close_application(app_name)
            elif any(keyword in command for keyword in ("define", "meaning of", "what is")):
                if "define" in command:
                        term = command.replace("define", "").strip()
                elif "meaning of" in command:
                        term = command.replace("meaning of", "").strip()
                elif "what is" in command:
                        term = command.replace("what is", "").strip()
                if term:
                    definition = get_definition(term)
                    if definition:
                        speak(f"The definition of {term} is: {definition}")
                    else:
                        wikipedia_info = get_wikipedia_info(term)
                        if wikipedia_info:
                            speak(f"Wikipedia result for {term}: {wikipedia_info}")
                        else:
                            speak(f"Sorry, I couldn't find any information on {term}. Please try another term.")
            elif any(keyword in command for keyword in ("search", "find")):
                query = command.replace("search for", "").strip()
                search_web(query) 
            else:
                speak("I didn't understand that. Please say 'help' for a list of commands.")
        else:
            silence_count += 1
        if silence_count >= 3:
            speak("You seem to be silent. Goodbye!")
            break

if __name__ == "__main__":
    main()
