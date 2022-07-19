import busio 
import board
import RPi.GPIO as GPIO
import datetime
import time
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import pprint
import json
import requests
from dotenv import load_dotenv
import os


load_dotenv()

HOST_NAME = os.getenv('API_SERVER_HOST_NAME')
PORT = os.getenv('API_PORT')
PLANT_ID = os.getenv('PLANT_ID')
GPIO_PUMP_OUT_PIN = 27


def main():

    # APIから土の水分の必要量と十分量を取得
    need_pump,complete_pump = get_pump_setting()

    # ラズパイの初期化
    moist = setup_pi()

    # 土の水分が必要量以上であればスキップ
    if need_pump < moist.voltage:
        print('no need to pump now')
        return

    # 給水のタイムアウト値を10秒とする
    base_time = time.time()
    timeout = base_time + 10

    # 開始時点の水分量を保持
    start_moist = moist.voltage
    is_bottle_empty = False

    # 給水開始
    pump_on()

    # 十分な量に達するまで実行
    while complete_pump <= moist.voltage:

        # 1秒ごとに値を計測（デバッグ確認用）
        if time.time() - base_time >= 1:
            recordtime = '{0:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())
            data = [recordtime, moist.voltage]
            print(data)
            base_time = time.time()

        # 最大時間を超過し
        if time.time() > timeout:
            # スタート地点の水分量と差が少なかったら
            if abs(start_moist - moist.voltage) < 0.03:
                # 水切れと判断
                is_bottle_empty = True
                print("water bottle is empty")
            break

    # 給水終了
    pump_off()

    # 水切れ？
    if is_bottle_empty:
        message = " @kohei_ito_smn おみずないよー :angry: :anger: "
    else:
        message = "おみずごちそうさま :blush: "
        # 給水ログの登録
        send_pump_log()

    # 通知登録
    send_notification(message)

# ラズベリーパイの立ち上げ
def setup_pi():
    GPIO.setup(GPIO_PUMP_OUT_PIN, GPIO.OUT)
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1015(i2c)
    moist = AnalogIn(ads, ADS.P0)
    return moist

# APIから水やり開始/完了の閾値を取
def get_pump_setting():
    res = requests.get(f'http://{HOST_NAME}:{PORT}/api/pump_settings/?plant_id={PLANT_ID}')
    if res.status_code != 200: raise Exception('ERROR')
    json = res.json()
    need_pump = json['need_pump']
    complete_pump = json['complete_pump'] 
    return need_pump, complete_pump

# 水やりポンプON
def pump_on():
    GPIO.output(GPIO_PUMP_OUT_PIN, True)
    print("start pumping")

# 水やりポンプOFF
def pump_off():
    GPIO.output(GPIO_PUMP_OUT_PIN, False)
    print("stop pumping")


def send_notification(message: str):
    res = requests.post(
        f'http://{HOST_NAME}:{PORT}/api/notifications',
            json.dumps({
            'new_notification':{
                'plant_id': PLANT_ID,
                'service_type': "TYPETALK",
                "notified_to_service": "false",
                "snapshot_id": None,
                "message": message
                }
            })
    )
    if res.status_code != 201:  
        pprint(res)
        raise Exception('send_notification failed')

def send_pump_log():
    res = requests.post(
        f'http://{HOST_NAME}:{PORT}/api/pump_logs',
            json.dumps({
            'new_pump_log':{
                'plant_id': PLANT_ID
                }
            })
    )
    if res.status_code != 201:  
        pprint(res)
        raise Exception('send_pump_log failed')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pprint('catch exception', e)
    finally:
        GPIO.cleanup()