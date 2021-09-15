import math
import os
import struct
import wave

import numpy as np


def preprocess_wave(audio_file_path, time, wav_cut_dir):
    with wave.open(audio_file_path, "r") as wr:
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        integer = math.floor(total_time)
        t = int(time)
        frames = int(ch * fr * t)
        num_cut = int(math.ceil(integer / t))
        data = wr.readframes(wr.getnframes())
        audio_channel_count = wr.getnchannels()

    X = np.frombuffer(data, dtype=np.int16)

    audio_file_paths = []
    for i in range(num_cut):
        outf = os.sep.join([wav_cut_dir, str(i) + ".wav"])
        start_cut = int(i * frames)
        end_cut = int(i * frames + frames)
        Y = X[start_cut:end_cut]
        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        with wave.open(outf, "w") as ww:
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
        audio_file_paths.append(outf)

    return audio_file_paths, fr, audio_channel_count
