import PySimpleGUI as sg
from threading import Thread
from dbMeter_KCX.dbMeter import RecordDB

class DBMeter:
    #class run avec pysimplegui pour monitor le rec et modifier le db offset vu dans dbMeter.py
    
    def __init__(self):
        self.recorder = RecordDB()
        sg.theme("DarkAmber")
        self.window = None
        self.readdb_onfile()
        self.layout = [
            [sg.Text("Status : "), sg.Text("Not recording", key = "status"), sg.Button("Change Status", key = "changestatus")],
            [sg.Text("Currently stored value : "), sg.Text(self.storedvalue, key = "storedvalue")],
            [sg.Text("Modify dbgain inside recorder : "), sg.InputText(key = "-DBGAIN-"), sg.Button("Send", key="senddbgain")]
        ]

    def readdb_onfile(self):
        with open("C:/Users/lvteo/Documents/GitHub/dbMeter/dbMeter_KCX/kcx-barre-robin/test.json") as file:
            self.storedvalue = file.read()

    def run(self):

        self.window = sg.Window("dbMeter", layout = self.layout)

        self.window.read(timeout = 1)

        while True:
            event, valuesread = self.window.read(timeout = 33)
            self.readdb_onfile()
            self.window["storedvalue"](value = self.storedvalue)
            if event == sg.WIN_CLOSED:
                self.window.close()
                self.window["status"](value = "Not recording")
                break
            elif event == "senddbgain":
                self.recorder.dbgain = float(valuesread["-DBGAIN-"])
            elif event == "changestatus":
                if not self.recorder.recording:
                    self.recorder.recording = True
                    Thread(target = self.recorder.record).start()
                    self.window["status"](value  = "Recording")
                elif self.recorder.recording:
                    self.recorder.recording = False
                    self.window["status"](value = "Not recording")
            elif event != "__TIMEOUT__":
                print(event, valuesread)
