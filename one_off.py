import os
import youtube_dl
from AudioManipulator import slow_and_reverb
from Giphy import download_gif
from moviepy.editor import (VideoFileClip, AudioFileClip, ImageClip)
from Youtube import upload
from dotenv import load_dotenv
load_dotenv()

# input file

filename = ''
youtube_url = 'https://www.youtube.com/watch?v=jnKYWFB_Bk0'
youtube_title = 'ODIE - North Face' + ' - Slowed And Reverbed'
description = '😈'

if(filename and youtube_url):
  print("filename and youtube_url cannot both be set")
  quit()
elif(youtube_url):
  filename = 'temp_from_youtube.mp3'
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': filename
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(youtube_url, download=True)
    youtube_title = info.get('title', None) + ' - Slowed And Reverbed'

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
    'description': description,
    'categoryId': '10',
    'tags': keywords
  }
}

upload(path=final_path, options=options)
