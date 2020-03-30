import praw
import youtube_dl
import os
import uuid
from AudioManipulator import AudioManipulator
from Giphy import download_gif
from moviepy.editor import (VideoFileClip, AudioFileClip)

reddit = praw.Reddit(
  client_id='_4C0vS7OcJbrDw',
  client_secret='jCFBG9NgScpF7A12iiWS1cmf1zA',
  user_agent='my user agent'
)

download_dir = os.path.abspath('downloads')


for submission in reddit.subreddit('hiphopheads').stream.submissions():
  # if its a FRESH post and on youtube, download it
  if('fresh' in submission.title.lower() and 'youtube' in submission.url.lower()):
    print(submission.title, submission.url)
    unique_id = str(uuid.uuid1())
    filename_temp = download_dir + '/' + unique_id + '.mp3'
    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }],
      'outtmpl': filename_temp
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(submission.url, download=True)
      video_title = info.get('title', None)

      os.mkdir(download_dir + '/' + unique_id )
      filename = download_dir + '/' + unique_id  + '/' + unique_id + '.mp3'

      os.rename(filename_temp, filename)

      am = AudioManipulator(filename)
      audio_output_path = filename.replace('.mp3', '-manipulated.wav')
      am.slow_and_reverb(output_path=audio_output_path)
      os.remove(filename)

      video_output_path = filename.replace('.mp3', '.gif')
      download_gif(video_output_path)
      soundtrack = AudioFileClip(audio_output_path)
      videoclip = VideoFileClip(video_output_path).loop(duration=soundtrack.duration)

      videoclip.audio = soundtrack
      videoclip.write_videofile(download_dir + '/' + unique_id + '/' + video_title + ' - Slowed And Reverbed.mp4')
      youtube_title = video_title + ' - Slowed And Reverbed'

      os.remove(audio_output_path)
      os.remove(video_output_path)

      break
