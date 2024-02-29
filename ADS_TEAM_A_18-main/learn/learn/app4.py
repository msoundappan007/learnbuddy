from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Users\Gowtham\Downloads\ImageMagick-7.1.1-21-Q16-HDRI-x64-dll.exe"})
import imageio.plugins.ffmpeg
imageio.plugins.ffmpeg.download()

import streamlit as st
from moviepy.editor import TextClip

# Function to convert text input into an animated video
def generate_animated_video(text_input):
    # Set up the clip with the provided text
    clip = TextClip(text_input, color='white', font='Arial', fontsize=70)

    # Set duration (5 seconds in this example)
    clip = clip.set_duration(5)

    # Define the path to save the video
    video_path = "animated_text_video.mp4"

    # Save the video file
    clip.write_videofile(video_path, fps=24)

    return video_path

def main():
    st.title("Text to Animated Video")
    st.write("Enter text below to generate an animated video.")

    # Text input for the user
    text_input = st.text_input("Enter text:")

    if st.button("Generate Video"):
        if text_input:
            st.write(f"Generating video for text: {text_input}")
            video_path = generate_animated_video(text_input)
            st.video(open(video_path, 'rb').read())
        else:
            st.write("Please enter some text.")

if __name__ == "__main__":
    main()
