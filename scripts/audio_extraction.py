from pytube import YouTube
import ffmpeg as fp
import os
import librosa
import numpy as np
from sklearn.decomposition import PCA


#* Download Audio Function
count = 0

def download_audio(url, path="assets/audio.mp4"):
    global count
    try:
        yt = YouTube(url)

        audio = yt.streams.filter(only_audio=True).first()
        audio.download(filename=path)

        count = 0

        return path
    
    except Exception as e:
        count += 1
        if count < 3:
            print("Some Error Occurred..... Trying again")
            res = download_audio(url, path)
            return res
        else:
            count = 0
            print("Error Occurred..... Skipping")
            return None


#* Audio Extractor Class
class Audio:
    def __init__(self, path):
        self.path = path
        self.y, self.sr = librosa.load(path, sr=None)


    def get_tempo(self):
        onset = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        tempo = librosa.feature.tempo(onset_envelope=onset, sr=self.sr)

        return tempo[0]
    
    def get_melspectogram(self, reduce_dimensions=False, dims=16, n_components=10):
        melspectrogram = librosa.feature.melspectrogram(y=self.y, sr=self.sr, n_mels=128, fmax=8000)
        melspectrogram = librosa.power_to_db(melspectrogram, ref=np.max)

        if reduce_dimensions:
            try:
                melspectrogram = melspectrogram.flatten().reshape(dims, -1)
            except ValueError as err:
                return err
            
            pca = PCA(n_components=n_components)
            melspectrogram = pca.fit_transform(melspectrogram)

        return melspectrogram