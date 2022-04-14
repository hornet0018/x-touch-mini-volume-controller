from tkinter import *
from tkinter import ttk
from ttkthemes import *
import sys
import os

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pygame.midi

pygame.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
i = pygame.midi.Input(input_id)


def main():
    root.after(5, main)

    sessions = AudioUtilities.GetAllSessions()
    if i.poll():
        midi_events = i.read(10)
        midi_control_channel = midi_events[0][0][1]
        midi_control_value = midi_events[0][0][2]
        if(midi_control_channel == 9):
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                print('% 1.0f' % (midi_control_value/127*100), '%')
                volume.SetMasterVolume(midi_control_value/127, None)
                volume = midi_control_value / 127
                label["text"] = str(round(midi_control_value/127*100)) + "%"

# アイコンファイルの絶対パスを取得する関数


def get_icon_path(relative_path):
    try:
        # 一時フォルダのパスを取得
        base_path = sys._MEIPASS
    except Exception:
        # 一時フォルダパスを取得できない場合は実行階層パスを取得
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    # アイコンファイルの絶対パスを作成
    return os.path.join(base_path, relative_path)


root = ThemedTk()
root.title('')
root.minsize(width=200, height=100)

s = ttk.Style()
s.theme_use('black')

# Create Widgets
frame1 = ttk.Frame(root, padding=10)
label_title = ttk.Label(frame1, text='x-touch-mini volume controller', font=("Ubunt Mono", 10))
label = ttk.Label(frame1, text='', font=("Ubunt Mono", 30))
t = StringVar()


# Grid
frame1.grid(row=0, column=0, sticky=(N, W, S, E))
label_title.grid(row=0, column=1)
label.grid(row=1, column=1)

# Set Padding
for child in frame1.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Set Grid Weight
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)

# Window Position
root.geometry("+300+200")
root.iconbitmap(default=get_icon_path('slider_icon.ico'))

# Start App
main()
root.mainloop()
