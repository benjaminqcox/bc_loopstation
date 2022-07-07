import os
from tkinter import messagebox

import record_audio as ra
import pyaudio
import psutil
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5
device_index = 1
audio = pyaudio.PyAudio()


class LoopSound:
    sound_process = None

    def __init__(self, name, sound_file_loc, mp_process):
        self.name = name
        self.sound_file_loc = sound_file_loc
        self.mp_process = mp_process

    def start_recording(self):
        # add the ability to just click start stop recording in 1 button instead of 2 separate buttons
        # also add the ability to record multiple sounds at once (press record sound 1, then without stopping, press
        # record sound 2, then stop sound 1 and sound 2 recording)
        ra.start(self.sound_file_loc)

    def stop_recording(self):
        ra.stop()

    def save_recording(self, recording):
        audio = pyaudio.PyAudio()
        waveFile = wave.open(f'{self.sound_file_loc}', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(recording))
        waveFile.close()
        audio.terminate()

    def play_audio(self, loop=True):
        CHUNK = 1024
        # Open Wave File and start play!
        wf = wave.open(self.sound_file_loc, 'rb')
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

    def play_pause_process(self):
        status = self.get_sound_process_status()
        if status == 'running':
            self.pause_process()
        else:
            self.play_process()

    def manipulate_single_sound(self):
        if self.get_sound_process_status():
            self.play_pause_process()
        else:
            if self.file_exists():
                self.mp_process.start()
                self.sound_process = psutil.Process(self.mp_process.pid)
            else:
                messagebox.showinfo(f"Sound not found for: {self.name}",
                                    "Please record a sound before trying to play/pause it.")

    def play_process(self):
        status = self.get_sound_process_status()
        if status == 'stopped':
            self.sound_process.resume()
        elif not status:
            if os.path.isfile(self.sound_file_loc):
                self.mp_process.start()
                self.sound_process = psutil.Process(self.mp_process.pid)

    def pause_process(self):
        if self.get_sound_process_status() == 'running':
            self.sound_process.suspend()

    def get_sound_process_status(self):
        return self.sound_process.status() if self.sound_process else None

    def is_playing(self):
        return True if self.get_sound_process_status() == 'running' else False

    def file_exists(self):
        return os.path.isfile(self.sound_file_loc)

