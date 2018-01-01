import requests
import json


def send_notification(pushbullet_token, title, message):
    if pushbullet_token:
        payload = {"type": "note", "title": title, "body": message}
        r = requests.post('https://api.pushbullet.com/v2/pushes',
                          data=json.dumps(payload),
                          headers={'Authorization': 'Bearer ' + pushbullet_token,
                                   'Content-Type': 'application/json'})
        if r.status_code != 200:
          print 'ERROR: Unable to send pushbullet (status code: {0} | error: {1})'.format(r.status_code, r)