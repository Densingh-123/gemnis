# ==============================================================================
#  J.A.R.V.I.S 4.1 - A Personalized AI Assistant (Hacker UI Edition)
# ==============================================================================
#
#  Author: Densingh
#  Version: 4.1 (Enhanced Edition)
#
# ==============================================================================

import streamlit as st
import json
import base64
import time
import os
import sys
import webbrowser
import random
import datetime
import requests
import pyautogui
import psutil
import speedtest
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from pynput.keyboard import Key, Controller as KeyboardController
import google.generativeai as genai
import numpy as np
import pandas as pd
import wikipedia
import wolframalpha

# --- Embedded API Keys ---
GOOGLE_GEMINI_API_KEY = "AIzaSyDtocV5hj33vKT8NiUMUSLQPGtNneAjXcw"
WOLFRAM_ALPHA_APP_ID = "fa6b4bd3987f4d058564cf9277268913"
OPENWEATHER_API_KEY = "2fd506e89b19f4cfa2d6cef84a0bef58"

# --- Page Configuration ---
st.set_page_config(
    page_title="J.A.R.V.I.S 4.1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Hacker UI Background ---
BACKGROUND_IMAGE = "https://cdn.dribbble.com/userupload/32349104/file/still-bb4ca24ed43ac46181878740857a0605.gif?resize=400x0"

# --- Custom UI Styling (Hacker Theme) ---
def apply_custom_css():
    hacker_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
    
    .stApp {{
        background-image: url("{BACKGROUND_IMAGE}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: #00ff41 !important;
    }}
    
    .st-emotion-cache-18ni7ap {{
        background-color: rgba(0, 0, 0, 0.8) !important;
    }}
    
    h1, h2, h3 {{
        font-family: 'Orbitron', sans-serif;
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
        text-align: center;
        animation: flicker 2s infinite alternate;
    }}
    
    @keyframes flicker {{
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {{
            text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
            opacity: 1;
        }}
        20%, 24%, 55% {{
            text-shadow: none;
            opacity: 0.8;
        }}
    }}
    
    .stChatMessage {{
        width:70%;
        background-color: rgba(0, 20, 0, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #00ff41 !important;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41 !important;
    }}
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        background-color: rgba(0, 10, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 10px;
        font-family: 'Share Tech Mono', monospace;
        height: 100px;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #008f27 !important;
    }}
    
    .stButton > button {{
        background-color: rgba(0, 30, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 10px;
        font-family: 'Share Tech Mono', monospace;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: rgba(0, 50, 0, 0.8) !important;
        box-shadow: 0 0 15px #00ff41;
    }}
    
    .audio-recorder {{
        background-color: rgba(0, 30, 0, 0.8) !important;
        border: 1px solid #00ff41 !important;
        border-radius: 50px !important;
        box-shadow: 0 0 10px #00ff41 !important;
        width: 50px !important;
        height: 50px !important;
        margin-top: 10px !important;
    }}
    
    .audio-recorder:hover {{
        box-shadow: 0 0 15px #00ff41 !important;
    }}
    
    .st-emotion-cache-1c7y2kd {{
        background-color: rgba(0, 15, 0, 0.8) !important;
        border: 1px solid #00ff41 !important;
    }}
    
    .mode-selector {{
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }}
    
    .mode-button {{
        background-color: rgba(0, 30, 0, 0.8);
        color: #00ff41;
        border: 1px solid #00ff41;
        border-radius: 10px;
        padding: 10px 20px;
        margin: 0 10px;
        font-family: 'Share Tech Mono', monospace;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .mode-button.active {{
        background-color: rgba(0, 60, 0, 0.8);
        box-shadow: 0 0 15px #00ff41;
    }}
    
    .status-bar {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(0, 10, 0, 0.8);
        border-top: 1px solid #00ff41;
        padding: 5px 20px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        z-index: 100;
    }}
    
    audio {{
        display: none !important;
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
        100% {{ opacity: 1; }}
    }}
    
    .status-panel {{
        position: fixed;
        top: 40px;
        right: 40px;
        width: 500px;
        height: 550px;
        background-color: rgba(0, 10, 0, 0.8);
        border: 1px solid #00ff41;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Share Tech Mono', monospace;
        z-index: 100;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
    }}
    
    .status-header {{
        text-align: center;
        font-size: 18px;
        margin-bottom: 15px;
        color: #00ff41;
        text-shadow: 0 0 5px #00ff41;
    }}
    
    .status-item {{
        margin-bottom: 10px;
        padding: 8px;
        background-color: rgba(0, 20, 0, 0.5);
        border-radius: 5px;
        border: 1px solid #008f27;
    }}
    
    .status-label {{
        font-weight: bold;
        margin-bottom: 3px;
    }}
    
    .status-value {{
        color: #00ff41;
    }}
    .status-value.top_left {{
    position: absolute;
   
    left: 65px;
    font-size: 36px;
    font-family: 'Orbitron', sans-serif;
    color: #00ff41;
    text-shadow:
        0 0 5px #00ff41,
        0 0 10px #00ff41,
        0 0 15px #00ff41,
        0 0 20px #00ff41;
    z-index: 9999;
    user-select: none;
}}
    .status-meter {{
        height: 10px;
        background-color: rgba(0, 20, 0, 0.5);
        border-radius: 5px;
        margin-top: 5px;
        overflow: hidden;
    }}
    
    .status-meter-inner {{
        height: 100%;
        background-color: #00ff41;
        box-shadow: 0 0 5px #00ff41;
    }}
    
    .typing-cursor {{
        display: inline-block;
        width: 8px;
        height: 20px;
        background-color: #00ff41;
        animation: blink 1s infinite;
        margin-left: 4px;
        vertical-align: middle;
    }}
    
    @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
    }}
    </style>
    """
    st.markdown(hacker_css, unsafe_allow_html=True)

# ==============================================================================
# --- THE CORE ASSISTANT ENGINE ---
# ==============================================================================
class JarvisAssistant:
    def __init__(self, user_name="Densingh"):
        self.user_name = user_name
        self.keyboard = KeyboardController()
        
        # Initialize data first
        self.personal_data = self._load_personal_data()
        self.timetable = self._load_timetable()
        self.app_map = {"command prompt": "cmd", "paint": "mspaint", "word": "winword", 
                        "excel": "excel", "chrome": "chrome", "vscode": "code", 
                        "powerpoint": "powerpnt", "edge": "msedge", "firefox": "firefox",
                        "brave": "brave"}
        
        # Configure APIs with embedded keys
        self.configure_apis(GOOGLE_GEMINI_API_KEY, WOLFRAM_ALPHA_APP_ID, OPENWEATHER_API_KEY)

    def _load_personal_data(self):
        return {
            "full name": "My designation is Densingh D.", 
            "date of birth": "My birthdate is recorded as June 9th, 2005.",
            "skills": "Your profile indicates proficiency in Java, JavaScript, Python, C, C++, and TypeScript, with experience in frameworks like React, React Native, Spring Boot, and Node.js.",
            "projects": "You have successfully developed an E-commerce Platform, a Meal-Tracker App, and a Doctor Appointment System.",
            "gpa": "Your current Grade Point Average is 7.54 out of 10.",
            "college": "You are enrolled in a B.Tech in Information Technology at R.M.K Engineering College, with an expected graduation in 2026."
        }
        
    def _load_timetable(self):
        return {
            "TUESDAY": {"2": {"time": "09:40 - 11:20", "course": "Placement AAL"}, "3": {"time": "11:20 - 12:10", "course": "Placement TAA"}, "5": {"time": "13:50 - 14:40", "course": "Placement KSN"}},
            "WEDNESDAY": {"1": {"time": "08:50 - 09:40", "course": "Microservice Architecture"}, "2": {"time": "09:40 - 11:20", "course": "Microservice Architecture Lab"}, "5": {"time": "13:50 - 15:30", "course": "Placement TMM"}},
            "THURSDAY": {"1": {"time": "08:50 - 09:40", "course": "Professional Ethics"}, "3": {"time": "11:20 - 12:10", "course": "Natural Language Processing"}, "5": {"time": "13:50 - 15:30", "course": "Robotic Operating System"}},
            "FRIDAY": {"1": {"time": "08:50 - 09:40", "course": "Scalable Messaging Infrastructure"}, "2": {"time": "09:40 - 11:20", "course": "Image and Video Analytics"}, "5": {"time": "13:50 - 15:30", "course": "Placement RRJ"}},
            "SATURDAY": {"1": {"time": "08:50 - 09:40", "course": "Professional Readiness for Innovation"}, "2": {"time": "09:40 - 11:20", "course": "Placement TMM"}, "4": {"time": "12:10 - 13:00", "course": "Library"}, "5": {"time": "13:50 - 15:30", "course": "Placement SSH"}}
        }

    def configure_apis(self, gemini_key, wolfram_id, openweather_key):
        """Configures the assistant with the provided API keys."""
        self.GOOGLE_GEMINI_API_KEY = gemini_key
        self.WOLFRAM_ALPHA_APP_ID = wolfram_id
        self.OPENWEATHER_API_KEY = openweather_key
        
        try:
            if self.GOOGLE_GEMINI_API_KEY:
                genai.configure(api_key=self.GOOGLE_GEMINI_API_KEY)
                model = genai.GenerativeModel(
                    'gemini-1.5-flash',
                    system_instruction=f"You are JARVIS, a helpful and witty AI assistant for a user named {self.user_name}. Be concise, friendly, and use a futuristic, tech-savvy tone. Your primary goal is to assist the user efficiently."
                )
                self.chat = model.start_chat(history=[])
                return True
            return False
        except Exception as e:
            st.error(f"Failed to initialize Gemini: {e}")
            self.chat = None
            return False

    def greet_user(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: greeting = "Good morning"
        elif 12 <= hour < 18: greeting = "Good afternoon"
        else: greeting = "Good evening"
        return f"{greeting}, {self.user_name}. J.A.R.V.I.S. systems are online and ready."

    # --- Main Command Handler ---
    def handle_command(self, query):
        query = query.lower().strip()
        
        command_map = {
            "hello": lambda q: f"Hello {self.user_name}, how can I be of service?",
            "hi": lambda q: f"Hello {self.user_name}, how can I be of service?",
            "hey": lambda q: f"Hello {self.user_name}, how can I be of service?",
            "jarvis": lambda q: f"At your service, {self.user_name}.",
            "schedule": self.get_schedule,
            "time table": self.get_schedule,
            "time": lambda q: f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.",
            "date": lambda q: f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}.",
            "weather": self.get_weather,
            "temperature": self.get_weather,
            "calculate": self.calculate,
            "google": lambda q: self.search_web(q.replace("google", "").strip(), "google"),
            "youtube": lambda q: self.search_web(q.replace("youtube", "").strip(), "youtube"),
            "wikipedia": lambda q: self.search_web(q.replace("wikipedia", "").strip(), "wikipedia"),
            "edge": lambda q: self.search_web(q.replace("edge", "").strip(), "edge"),
            "firefox": lambda q: self.search_web(q.replace("firefox", "").strip(), "firefox"),
            "brave": lambda q: self.search_web(q.replace("brave", "").strip(), "brave"),
            "open": lambda q: self.open_local_app(q.replace("open", "").strip()),
            "close": lambda q: self.close_local_app(q.replace("close", "").strip()),
            "screenshot": self.take_screenshot,
            "volume up": lambda q: self.adjust_volume("up"),
            "volume down": lambda q: self.adjust_volume("down"),
            "play": lambda q: self.control_media("playpause"),
            "pause": lambda q: self.control_media("playpause"),
            "mute": lambda q: self.control_media("mute"),
            "audio on": lambda q: self.adjust_volume("up"),
            "sound on": lambda q: self.adjust_volume("up"),
            "speed test": self.run_speed_test,
            "internet speed": self.run_speed_test,
            "system info": self.get_system_info,
            "thank you": lambda q: "You're welcome, sir. Always at your service.",
            "thanks": lambda q: "You're welcome, sir. Always at your service.",
            "help": lambda q: self.get_help(),
            "what can you do": lambda q: self.get_help(),
            "joke": lambda q: self.tell_joke(),
            "shutdown": lambda q: self.system_shutdown(),
        }

        for key, value in self.personal_data.items():
            if key in query:
                return value
        
        for keyword, func in command_map.items():
            if keyword in query:
                return func(query)
        
        return self.get_gemini_response(query)

    def get_help(self):
        """Returns a list of available commands"""
        help_text = """
        **I can assist you with the following:**
        - Check your class schedule (`schedule` or `time table`)
        - Get current time and date (`time`, `date`)
        - Check weather conditions (`weather`)
        - Perform calculations (`calculate [expression]`)
        - Web searches (`google [query]`, `youtube [query]`)
        - Open/close applications (`open [app name]`, `close [app name]`)
        - Take screenshots (`screenshot`)
        - Control media (`play`, `pause`, `volume up`, `volume down`)
        - Run internet speed tests (`speed test`)
        - Get system information (`system info`)
        - Tell a joke (`joke`)
        - Simulate system shutdown (`shutdown`)
        - And much more using AI capabilities!
        """
        return help_text

    def tell_joke(self):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What do you call a computer that sings? A Dell!",
            "Why was the JavaScript developer sad? Because he didn't know how to express himself!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why do Java developers wear glasses? Because they can't C#!"
        ]
        return random.choice(jokes)

    def system_shutdown(self):
        shutdown_sequence = [
            "Initiating system shutdown protocol",
            "Saving all active sessions",
            "Closing network connections",
            "Terminating background processes",
            "All systems secured",
            "Goodbye sir. J.A.R.V.I.S. signing off"
        ]
        return "\n".join(shutdown_sequence)

    def get_gemini_response(self, query):
        if not self.chat:
            return "Gemini AI is not configured. Please enter the API key in the sidebar."
        try:
            response = self.chat.send_message(query)
            return response.text
        except Exception as e:
            return f"An error occurred with the Gemini API: {e}"

    def get_weather(self, query=None):
        if not self.OPENWEATHER_API_KEY:
            return "OpenWeatherMap API key is not configured."

        try:
            city = "Chennai"  # Default city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.OPENWEATHER_API_KEY}&units=metric"
            res = requests.get(url).json()

            if res.get("cod") != 200:
                return f"Could not retrieve weather for {city}. Error: {res.get('message', 'Unknown Error')}"

            temp = res["main"]["temp"]
            feels_like = res["main"]["feels_like"]
            humidity = res["main"]["humidity"]
            description = res["weather"][0]["description"]
            return (f"Weather in {city}: {description.capitalize()}\n"
                    f"Temperature: {temp}°C (Feels like: {feels_like}°C)\n"
                    f"Humidity: {humidity}%")
        except Exception as e:
            return f"Sorry, I couldn't fetch the weather. Error: {e}"

    def calculate(self, query):
        if not self.WOLFRAM_ALPHA_APP_ID:
            return "WolframAlpha App ID is not configured."
        try:
            client = wolframalpha.Client(self.WOLFRAM_ALPHA_APP_ID)
            res = client.query(query.replace("calculate", "").strip())
            answer = next(res.results).text
            return f"The calculated result is: {answer}."
        except Exception:
            return self.get_gemini_response(f"Calculate: {query}")
            
    def search_web(self, query, engine):
        query = query.strip()
        if engine == "google":
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Here are the Google search results for '{query}'."
        elif engine == "youtube":
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Searching YouTube for '{query}'."
        elif engine == "wikipedia":
            try:
                return self.get_gemini_response(f"Summarize the key points from the Wikipedia page for '{query}' in a concise paragraph.")
            except Exception as e:
                return f"I couldn't get a summary for that. Error: {e}"
        elif engine == "edge":
            webbrowser.open(f"microsoft-edge:https://www.bing.com/search?q={query}")
            return f"Searching Bing via Edge for '{query}'."
        elif engine == "firefox":
            webbrowser.open(f"https://www.bing.com/search?q={query}", new=2)
            return f"Searching via Firefox for '{query}'."
        elif engine == "brave":
            webbrowser.open(f"https://search.brave.com/search?q={query}")
            return f"Searching via Brave for '{query}'."

    def get_schedule(self, query=None):
        day_name = datetime.datetime.now().strftime('%A').upper()
        if day_name in self.timetable and self.timetable[day_name]:
            schedule_text = f"**Schedule for Today ({day_name}):**\n"
            for period, details in self.timetable[day_name].items():
                schedule_text += f"- **{details['course']}**: {details['time']} (Period {period})\n"
            return schedule_text
        return "You have no classes scheduled for today. Enjoy your day off!"

    def open_local_app(self, app_name):
        app_cmd = self.app_map.get(app_name)
        if app_cmd:
            os.system(f"start {app_cmd}")
            return f"Affirmative. Launching {app_name}."
        return f"I don't have a protocol for opening {app_name}, sir."

    def close_local_app(self, app_name):
        app_cmd = self.app_map.get(app_name)
        if app_cmd:
            os.system(f"taskkill /f /im {app_cmd}.exe")
            return f"Terminating {app_name} process."
        return f"Unable to specifically close {app_name}."

    def take_screenshot(self, query=None):
        try:
            path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            pyautogui.screenshot(path)
            return f"Screenshot captured and saved to your desktop."
        except Exception as e:
            return f"Failed to capture screenshot: {e}"

    def adjust_volume(self, direction):
        key = Key.media_volume_up if direction == "up" else Key.media_volume_down
        for _ in range(5):
            self.keyboard.press(key); self.keyboard.release(key); time.sleep(0.1)
        return f"System volume adjusted {direction}."

    def control_media(self, action):
        if action == "playpause":
            pyautogui.press("playpause")
            return "Playback toggled."
        elif action == "mute":
            pyautogui.press("volumemute")
            return "Mute toggled."
        return ""

    def run_speed_test(self, query=None):
        st.info("Running internet speed test... This may take a moment.")
        try:
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download()
            s.upload()
            res = s.results.dict()
            dl_speed = f"{res['download'] / 1_000_000:.2f} Mbps"
            ul_speed = f"{res['upload'] / 1_000_000:.2f} Mbps"
            ping = f"{res['ping']:.2f} ms"
            return f"**Internet Speed Test Results:**\n- **Download:** {dl_speed}\n- **Upload:** {ul_speed}\n- **Ping:** {ping}"
        except Exception as e:
            return f"An error occurred during the speed test: {e}"
            
    def get_system_info(self, query=None):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        return f"**System Status:**\n- **CPU Load:** {cpu_usage}%\n- **RAM Usage:** {ram_usage}%\n- **Disk Usage:** {disk_usage}%"

# --- Text-to-Speech & Speech-to-Text Functions ---
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        audio_fp = "temp_audio.mp3"
        tts.save(audio_fp)
        with open(audio_fp, "rb") as f:
            audio_bytes = f.read()
        os.remove(audio_fp)
        return audio_bytes
    except Exception as e: 
        st.error(f"Text-to-speech error: {e}")
        return None

def speech_to_text(audio_data):
    if not audio_data: 
        return ""
    r = sr.Recognizer()
    try:
        # Save audio to file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data)
        
        # Adjust for ambient noise
        with sr.AudioFile("temp_audio.wav") as source:
            r.adjust_for_ambient_noise(source, duration=1.0)
            audio = r.record(source)
        
        # Recognize with Google
        text = r.recognize_google(audio, language='en-in')
        os.remove("temp_audio.wav")
        return text
    except sr.UnknownValueError:
        return "I couldn't understand the audio. Please try again."
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"
    except Exception as e:
        return f"Audio processing error: {str(e)}"

# --- System Status Panel ---
def display_system_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    status_html = f"""
    <div class="status-panel">
        <div class="status-header">SYSTEM STATUS</div>
        <div class="status-item">
            <div class="status-label">CPU Usage</div>
            <div class="status-value">{cpu_usage}%</div>
            <div class="status-meter">
                <div class="status-meter-inner" style="width: {cpu_usage}%"></div>
            </div>
        </div>
        <div class="status-item">
            <div class="status-label">RAM Usage</div>
            <div class="status-value">{ram_usage}%</div>
            <div class="status-meter">
                <div class="status-meter-inner" style="width: {ram_usage}%"></div>
            </div>
        </div>
        <div class="status-item">
            <div class="status-label">Disk Usage</div>
            <div class="status-value">{disk_usage}%</div>
            <div class="status-meter">
                <div class="status-meter-inner" style="width: {disk_usage}%"></div>
            </div>
        </div>
        <div class="status-item">
            <div class="status-label">System Time</div>
            <div class="status-value">{datetime.datetime.now().strftime('%H:%M:%S')}</div>
        </div>
        <div class="status-item">
            <div class="status-label">Network Status</div>
            <div class="status-value">Online</div>
        </div>
    </div>
    <div>
     <div class="status-value top_left">{datetime.datetime.now().strftime('%H:%M:%S')}</div>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)

# ==============================================================================
# --- MAIN STREAMLIT APP UI ---
# ==============================================================================
apply_custom_css()

# --- Weather/DateTime Display ---
def display_weather_or_datetime_box(content):
    box_css = """
    <style>
    .weather-box {
        position: fixed;
        bottom: 240px;
        right: 40px;
        width: 500px;
        background-color: rgba(0, 10, 0, 0.85);
        border: 1px solid #00ff41;
        border-radius: 10px;
        padding: 15px;
        z-index: 1000;
        font-family: 'Share Tech Mono', monospace;
        box-shadow: 0 0 15px #00ff41;
        color: #00ff41;
    }
    </style>
    """
    st.markdown(box_css, unsafe_allow_html=True)
    weather_html = f"""
    <div class="weather-box">
        <strong>🛰️ Location: Chennai</strong><br>
        {content}
    </div>
    """
    st.markdown(weather_html, unsafe_allow_html=True)

try:
    weather_response = st.session_state.assistant.get_weather()
    if "Could not retrieve weather" in weather_response or "API key" in weather_response:
        raise Exception("Weather unavailable")
    display_weather_or_datetime_box(weather_response.replace('\n', '<br>'))
except:
    now = datetime.datetime.now()
    fallback_info = f"""<br>
        📆 Date: {now.strftime('%B %d, %Y')}<br>
        ⏰ Time: {now.strftime('%I:%M %p')}<br>
        🕓 Day: {now.strftime('%A')}
    """
    display_weather_or_datetime_box(fallback_info)

display_system_status()

# --- Session State Initialization ---
if 'assistant' not in st.session_state:
    st.session_state.assistant = JarvisAssistant(user_name="Densingh")
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": st.session_state.assistant.greet_user()}]
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Chat Mode"  # Default to Chat Mode
if 'prev_responses' not in st.session_state:
    st.session_state.prev_responses = []

# --- Main Content Area ---
st.title("J.A.R.V.I.S 4.1")
st.caption("Just A Rather Very Intelligent System")

# --- Interaction Mode Selector ---
st.markdown('<div class="mode-selector">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    chat_active = st.button("💬 Chat Mode", use_container_width=True, 
                           type="primary" if st.session_state.app_mode == "Chat Mode" else "secondary")
with col2:
    voice_active = st.button("🎙️ Voice Mode", use_container_width=True, 
                            type="primary" if st.session_state.app_mode == "Voice Mode" else "secondary")
with col3:
    st.write("")  # Spacer for alignment
    audio_bytes = audio_recorder(
        pause_threshold=5.0,
        text="",
        recording_color="#ff0000",
        neutral_color="#00ff41",
        icon_name="microphone",
        icon_size="3x",
    )
st.markdown('</div>', unsafe_allow_html=True)

if chat_active:
    st.session_state.app_mode = "Chat Mode"
if voice_active:
    st.session_state.app_mode = "Voice Mode"

# --- Chat History Display ---
if st.session_state.messages:
    # Show previous responses in expander
    if st.session_state.prev_responses:
        with st.expander("Previous Conversations", expanded=False):
            for msg in st.session_state.prev_responses:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
    
    # Show latest exchange
    last_exchange = st.session_state.messages[-2:] if len(st.session_state.messages) > 1 else st.session_state.messages
    for message in last_exchange:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Input Handling ---
def process_prompt(prompt):
    if not prompt.strip():
        return
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get assistant response
        assistant_response = st.session_state.assistant.handle_command(prompt)
        
        # Stream response with typing animation
        for char in assistant_response:
            full_response += char
            time.sleep(0.02)  # Adjust typing speed
            message_placeholder.markdown(full_response + "<span class='typing-cursor'></span>", unsafe_allow_html=True)
        
        message_placeholder.markdown(full_response)
        
        # Generate and play audio for the response
        audio_response = text_to_speech(full_response)
        if audio_response:
            st.audio(audio_response, format="audio/mp3", autoplay=True)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Archive previous responses
    if len(st.session_state.messages) > 4:
        st.session_state.prev_responses = st.session_state.messages[:-2]

# --- Chat Mode Input ---
if st.session_state.app_mode == "Chat Mode":
    if prompt := st.chat_input("What can I help you with, sir?"):
        process_prompt(prompt)

# --- Voice Mode Input ---
elif st.session_state.app_mode == "Voice Mode" and audio_bytes:
    with st.spinner("Analyzing audio..."):
        user_query = speech_to_text(audio_bytes)
        if user_query and "couldn't understand" not in user_query and "error" not in user_query.lower():
            process_prompt(user_query)
        elif user_query:
            with st.chat_message("assistant"):
                st.error(user_query)

# --- Status Bar ---
status_bar = f"""
<div class="status-bar">
    <div>Status: <span class="pulse">Online</span></div>
    <div>User: Densingh</div>
    <div>Mode: {st.session_state.app_mode}</div>
    <div>{datetime.datetime.now().strftime('%Y-%m-%d | %H:%M:%S')}</div>
</div>
"""
st.markdown(status_bar, unsafe_allow_html=True)