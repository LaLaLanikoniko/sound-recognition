import io

from google.cloud import speech


def execute_speech_to_text(audio_file_path, sample_rate_hertz, audio_channel_count):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        audio_channel_count=audio_channel_count,
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code="ja-JP",
        enable_word_time_offsets=True,
    )

    return client.recognize(config=config, audio=audio)
