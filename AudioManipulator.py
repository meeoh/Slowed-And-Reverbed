import os
from pydub import AudioSegment
from pydub.playback import play
from pysndfx import AudioEffectsChain
import uuid

def pitch_change(sound, octaves):
  new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
  return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

def speed_change(sound, speed=1.0):
  # Manually override the frame_rate. This tells the computer how many
  # samples to play per second
  sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
    "frame_rate": int(sound.frame_rate * speed)
  })
  # convert the sound with altered frame rate to a standard frame rate
  # so that regular playback programs will work right. They often only
  # know how to play audio at standard frame rate (like 44.1k)
  return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def slow_and_reverb(input_path, output_path=None, octaves=-0.05, speed=0.9):
  sound = AudioSegment.from_file(input_path)
  slow(sound, output_path, octaves, speed)
  reverb(sound, output_path)

def slow(sound, path, octaves=-0.05, speed=0.9):
  sound = speed_change(sound, speed)
  sound = pitch_change(sound, octaves)
  sound.export(path.replace('.wav', '-slowed.wav'), format="wav")

def reverb(sound, path):
  infile = path.replace('.wav', '-slowed.wav')
  # This library doesnt like spaces in file names, so replace all spaces with '~+', when we upload to youtube make sure we replace all groups of '~+' with a space
  outfile = path

  fx = (
    AudioEffectsChain()
    .reverb()
  )
  fx(infile, outfile)
  os.remove(infile)
