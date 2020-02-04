import requests

def deldog(data):
	BASE_URL = 'https://del.dog'
	r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))
	if r.status_code == 404:
		update.effective_message.reply_text('Failed to reach dogbin')
		r.raise_for_status()
	res = r.json()
	if r.status_code != 200:
		update.effective_message.reply_text(res['message'])
		r.raise_for_status()
	key = res['key']
	if res['isUrl']:
		reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
	else:
		reply = f'{BASE_URL}/{key}'
	return reply
