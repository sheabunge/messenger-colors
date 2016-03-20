#!/usr/bin/env python3

import argparse
import requests
import re
import random
import config


def get_uid(user):
	if user.isnumeric(): return user

	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = 'url=' + user
	response = requests.post('http://findmyfbid.com/', headers=headers, data=data)
	return re.search(r'<code>(\d+)</code>', response.text).group(1)


def get_args():
	parser = argparse.ArgumentParser(description='Sets the color of a Facebook Messenger chat thread')
	parser.add_argument('thread', help='username or ID of the chat thread')

	parser.add_argument(
		'--user', '-u',
		dest='user',
		default=config.user,
		required=False,
		help='username or ID of the user used to set the color'
	)

	parser.add_argument(
		'--color', '-c',
		dest='color',
		required=True,
		help='new color of the thread, in hex form'
	)

	return parser.parse_args()


def main():
	args = get_args()

	user_id = get_uid(args.user)
	thread_id = get_uid(args.thread)
	color = args.color

	print('user id:', user_id)
	print('thread id:', thread_id)
	print('color:', color)

	headers = {
		'origin': 'https://www.messenger.com',
		'accept-encoding': 'gzip, deflate',
		'content-type': 'application/x-www-form-urlencoded',
		'accept': '*/*',
		'referer': 'https://www.messenger.com',
		'authority': 'www.messenger.com',
		'cookie': config.cookie,
	}

	timestamp = random.randint(0, 10**60 - 1)

	data = 'color_choice={0}&thread_or_other_fbid={1}&__user={2}&__a=1' \
		'&__dyn=7AzkXh8Z38ogDxKy1l0BwRyaF3oyfJLFwXBxG3F6xybxu13wCGGwPBxZi28cWwADKuEjxa2y7E4i3K5VqCzEb8uzUixu' \
		'&__req=1t&fb_dtsg=AQFImQcwz2ZB%3AAQF78ivRPO5b&ttstamp={3}&__rev=2239045'
	data = data.format(requests.utils.quote(color), thread_id, user_id, timestamp)

	request_url = 'https://www.messenger.com/messaging/save_thread_color/?source=thread_settings'
	response = requests.post(request_url, headers=headers, data=data)

	print()
	print(response.text)


if __name__ == '__main__':
	main()
