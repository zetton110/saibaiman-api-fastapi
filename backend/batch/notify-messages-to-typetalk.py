import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def main():

    API_URL = "http://localhost:8000/api/"
    OPEN_METEO_URL = os.getenv('OPEN_METEO_URL')

    try:
        plants = requests.get(API_URL + "plants/").json()
        for plant in plants:
            settings = requests.get(API_URL + "notification_settings/", {'plant_id': plant['id']}).json()
            for setting in settings:
                if setting['service_type'] != 'TYPETALK': break
                if setting['enabled'] == False: break

                notification = requests.get(
                    API_URL + "notifications/latest-one", 
                    {
                        'plant_id': plant['id'], 
                        'service_type': 'TYPETALK'
                    }).json()
                
                if not notification: break
                if notification['notified_to_service'] == True: break

                message = notification['message']

                url = setting['api_url']
                headers = { 'X-TYPETALK-TOKEN': setting['access_token']}

                print(notification['snapshot_id'])

                if notification['snapshot_id']:
                    snapshot = requests.get(API_URL + 'snapshots/' + str(notification['snapshot_id'])).json()
                    print(snapshot)
                    path = '../uploads/' + snapshot['image_file']
                    file = {'file': open(path, 'rb')}
                    res_post_attachment = requests.post(url + '/attachments', files=file, headers = headers)
                    res_post_attachment_json = res_post_attachment.json()


                    res_weather_api = requests.get(OPEN_METEO_URL).json()
                    current_temperature = res_weather_api['current_weather']['temperature']
                    current_weather_status = res_weather_api['current_weather']['weathercode']
                    weather_message = f'きょうの天気：{getEmojiStr(current_weather_status)}、そとの気温：{current_temperature}度'
                    message = weather_message

                    fileKey = res_post_attachment_json["fileKey"]
                    data = {
                    'message': message,
                    'fileKeys[0]': fileKey
                    }
                else:
                    data = { 'message': message }

                res_typtalk = requests.post(url, json = data, headers = headers)
                print(res_typtalk.status_code)

                if res_typtalk.status_code == 200:
                    json_data = {
                        'notification_update': {
                            'plant_id': plant['id'], 
                            'service_type': 'TYPETALK',
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

if __name__ == '__main__':
    main()