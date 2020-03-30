import os
from pydub import AudioSegment
from pydub.playback import play
from pysndfx import AudioEffectsChain
import uuid

class AudioManipulator:
  def __init__(self, sound_path):
    self.sound = AudioSegment.from_file(sound_path)
    self.sound_path = sound_path

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

  def slow_and_reverb(self, output_path=None, octaves=-0.05, speed=0.9):
    self.slow(output_path, octaves, speed)
    self.reverb(output_path)

  def slow(self, path, octaves=-0.05, speed=0.9):
    self.__speed_change(speed)
    self.__pitch_change(octaves)
    self.sound.export(path.replace('.wav', '-temp.wav'), format="wav")

  def reverb(self, path):
    infile = path.replace('.wav', '-temp.wav')
    # This library doesnt like spaces in file names, so replace all spaces with '~+', when we upload to youtube make sure we replace all groups of '~+' with a space
    outfile = path

    fx = (
      AudioEffectsChain()
      .reverb()
    )
    fx(infile, outfile)
    os.remove(infile)
