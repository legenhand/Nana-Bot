import requests


async def deldog(message, data):
    BASE_URL = 'https://del.dog'
    r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))
    if r.status_code == 404:
        await message.edit('Failed to reach dogbin')
        r.raise_for_status()
    res = r.json()
    if r.status_code != 200:
        await message.edit(res['message'])
        r.raise_for_status()
    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    return reply
