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

gui = Tk()
gui.geometry('500x500')


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


def key_press_int(key_press):
    try:
        int_key_press = int(key_press)
        return int_key_press
    except ValueError:
        return key_press


def play_pause_process(process):
    status = process.status()
    if status == 'running':
        process.suspend()
    else:
        process.resume()
    #print(f'process {process} changed from {status} to {process.status}')


def manipulate_all_sounds(key_press, recording_processes):
    #need to update this function to take the same error handling as the manipulate single audio function
    print(f'Keypress chosen: {key_press}')
    if key_press == 'p': # p => pause all
        for recording in recording_processes:
            if recording.status() == 'running':
                recording.suspend()
    elif key_press == 'u': # u => unpause all
        for recording in recording_processes:
            if recording.status() == 'stopped':
                recording.resume()
    elif key_press == 'i': # i => invert all (if sound is playing pause it, if sound is paused play it)
        for recording in recording_processes:
            play_pause_process(recording)
    elif key_press == '\\':
        sys.exit()
    else:
        logging.warning(f'{key_press} is not a valid input')



def manipulate_single_sound(recording, file_path):
    get_playing_sound_files()
    if recording.is_alive():
        play_pause_process(SOUND_PROCESSES[recording.pid]['process'])
    else:
        if os.path.isfile(recording.name + '.wav'):
            recording.start()
            SOUND_PROCESSES[recording.pid] = {'file_path': file_path, 'process': psutil.Process(recording.pid)}
        else:
            messagebox.showinfo(f"Sound not found for: {recording.name}", "Please record a sound before trying to play/pause it.")


def test_keyboard_input():
    key_press = keyboard.read_key()
    return key_press


def helloCallBack():
    # example of showing info to screen using tkinter
    messagebox.showinfo("Hello Python", "Hello World")


def record_audio(recording_file_loc):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = 1,
                    frames_per_buffer=CHUNK)
    print("recording started")
    Recordframes = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    save_recording(recording_file_loc, Recordframes)


def save_recording(recording_file_loc, recording):
    audio = pyaudio.PyAudio()
    waveFile = wave.open(f'{recording_file_loc}', 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(recording))
    waveFile.close()
    audio.terminate()


def get_playing_sound_files():
    playing_sounds = []
    for name, values in SOUND_PROCESSES.items():
        if values['process'].status() == 'running':
            playing_sounds.append(values['file_path'])
    return playing_sounds

def recording_overlay(recording_file_loc: str):
    #Doesn't do anything for now
    test_segment = AudioSegment.from_wav(recording_file_loc)
    return None

def record_all_current_sounds_into_one(recording_file_loc: str):
    temp_sound = AudioSegment.from_wav(recording_file_loc)
    audio_segments = [AudioSegment.from_wav(file) for file in get_playing_sound_files() if file != recording_file_loc]
    for sound_playing in audio_segments:
        temp_sound = temp_sound.overlay(sound_playing)
    temp_sound.export(recording_file_loc, format='wav')
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




