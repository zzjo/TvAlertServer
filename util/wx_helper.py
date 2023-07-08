import json

import requests


class WxHelper(object):
    def __init__(self):
        self.corpid = "ww0c99805eae0a4591"
        self.corpsecret = "i8pEY7_mDrtpyWnLsu8EvCHWHRmiKP4lxOC0kcgMf0s"

    @property
    def get_access_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
        resp = requests.get(url)
        assert resp.status_code == 200
        return resp.json()['access_token']

    def post_file_to_wechat_get_media_id(self, filepath, filename, type='file'):
        from requests_toolbelt import MultipartEncoder

        post_file_url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.get_access_token}&type={type}"

        m = MultipartEncoder(
            fields={filename: (filename, open(filepath, 'rb'), 'text/plain')},
        )
        r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type})
        return r.json()['media_id']

    def send_media(self, media_id):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_access_token}"
        params = {
            "touser": "@all",
            "msgtype": "file",
            "agentid": 1000002,
            "file": {'media_id': media_id}
        }
        ret = requests.post(url, json=params)
        ret = ret.json()
        print(ret)

    def send(self, msg):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_access_token}"
        params = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {'content': msg}
        }
        ret = requests.post(url, json=params)
        ret = ret.json()
        print(ret)

    def robot_send(self, msg, webhook):
        params = {
            "msgtype": "text",
            "text": {
                "content": msg
            }
        }
        requests.post(webhook, json=params)
