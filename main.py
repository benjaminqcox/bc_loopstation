import multiprocessing
import logging
import pyaudio
import psutil
import wave
import sys
import os

import loopstation as lp

from pydub import AudioSegment
from sound_object import LoopSound
from tkinter import *
from tkinter import ttk, messagebox



gui = Tk()
gui.geometry('500x500')
gui.grid_columnconfigure(0, weight=1, uniform="fred")

def Close():
    gui.destroy()

if __name__ == '__main__':
    # This code is VERY messy but it currently runs and mostly does what is intended.
    # TODO: Change the overlay so that all sounds fill to the longest sound file
    #  (It doesnt have to loop necessarily for now. That could be a separate option.)

    audio_file_loc = ['audio_files/sound'+str(i)+'.wav' for i in range(1, 6)]

    loop_sounds = [LoopSound(name=loc[12:-4],
                             sound_file_loc=loc,
                             mp_process=multiprocessing.Process(target=lp.play_audio, args=(loc,),)) for loc in audio_file_loc]

    for sound in loop_sounds:
        for attribute, value in vars(sound).items():
            print(f'{attribute}: {value}')


    sound1 = ttk.Button(gui, text="Play\nPause", command=lambda: loop_sounds[0].manipulate_single_sound())
    sound1_record = ttk.Button(gui, text="Record", command=lambda: loop_sounds[0].start_recording())
    sound1_stop_record = ttk.Button(gui, text="Stop\nRecord", command=lambda: loop_sounds[0].stop_recording())
    sound1_record_overlay = ttk.Button(gui, text="Overlay", command=lambda: lp.record_all_current_sounds_into_one(loop_sounds, loop_sounds[0]))

    sound2 = ttk.Button(gui, text="Play\nPause", command=lambda: loop_sounds[1].manipulate_single_sound())
    sound2_record = ttk.Button(gui, text="Record", command=lambda: loop_sounds[1].start_recording())
    sound2_stop_record = ttk.Button(gui, text="Stop\nRecord", command=lambda: loop_sounds[1].stop_recording())
    sound2_record_overlay = ttk.Button(gui, text="Overlay", command=lambda: lp.record_all_current_sounds_into_one(loop_sounds, loop_sounds[1]))

    sound3 = ttk.Button(gui, text="Play\nPause", command=lambda: loop_sounds[2].manipulate_single_sound())
    sound3_record = ttk.Button(gui, text="Record", command=lambda: loop_sounds[2].start_recording())
    sound3_stop_record = ttk.Button(gui, text="Stop\nRecord", command=lambda: loop_sounds[2].stop_recording())
    sound3_record_overlay = ttk.Button(gui, text="Overlay", command=lambda: lp.record_all_current_sounds_into_one(loop_sounds, loop_sounds[2]))

    sound4 = ttk.Button(gui, text="Play\nPause", command=lambda: loop_sounds[3].manipulate_single_sound())
    sound4_record = ttk.Button(gui, text="Record", command=lambda: loop_sounds[3].start_recording())
    sound4_stop_record = ttk.Button(gui, text="Stop\nRecord", command=lambda: loop_sounds[3].stop_recording())
    sound4_record_overlay = ttk.Button(gui, text="Overlay", command=lambda: lp.record_all_current_sounds_into_one(loop_sounds, loop_sounds[3]))

    sound5 = ttk.Button(gui, text="Play\nPause", command=lambda: loop_sounds[4].manipulate_single_sound())
    sound5_record = ttk.Button(gui, text="Record", command=lambda: loop_sounds[4].start_recording())
    sound5_stop_record = ttk.Button(gui, text="Stop\nRecord", command=lambda: loop_sounds[4].stop_recording())
    sound5_record_overlay = ttk.Button(gui, text="Overlay", command=lambda: lp.record_all_current_sounds_into_one(loop_sounds, loop_sounds[4]))

    all_sounds_pause = ttk.Button(gui, text="Play\nall", command=lambda: lp.manipulate_all_sounds(key_press='u', recording_processes=loop_sounds))
    all_sounds_play = ttk.Button(gui, text="Pause\nall", command=lambda: lp.manipulate_all_sounds(key_press='p', recording_processes=loop_sounds))
    all_sounds_inverse = ttk.Button(gui, text="Invert\nall", command=lambda: lp.manipulate_all_sounds(key_press='i', recording_processes=loop_sounds))


    end_prog = ttk.Button(gui, text="Exit program", command=gui.destroy)

    sound1.place(height=50, width=50, x=140, y=57.5)
    sound1_record.place(height=50, width=50, x=195, y=57.5)
    sound1_stop_record.place(height=50, width=50, x=250, y=57.5)
    sound1_record_overlay.place(height=50, width=50, x=305, y=57.5)

    sound2.place(height=50, width=50, x=140, y=112.5)
    sound2_record.place(height=50, width=50, x=195, y=112.5)
    sound2_stop_record.place(height=50, width=50, x=250, y=112.5)
    sound2_record_overlay.place(height=50, width=50, x=305, y=112.5)

    sound3.place(height=50, width=50, x=140, y=167.5)
    sound3_record.place(height=50, width=50, x=195, y=167.5)
    sound3_stop_record.place(height=50, width=50, x=250, y=167.5)
    sound3_record_overlay.place(height=50, width=50, x=305, y=167.5)

    sound4.place(height=50, width=50, x=140, y=222.5)
    sound4_record.place(height=50, width=50, x=195, y=222.5)
    sound4_stop_record.place(height=50, width=50, x=250, y=222.5)
    sound4_record_overlay.place(height=50, width=50, x=305, y=222.5)

    sound5.place(height=50, width=50, x=140, y=277.5)
    sound5_record.place(height=50, width=50, x=195, y=277.5)
    sound5_stop_record.place(height=50, width=50, x=250, y=277.5)
    sound5_record_overlay.place(height=50, width=50, x=305, y=277.5)

    all_sounds_play.place(height=50, width=50, x=167.5, y=332.5)
    all_sounds_pause.place(height=50, width=50, x=222.5, y=332.5)
    all_sounds_inverse.place(height=50, width=50, x=277.5, y=332.5)

    end_prog.place(height=60, width=60, x=222.5, y=387.5)
    

    

    gui.mainloop()

    for _sound in loop_sounds:
        if _sound.get_sound_process_status() is not None:
            print(_sound.name)
            _sound.mp_process.terminate()
    # this site may be useful for the recording of sounds based on holding down keys 'https://www.delftstack.com/howto/python/python-detect-keypress/'
