from __future__ import print_function
from botocore.vendored import requests
import json
import os


def lambda_handler(event, context):
    webhook_url = 'https://hooks.slack.com'+ str(os.environ['slack_path'])
    snsSubject = event['Records'][0]['Sns']['Subject'] 
    
    slack_data = {
        "channel": "#Alert-aws-fastgo",
        "username": "Fastgo - 4114",
        "text": "*" + snsSubject + "*",
    }
    
    message_data =  event['Records'][0]['Sns']['Message'] 
    message_json =  json.loads(message_data)
    message = ''
    for k, v in message_json.items():
        
        if k == 'Trigger':
            for kt, vt in v.items():
                message += "*" + str(kt) + "*: " + str(vt) +"\n"
        else:
            message += "*" + str(k) + "*: " + str(v) +"\n"

    if 'ALARM' in snsSubject:
        severity = 'danger'
        icon_emoji = ':fire:'
    else:
        severity = 'good'
        icon_emoji = ':ok_hand:'
        
    slack_data['icon_emoji'] = icon_emoji
    slack_data['attachments'] = [{'color': severity, 'text': message}]
    response = requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
    
    return message
