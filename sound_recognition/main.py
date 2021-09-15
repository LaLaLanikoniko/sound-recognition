import glob
import os
import shutil
import sys

from preprocessor import preprocess_wave
from recognizer import recognize_speech
from writer import write


SEPARATED_AUDIO_FILE_TIME = 45

def main():
    current_dir = os.getcwd()
    tmp_dir = os.sep.join([current_dir, "tmp"])
    source_audio_file_path = sys.argv[1]
    # init tmp folder
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    separated_audio_file_paths, sample_rate_hertz, audio_channel_count = preprocess_wave(
        source_audio_file_path, SEPARATED_AUDIO_FILE_TIME, tmp_dir
    )
    while len(os.listdir(tmp_dir)) < len(separated_audio_file_paths):
        pass

    recognition_result = recognize_speech(
        separated_audio_file_paths, sample_rate_hertz, audio_channel_count, SEPARATED_AUDIO_FILE_TIME
    )
    shutil.rmtree(tmp_dir)

    srt_file_path = create_srt_file_path(source_audio_file_path, current_dir)
    write(recognition_result, srt_file_path)


def create_srt_file_path(audio_file_path, current_dir):
    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    srt_file_path = os.sep.join([current_dir, base_name + ".srt"])

    while os.path.isfile(srt_file_path):
        base_name += "_コピー"
        srt_file_path = os.sep.join([current_dir, base_name + ".srt"])

    return srt_file_path


if __name__ == "__main__":
    main()
