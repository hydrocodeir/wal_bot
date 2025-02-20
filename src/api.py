from config import PANEL_ADDRES, SUB_ADDRES
import requests
import os
import json

panel = PANEL_ADDRES
sub = SUB_ADDRES
url = f"https://{panel}/login"
s = requests.Session()

data = {"username": os.getenv("PANEL_USER"), "password": os.getenv("PANEL_PASS")}
headers = {
    "Accept": "application/json",
}

res = s.post(url=url, json=data, headers=headers, timeout=15)


def login():
    global s
    url = f"https://{panel}/login"
    data = {"username": os.getenv("PANEL_USER"), "password": os.getenv("PANEL_PASS")}
    headers = {
        "Accept": "application/json",
    }
    res = s.post(url=url, json=data, headers=headers, timeout=15)


def check_and_renew_session(response):
    if response.status_code == 401:  # Unauthorized
        login()
        return True
    return False


class Panel_api:
    def add_user(self, c_uuid, email, bytes_value, expiry_time, sub_id, inb_id):
        try:
            add = f"https://{panel}/panel/inbound/addClient"
            settings = {
                "clients": [
                    {
                        "id": c_uuid,
                        "enable": True,
                        "flow": "",
                        "email": email,
                        "imitIp": "",
                        "totalGB": bytes_value,
                        "expiryTime": expiry_time,
                        "tgId": "",
                        "subId": sub_id,
                        "reset": "",
                    }
                ]
            }
            proces = {"id": inb_id, "settings": json.dumps(settings)}
            res2 = s.post(add, proces)
            if check_and_renew_session(res2):
                res2 = s.post(add, proces)
            if res2.status_code == 200:
                return True
            else:
                return res2.text
        except:
            return False

    def show_users(self, inb_id):
        try:
            headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
            url = f"https://{panel}/panel/api/inbounds/get/{inb_id}"
            res = s.get(url=url, headers=headers, timeout=15)
            if check_and_renew_session(res):
                res = s.get(url=url, headers=headers, timeout=15)
            return res
        except:
            return False

    def user_obj(self, email):
        try:
            url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
            get = s.get(url=url, headers=headers)
            if check_and_renew_session(get):
                get = s.get(url=url, headers=headers)
            return get
        except:
            return False

    def renew_user(self, email):
        try:
            url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
            get = s.get(url=url, headers=headers)
            if check_and_renew_session(get):
                get = s.get(url=url, headers=headers)
            return get
        except:
            return False

    def reset_traffic(self, inb_id, email):
        try:
            url = f"https://{panel}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
            response = s.post(url=url, headers=headers)
            if check_and_renew_session(response):
                response = s.post(url=url, headers=headers)
            return response
        except:
            return False

    def get_inbound(self, inb_id):
        try:
            url = f"https://{panel}/panel/api/inbounds/get/{inb_id}"
            response = s.get(url=url, headers=headers)
            if check_and_renew_session(response):
                response = s.get(url=url, headers=headers)
            return response
        except:
            return False

    def update_email(self, id, proces):
        try:
            url = f"https://{panel}/panel/api/inbounds/updateClient/{id}"
            res = s.post(url=url, headers=headers, data=proces)
            if check_and_renew_session(res):
                res = s.post(url=url, headers=headers, data=proces)
            return res
        except:
            return False

    def delete_user(self, inb_id, user_id):
        try:
            url = f"https://{panel}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
            response = s.post(url=url, headers=headers)
            if check_and_renew_session(response):
                response = s.post(url=url, headers=headers)
            return response
        except:
            return False
