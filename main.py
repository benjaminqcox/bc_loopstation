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

if __name__ == '__main__':
    audio_file_loc = ['audio_files/sound'+str(i)+'.wav' for i in range(1, 6)]

    loop_sounds = [LoopSound(name=loc[12:-4],
                             sound_file_loc=loc,
                             mp_process=multiprocessing.Process(target=lp.play_audio, args=(loc,),)) for loc in audio_file_loc]

    for sound in loop_sounds:
        for attribute, value in vars(sound).items():
            print(f'{attribute}: {value}')


    sound1 = ttk.Button(gui, text="Sound 1 pause/play",
                        command=lambda: loop_sounds[0].manipulate_single_sound())
    sound1_record = ttk.Button(gui, text="Sound 1 record", command=lambda: loop_sounds[0].record_audio())
    sound1_record_overlay = ttk.Button(gui, text="Overlay current playing sounds into sound 1",
                                       command=lambda: lp.record_all_current_sounds_into_one(loop_sounds, loop_sounds[0]))
    sound2 = ttk.Button(gui, text="Sound 2 pause/play",
                        command=lambda: loop_sounds[1].manipulate_single_sound())
    sound2_record = ttk.Button(gui, text="Sound 2 record", command=lambda: loop_sounds[1].record_audio())
    sound3 = ttk.Button(gui, text="Sound 3 pause/play",
                        command=lambda: loop_sounds[2].manipulate_single_sound())
    sound3_record = ttk.Button(gui, text="Sound 3 record", command=lambda: loop_sounds[2].record_audio())
    sound4 = ttk.Button(gui, text="Sound 4 pause/play",
                        command=lambda: loop_sounds[3].manipulate_single_sound())
    sound4_record = ttk.Button(gui, text="Sound 4 record", command=lambda: loop_sounds[3].record_audio())
    sound5 = ttk.Button(gui, text="Sound 5 pause/play",
                        command=lambda: loop_sounds[4].manipulate_single_sound())
    sound5_record = ttk.Button(gui, text="Sound 5 record", command=lambda: loop_sounds[4].record_audio())
    all_sounds_pause = ttk.Button(gui, text="All sounds play",
                                  command=lambda: lp.manipulate_all_sounds(key_press='u',
                                                                           recording_processes=loop_sounds))
    all_sounds_play = ttk.Button(gui, text="All sounds pause",
                                 command=lambda: lp.manipulate_all_sounds(key_press='p',
                                                                       recording_processes=loop_sounds))
    all_sounds_inverse = ttk.Button(gui, text="All sounds inverse",
                                    command=lambda: lp.manipulate_all_sounds(key_press='i',
                                                                          recording_processes=loop_sounds))

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
    # this site may be useful for the recording of sounds based on holding down keys 'https://www.delftstack.com/howto/python/python-detect-keypress/'
