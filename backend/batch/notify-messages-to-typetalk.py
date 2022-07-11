import requests
import json

def main():

    API_URL = "http://localhost:8000/api/"

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

                url = setting['api_url']
                headers = { 'X-TYPETALK-TOKEN': setting['access_token']}
                data = {'message': notification['message']}

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

if __name__ == '__main__':
    main()