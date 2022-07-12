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

                print(notification['snapshot_id'])

                if notification['snapshot_id']:
                    snapshot = requests.get(API_URL + 'snapshots/' + str(notification['snapshot_id'])).json()
                    print(snapshot)
                    path = '../uploads/' + snapshot['image_file']
                    file = {'file': open(path, 'rb')}
                    res_post_attachment = requests.post(url + '/attachments', files=file, headers = headers)
                    res_post_attachment_json = res_post_attachment.json()

                    fileKey = res_post_attachment_json["fileKey"]
                    data = {
                    'message': notification['message'],
                    'fileKeys[0]': fileKey
                    }
                else:
                    data = { 'message': notification['message'] }

                
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