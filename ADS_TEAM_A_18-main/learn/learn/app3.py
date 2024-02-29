import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3
from PIL import Image
import time

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
        audio = recognizer.listen(source)
        user_input = recognizer.recognize_google(audio)
    return user_input

# Function for text-to-speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to display the avatar image
def display_avatar(image_path):
    avatar_img = Image.open(image_path)
    st.image(avatar_img, use_column_width=True)

# Function to simulate speaking animation
def simulate_speaking():
    for i in range(3):  # Change the number based on the number of speech frames or expressions
        display_avatar(f"path_to_avatar_{i + 1}.jpg")  # Replace with the path to different speech frames
        time.sleep(0.5)  # Adjust the duration as needed

# Main function to start a conversation with the chatbot
def main():
    st.title("Learn Buddy")

    st.write("Welcome to the Learn Buddy! Speak or type 'exit' to end the conversation.")
    display_avatar('path_to_initial_avatar_image.jpg')  # Replace with initial avatar image path

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
            simulate_speaking()  # Simulate the avatar speaking
            speak_text(chatbot_response)
            display_avatar('path_to_initial_avatar_image.jpg')  # Return to the initial avatar image

if __name__ == "__main__":
    main()
