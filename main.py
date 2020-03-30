import praw
import youtube_dl
from AudioManipulator import AudioManipulator
import os

reddit = praw.Reddit(
  client_id='_4C0vS7OcJbrDw',
  client_secret='jCFBG9NgScpF7A12iiWS1cmf1zA',
  user_agent='my user agent'
)

download_dir = os.path.abspath('downloads')
ydl_opts = {
  'format': 'bestaudio/best',
  'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
  }],
  'outtmpl': download_dir + '/%(title)s.%(ext)s'
}


for submission in reddit.subreddit('hiphopheads').stream.submissions():
  # if its a FRESH post and on youtube, download it
  if('fresh' in submission.title.lower() and 'youtube' in submission.url.lower()):
    print(submission.url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(submission.url, download=True)
      filename = ydl.prepare_filename(info).replace('.webm', '.mp3')
      am = AudioManipulator(filename)
      am.slow_and_reverb(filename.replace('.mp3', '.wav'))
      os.remove(filename)
      break
