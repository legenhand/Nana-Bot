import requests


async def deldog(message, data):
    r = requests.post('https://del.dog/documents', data=data.encode('utf-8'))
    if r.status_code == 404:
        await message.edit('Failed to reach dog.del')
        r.raise_for_status()
    res = r.json()
    if r.status_code != 200:
        await message.edit(res['message'])
        r.raise_for_status()
    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL: https://del.dog/{key}\nView stats, etc. [here](https://del.dog/v/{key})'
    else:
        reply = f'https://del.dog/{key}'
    return reply
