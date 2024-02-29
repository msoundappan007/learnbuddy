import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
from PIL import Image
from moviepy.editor import *

# Set your API key here
api_key = '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'
openai.api_key = api_key



# Function to interact with the chatbot
def chat_with_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Function for voice recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        st.write("Speak:")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            return user_input
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand the audio.")
            return ""
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
            return ""

# Function for text-to-speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

# Function to create a video from the audio response
def generate_video_response(text_response):
    speak_text(text_response)
    audio = AudioFileClip("C:\Users\malli\Downloads\ADS_TEAM_A_18-main\ADS_TEAM_A_18-main\learn\learn\output.mp3")
    video = ImageClip("C:\Users\malli\Downloads\ADS_TEAM_A_18-main\ADS_TEAM_A_18-main\learn\learn\path_to_avatar_0.jpg").set_duration(audio.duration) # Replace 'path_to_avatar_1.jpg' with your image path
    video = video.set_audio(audio)
    video.write_videofile("output.mp4", codec='libx264', fps=24)

# Function to display the generated video
def display_video(video_file):
    video = VideoFileClip(video_file)
    st.video(video_file)

# Streamlit app
def main():
    st.title("Learn Buddy")
    
    session_state = st.session_state.setdefault("session_state", {"query_history": []})
    query_history = session_state["query_history"]

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
            generate_video_response(chatbot_response)
            display_video("output.mp4")

    if choice == "Conversation History":
        st.write("Conversation History:")
        for idx, query_info in enumerate(query_history, start=1):
            st.write(f"Query {idx}: {query_info['query']}")
            st.write(f"Response {idx}: {query_info['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
