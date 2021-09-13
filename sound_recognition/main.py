import glob
import os
import sys
import shutil
from preprocessor import preprocess_wave
from recognizer import  recognize_speech
from writer import write


SOURCE_DIR = r"B:\SpeechToText"
TMP_DIR = os.sep.join([SOURCE_DIR, "tmp"])


def main():
    file_name = sys.argv[1]
    audio_file_path = os.sep.join([SOURCE_DIR, file_name])
    # init tmp folder
    shutil.rmtree(TMP_DIR)
    os.mkdir(TMP_DIR)

    num_cut, sample_rate_hertz, audio_channel_count = preprocess_wave(audio_file_path, 45, TMP_DIR)
    while len(os.listdir(TMP_DIR)) < num_cut:
        pass

    audio_files = glob.glob(os.sep.join([TMP_DIR, "*"]))
    recognition_result = recognize_speech(audio_files, sample_rate_hertz, audio_channel_count)
    srt_file_path = os.sep.join([SOURCE_DIR, os.path.splitext(file_name)[0] + ".srt"])
    write(recognition_result, srt_file_path)


main()
