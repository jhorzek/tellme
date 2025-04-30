"""Generate a podcast based on the transcript using edge tts."""

import os
import uuid

import edge_tts
import ffmpeg
from openai import OpenAI


async def create_audio_segment_edge(utterance: str, voice: str, file_name: str) -> None:
    """Create a segment of a podcast with edge tts.

    Args:
        utterance (str): The text that the voice should read.
        voice (str): The voice used.
        file_name (str): The name of the file where the result should be saved.
    """
    voiced_utterance = edge_tts.Communicate(text=utterance, voice=voice)
    await voiced_utterance.save(file_name)


async def create_audio_segments_openai(
    api_key: str,
    file_names: list[str],
    transcript: list[dict[str, str]],
    speech_model: str,
    voices: dict[str, str],
) -> None:
    """Create the audio for the segments of the podcast with OpenAI.

    Args:
        api_key (str): API key for OpenAI
        file_names (list[str]): Names of the files where the audio should be saved
        transcript (list[dict[str, str]]): The transcript of the podcast
        speech_model (str): Name of the speech model from OpenAI to use
        voices (dict[str, str]): voices from OpenAI to use
    """
    openai = OpenAI(api_key=api_key)
    for i, utter in enumerate(transcript):
        if (utter.get('speaker') is not None) and (utter.get('utterance') is not None):
            with openai.audio.speech.with_streaming_response.create(
                model=speech_model,
                voice=voices[utter.get('speaker')],
                input=utter.get('utterance'),
            ) as response:
                response.stream_to_file(file_names[i])


async def create_podcast_audio_openai(
    transcript: list[dict[str, str]],
    voices: dict[str, str],
    output_file: str,
    output_folder: str,
    speech_model: str,
    api_key: str,
) -> str:
    """Generate a podcast using OpenAI tts.

    Based on a transcript, this function generates an mp3 file of the podcast using
    edge tts. edge tts is free, but of lower quality than alternatives.

    Args:
        transcript (list[dict[str, str]]): The transcript of the podcast. This is created with
            create_podcast_transcript
        voices (dict[str, str]): A dict with voices for each speaker in the podcast.
            Example: If the speakers are named Mark and Sara, we have to specify
            voices as {"Mark": "en-US-RogerNeural", "Sara": "en-GB-SoniaNeural"}.
            See edge-tts --list-voices for a list of all voices.
        output_file (str): Name of the file where the podcast should be saved.
            Must end in .mp3
        output_folder (str): Name of the folder where the podcast should be saved.
        speech_model (str): Nane if the speech model from OpenAI
        api_key (str): api key for OpenAI

    Raises:
        ValueError: Error if one of the speakers has no defined voice.

    Returns:
        str: location of the podcast
    """
    # Check that a voice was defined for each host:
    for utter in transcript:
        if not any([utter['speaker'] == x for x in list(voices.keys())]):
            raise ValueError(
                'Each host must be given a voice. Found no voice for '
                + utter['speaker']
                + '.'
            )
    if not output_file.endswith('.mp3'):
        raise ValueError('output_file must end with .mp3.')

    os.makedirs(output_folder, exist_ok=True)

    # we need to iterate over each of our utterances in the transcript and generate
    # the audio.
    audio_files = [
        os.path.join(output_folder, 'pod_' + uuid.uuid4().hex + '.mp3')
        for utter in transcript
    ]
    print('Generating audio')
    await create_audio_segments_openai(
        api_key=api_key,
        file_names=audio_files,
        transcript=transcript,
        speech_model=speech_model,
        voices=voices,
    )
    print('Done generating audio')
    # After creating the individual segments, we want to combine them.
    ffmpeg_input = []
    for file in audio_files:
        ffmpeg_input.append(ffmpeg.input(file))
    ffmpeg.concat(*ffmpeg_input, v=0, a=1).output(
        os.path.join(output_folder, output_file)
    ).run(overwrite_output=True)
    return output_file


async def create_podcast_audio_edge(
    transcript: list[dict[str, str]],
    voices: dict[str, str],
    output_file: str,
    output_folder: str,
) -> str:
    """Generate a podcast using edge tts.

    Based on a transcript, this function generates an mp3 file of the podcast using
    edge tts. edge tts is free, but of lower quality than alternatives.

    Args:
        transcript (list[dict[str, str]]): The transcript of the podcast. This is created with
            create_podcast_transcript
        voices (dict[str, str]): A dict with voices for each speaker in the podcast.
            Example: If the speakers are named Mark and Sara, we have to specify
            voices as {"Mark": "en-US-RogerNeural", "Sara": "en-GB-SoniaNeural"}.
            See edge-tts --list-voices for a list of all voices.
        output_file (str): Name of the file where the podcast should be saved.
            Must end in .mp3
        output_folder (str): Name of the folder where the podcast should be saved.

    Raises:
        ValueError: Error if one of the speakers has no defined voice.

    Returns:
        str: location of the podcast
    """
    # Check that a voice was defined for each host:
    for utter in transcript:
        if not any([utter['speaker'] == x for x in list(voices.keys())]):
            raise ValueError(
                'Each host must be given a voice. Found no voice for '
                + utter['speaker']
                + '.'
            )
    if not output_file.endswith('.mp3'):
        raise ValueError('output_file must end with .mp3.')

    os.makedirs(output_folder, exist_ok=True)

    # we need to iterate over each of our utterances in the transcript and generate
    # the audio.
    audio_files = []
    for utter in transcript:
        # generate a unique id for the audio file
        file_name = os.path.join(output_folder, 'pod_' + uuid.uuid4().hex + '.mp3')
        await create_audio_segment_edge(
            utterance=utter['utterance'],
            voice=voices[utter['speaker']],
            file_name=file_name,
        )
        audio_files.append(file_name)

    # After creating the individual segments, we want to combine them.
    ffmpeg_input = []
    for file in audio_files:
        ffmpeg_input.append(ffmpeg.input(file))
    ffmpeg.concat(*ffmpeg_input, v=0, a=1).output(
        os.path.join(output_folder, output_file)
    ).run(overwrite_output=True)
    return output_file
