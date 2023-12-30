import openai
import os
from langchain.chat_models import ChatOpenAI
import elevenlabs
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip,TextClip, CompositeVideoClip
from pydub import AudioSegment
import cv2
from tqdm import tqdm
import random

script=[]

# Set the OpenAI API key as an environment variable
os.environ['OPENAI_API_KEY'] = 'ChatGPTAPIKEY'

# Create an OpenAI LLM
llm=ChatOpenAI(temperature=0.8,model_name='gpt-3.5-turbo-16k')

def extract_story():
    prompt = f"Write me a AITA story 1st line title, empty line, content (1 big paragraph). Don't need to include the words content: or 'title'. Replace AITA with the words 'am i the jerk'.make the content really long and dramatic that really gets the audience attention.  "

    response = llm.predict(prompt)  # Adjust model as per availability
    script.append(response)
    return response
print(extract_story())


elevenlabs.set_api_key("ElevenlabsAPIKey")


def get_audio_duration(file_path):
    # Load the audio file
    audio = AudioSegment.from_mp3(file_path)

    # Calculate the duration in seconds
    duration_seconds = len(audio) / 1000
    return duration_seconds

# Create a subclip based on audio duration
# Create a subclip and crop it for TikTok
def create_subclip(video_file_path, start_time, audio_file_path):
    # Get the duration of the audio file
    audio_duration = get_audio_duration(audio_file_path)

    # Load the video file
    clip = VideoFileClip(video_file_path)

    # Calculate the end time for the subclip
    end_time = start_time + audio_duration

    # Ensure end_time does not exceed the video's total duration
    end_time = min(end_time, clip.duration)

    # Create the subclip
    subclip = clip.subclip(start_time, end_time)

    # TikTok format (9:16 aspect ratio)
    width, height = subclip.size
    new_width = height * 9 / 16
    crop_x_center = (width - new_width) / 2

    # Crop the video to TikTok format
    cropped_subclip = subclip.crop(x1=crop_x_center, width=new_width)

    # Output
    output_file_path = "subclip_output.mp4"


    # Write the cropped subclipp
    cropped_subclip.write_videofile(output_file_path, codec='libx264')

    print(f"Subclip created and saved to {output_file_path}")


#create overlay mp3
# Function to overlay MP3 on MP4
def overlay_mp3(video_file_path, mp3_file_path, output_file_path):
    # Load the video file
    video_clip = VideoFileClip(video_file_path)

    # Load the MP3 file
    audio_clip = AudioFileClip(mp3_file_path)

    # The duration of the overlay should be the minimum of both clips
    min_duration = min(video_clip.duration, audio_clip.duration)

    # Set the duration of the audio clip to the duration of the video clip
    audio_clip = audio_clip.set_duration(min_duration)

    # Create a composite audio clip (original audio + mp3)
    composite_audio = CompositeAudioClip([video_clip.audio, audio_clip])

    # Set the composite audio to the video clip
    video_clip.audio = composite_audio

    # Write the result to a file
    video_clip.write_videofile(output_file_path, codec='libx264')

    print(f"Video with overlaid audio saved to {output_file_path}")


for i in range(10):
    # Replace these with your actual file paths
    video_file_path = "video/Chill Minecraft Hypixel parkour gameplay for commentary! (free to use).mp4"
    audio_file_path = 'Audio/audio.mp3'
    # adding auto generated captions and 1.5x the video first
    audio = elevenlabs.generate(
        text=extract_story(),
        voice="Adam",
    )
    elevenlabs.save(audio, "Audio/audio.mp3")

    # Create the subclip video based on audio length
    create_subclip(video_file_path, random.randint(1, 100), audio_file_path)

    # overlaying thevideo and labeling that output
    overlay_mp3('subclip_output.mp4', audio_file_path, f'cleaned video/combinedvideo{i}.mp4')

