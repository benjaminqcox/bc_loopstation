import multiprocessing
import logging
import pyaudio
import psutil
import wave
import sys
import os

from pydub import AudioSegment
from tkinter import *
from tkinter import ttk, messagebox


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5
device_index = 1
audio = pyaudio.PyAudio()


SOUND_PROCESSES = {}
SOUND_FILE_LOC_BY_PID = {}


def play_audio(audio_file: str, loop=True):
  CHUNK = 1024
  # Open Wave File and start play!
  wf = wave.open(audio_file, 'rb')
  player = pyaudio.PyAudio()

  # Open Output Stream (basen on PyAudio tutorial)
  stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                       channels=wf.getnchannels(),
                       rate=wf.getframerate(),
                       output=True)

  # PLAYBACK LOOP
  data = wf.readframes(CHUNK)
  while loop:
    stream.write(data)
    data = wf.readframes(CHUNK)
    if data == b'':  # If file is over then rewind.
      wf.rewind()
      data = wf.readframes(CHUNK)

  stream.close()
  player.terminate()



def manipulate_all_sounds(key_press, recording_processes):
    #need to update this function to take the same error handling as the manipulate single audio function
    print(f'Keypress chosen: {key_press}')
    for recording in recording_processes:
        if key_press == 'p': # p => pause all
            recording.pause_process()
        elif key_press == 'u': # u => unpause all
            recording.play_process()
        elif key_press == 'i': # i => invert all (if sound is playing pause it, if sound is paused play it)
                recording.play_pause_process()
        elif key_press == '\\':
            sys.exit()
        else:
            logging.warning(f'{key_press} is not a valid input')



def helloCallBack():
    # example of showing info to screen using tkinter
    messagebox.showinfo("Hello Python", "Hello World")



def get_playing_sound_files(sounds):
    playing_sounds = []
    for sound in sounds:
        if sound.is_playing():
            playing_sounds.append(sound.sound_file_loc)
    return playing_sounds

def recording_overlay(recording_file_loc: str):
    #Doesn't do anything for now
    test_segment = AudioSegment.from_wav(recording_file_loc)
    return None

def record_all_current_sounds_into_one(all_sounds, sound):
    sound_file_loc = sound.sound_file_loc
    audio_segments = [AudioSegment.from_wav(file) for file in get_playing_sound_files(all_sounds) if
                      file != sound_file_loc]
    if audio_segments:
        if sound.file_exists():
            temp_sound = AudioSegment.from_wav(sound_file_loc)
        else:
            temp_sound = ''

        for sound_playing in audio_segments:
            if temp_sound == '':
                temp_sound = sound_playing
            else:
                temp_sound = temp_sound.overlay(sound_playing)
        temp_sound.export(sound_file_loc, format='wav')
        print('Sounds overlayed')


