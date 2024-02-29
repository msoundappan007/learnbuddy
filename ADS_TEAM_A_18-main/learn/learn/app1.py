import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3

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

# Main function to start a conversation with the chatbot
def main():
    st.title("Learn Buddy")

    st.write("Welcome to the learn buddy! Speak or type 'exit' to end the conversation.")

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
            speak_text(chatbot_response)
0
if __name__ == "__main__":
    main()