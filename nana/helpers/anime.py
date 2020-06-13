import textwrap
import jikanpy
import requests


def getPosterLink(mal):
    # grab poster from kitsu
    kitsu = getKitsu(mal)
    image = requests.get(f'https://kitsu.io/api/edge/anime/{kitsu}').json()
    return image['data']['attributes']['posterImage']['original']


def getKitsu(mal):
    # get kitsu id from mal id
    link = f'https://kitsu.io/api/edge/mappings?filter[external_site]=myanimelist/anime&filter[external_id]={mal}'
    result = requests.get(link).json()['data'][0]['id']
    link = f'https://kitsu.io/api/edge/mappings/{result}/item?fields[anime]=slug'
    kitsu = requests.get(link).json()['data']['id']
    return kitsu


def getBannerLink(mal, kitsu_search=True):
    # try getting kitsu backdrop
    if kitsu_search:
        kitsu = getKitsu(mal)
        image = f'http://media.kitsu.io/anime/cover_images/{kitsu}/original.jpg'
        response = requests.get(image)
        if response.status_code == 200:
            return image
    # try getting anilist banner
    query = """
    query ($idMal: Int){
        Media(idMal: $idMal){
            bannerImage
        }
    }
    """
    data = {'query': query, 'variables': {'idMal': int(mal)}}
    image = requests.post('https://graphql.anilist.co', json=data).json()['data']['Media']['bannerImage']
    if image:
        return image
    return getPosterLink(mal)


def get_anime_manga(mal_id, search_type, _user_id):
    jikan = jikanpy.jikan.Jikan()
    if search_type == "anime_anime":
        result = jikan.anime(mal_id)
        image = getBannerLink(mal_id)
        studio_string = ', '.join(studio_info['name'] for studio_info in result['studios'])
        producer_string = ', '.join(producer_info['name'] for producer_info in result['producers'])
    elif search_type == "anime_manga":
        result = jikan.manga(mal_id)
        image = result['image_url']
    caption = f"<a href=\'{result['url']}\'>{result['title']}</a>"
    if result['title_japanese']:
        caption += f" ({result['title_japanese']})\n"
    else:
        caption += "\n"
    alternative_names = []
    if result['title_english'] is not None:
        alternative_names.append(result['title_english'])
    alternative_names.extend(result['title_synonyms'])
    if alternative_names:
        alternative_names_string = ", ".join(alternative_names)
        caption += f"\n<b>Also known as</b>: <code>{alternative_names_string}</code>"
    genre_string = ', '.join(genre_info['name'] for genre_info in result['genres'])
    if result['synopsis'] is not None:
        synopsis = result['synopsis'].split(" ", 60)
        try:
            synopsis.pop(60)
        except IndexError:
            pass
        synopsis_string = ' '.join(synopsis) + "..."
    else:
        synopsis_string = "Unknown"
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    if search_type == "anime_anime":
        caption += textwrap.dedent(f"""
        <b>Type</b>: <code>{result['type']}</code>
        <b>Status</b>: <code>{result['status']}</code>
        <b>Aired</b>: <code>{result['aired']['string']}</code>
        <b>Episodes</b>: <code>{result['episodes']}</code>
        <b>Score</b>: <code>{result['score']}</code>
        <b>Premiered</b>: <code>{result['premiered']}</code>
        <b>Duration</b>: <code>{result['duration']}</code>
        <b>Genres</b>: <code>{genre_string}</code>
        <b>Studios</b>: <code>{studio_string}</code>
        <b>Producers</b>: <code>{producer_string}</code>
        📖 <b>Synopsis</b>: {synopsis_string} <a href='{result['url']}'>read more</a>
        <i>Search an encode on..</i>
        """)
    elif search_type == "anime_manga":
        caption += textwrap.dedent(f"""
        <b>Type</b>: <code>{result['type']}</code>
        <b>Status</b>: <code>{result['status']}</code>
        <b>Volumes</b>: <code>{result['volumes']}</code>
        <b>Chapters</b>: <code>{result['chapters']}</code>
        <b>Score</b>: <code>{result['score']}</code>
        <b>Genres</b>: <code>{genre_string}</code>
        📖 <b>Synopsis</b>: {synopsis_string}
        """)
    return caption, image