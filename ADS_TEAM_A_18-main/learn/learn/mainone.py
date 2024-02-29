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
    engine="code-davinci-002	",  # Replace "text-davinci" with the desired model name
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
    audio = AudioFileClip("C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\output.mp3")
    video = ImageClip("C:\\Users\\malli\\Downloads\\ADS_TEAM_A_18-main\\ADS_TEAM_A_18-main\\learn\\learn\\path_to_avatar_1.jpg").set_duration(audio.duration)
    video = video.set_audio(audio)
    video.write_videofile("output.mp4", codec='libx264', fps=24)

# Main function to start a conversation with the chatbot
def main():
    st.title("Learn Buddy")

    st.write("Welcome to the Learn Buddy! Speak or type 'exit' to end the conversation.")
    
    input_method = st.radio("Select input method:", ("Voice", "Text"))

    if input_method == "Voice":
        user_input = recognize_speech()
    else:
        user_input = st.text_input("You:")

    if st.button("Send"):
        if user_input.lower() == 'exit':
            st.write("Conversation ended.")
        else:
            chatbot_response = chat_with_openai(user_input)
            st.write("Learn Buddy:", chatbot_response)
            generate_video_response(chatbot_response)
            st.video("output.mp4")

if __name__ == "__main__":
    main()
