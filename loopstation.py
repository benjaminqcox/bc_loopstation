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






if __name__ == '__main__':
    audio_file_loc = ['sound1.wav',
                      'sound2.wav',
                      'sound3.wav',
                      'sound4.wav',
                      'sound5.wav']

    recordings = [multiprocessing.Process(target=play_audio, args=(audio_file_loc[0],)),
                  multiprocessing.Process(target=play_audio, args=(audio_file_loc[1],)),
                  multiprocessing.Process(target=play_audio, args=(audio_file_loc[2],)),
                  multiprocessing.Process(target=play_audio, args=(audio_file_loc[3],)),
                  multiprocessing.Process(target=play_audio, args=(audio_file_loc[4],))]

    print()
    i = 0;
    for recording in recordings:
        i+=1
        recording.name = 'sound' + str(i)

        #recording.start()


    #for process in recording_processes:
    #    print(process)
    """
    #statuses are 'stopped' and 'running' for psutil.Process(pid).status()
    print('Input:\nPress number of the station to pause play\nManipulate all sounds by using characters\n\\ Exit')
    while True:
        #key_press = keyboard.read_key() # This detects key_press and key release, so may need another way to do this. It may work to function wrap it
        #pygame has a way that may work, look into that
        key_press = test_keyboard_input()
        print(key_press)
        key_press = key_press_int(key_press)
        if isinstance(key_press, int):
            if 1 <= key_press <= 5:
                manipulate_single_sound(recording_processes[key_press-1])
            else:
                logging.warning(f'You need to choose between 1 and 5. You chose {key_press}')
        else:
            manipulate_all_sounds(key_press, recording_processes)
    """
    # for overlaying audio, I may need a keypress to choose the channel to record over then use the pydub overlay method
    # Lto record the sound then replace the original recording
    sound1 = ttk.Button(gui, text="Sound 1 pause/play", command=lambda: manipulate_single_sound(recordings[0], audio_file_loc[0]))
    sound1_record = ttk.Button(gui, text="Sound 1 record", command=lambda: record_audio(audio_file_loc[0]))
    sound1_record_overlay = ttk.Button(gui, text="Overlay current playing sounds into sound 1", command= lambda: record_all_current_sounds_into_one(audio_file_loc[0]))
    sound2 = ttk.Button(gui, text="Sound 2 pause/play", command=lambda: manipulate_single_sound(recordings[1], audio_file_loc[1]))
    sound2_record = ttk.Button(gui, text="Sound 2 record", command=lambda: record_audio(audio_file_loc[1]))
    sound3 = ttk.Button(gui, text="Sound 3 pause/play", command=lambda: manipulate_single_sound(recordings[2], audio_file_loc[2]))
    sound3_record = ttk.Button(gui, text="Sound 3 record", command=lambda: record_audio(audio_file_loc[2]))
    sound4 = ttk.Button(gui, text="Sound 4 pause/play", command=lambda: manipulate_single_sound(recordings[3], audio_file_loc[3]))
    sound4_record = ttk.Button(gui, text="Sound 4 record", command=lambda: record_audio(audio_file_loc[3]))
    sound5 = ttk.Button(gui, text="Sound 5 pause/play", command=lambda: manipulate_single_sound(recordings[4], audio_file_loc[4]))
    sound5_record = ttk.Button(gui, text="Sound 5 record", command=lambda: record_audio(audio_file_loc[4]))
    all_sounds_pause = ttk.Button(gui, text="All sounds play", command=lambda: manipulate_all_sounds(key_press='u', recording_processes=recordings))
    all_sounds_play = ttk.Button(gui, text="All sounds pause", command=lambda: manipulate_all_sounds(key_press='p', recording_processes=recordings))
    all_sounds_inverse = ttk.Button(gui, text="All sounds inverse", command=lambda: manipulate_all_sounds(key_press='i', recording_processes=recordings))

    sound1.pack()
    sound1_record.pack()
    sound1_record_overlay.pack()
    sound2.pack()
    sound2_record.pack()
    sound3.pack()
    sound3_record.pack()
    sound4.pack()
    sound4_record.pack()
    sound5.pack()
    sound5_record.pack()
    all_sounds_play.pack()
    all_sounds_pause.pack()
    all_sounds_inverse.pack()
    gui.mainloop()
    print('hello world')
    # this site may be useful for the recording of sounds based on holding down keys 'https://www.delftstack.com/howto/python/python-detect-keypress/'




