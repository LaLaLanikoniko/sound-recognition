from datetime import timedelta

from api_runner import execute_speech_to_text


def recognize_speech(audio_files, sample_rate_hertz, audio_channel_count, separated_audio_file_time):
    recognition_results = []
    script = ""
    last_end_time = None
    script_start_time = None
    for i, audio_file in enumerate(audio_files):
        response = execute_speech_to_text(
            audio_file, sample_rate_hertz, audio_channel_count
        )
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            alternative = result.alternatives[0]
            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}".format(alternative.confidence))

            for word_info in alternative.words:
                word = word_info.word
                if "|" in word:
                    word = word.split("|")[0]

                start_time_offset = word_info.start_time
                end_time_offset = word_info.end_time
                delta = timedelta(seconds=i * separated_audio_file_time)
                start_time = start_time_offset + delta
                end_time = end_time_offset + delta
                if script_start_time is None:
                    script_start_time = start_time

                if need_new_script(script, start_time, last_end_time):
                    append_telop_data(
                        recognition_results, script, script_start_time, last_end_time
                    )
                    script = word
                    script_start_time = start_time
                else:
                    script += word

                last_end_time = end_time

    if script:
        append_telop_data(recognition_results, script, script_start_time, last_end_time)

    return recognition_results


def need_new_script(script, start_time, last_end_time):
    if len(script) >= 25:
        return True

    if last_end_time is not None and (
        start_time - last_end_time >= timedelta(seconds=0.2)
    ):
        return True

    return False


def append_telop_data(recognition_results, script, script_start_time, last_end_time):
    telop_data = {
        "script": script,
        "start_time": script_start_time,
        "end_time": last_end_time,
    }
    recognition_results.append(telop_data)
