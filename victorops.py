import os
import requests


vo_api_id = os.environ['VICTOROPS_API_ID']
vo_api_key = os.environ['VICTOROPS_API_KEY']
vo_team = os.environ['VICTOROPS_TEAM']

headers = {'X-VO-Api-Id': vo_api_id, 'X-VO-Api-Key': vo_api_key}


def schedule():
    vo_url = "https://api.victorops.com/api-public/v2/team/" + vo_team + "/oncall/schedule?daysForward=8"
    r = requests.get(vo_url, headers=headers)
    json_data = r.json()

    current_ba = json_data['schedules'][0]['schedule'][0]['rolls'][0]['onCallUser']['username']
    next_ba = json_data['schedules'][0]['schedule'][0]['rolls'][5]['onCallUser']['username']
    current_mv = json_data['schedules'][0]['schedule'][1]['rolls'][0]['onCallUser']['username']
    next_mv = json_data['schedules'][0]['schedule'][1]['rolls'][5]['onCallUser']['username']

    message = f"This week's oncall duties are covered by `{current_ba}` and `{current_mv}`. Next week are `{next_ba}` and `{next_mv}` turns."

    return message
