from shutil import ExecError
import cv2
import numpy as np
from datetime import datetime
import pprint
import json
import requests
from dotenv import load_dotenv
import os
from logging import getLogger
import sys

logger = getLogger(__name__)
load_dotenv()

# /dev/video0を指定
DEV_ID = int(os.getenv('DEV_ID_WEB_CAM'))
HOST_NAME = os.getenv('API_SERVER_HOST_NAME')
PORT = os.getenv('API_PORT')
PLANT_ID = os.getenv('PLANT_ID')

# パラメータ
IMG_WIDTH = 800
IMG_HEIGHT = 600

def main():

    try:
        service_name= sys.argv[1]

        # Webカメラののデバイス番号を指定(/dev/video*)
        cap = cv2.VideoCapture(DEV_ID)

        # 解像度の指定
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)

        
        # カメラのフレームの読み込み
        read_complete, frame = cap.read()
        if not read_complete: raise Exception('frame read failed')

        # 明るさ補正
        frame_adjusted = adjust_brightness(frame, alpha=0.8, beta=70.0)

        # 画像出力
        img_file_name = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        img_file_path = "./" + img_file_name
        write_complete = cv2.imwrite(img_file_path, frame_adjusted)
        if not write_complete: raise Exception('image write failed')

        # 画像 + メタデータをAPIへ送信
        upload_image(img_file_path)
        image_id = send_image_meta_info(img_file_name)
        
        # 通知を予約
        send_notification(image_id, service_name)

    except Exception as e:
        pprint('catch exception:', e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return


def adjust_brightness(img, alpha=1.0, beta=0.0):
    dst = alpha * img + beta
    return np.clip(dst, 0, 255).astype(np.uint8)

def upload_image(img_file_path: str):
    file = {'upload_file': open(img_file_path, 'rb')}
    res = requests.post(
        f'http://{HOST_NAME}:{PORT}/api/snapshots/upload/image', 
        files=file)
    if res.status_code != 200: 
        pprint(res)
        raise Exception('upload image failed:')

def send_image_meta_info(img_file_name: str):
    res = requests.post(
        f'http://{HOST_NAME}:{PORT}/api/snapshots/upload/meta',
        json.dumps({
            'new_snapshot': {
                'plant_id': PLANT_ID,
                'image_file': img_file_name
            }
        }),
        headers={'Content-Type': 'application/json'})
    if res.status_code != 201: 
        pprint(res)
        raise Exception('send image meta info failed')
    res_json = res.json()
    image_id = res_json["id"]
    return image_id

def send_notification(image_id: str, service_name: str):
    res = requests.post(
        f'http://{HOST_NAME}:{PORT}/api/notifications',
        json.dumps({
        'new_notification':{
            'plant_id': PLANT_ID,
            'service_type': service_name,
            "notified_to_service": "false",
            "snapshot_id": image_id,
            "message": ""
            }
        })
    )
    if res.status_code != 201:  
        pprint(res)
        raise Exception('send_notification failed')

if __name__ == "__main__":
    main()