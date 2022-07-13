import requests
import json
from dotenv import load_dotenv
import os
import datetime
import sys

import tweepy

load_dotenv()

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

def main(): 
    arg_service_type = sys.argv[1]
    API_ROOT_URL = os.getenv('API_ROOT_URL')
    OPEN_METEO_URL = os.getenv('OPEN_METEO_URL')

    try:
        plants = requests.get(API_ROOT_URL + "plants/").json()
        for plant in plants:
            settings = requests.get(API_ROOT_URL + "notification_settings/", {'plant_id': plant['id']}).json()
            for setting in settings:
                
                # not enabled -> skip
                if setting['service_type'] != arg_service_type: continue
                if setting['enabled'] == False: continue

                service_type = setting['service_type']
                
                # get a latest notification
                notification = requests.get(
                    API_ROOT_URL + "notifications/latest-one", 
                    {
                        'plant_id': plant['id'], 
                        'service_type': service_type
                    }).json()
                if not notification or notification['notified_to_service'] == True: continue

                # get authentication info to call external api
                if service_type == 'TYPETALK':
                    url = setting['api_url']
                    headers = { 'X-TYPETALK-TOKEN': setting['access_token']}
                elif service_type == 'TWITTER':
                    consumer_key =setting['consumer_key']
                    consumer_secret =setting['consumer_secret']
                    access_token=setting['access_token']
                    access_token_secret =setting['access_secret']
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(access_token, access_token_secret)

                    api = tweepy.API(auth)
                else:
                    print("error")

                # create hashtag
                plant_name = plant['name']
                tag_name = f'{plant_name}の観察日記'
                hash_tag_title = f'#{tag_name}'
                hash_tag_site = '#Piと俺とエバーガーデン'
                
                # In the case of TYPETALK, need to create tag
                if service_type == 'TYPETALK':
                    # the tag already exist?
                    tags_json = requests.get(url + '/talks', headers = headers).json()
                    found = next((tag for tag in tags_json['talks'] if tag['name'] == tag_name), None)

                    if found :
                        tag_id = found['id'] 
                    else:
                        tag_data_param = {
                        'talkName': tag_name
                        }
                        res_tag_post = requests.post(url + '/talks', json = tag_data_param, headers = headers).json()
                        tag_id = res_tag_post['talk']['id']
                
                # snapshot
                if notification['snapshot_id']:
                    snapshot = requests.get(API_ROOT_URL + 'snapshots/' + str(notification['snapshot_id'])).json()

                    # upload image file and get key
                    path = '/backend/uploads/' + snapshot['image_file']
                    if service_type == 'TYPETALK':
                        file = {'file': open(path, 'rb')}
                        res_post_attachment = requests.post(url + '/attachments', files=file, headers = headers)
                        res_post_attachment_json = res_post_attachment.json()
                        fileKey = res_post_attachment_json["fileKey"]
                    elif service_type == 'TWITTER':
                        media = api.media_upload(path)
                        media_ids = [media.media_id]
                    
                    # create message
                    ## date info
                    d_week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水','Thu': '木', 'Fri': '金', 'Sat': '土'}
                    key = now.strftime('%a')
                    w = d_week[key]
                    time_message = now.strftime('%Y/%m/%d') + f'({w}) ' + " " + now.strftime('%H:%M')

                    ## weather info
                    res_weather_api = requests.get(OPEN_METEO_URL).json()
                    current_temperature = res_weather_api['current_weather']['temperature']
                    current_weather_status = res_weather_api['current_weather']['weathercode']
                    
                    if service_type == 'TYPETALK':
                        emoji = get_emoji_for_typetalk(current_weather_status)
                    elif service_type == 'TWITTER':
                        emoji = get_emoji_for_twitter(current_weather_status)
                    
                    weather_message = f'天気：{emoji}、気温：{current_temperature}度'

                    if service_type == 'TYPETALK':
                        message = time_message + '\n' + weather_message
                    elif service_type == 'TWITTER':
                        message = time_message + '\n' + weather_message + '\n\n' + hash_tag_title + '\n' + hash_tag_site
                    
                    #send message
                    if service_type == 'TYPETALK':
                        data = {
                        'message': message,
                        'fileKeys[0]': fileKey,
                        'talkIds[0]' : tag_id
                        }
                        res_typtalk = requests.post(url, json = data, headers = headers)
                    elif service_type == 'TWITTER':
                        status = api.update_status(status=message, media_ids=media_ids)
                else:
                    if service_type == 'TYPETALK':
                        message = notification['message']
                        data = { 'message': message }
                        res_typtalk = requests.post(url, json = data, headers = headers)
                    elif service_type == 'TWITTER':
                        status = api.update_status(message)

                # check result
                if service_type == 'TYPETALK':
                    if res_typtalk.status_code != 200: continue
                elif service_type == 'TWITTER':
                    if status is None: continue 

                # notification_update
                json_data = {
                    'notification_update': {
                        'plant_id': plant['id'], 
                        'service_type': 'TYPETALK',
                        'notified_to_service': 'true'
                    }
                }
                res = requests.post(API_ROOT_URL + 'notifications/executed', json.dumps(json_data)) 
                if res.status_code != 200:
                    raise Exception("failed to notification_update ")
                
    except Exception as e:
        print(e)

def get_emoji_for_typetalk(code):
        if code == 0:
            return " :sunny: "
        elif code == 1:
            return " :mostly_sunny: "
        elif code == 2:
            return " :partly_sunny: "
        elif code == 3:
            return " :cloud: "
        elif code == 45 or code == 48:
            return " :fog: "
        elif code == 51 or code == 53 or code == 55:
            return " :rain_cloud: "
        elif code == 56 or code == 53 or code == 66 or code == 67:
            return " :snow_cloud: "
        elif code == 61:
            return " :closed_umbrella: "
        elif code == 63:
            return " :umbrella: "
        elif code == 65:
            return " :umbrella_with_rain_drops: "
        elif code == 71 or code == 73:
            return " :snow_cloud: "
        elif code == 75 or code == 77:
            return " :snowman_without_snow: "
        elif code == 80 or code == 81 or code == 82:
            return " :ocean: "
        elif code == 85 or code == 86:
            return " :snowflake: "
        elif code == 96 or code == 99:
            return " :zap: "
        else:
            return " :t-rex: "

def get_emoji_for_twitter(code):
        if code == 0:
            return " ☀ "
        elif code == 1:
            return " 🌤️ "
        elif code == 2:
            return " 🌥️ "
        elif code == 3:
            return " ☁ "
        elif code == 45 or code == 48:
            return " 🌫️ "
        elif code == 51 or code == 53 or code == 55:
            return " 🌧️ "
        elif code == 56 or code == 53 or code == 66 or code == 67:
            return " 🌨️ "
        elif code == 61:
            return " 🌂 "
        elif code == 63:
            return " ☂ "
        elif code == 65:
            return " ☔ "
        elif code == 71 or code == 73:
            return " 🌨️ "
        elif code == 75 or code == 77:
            return " ⛄ "
        elif code == 80 or code == 81 or code == 82:
            return " 🌊 "
        elif code == 85 or code == 86:
            return " ❄ "
        elif code == 96 or code == 99:
            return " ⚡ "
        else:
            return " 🪐 "

if __name__ == '__main__':
    main()