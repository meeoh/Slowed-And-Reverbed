import praw
import youtube_dl
import os
import uuid
import json
import pytz
from AudioManipulator import slow_and_reverb
from Giphy import download_gif
from moviepy.editor import (VideoFileClip, AudioFileClip)
from datetime import datetime
from Youtube import upload

from dotenv import load_dotenv
load_dotenv()

def remove_processed(submissions):
  new_submissions = []
  with open("processed.json", "r+") as file:
    processed_submissions = json.load(file)
    new_submissions = [submission for submission in submissions if submission.id not in processed_submissions]
  return new_submissions

def mark_as_processed(submissions):
  with open("processed.json", "r+") as file:
    data = json.load(file)
    submission_ids = map(lambda x: x.id, submissions)

    # Method to remove old items, if its in the file and not back in the reddit posts, remove it from the file
    # keys_to_pop = []
    # for (k, v) in data.items():
    #   if k not in submission_ids:
    #     keys_to_pop.append(k)
    # for k in keys_to_pop:
    #   data.pop(k, None)

    tz = pytz.timezone('America/New_York')
    today = datetime.now(tz)
    for submission in submissions:
      data[submission.id] = {
        'title': submission.title,
        'date': str(today)
      }
    file.seek(0)
    file.truncate()
    json.dump(data, file)

reddit = praw.Reddit(
  client_id=os.getenv('REDDIT_CLIENT_ID'),
  client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
  user_agent='temp val'
)

download_dir = os.path.abspath('downloads')
# submissions = remove_processed(reddit.subreddit('hiphopheads').hot())
submissions = remove_processed(reddit.subreddit('hiphopheads').top('week'))
processed_submissions = []

for submission in submissions:
  if(
    'fresh' in submission.title.lower() and
    'youtube' in submission.url.lower() and
    'video' not in submission.title.lower() and
    'cypher' not in submission.title.lower() and
    submission.score > 100
  ):
    print(submission.title, submission.url, submission.id, submission.score)
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

      audio_output_path = filename.replace('.mp3', '-manipulated.wav')
      print("SLOWING AND REVERBING")
      slow_and_reverb(input_path=filename, output_path=audio_output_path)
      os.remove(filename)
      print("DONE SLOWING AND REVERBING")

      print("MAKING VIDEO")
      video_output_path = filename.replace('.mp3', '.gif')
      download_gif(video_output_path)
      soundtrack = AudioFileClip(audio_output_path)
      videoclip = VideoFileClip(video_output_path).loop(duration=soundtrack.duration)

      final_path = download_dir + '/' + unique_id + '/' + video_title + ' - Slowed And Reverbed.mp4'
      videoclip.audio = soundtrack
      videoclip.write_videofile(final_path, codec='mpeg4', audio_bitrate="320k")
      print("DONE MAKING VIDEO")
      youtube_title = video_title + ' - Slowed And Reverbed'

      os.remove(audio_output_path)
      os.remove(video_output_path)

      keywords = youtube_title.split(' ') + ['slowed', 'reverbed']
      options = {
        'snippet': {
          'title': youtube_title,
          'description': '😈',
          'categoryId': '10',
          'tags': keywords
        }
      }

      try:
        upload(path=final_path, options=options)
        processed_submissions.append(submission)
      except:
        print("Could not upload")

      # break

mark_as_processed(processed_submissions)
