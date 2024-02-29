import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
from PIL import Image
from moviepy.editor import *

# Set your API key here
api_key = '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'
openai.api_key = api_key
def authenticate(username, password):
    # Add your authentication logic here, e.g., check against a database or hardcoded credentials
    return username == "s" and password == "123"


def chat_with_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set voice properties for a more human-like voice
    engine.setProperty('voice', voices[1].id)  # Change index for different voices

    with mic as source:
        st.write("Speak:")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            engine.say(user_input)  # Speak back the recognized text
            engine.runAndWait()
            return user_input
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand the audio.")
            return ""
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
            return ""
def learn_buddy(session_state):
    st.title("Learn Buddy")
    
    query_history = session_state.get("query_history", [])
    menu = ["Voice Input", "Text Input", "Conversation History"]
    choice = st.sidebar.selectbox("Select input method:", menu)
def speak_text(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()


from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

from moviepy.editor import VideoFileClip

def generate_video_response(text_response, video_paths, interval=2):
    speak_text(text_response)
    audio = AudioFileClip("C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\output.mp3")
    audio_duration = audio.duration  # Get the duration of the audio clip

    video_clips = []
    for vid_path in video_paths:
        vid_clip = VideoFileClip(vid_path).set_duration(interval)
        video_clips.append(vid_clip)

    final_clip = concatenate_videoclips(video_clips)
    final_clip = final_clip.set_audio(audio)

    # Set the final video duration to match the audio duration
    final_clip = final_clip.set_duration(audio_duration)

    final_clip.write_videofile("output.mp4", codec='libx264', fps=24)

# Usage example



# Usage example
video_paths = [
'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py',
    'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py','C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py',
    'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py','C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py',
    'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py','C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py',
    'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py','C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py',
    'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py','C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py',
    'C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\bar.py'    # Add all your video paths here
]

generate_video_response("Your text response", video_paths, interval=3)


def display_video(video_file):
    video = VideoFileClip(video_file)
    st.video(video_file)


def learn_buddy():
    st.title("Learn Buddy")
    
    session_state = st.session_state
    query_history = session_state.get("query_history", [])
    menu = ["Voice Input", "Text Input", "Conversation History"]
    choice = st.sidebar.selectbox("Select input method:", menu)

    if choice == "Voice Input":
        user_input = recognize_speech()
    elif choice == "Text Input":
        user_input = st.text_input("You:")

    if st.button("Send"):
        if user_input.lower() == 'exit':
            st.write("Conversation ended.")
        else:
            chatbot_response = chat_with_openai(user_input)
            query_history.append({"query": user_input, "response": chatbot_response})
            session_state["query_history"] = query_history

            st.write("Learn Buddy:", chatbot_response)
            generate_video_response(chatbot_response,video_paths)
            display_video("output.mp4")

    if choice == "Conversation History":
        st.write("Conversation History:")
        for idx, query_info in enumerate(query_history, start=1):
            st.write(f"Query {idx}: {query_info['query']}")
            st.write(f"Response {idx}: {query_info['response']}")
            st.markdown("---")
def main():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("Logged in as {}".format(username))
            session_state = st.session_state
            session_state["authenticated"] = True
            session_state.setdefault("query_history", [])  # Initialize query_history in session_state
            st.experimental_rerun()  # Reload the app to go to the 'Learn Buddy' page
        else:
            st.error("Invalid credentials. Please try again.")
if __name__ == "__main__":
    session_state = st.session_state
    if session_state.get("authenticated"):
        learn_buddy()
    else:
        main()

