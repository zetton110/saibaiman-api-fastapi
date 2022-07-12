import requests
import json
from dotenv import load_dotenv
import os
import tweepy
import datetime

load_dotenv()

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

def main():

    API_URL = "http://localhost:8000/api/"
    OPEN_METEO_URL = os.getenv('OPEN_METEO_URL')

    try:
        plants = requests.get(API_URL + "plants/").json()
        for plant in plants:
            settings = requests.get(API_URL + "notification_settings/", {'plant_id': plant['id']}).json()
            for setting in settings:
                if setting['service_type'] != 'TWITTER': continue
                if setting['enabled'] == False: continue

                notification = requests.get(
                    API_URL + "notifications/latest-one", 
                    {
                        'plant_id': plant['id'], 
                        'service_type': 'TWITTER'
                    }).json()
                
                if not notification: continue
                if notification['notified_to_service'] == True: continue

                message = notification['message']

                consumer_key =setting['consumer_key']
                consumer_secret =setting['consumer_secret']
                access_token=setting['access_token']
                access_token_secret =setting['access_secret']

                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)

                api = tweepy.API(auth)


                print(notification['snapshot_id'])

                if notification['snapshot_id']:
                    snapshot = requests.get(API_URL + 'snapshots/' + str(notification['snapshot_id'])).json()
                    print(snapshot)
                    path = '../uploads/' + snapshot['image_file']


                    res_weather_api = requests.get(OPEN_METEO_URL).json()
                    current_temperature = res_weather_api['current_weather']['temperature']
                    current_weather_status = res_weather_api['current_weather']['weathercode']
                    d_week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水','Thu': '木', 'Fri': '金', 'Sat': '土'}
                    key = now.strftime('%a')
                    w = d_week[key]
                    time_message = now.strftime('%Y/%m/%d') + f'({w}) ' + " " + now.strftime('%H:%M')
                    weather_message = f'天気：{getEmojiStr(current_weather_status)}、気温：{current_temperature}度'
                    message = time_message + '\n' + weather_message

                    media = api.media_upload(path)
                    status = api.update_status(status=message, media_ids=[media.media_id])
                else:
                    status = api.update_status(message)

                
                print(status)

                if status:
                    json_data = {
                        'notification_update': {
                            'plant_id': plant['id'], 
                            'service_type': 'TWITTER',
                            'notified_to_service': 'true'
                        }
                    }
                    res = requests.post(
                    API_URL + 'notifications/executed', json.dumps(json_data)) 
                    if res.status_code != 200:
                        raise Exception

    except Exception as e:
        print(e)

def getEmojiStr(code):
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