#!/usr/bin/env python3

import requests
import sys
import re
import random
import config
from getopt import GetoptError, gnu_getopt


def get_uid(user):
	if user.isnumeric(): return user

	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = 'url=' + user
	response = requests.post('http://findmyfbid.com/', headers=headers, data=data)
	return re.search(r'<code>(\d+)</code>', response.text).group(1)


def get_args(argv):
	niceargs = { 'color': '', 'user': config.user, 'thread': '' }

	try:
		opts, args = gnu_getopt(argv, 'c:u:', ['color=', 'user='])
	except GetoptError:
		raise Exception('Invalid arguments: ' + str(sys.argv))

	niceargs['thread'] = args[0]

	for opt, arg in opts:
		if opt in ('-c', '--color'):
			niceargs['color'] = arg
		elif opt in ('u', '--user'):
			niceargs['user'] = arg

	return niceargs


def main(argv):
	args = get_args(argv)

	user_id = get_uid(args['user'])
	thread_id = get_uid(args['thread'])
	color = args['color']

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
	main(sys.argv[1:])
