from urllib import request

import requests

API_Key = 'U7f3DErGN6QHwIdpniNSdwxR'
Secret_Key = 'caWVapY3bVncjqGo8angbbp2U9EANXyC'
AppID = '15145395'


def get_token():
    client_id = API_Key
    client_secret = Secret_Key
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        client_id, client_secret)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    try:
        response = request.urlopen(req)
        # 获得请求结果
        content = response.read()
        # 结果转化为字符
        content = bytes.decode(content)
        # 转化为字典
        content = eval(content[:-1])
        return content['access_token']
    except Exception:
        return False


def upload_pic(token, pic_data, filename):
    uid = filename[:12]
    print(pic_data)
    host = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token='+token
    data = {'image_type': 'BASE64', 'user_id': uid, 'group_id': '1', 'image': pic_data, 'user_info': filename.split('.')[0], 'action_type': 'replace'}
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                     'Content-Type': 'application/json'}
    rq = requests.post(url=host, data=data, headers=header)
    rq.encoding = 'UTF-8'
    print(rq.text)


def imgdata(file1path):
    import base64
    f = open(file1path, 'rb')
    pic1 = base64.b64encode(f.read())
    s = pic1.decode()
    f.close()
    return s