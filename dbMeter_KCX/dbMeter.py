import pyaudio
import math
import audioop
import time
import numpy as np

print(int(1000*time.time()))

class RecordDB:
    #class recorder utilisant pyaudio pour ecouter et calculer le db en direct via le micro par defaut
    #db calculé par sa valeur rms, n'ayant pas d'étalonnage cette valeur a un offset fixable avec dbgain dans db_from_rms()

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5
        self.recording = False
        self.chunkperioddb = 125
        self.dbgain = 1
        self.currentrms = 1
        self.currentdb = 0
        
        self.audio = pyaudio.PyAudio()

    def db_from_rms(self,rms_data, dbgain = 20):
        if rms_data == 0:
            return 0
        decibel = 20*math.log10(rms_data*dbgain)
        return decibel

    def record(self):
        # start Recording
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        print("recording...")

        while self.recording:
            decibel_list = []
            startloop = 1000*time.time()
            while startloop + self.chunkperioddb > 1000*time.time():
                data = stream.read(self.CHUNK)
                self.currentrms = audioop.rms(data,2)
                self.currentdb = self.db_from_rms(self.currentrms, self.dbgain)
                decibel_list.append(self.currentdb)
            decibelaveraged = np.median(decibel_list)
            with open("dbMeter_KCX/kcx-barre-robin/test.json", "w") as outfile:
                 outfile.write(str(round(decibelaveraged, 1)))

        print("recording ended.")

        # stop Recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()

