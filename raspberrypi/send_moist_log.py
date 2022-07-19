import busio 
import board
import RPi.GPIO as GPIO
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

    # ラズパイの初期化
    moist = setup_pi()

    # moist_logの送信
    send_moist_log(moist.voltage)

    

# ラズベリーパイの立ち上げ
def setup_pi():
    GPIO.setup(GPIO_PUMP_OUT_PIN, GPIO.OUT)
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1015(i2c)
    moist = AnalogIn(ads, ADS.P0)
    return moist

# 水分量測定結果の送信
def send_moist_log(moist_val: float):
    res = requests.post(
        f'http://{HOST_NAME}:{PORT}/api/moist_logs',
            json.dumps({
            'new_moist_log':{
                'plant_id': PLANT_ID,
                'moist': moist_val
                }
            })
    )
    if res.status_code != 201:  
        pprint(res)
        raise Exception('send_moist_log failed')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pprint('catch exception', e)
    finally:
        GPIO.cleanup()