import os
from AudioManipulator import slow_and_reverb
from Giphy import download_gif
from moviepy.editor import (VideoFileClip, AudioFileClip, ImageClip)
from Youtube import upload
from dotenv import load_dotenv
load_dotenv()

# input file
filename = 'show.mp3'
youtube_title = 'Will I See You At The Show Tonight' + ' - Slowed And Reverbed'

audio_output_path = filename.replace('.mp3', '-manipulated.wav')
print("SLOWING AND REVERBING")
slow_and_reverb(input_path=filename, output_path=audio_output_path)
os.remove(filename)
print("DONE SLOWING AND REVERBING")

print("MAKING VIDEO")

soundtrack = AudioFileClip(audio_output_path)

# Gif
video_output_path = filename.replace('.mp3', '.gif')
download_gif(video_output_path)
videoclip = VideoFileClip(video_output_path).loop(duration=soundtrack.duration)
# Image
# videoclip = ImageClip('testimage.jpg').set_duration(soundtrack.duration)
# videoclip.fps = 24

final_path =  youtube_title + '.mp4'
videoclip.audio = soundtrack
videoclip.write_videofile(final_path, codec='mpeg4', audio_bitrate="320k")
print("DONE MAKING VIDEO")

os.remove(audio_output_path)
os.remove(video_output_path)

keywords = youtube_title.split(' ').extend(['slowed', 'reverbed'])
options = {
  'snippet': {
    'title': youtube_title,
    'description': '😈',
    'categoryId': '10',
    'tags': keywords
  }
}

upload(path=final_path, options=options)
