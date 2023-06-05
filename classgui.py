import tkinter as tk
from tkinter import ttk
import pyautogui
import pygetwindow
import keyboard
import mouse
import time
import pywintypes
import win32gui
import win32api
import win32ui
import configparser
import threading
import random
import pytesseract
from ctypes import windll
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
FasthandStan = False
LooterButtonStan = False
HPButtonStan = False
ManaButtonStan = False
HasteButtonStan = False
additionalButtonsShow = False
expandStan = False
RunemakerStan = False
lootwindow = False
potionUsage = time.time()
healingSpell = time.time()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Atlas")
        self.wm_attributes("-topmost", 1,)
        self.overrideredirect(1)
        # BINDS
        self.bind('<Button-1>', self.Save_Last_Click_Pos)
        self.bind('<B1-Motion>', self.dragging)

        # button

        self.HPButton = tk.Button(
            self, text='HP', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.hp_clicked())
        self.HPButton.grid(row=1, column=1, padx=0, pady=0)

        self.ManaButton = tk.Button(
            self, text='Mana', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.mana_clicked())
        self.ManaButton.grid(row=1, column=2, padx=0, pady=0)

        self.HasteButton = tk.Button(
            self, text='Timers', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.timers_clicked())
        self.HasteButton.grid(row=2, column=1, padx=0, pady=0)

        self.LooterButton = tk.Button(
            self, text='LOOTER', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.looter_clicked())
        self.LooterButton.grid(row=2, column=2, padx=0, pady=0)

        self.ConfigButton = tk.Button(
            self, text='Config', bg='gray', fg='black', height=1, width=11)
        self.ConfigButton['command'] = self.createConfigWindow
        self.ConfigButton.grid(row=3, column=1, padx=0, pady=0)

        self.ExitButton = tk.Button(
            self, text='EXIT', bg='gray', fg='black', height=1, width=11)
        self.ExitButton['command'] = self.close_window
        self.ExitButton.grid(row=3, column=2, padx=0, pady=0)

        self.moveLabel = tk.Label(self, text='Hold to move', font=("Arial", 9))
        self.moveLabel.grid(row=4, column=1, padx=0, pady=0)

        self.ExpandButton = tk.Button(
            self, text='V', bg='gray', fg='black', height=1, width=11)
        self.ExpandButton['command'] = self.expandButtons
        self.ExpandButton.grid(row=4, column=2, padx=0, pady=0)


        self.fasthandButton = tk.Button(
            self, text='Fasthand', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.fasthand_clicked())

        self.runemakerButton = tk.Button(
            self, text='Runemaker', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.runemaker_clicked())
        
        self.testerButton = tk.Button(
            self, text='tester', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.visibleenemies())
        
        self.tester2Button = tk.Button(
            self, text='supply', bg='#990000', fg='black', height=1, width=11,
            command=lambda: self.supply_check())
  
    def expandButtons(self):
        global expandStan
        if expandStan is False:
            self.ExpandButton.config(text="^")
            self.fasthandButton.grid(row=5, column=1)
            self.runemakerButton.grid(row=5, column=2)
            self.testerButton.grid(row=6, column=1)
            self.tester2Button.grid(row=6, column=2)
            expandStan = True
        elif expandStan is True:
            self.ExpandButton.config(text="V")
            self.fasthandButton.grid_remove()
            self.runemakerButton.grid_remove()
            self.testerButton.grid_remove()
            self.tester2Button.grid_remove()
            expandStan = False

    def createConfigWindow(self):
        ConfigWindow = tk.Toplevel()
        ConfigWindow.geometry('730x720')
        ConfigWindow.title('Config')
        ConfigWindow.wm_attributes("-topmost", 1,)

        # ROW 1
        tk.Label(ConfigWindow, text="Choose window of OBS full screen capture").grid(
            row=1, column=3, padx=0, pady=0)
        # ROW 2
        combo = ttk.Combobox(ConfigWindow, width=27)
        combo['values'] = self.get_all_windows()
        combo['state'] = 'readonly'
        if config['USER']['obsscreen'] != config['DEFAULT']['obsscreen']:
            combo.set(config['USER']['obsscreen'])
        else:
            combo.set(config['DEFAULT']['obsscreen'])
        combo.grid(row=2, column=3)

        # ROW 3
        tk.Label(ConfigWindow, text="HP Recovery").grid(
            row=3, column=3, padx=0, pady=0)
        # ROW 4
        tk.Label(ConfigWindow, text="HP bar coords").grid(
            row=4, column=1, padx=0, pady=0)

        HPEntryStr = tk.StringVar()
        if config['USER']['hpcoord'] != config['DEFAULT']['hpcoord']:
            HPEntryStr.set(config['USER']['hpcoord'])
        else:
            HPEntryStr.set(config['DEFAULT']['hpcoord'])
        HPEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=HPEntryStr, font=('calibre', 10, 'normal'))
        HPEntry.grid(
            row=4, column=2, padx=0, pady=0)

        HighStr = tk.StringVar()
        HighStr.set("")
        HPRGB = tk.Label(ConfigWindow, textvariable=HighStr)
        HPRGB.grid(
            row=4, column=4, padx=0, pady=0)

        def updateHighHPLabel():
            x, y = pyautogui.position()
            RGBValue = pyautogui.pixel(x, y)
            if RGBValue == (0, 175, 0):
                HPRGB.configure(fg='green')
            else:
                HPRGB.configure(fg='red')
            HighStr.set(RGBValue)
            updater = ConfigWindow.after(100, updateHighHPLabel)
            if win32api.GetAsyncKeyState(0x01) < 0:
                ConfigWindow.after_cancel(updater)
                HPEntryStr.set((str(x) + ', ' + str(y)))
                HighStr.set('')


        getPosition1 = tk.Button(
            ConfigWindow, text="Pixel", command=lambda: updateHighHPLabel())
        getPosition1.grid(row=4, column=3)

        # ROW 5
        tk.Label(ConfigWindow, text="green hp").grid(
            row=5, column=1, padx=0, pady=0)

        tk.Label(ConfigWindow, text="Hotkey to press").grid(
            row=5, column=2, padx=0, pady=0)

        combo2 = ttk.Combobox(ConfigWindow, width=4)
        combo2['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo2['state'] = 'readonly'
        combo2.grid(row=5, column=3)
        if config['USER']['highhpkey'] != config['DEFAULT']['highhpkey']:
            combo2.set(config['USER']['highhpkey'])
        else:
            combo2.set(config['DEFAULT']['highhpkey'])

        # ROW 6
        tk.Label(ConfigWindow, text="orange hp").grid(
            row=6, column=1, padx=0, pady=0)

        tk.Label(ConfigWindow, text="Hotkey to press").grid(
            row=6, column=2, padx=0, pady=0)

        combo3 = ttk.Combobox(ConfigWindow, width=4)
        combo3['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo3['state'] = 'readonly'
        combo3.grid(row=6, column=3)
        if config['USER']['midhpkey'] != config['DEFAULT']['midhpkey']:
            combo3.set(config['USER']['midhpkey'])
        else:
            combo3.set(config['DEFAULT']['midhpkey'])
        
        # ROW 7
        tk.Label(ConfigWindow, text="red hp").grid(
            row=7, column=1, padx=0, pady=0)

        tk.Label(ConfigWindow, text="Hotkey to press").grid(
            row=7, column=2, padx=0, pady=0)

        combo4 = ttk.Combobox(ConfigWindow, width=4)
        combo4['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo4['state'] = 'readonly'
        combo4.grid(row=7, column=3)
        if config['USER']['lowhpkey'] != config['DEFAULT']['lowhpkey']:
            combo4.set(config['USER']['lowhpkey'])
        else:
            combo4.set(config['DEFAULT']['lowhpkey'])



        tk.Label(ConfigWindow, text="Mana Recovery").grid(
            row=8, column=3, padx=0, pady=0)

        # ROW 8
        tk.Label(ConfigWindow, text="Mana").grid(
            row=9, column=1, padx=0, pady=0)

        ManaEntryStr = tk.StringVar()
        if config['USER']['manacoord'] != config['DEFAULT']['manacoord']:
            ManaEntryStr.set(config['USER']['manacoord'])
        else:
            ManaEntryStr.set(config['DEFAULT']['manacoord'])
        manaEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=ManaEntryStr, font=('calibre', 10, 'normal'))
        manaEntry.grid(
            row=9, column=2)

        ManaStr = tk.StringVar()
        ManaStr.set("")
        ManaRGB = tk.Label(ConfigWindow, textvariable=ManaStr)
        ManaRGB.grid(
            row=9, column=4, padx=0, pady=0)

        def updateManaLabel():
            x, y = pyautogui.position()
            RGBValue = pyautogui.pixel(x, y)
            if RGBValue == (0, 56, 116) or RGBValue == (0, 52, 116) or RGBValue == (125, 122, 255):
                ManaRGB.configure(fg='green')
            else:
                ManaRGB.configure(fg='red')
            ManaStr.set(RGBValue)
            updater = ConfigWindow.after(100, updateManaLabel)
            if win32api.GetAsyncKeyState(0x01) < 0:
                # print(RGBValue)
                ConfigWindow.after_cancel(updater)
                ManaEntryStr.set((str(x) + ', ' + str(y)))
                ManaStr.set('')

        ManaPixel = tk.Button(ConfigWindow, text="Pixel",
                              command=lambda: updateManaLabel())
        ManaPixel.grid(row=9, column=3)

        tk.Label(ConfigWindow, text="Hotkey to press").grid(
            row=9, column=4, padx=0, pady=0)

        combo5 = ttk.Combobox(ConfigWindow, width=4)
        combo5['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo5['state'] = 'readonly'
        combo5.grid(row=9, column=5)
        if config['USER']['manakey'] != config['DEFAULT']['manakey']:
            combo5.set(config['USER']['manakey'])
        else:
            combo5.set(config['DEFAULT']['manakey'])
        # ROW 9
        tk.Label(ConfigWindow, text="Looter").grid(
            row=10, column=3)
        # ROW 10
        tk.Label(ConfigWindow, text="Character").grid(
            row=11, column=1)
        CharacterEntryStr = tk.StringVar()
        if config['USER']['charactercoord'] != config['DEFAULT']['charactercoord']:
            CharacterEntryStr.set(config['USER']['charactercoord'])
        else:
            CharacterEntryStr.set(config['DEFAULT']['charactercoord'])
        CharacterEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=CharacterEntryStr, font=('calibre', 10, 'normal'))
        CharacterEntry.grid(
            row=11, column=2)

        def updateCharacterLabel():
            pass
            updater = ConfigWindow.after(100, updateCharacterLabel)
            if win32api.GetAsyncKeyState(0x01) < 0:
                ConfigWindow.after_cancel(updater)
                x, y = pyautogui.position()
                CharacterEntryStr.set((str(x) + ', ' + str(y)))
        CharacterPixel = tk.Button(
            ConfigWindow, text="Character", command=lambda: updateCharacterLabel())
        CharacterPixel.grid(row=11, column=3)
        tk.Label(ConfigWindow, text="Hotkey for looting").grid(
            row=11, column=4)
        # ROW 11
        tk.Label(ConfigWindow, text="SQM TOP-LEFT").grid(
            row=12, column=1)

        SQMEntryStr = tk.StringVar()
        if config['USER']['1sqmcoord'] != config['DEFAULT']['1sqmcoord']:
            SQMEntryStr.set(config['USER']['1sqmcoord'])
        else:
            SQMEntryStr.set(config['DEFAULT']['1sqmcoord'])
        SQMEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=SQMEntryStr, font=('calibre', 10, 'normal'))
        SQMEntry.grid(
            row=12, column=2)

        def updatesSQMLabel():
            pass
            updater = ConfigWindow.after(100, updatesSQMLabel)
            if win32api.GetAsyncKeyState(0x01) < 0:
                ConfigWindow.after_cancel(updater)
                x, y = pyautogui.position()
                SQMEntryStr.set((str(x) + ', ' + str(y)))

        SQMPixel = tk.Button(ConfigWindow, text="SQM",
                             command=lambda: updatesSQMLabel())
        SQMPixel.grid(row=12, column=3)

        combo6 = ttk.Combobox(ConfigWindow, width=4)
        combo6['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo6['state'] = 'readonly'
        combo6.grid(row=11, column=5)
        if config['USER']['looterkey'] != config['DEFAULT']['looterkey']:
            combo6.set(config['USER']['looterkey'])
        else:
            combo6.set(config['DEFAULT']['looterkey'])
        # ROW 13
        valueableSTR = tk.StringVar()
        valueableSTR.set("")
        valuableLabel = tk.Label(ConfigWindow, textvariable=valueableSTR)
        label1 = tk.Label(ConfigWindow, text="Valuable orange word")
        valuableLabel.grid(row=13, column=4)


        def updateValuableLoot():
            x, y = pyautogui.position()
            RGBValue = pyautogui.pixel(x, y)
            if RGBValue == (240, 180, 0):
                valuableLabel.configure(fg='green')
            else:
                valuableLabel.configure(fg='red')
            valueableSTR.set(RGBValue)
            updater = ConfigWindow.after(100, updateValuableLoot)
            if win32api.GetAsyncKeyState(0x01) < 0:
                ConfigWindow.after_cancel(updater)
                valueableLootStr.set((str(x) + ', ' + str(y)))
                valueableSTR.set('')

        
        
        

        valueableLootStr = tk.StringVar()
        if config['USER']['valuablelootcoord'] != config['DEFAULT']['valuablelootcoord']:
            valueableLootStr.set(config['USER']['valuablelootcoord'])
        else:
            valueableLootStr.set(config['DEFAULT']['valuablelootcoord'])
        lootvaluableEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=valueableLootStr, font=('calibre', 10, 'normal'))
        

        lootvaluableButton = tk.Button(ConfigWindow, text="coords",
                             command=lambda: updateValuableLoot())
        
        def autolootChecked():
            print(var1.get())
            if var1.get() > 0:
                label1.grid(row=13, column=1)
                lootvaluableEntry.grid(row=13, column=2)
                lootvaluableButton.grid(row=13, column=3)
            else:
                label1.grid_forget()
                lootvaluableEntry.grid_forget()
                lootvaluableButton.grid_forget()


        var1 = tk.IntVar()
        if config['USER']['autoloot'] != config['DEFAULT']['autoloot']:
            var1.set(config['USER']['autoloot'])
        else:
            var1.set(config['DEFAULT']['autoloot'])
        autolootChecked()

        tk.Checkbutton(ConfigWindow, text="Auto-loot?", variable=var1, command=autolootChecked).grid(
            row=12, column=4)
        

        # ROW 14
        tk.Label(ConfigWindow, text="Fasthand").grid(
            row=21, column=3)

        tk.Label(ConfigWindow, text="Click(left) at").grid(
            row=22, column=1)
        ClickerEntryStr = tk.StringVar()
        if config['USER']['clickercoord'] != config['DEFAULT']['clickercoord']:
            ClickerEntryStr.set(config['USER']['clickercoord'])
        else:
            ClickerEntryStr.set(config['DEFAULT']['clickercoord'])
        ClickerEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=ClickerEntryStr, font=('calibre', 10, 'normal'))
        ClickerEntry.grid(
            row=22, column=2)

        def updatesClickerLabel():
            pass
            updater = ConfigWindow.after(100, updatesClickerLabel)
            if win32api.GetAsyncKeyState(0x01) < 0:
                ConfigWindow.after_cancel(updater)
                x, y = pyautogui.position()
                ClickerEntryStr.set((str(x) + ', ' + str(y)))

        ClickerPixel = tk.Button(ConfigWindow, text="SQM",
                                 command=lambda: updatesClickerLabel())
        ClickerPixel.grid(row=22, column=3)

        tk.Label(ConfigWindow, text="after you press").grid(
            row=22, column=4)


        combo7 = ttk.Combobox(ConfigWindow, width=4)
        combo7['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo7['state'] = 'readonly'
        combo7.grid(row=22, column=5)
        if config['USER']['clickerkey'] != config['DEFAULT']['clickerkey']:
            combo7.set(config['USER']['clickerkey'])
        else:
            combo7.set(config['DEFAULT']['clickerkey'])

        
        # ROW 15
        tk.Label(ConfigWindow, text="Move to").grid(
            row=23, column=1)
        FasthandMoveToEntryStr = tk.StringVar()
        if config['USER']['clickercoord'] != config['DEFAULT']['clickercoord']:
            FasthandMoveToEntryStr.set(config['USER']['FasthandMoveToEntryStrcoord'])
        else:
            FasthandMoveToEntryStr.set(config['DEFAULT']['FasthandMoveToEntryStrcoord'])
        FasthandMoveToEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=FasthandMoveToEntryStr, font=('calibre', 10, 'normal'))
        FasthandMoveToEntry.grid(
            row=23, column=2)
        
        """
        def updatesFasthandLabel():
            pass
            updater = ConfigWindow.after(100, updatesFasthandLabel)
            if win32api.GetAsyncKeyState(0x01) < 0:
                ConfigWindow.after_cancel(updater)
                x, y = pyautogui.position()
                FasthandMoveToEntryStr.set((str(x) + ', ' + str(y)))

        FasthandPixel = tk.Button(ConfigWindow, text="TEST",
                                 command=lambda: updatesFasthandLabel())
        FasthandPixel.grid(row=15, column=3)
        """
        
        # ROW 15
        tk.Label(ConfigWindow, text="Runemaker").grid(
            row=26, column=3)
        # ROW 16
        tk.Label(ConfigWindow, text="Eat food delay(seconds)").grid(
            row=27, column=1)
        RunemakerEntryStr = tk.StringVar()
        if config['USER']['runemakerfooddelay'] != config['DEFAULT']['runemakerfooddelay']:
            RunemakerEntryStr.set(config['USER']['runemakerfooddelay'])
        else:
            RunemakerEntryStr.set(config['DEFAULT']['runemakerfooddelay'])
        RunemakerEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=RunemakerEntryStr, font=('calibre', 10, 'normal'))
        RunemakerEntry.grid(
            row=27, column=2)

        tk.Label(ConfigWindow, text="food button").grid(
            row=27, column=4)

        combo8 = ttk.Combobox(ConfigWindow, width=4)
        combo8['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo8['state'] = 'readonly'
        combo8.grid(row=27, column=5)
        if config['USER']['runemakerfoodbutton'] != config['DEFAULT']['runemakerfoodbutton']:
            combo8.set(config['USER']['runemakerfoodbutton'])
        else:
            combo8.set(config['DEFAULT']['runemakerfoodbutton'])
        # ROW 17

        tk.Label(ConfigWindow, text="Ring equip delay(seconds)").grid(
            row=28, column=1)
        RunemakerRingEntryStr = tk.StringVar()
        if config['USER']['runemakerringdelay'] != config['DEFAULT']['runemakerringdelay']:
            RunemakerRingEntryStr.set(config['USER']['runemakerringdelay'])
        else:
            RunemakerRingEntryStr.set(config['DEFAULT']['runemakerringdelay'])
        RunemakerRingEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=RunemakerRingEntryStr, font=('calibre', 10, 'normal'))
        RunemakerRingEntry.grid(
            row=28, column=2)

        tk.Label(ConfigWindow, text="delay 0 = not gonna use it").grid(
            row=28, column=3)

        tk.Label(ConfigWindow, text="ring button").grid(
            row=28, column=4)

        combo9 = ttk.Combobox(ConfigWindow, width=4)
        combo9['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo9['state'] = 'readonly'
        combo9.grid(row=28, column=5)
        if config['USER']['runemakerringbutton'] != config['DEFAULT']['runemakerringbutton']:
            combo9.set(config['USER']['runemakerringbutton'])
        else:
            combo9.set(config['DEFAULT']['runemakerringbutton'])
        # ROW 18
        tk.Label(ConfigWindow, text="Boots equip delay(seconds)").grid(
            row=29, column=1)
        RunemakerBootsEntryStr = tk.StringVar()
        if config['USER']['runemakerbootsdelay'] != config['DEFAULT']['runemakerbootsdelay']:
            RunemakerBootsEntryStr.set(config['USER']['runemakerbootsdelay'])
        else:
            RunemakerBootsEntryStr.set(config['DEFAULT']['runemakerbootsdelay'])
        RunemakerBootsEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=RunemakerBootsEntryStr, font=('calibre', 10, 'normal'))
        RunemakerBootsEntry.grid(
            row=29, column=2)

        tk.Label(ConfigWindow, text="delay 0 = not gonna use it").grid(
            row=29, column=3)

        tk.Label(ConfigWindow, text="boots button").grid(
            row=29, column=4)

        combo10 = ttk.Combobox(ConfigWindow, width=4)
        combo10['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo10['state'] = 'readonly'
        combo10.grid(row=29, column=5)
        if config['USER']['runemakerbootsbutton'] != config['DEFAULT']['runemakerbootsbutton']:
            combo10.set(config['USER']['runemakerbootsbutton'])
        else:
            combo10.set(config['DEFAULT']['runemakerbootsbutton'])

        # ROW 19
        tk.Label(ConfigWindow, text="Rune spellcast delay(seconds)").grid(
            row=30, column=1)
        RunemakerRuneEntryStr = tk.StringVar()
        if config['USER']['runemakerrunesdelay'] != config['DEFAULT']['runemakerrunesdelay']:
            RunemakerRuneEntryStr.set(config['USER']['runemakerrunesdelay'])
        else:
            RunemakerRuneEntryStr.set(config['DEFAULT']['runemakerrunesdelay'])
        RunemakerRuneEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=RunemakerRuneEntryStr, font=('calibre', 10, 'normal'))
        RunemakerRuneEntry.grid(
            row=30, column=2)

        tk.Label(ConfigWindow, text="delay 0 = not gonna use it").grid(
            row=30, column=3)

        tk.Label(ConfigWindow, text="rune button").grid(
            row=30, column=4)

        combo11 = ttk.Combobox(ConfigWindow, width=4)
        combo11['values'] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                            "R", "F", "X", "G"]
        combo11['state'] = 'readonly'
        combo11.grid(row=30, column=5)
        if config['USER']['runemakerrunebutton'] != config['DEFAULT']['runemakerrunebutton']:
            combo11.set(config['USER']['runemakerrunebutton'])
        else:
            combo11.set(config['DEFAULT']['runemakerrunebutton'])

        def capture_coords():
            mouse.wait(button='left', target_types='down')
            begin = pyautogui.position()
            mouse.wait(button='left', target_types='up')
            end = pyautogui.position()
            x1 = min(begin[0], end[0])
            y1 = min(begin[1], end[1])
            x2 = max(begin[0], end[0])
            y2 = max(begin[1], end[1])
            gl = "{}, {}".format(x1, y1)
            dp = "{}, {}".format(x2, y2)
            RefillglEntryStr.set(gl)
            RefilldpEntryStr.set(dp)


        tk.Label(ConfigWindow, text="Refill").grid(
            row=85, column=3)

        tk.Label(ConfigWindow, text="Refill top-left").grid(
            row=86, column=1)
        RefillglEntryStr = tk.StringVar()
        if config['USER']['refillgl'] != config['DEFAULT']['refillgl']:
            RefillglEntryStr.set(config['USER']['refillgl'])
        else:
            RefillglEntryStr.set(config['DEFAULT']['refillgl'])
        refilldpEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=RefillglEntryStr, font=('calibre', 10, 'normal'))
        refilldpEntry.grid(
            row=86, column=2)
        
        tk.Label(ConfigWindow, text="Refill bottom-right").grid(
            row=87, column=1)
        RefilldpEntryStr = tk.StringVar()
        if config['USER']['refilldp'] != config['DEFAULT']['refilldp']:
            RefilldpEntryStr.set(config['USER']['refilldp'])
        else:
            RefilldpEntryStr.set(config['DEFAULT']['refilldp'])
        refilldpEntry = tk.Entry(
            ConfigWindow, width=10, textvariable=RefilldpEntryStr, font=('calibre', 10, 'normal'))
        refilldpEntry.grid(
            row=87, column=2)


        captureButton = tk.Button(ConfigWindow, text="capture",
                                command=lambda: capture_coords())
        captureButton.grid(
            row=82, column=2, padx=0, pady=0)

        # ROW last
        tk.Label(ConfigWindow, text="").grid(
            row=98, column=1)
        saveButton = tk.Button(ConfigWindow, text="Save",
                               command=lambda: save_click())
        saveButton.grid(
            row=99, column=2, padx=0, pady=0)
        tk.Button(ConfigWindow, text="Close", command=ConfigWindow.destroy).grid(
            row=99, column=4, padx=0, pady=0)
        


        
        def save_click():
            config['USER']['obsscreen'] = combo.get()
            config['USER']['hpcoord'] = HPEntry.get()
            config['USER']['highhpkey'] = combo2.get()
            config['USER']['midhpkey'] = combo3.get()
            config['USER']['lowhpkey'] = combo4.get()
            config['USER']['manacoord'] = manaEntry.get()
            config['USER']['manakey'] = combo5.get()
            config['USER']['charactercoord'] = CharacterEntry.get()
            config['USER']['1sqmcoord'] = SQMEntry.get()
            config['USER']['looterkey'] = combo6.get()
            config['USER']['valuablelootcoord'] = valueableLootStr.get()
            config['USER']['autoloot'] = str(var1.get())
            config['USER']['clickercoord'] = ClickerEntry.get()
            config['USER']['clickerkey'] = combo7.get()
            config['USER']['FasthandMoveToEntryStrcoord'] = FasthandMoveToEntry.get()
            config['USER']['runemakerfoodbutton'] = combo8.get()
            config['USER']['runemakerfooddelay'] = RunemakerEntry.get()
            config['USER']['runemakerringbutton'] = combo9.get()
            config['USER']['runemakerringdelay'] = RunemakerRingEntry.get()
            config['USER']['runemakerbootsbutton'] = combo10.get()
            config['USER']['runemakerbootsdelay'] = RunemakerBootsEntry.get()
            config['USER']['runemakerrunebutton'] = combo11.get()
            config['USER']['runemakerrunesdelay'] = RunemakerRuneEntry.get()
            config['USER']['refillgl'] = RefillglEntryStr.get()
            config['USER']['refilldp'] = RefilldpEntryStr.get()
            with open('config.ini', 'w', encoding="utf-8") as configfile:
                config.write(configfile)

    def Save_Last_Click_Pos(self, event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def dragging(self, event):
        x, y = event.x - lastClickX + self.winfo_x(), event.y - lastClickY + \
            self.winfo_y()
        self.geometry("+%s+%s" % (x, y))

    def close_window(self):
        print("zamykanie GUI")
        self.destroy()
        exit()

    def get_all_windows(self):
        x = []
        for i in pygetwindow.getAllTitles():
            x.append(i)
        for _ in range(x.count('')):
            x.remove('')
        return x

    def fasthand(self):
        global FasthandStan
        rozdzielClickerCoord = config['USER']['clickercoord'].partition(', ')
        clickerCoordX = int(rozdzielClickerCoord[0])
        clickerCoordY = int(rozdzielClickerCoord[2])
        rozdzielFasthandCoord = config['USER']['fasthandmovetoentrystrcoord'].partition(', ')
        FasthandCoordX = int(rozdzielFasthandCoord[0])
        FasthandCoordY = int(rozdzielFasthandCoord[2])
        pyautogui.PAUSE = 0
        while True:
            keyboard.wait(config['USER']['clickerkey'])
            if FasthandStan is True:
                pyautogui.moveTo((clickerCoordX, clickerCoordY))
                pyautogui.dragTo((FasthandCoordX, FasthandCoordY), button='left')
            else:
                break

    def fasthand_clicked(self):
        global FasthandStan

        thread = threading.Thread(target=self.fasthand)
        thread.daemon = True

        if FasthandStan:
            self.fasthandButton.config(bg='#990000')
            FasthandStan = False
        else:
            FasthandStan = True
            self.fasthandButton.config(bg='green')
            thread.start()

    def looter(self):
        global LooterButtonStan
        
        rozdzielCharacter = config['USER']['charactercoord'].partition(', ')
        rozdziel1sqm = config['USER']['1sqmcoord'].partition(', ')
        characterx = int(rozdzielCharacter[0])
        charactery = int(rozdzielCharacter[2])
        sqm1x = int(rozdziel1sqm[0])
        sqm1y = int(rozdziel1sqm[2])

        pyautogui.PAUSE = 0
        randomizationRange = 15

        diferencex = characterx - sqm1x
        diferencey = charactery - sqm1y
        sqm2x = characterx
        sqm2y = charactery - diferencey
        sqm3x = characterx + diferencex
        sqm3y = charactery - diferencey
        sqm4x = characterx - diferencex
        sqm4y = charactery
        sqm6x = characterx + diferencex
        sqm6y = charactery
        sqm7x = characterx - diferencex
        sqm7y = charactery + diferencey
        sqm8x = characterx
        sqm8y = charactery + diferencey
        sqm9x = characterx + diferencex
        sqm9y = charactery + diferencey

        
        while LooterButtonStan is True:
            if config['USER']['autoloot'] == '1':
                time.sleep(0.7)
                lootcords = config['USER']['valuablelootcoord'].partition(', ')
                coordy = (int(lootcords[0]), int(lootcords[2]))
                kolory = self.GetPixelRGBColor(coordy)
                if kolory == (240, 180, 0):
                    if LooterButtonStan is True:
                        mousePos = pyautogui.position()
                        pyautogui.keyDown("shift")
                        pyautogui.click((sqm1x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm1y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click(sqm2x + random.randint(a=-randomizationRange, b=randomizationRange),
                                        (sqm2y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((sqm3x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm3y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((sqm4x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm4y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((characterx + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (charactery + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((sqm6x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm6y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((sqm7x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm7y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((sqm8x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm8y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.click((sqm9x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                        (sqm9y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                        pyautogui.keyUp("shift")
                        pyautogui.moveTo(mousePos)
                        # time.sleep(0.1)
                    else:
                        break
            else:
                keyboard.wait(config['USER']['looterkey'])
                if LooterButtonStan is True:
                    mousePos = pyautogui.position()
                    pyautogui.keyDown("shift")
                    pyautogui.click((sqm1x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm1y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click(sqm2x + random.randint(a=-randomizationRange, b=randomizationRange),
                                    (sqm2y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((sqm3x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm3y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((sqm4x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm4y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((characterx + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (charactery + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((sqm6x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm6y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((sqm7x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm7y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((sqm8x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm8y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.click((sqm9x + random.randint(a=-randomizationRange, b=randomizationRange)),
                                    (sqm9y + random.randint(a=-randomizationRange, b=randomizationRange)), button='right')
                    pyautogui.keyUp("shift")
                    pyautogui.moveTo(mousePos)
                    # time.sleep(0.1)
                else:
                    break

    def looter_clicked(self):
        global LooterButtonStan
        thread = threading.Thread(target=self.looter)
        thread.daemon = True
        if LooterButtonStan:
            self.LooterButton.config(bg='#990000')
            LooterButtonStan = False
        else:
            LooterButtonStan = True
            self.LooterButton.config(bg='green')
            thread.start()
# not completed
    def timers_clicked(self):
        global HasteButtonStan
        if HasteButtonStan:
            self.HasteButton.config(bg='#990000')
            HasteButtonStan = False
        else:
            self.HasteButton.config(bg='yellow')
            HasteButtonStan = True

    def GetPixelRGBColor(self, pos):
        obsfull = config['USER']['obsscreen']
        hwnd = win32gui.FindWindow(None, obsfull)

        # Change the line below depending on whether you want the whole window
        # or just the client area. 

        #left, top, right, bot = win32gui.GetClientRect(hwnd)
        """
        try:
            left, top, right, bot = win32gui.GetClientRect(hwnd)
        
        """
        try:
            self.moveLabel.config(bg= 'white', text='Hold to move', font=("Arial", 9))
            left, top, right, bot = win32gui.GetClientRect(hwnd)
            w = right - left
            h = bot - top

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

            saveDC.SelectObject(saveBitMap)

            # Change the line below depending on whether you want the whole window
            # or just the client area. 
            #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
            windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
            #print(result)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)

            width, height = im.size
            pixel_values = list(im.getdata())


            """
            rgb_im = im.convert('RGB')
            print(pos)
            r, g, b = rgb_im.getpixel(pos)
            """

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)

            return pixel_values[width*pos[1]+pos[0]]
        except pywintypes.error as e:
            if e.args[0] == 1400:
                print("Błąd: Nieprawidłowe dojście okna.")
                self.moveLabel.config(bg= 'yellow', text='OPEN OBS', font=("Arial", 11))
            else:
                print(f"Wystąpił inny błąd: {e}")
        except win32ui.error as e:
            print(e)
        #left, top, right, bot = win32gui.GetWindowRect(hwnd)

    def healer(self):
        global HPButtonStan
        global potionUsage
        global healingSpell
        HP = config['USER']['hpcoord'].partition(', ')
        coordy = (int(HP[0]), int(HP[2]))
        while HPButtonStan is True:
            time.sleep(0.35)
            #--------------------------------------------
            kolory = self.GetPixelRGBColor(coordy)
            if kolory == (175, 44, 44) and (time.time()-potionUsage) > 1:
                pyautogui.press(config['USER']['lowhpkey'])
                potionUsage = time.time()
            elif kolory == (184, 140, 8) and (time.time()-potionUsage) > 1:
                pyautogui.press(config['USER']['midhpkey'])
                potionUsage = time.time()
            if kolory == (100, 146, 4) and (time.time()-healingSpell) > 1:
                pyautogui.press(config['USER']['highhpkey'])
                potionUsage = time.time()
            #else:
                #print(kolory)

    def hp_clicked(self):
        global HPButtonStan
        thread = threading.Thread(target=self.healer)
        thread.daemon = True
        if HPButtonStan:
            self.HPButton.config(bg='#990000')
            HPButtonStan = False
        else:
            self.HPButton.config(bg='green')
            HPButtonStan = True
            thread.start()

    def mana_recovery(self):
        global ManaButtonStan
        global potionUsage
        MANA = config['USER']['manacoord'].partition(', ')
        coordy = (int(MANA[0]), int(MANA[2]))
        while ManaButtonStan is True:
            time.sleep(0.3)
            #--------------------------------------------
            kolory = self.GetPixelRGBColor(coordy)
            if kolory != (0,56,116) and (time.time()-potionUsage) > 1:
                pyautogui.press(config['USER']['manakey'])
                potionUsage = time.time()
            #else:
                #print(kolory)

    def mana_clicked(self):
        global ManaButtonStan
        thread = threading.Thread(target=self.mana_recovery)
        thread.daemon = True
        if ManaButtonStan:
            self.ManaButton.config(bg='#990000')
            ManaButtonStan = False
        else:
            self.ManaButton.config(bg='green')
            ManaButtonStan = True
            thread.start()

    def runemaker_clicked(self):
        global RunemakerStan
        t1 = threading.Thread(target=self.runemakerfood)
        t1.daemon = True
        t2 = threading.Thread(target=self.runemakerring)
        t2.daemon = True
        t3 = threading.Thread(target=self.runemakerboots)
        t3.daemon = True
        t4 = threading.Thread(target=self.runemakerrune)
        t4.daemon = True

        if RunemakerStan:
            RunemakerStan = False
            self.runemakerButton.config(bg='#990000')
        else:
            RunemakerStan = True
            self.runemakerButton.config(bg='green')
            if int(config['USER']['runemakerfooddelay']) != 0:
                t1.start()
            if int(config['USER']['runemakerringdelay']) != 0:
                t2.start()
            if int(config['USER']['runemakerbootsdelay']) != 0:
                t3.start()
            if int(config['USER']['runemakerrunesdelay']) != 0:
                t4.start()
            
    def runemakerfood(self):
        global RunemakerStan
        delay = int(config['USER']['runemakerfooddelay']) + random.randint(4, 15)
        button = config['USER']['runemakerfoodbutton']
        while RunemakerStan is True:
            time.sleep(delay)
            pyautogui.press(button)

    def runemakerring(self):
        global RunemakerStan
        delay = int(config['USER']['runemakerringdelay']) + random.randint(4, 15)
        button = config['USER']['runemakerringbutton']
        while RunemakerStan is True:
            time.sleep(delay)
            pyautogui.press(button)

    def runemakerboots(self):
        global RunemakerStan
        delay = int(config['USER']['runemakerbootsdelay']) + random.randint(4, 15)
        button = config['USER']['runemakerbootsbutton']
        while RunemakerStan is True:
            time.sleep(delay)
            pyautogui.press(button)

    def runemakerrune(self):
        global RunemakerStan
        delay = int(config['USER']['runemakerrunesdelay']) + random.randint(4, 15)
        button = config['USER']['runemakerrunebutton']
        while RunemakerStan is True:
            time.sleep(delay)
            pyautogui.press(button)

    def visibleenemies(self):
        if config['USER']['firstmob'] != config['DEFAULT']['firstmob']:
            firstmob = config['USER']['firstmob']
        else:
            firstmob = config['DEFAULT']['firstmob']

        if config['USER']['secondmob'] != config['DEFAULT']['secondmob']:
            secondmob = config['USER']['secondmob']
        else:
            secondmob = config['DEFAULT']['secondmob']
        firstmob = firstmob.partition(', ')
        secondmob = secondmob.partition(', ')
        firstmobx, firstmoby = int(firstmob[0]), int(firstmob[2])
        secondmobx, secondmoby = int(secondmob[0]), int(secondmob[2])
        roznica = int(secondmoby) - int(firstmoby)
        monsterQuant = 0
        """
        if not (60, 60, 60) < self.GetPixelRGBColor((firstmobx, secondmoby)) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < self.GetPixelRGBColor((firstmobx, firstmoby+roznica)) < (81, 81, 81):
            monsterQuant += 1
        """
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+roznica) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+2*roznica) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+3*roznica) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+4*roznica) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+5*roznica) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+6*roznica) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < pyautogui.pixel(firstmobx, firstmoby+7*roznica) < (81, 81, 81):
            monsterQuant += 1
        print(monsterQuant, 'monsters at screen')

    def monstersNearby(self):
        # poprawny kolor hp na zielono 0,192,0
        # gora lewo pasek hp 1096,475
        # gora pasek hp 1201,475

        if config['USER']['mobG'] != config['DEFAULT']['mobG']:
            mobG = config['USER']['mobG']
        else:
            mobG = config['DEFAULT']['mobG']

        if config['USER']['mobSL'] != config['DEFAULT']['mobSL']:
            mobSL = config['USER']['mobSL']
        else:
            mobSL = config['DEFAULT']['mobSL']

        mobG = mobG.partition(', ')
        mobSL = mobSL.partition(', ')

        mobGx, mobGy = int(mobG[0]), int(mobG[2])
        mobSLx, mobSLy = int(mobSL[0]), int(mobSL[2])

        roznicaPoziomo = mobGx - mobSLx
        roznicaPionowo = mobSLy - mobGy
        """
        mobGL = mobSLx, mobGy 
        mobGP = mobGx + roznicaPoziomo, mobGy
        mobSP = mobGx + roznicaPoziomo, mobGy + roznicaPionowo
        mobDL = mobSLx, mobSLy + roznicaPionowo
        mobD = mobGx, mobSLy + roznicaPionowo
        mobDP = mobGx + roznicaPoziomo, mobSLy + roznicaPionowo
        """
        monsterQuanty = 0
        """
        if not (60, 60, 60) < self.GetPixelRGBColor((firstmobx, secondmoby)) < (81, 81, 81):
            monsterQuant += 1
        if not (60, 60, 60) < self.GetPixelRGBColor((firstmobx, firstmoby+roznica)) < (81, 81, 81):
            monsterQuant += 1
        """
        if pyautogui.pixel(mobSLx, mobGy) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobGx, mobGy) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobGx + roznicaPoziomo, mobGy) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobSLx, mobSLy) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobGx + roznicaPoziomo, mobGy + roznicaPionowo) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobSLx, mobSLy + roznicaPionowo) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobGx, mobSLy + roznicaPionowo) == (0,192,0):
            monsterQuanty += 1
        if pyautogui.pixel(mobGx + roznicaPoziomo, mobSLy + roznicaPionowo) == (0,192,0):
            monsterQuanty += 1
        print(monsterQuanty, 'monsters near character')
    
    def supply_check(self):
        obsfull = config['USER']['obsscreen']
        hwnd = win32gui.FindWindow(None, obsfull)
        # Pobierz obraz z ekranu w zadanych koordynatach
        gl = config['USER']['refillgl'].partition(', ')
        dp = config['USER']['refilldp'].partition(', ')
        (int(gl[0]), int(gl[2]))
        left, top = gl[0], gl[2]
        right, bottom = dp[0], dp[2]

        left = int(left)
        top = int(top)
        right = int(right)
        bottom = int(bottom)

        width, height = right - left, bottom - top  # wielkość obszaru do przechwycenia
        


        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        if result == 1:
        #PrintWindow Succeeded
            im.save("test.png")
        
        # Odczytaj liczbę z obrazu przy użyciu biblioteki pytesseract
        number = pytesseract.image_to_string(im, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        # Zwolnij zasoby
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        # Zwróć wykrytą liczbę
        print(number)



        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()