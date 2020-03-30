import os
from AudioManipulator import AudioManipulator
from Giphy import download_gif
from moviepy.editor import (VideoFileClip, AudioFileClip)

filename = 'december.mp3'
am = AudioManipulator(filename)
am.slow_and_reverb(output_path=filename.replace('.mp3', '.wav'))

audio_output_path = filename.replace('.mp3', '.wav')
video_output_path = filename.replace('.mp3', '.gif')
download_gif(video_output_path)
soundtrack = AudioFileClip(audio_output_path)
videoclip = VideoFileClip(video_output_path).loop(duration=soundtrack.duration)

videoclip.audio = soundtrack
videoclip.write_videofile(filename.split('.mp3')[0] + ' - Slowed And Reverbed.mp4')

os.remove(audio_output_path)
os.remove(video_output_path)
