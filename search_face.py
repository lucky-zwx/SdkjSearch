import requests
import json


API_Key = 'U7f3DErGN6QHwIdpniNSdwxR'
Secret_Key = 'caWVapY3bVncjqGo8angbbp2U9EANXyC'
AppID = '15145395'


def searchface(token, pic_data):
    host = 'https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=' + token
    data = {'image_type': 'BASE64', 'group_id_list': '1', 'image': pic_data, 'max_user_num': 5}
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
              'Content-Type': 'application/json'}
    rq = requests.post(url=host, data=data, headers=header)
    rq.encoding = 'UTF-8'
    dictinfo = json.loads(rq.text)
    if dictinfo['error_code'] == 0:
        # return dictinfo['result']['user_list'][0]['user_info']
        return dictinfo['result']['user_list']
