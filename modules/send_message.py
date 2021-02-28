import os
import requests
import configparser

config = configparser.ConfigParser()
print(os.path.dirname(os.path.dirname(__file__)))
config.read(os.path.dirname(os.path.dirname(__file__)) + '\\config.ini', encoding='GB18030')

def send_message(msg,qq_id,qq_type):
	if qq_type == "private":
		data = {
			'user_id':qq_id,
			'message':msg,
			'auto_escape':False
		}
		cq_url = config.get('network','SEND_ADDRESS') + "send_private_msg"
		rev = requests.post(cq_url,data=data)
	elif qq_type == "group":
		data = {
			'group_id':qq_id,
			'message':msg,
			'auto_escape':False
		}
		cq_url = config.get('network','SEND_ADDRESS') + "send_group_msg"
		rev = requests.post(cq_url,data=data)
	else:
		return False
	if rev.json()['status'] == 'ok':
		return True
	return False