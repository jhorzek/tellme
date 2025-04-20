from tellme.AI_Podcast.create_podcast_audio import create_podcast_audio_edge
from tellme.AI_Podcast.create_podcast_transcript import create_podcast_transcript
from tellme.AI_Podcast.podcast_setups import Sofia_Mark
from tellme.Articles.get_wiki_article import get_wiki_article


async def location_to_podcast(
    attraction_name, Chat, model_name, api_key, voice_instructions=Sofia_Mark
):
    art = get_wiki_article(article_title=attraction_name)

    if (api_key is not None) and (api_key != ''):
        pod_transcript = create_podcast_transcript(
            system_prompt=voice_instructions,
            Chat=Chat,
            model=model_name,
            wiki_article=art,
            api_key=api_key,
        )
    else:
        pod_transcript = create_podcast_transcript(
            system_prompt=voice_instructions,
            Chat=Chat,
            model=model_name,
            wiki_article=art,
        )

    await create_podcast_audio_edge(
        transcript=pod_transcript,
        output_file=f'{attraction_name}.mp3',
        output_folder='data',
        voices={'Mark': 'en-US-RogerNeural', 'Sofia': 'en-GB-SoniaNeural'},
    )

    return f'data/{attraction_name}.mp3'
