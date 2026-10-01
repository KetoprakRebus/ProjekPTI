import librosa
import numpy as np


def audio_check(file):

    audio, sr = librosa.load(file)


    energy = np.mean(
        librosa.feature.rms(
            y=audio
        )
    )


    return {

        "sample_rate": sr,

        "duration":
        round(
            len(audio)/sr,
            2
        ),

        "energy":
        round(
            float(energy),
            5
        ),

        "status":
        "Analisis audio selesai"

    }