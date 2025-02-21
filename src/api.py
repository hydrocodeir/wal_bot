from config import PANEL_ADDRES, SUB_ADDRES
import requests
import os
import json
from functools import wraps

class PanelAPI:
    def __init__(self):
        self.panel = PANEL_ADDRES
        self.session = requests.Session()
        self.headers = {"Accept": "application/json"}
        self.login()

    def login(self):
        url = f"https://{self.panel}/login"
        data = {"username": os.getenv("PANEL_USER"), "password": os.getenv("PANEL_PASS")}
        response = self.session.post(url, json=data, headers=self.headers, timeout=15)
        if response.status_code == 200:
            token = response.json().get("token")
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            raise Exception("Login failed! Check credentials.")

    def ensure_logged_in(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if response.status_code == 401:
                self.login()
                response = func(self, *args, **kwargs)
            return response
        return wrapper

    @ensure_logged_in
    def add_user(self, c_uuid, email, bytes_value, expiry_time, sub_id, inb_id):
        url = f"https://{self.panel}/panel/inbound/addClient"
        settings = {
            "clients": [{
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
            }]
        }
        data = {"id": inb_id, "settings": json.dumps(settings)}
        return self.session.post(url, json=data)

    @ensure_logged_in
    def show_users(self, inb_id):
        url = f"https://{self.panel}/panel/api/inbounds/get/{inb_id}"
        return self.session.get(url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})

    @ensure_logged_in
    def user_obj(self, email):
        url = f"https://{self.panel}/panel/api/inbounds/getClientTraffics/{email}"
        return self.session.get(url)

    @ensure_logged_in
    def renew_user(self, email):
        url = f"https://{self.panel}/panel/api/inbounds/getClientTraffics/{email}"
        return self.session.get(url)

    @ensure_logged_in
    def reset_traffic(self, inb_id, email):
        url = f"https://{self.panel}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
        return self.session.post(url)

    @ensure_logged_in
    def get_inbound(self, inb_id):
        url = f"https://{self.panel}/panel/api/inbounds/get/{inb_id}"
        return self.session.get(url)

    @ensure_logged_in
    def update_email(self, user_id, data):
        url = f"https://{self.panel}/panel/api/inbounds/updateClient/{user_id}"
        return self.session.post(url, json=data)

    @ensure_logged_in
    def delete_user(self, inb_id, user_id):
        url = f"https://{self.panel}/panel/api/inbounds/{inb_id}/delClient/{user_id}"
        return self.session.post(url)
