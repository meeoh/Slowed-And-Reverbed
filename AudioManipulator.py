import os
from pydub import AudioSegment
from pydub.playback import play
from pysndfx import AudioEffectsChain
import uuid

class AudioManipulator:
  def __init__(self, sound_path, download_path):
    self.sound = AudioSegment.from_file(sound_path)
    self.download_path = download_path

  def __pitch_change(self, octaves):
    sound = self.sound
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    self.sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

  def __speed_change(self, speed=1.0):
    sound = self.sound
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
      "frame_rate": int(sound.frame_rate * speed)
    })
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    self.sound = sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

  def slow_and_reverb(self, path='downloads/final.wav', octaves=-0.05, speed=0.9):
    self.slow(octaves, speed)
    self.reverb(path)

  def slow(self, octaves=-0.05, speed=0.9):
    self.__speed_change(speed)
    self.__pitch_change(octaves)
    self.sound.export('downloads/speed_and_pitch.wav', format="wav")

  def reverb(self, path):
    fx = (
      AudioEffectsChain()
      .reverb()
    )
    infile = 'downloads/speed_and_pitch.wav'
    outfile = path
    # Apply phaser and reverb directly to an audio file.
    fx(infile, outfile)
    os.remove("downloads/speed_and_pitch.wav")


# am = AudioManipulator('./empty.mp3')
# am.slow_and_reverb()