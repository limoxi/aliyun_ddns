# coding: utf-8

import json
import os
import sys
import time

import requests

from aliyun_api import update_yun

LOCAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ip.txt')
IP_URLS = {
	'4': 'https://ipv4.lookup.test-ipv6.com/?_t={}',
	'6': 'https://ipv6.lookup.test-ipv6.com/?_t={}'
}

def get_curr_ip(ip_type):
	headers = {
		'content-type': 'text/html',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
	}
	url = IP_URLS[ip_type].format(int(time.time()))
	resp = requests.get(url, headers=headers, timeout=30)

	return str(resp.json().get('ip'))

def get_lastest_local_ip():
	"""
	获取最近一次保存在本地的ip
	"""
	try:
		with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
			return json.loads(f.read())
	except (OSError, ValueError) as e:
		print(e)
		return {}

def get_ip_types():
	"""
	获取命令行传入的ip类型参数，4代表ipv4，6代表ipv6，不传默认两者都更新
	"""
	ip_types = sys.argv[1:] or ['4', '6']
	invalid_types = [t for t in ip_types if t not in IP_URLS]
	if invalid_types:
		print('invalid argument: {}'.format(' '.join(invalid_types)))
		print('usage: python aliyun_ddns.py [4] [6]')
		sys.exit(1)

	return sorted(set(ip_types))

if __name__ == '__main__':
	ip_types = get_ip_types()
	last_ip_data = get_lastest_local_ip()
	ip_data = dict(last_ip_data)
	need_write = False
	for ip_type in ip_types:
		key = 'v' + ip_type
		curr_ip = get_curr_ip(ip_type)
		print('ipv{}: {}'.format(ip_type, curr_ip))
		if curr_ip != last_ip_data.get(key, ''):
			update_yun(**{'ipv' + ip_type: curr_ip})
			ip_data[key] = curr_ip
			need_write = True

	if need_write:
		print('save ip to {}...'.format(LOCAL_FILE))
		with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
			f.write(json.dumps(ip_data))
