# coding: utf-8

import os
import json
import requests
import time

from aliyun_api import update_yun

LOCAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ip.txt')

def get_curr_ip():
	headers = {
		'content-type': 'text/html',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
	}
	resp_v4 = requests.get('https://ipv4.ipw.cn/api/ip/&_t={}'.format(int(time.time()), headers=headers))
	resp_v6 = requests.get('https://ipv6.ipw.cn/api/ipv6/&_t={}'.format(int(time.time()), headers=headers))

	return {
		'v4': resp_v4.content,
		'v6': resp_v6.content
	}

def get_lastest_local_ip():
	"""
	获取最近一次保存在本地的ip
	"""
	with open(LOCAL_FILE, 'r') as f:
		data = f.read()
		try:
			return json.loads(data)
		except Exception as e:
			print(e.message)
			return {}

if __name__ == '__main__':
	ip_data = get_curr_ip()
	print(ip_data)
	last_ip_data = get_lastest_local_ip()
	need_write = False
	if ip_data.get('v4', '') != last_ip_data.get('v4', ''):
		need_write = True
		update_yun(ipv4=ip_data['v4'])

	if ip_data.get('v6', '') != last_ip_data.get('v6', ''):
		need_write = True
		update_yun(ipv6=ip_data['v6'])

	if need_write:
		print('save ip to {}...'.format(LOCAL_FILE))
		with open(LOCAL_FILE, 'wb') as f:
			f.write(json.dumps(ip_data))