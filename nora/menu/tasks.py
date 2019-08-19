from nora.celery import app
import requests
import os
from datetime import datetime
from nora.settings import SLACK_CHANNEL, SLACK_TOKEN

@app.task(bind=True, name='send_menu')
def send_menu(self, message):
    
    response = requests.post('https://slack.com/api/chat.postMessage', params={
        "token": SLACK_TOKEN,
        "channel": SLACK_CHANNEL,
        "text": message
    })

    path = './data'
    if response.ok:
        if not os.path.exists(path):
            os.makedirs(path)
        slug = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')
        with open(os.path.join(path, slug), 'w') as f:
            f.write(response.text)
    else:
        raise ValueError('Unexpected response') 


