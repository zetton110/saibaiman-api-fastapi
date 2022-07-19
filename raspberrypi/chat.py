import numpy as np
import requests
import json
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

PLANT_ID = os.getenv('PLANT_ID')
HOST_NAME = os.getenv('API_SERVER_HOST_NAME')
PORT = os.getenv('API_PORT')

def main():
    # wheher to chat or not
    if not want_to_chat(): return 
    action = get_action()

    # choose action
    msg = ''
    if action == ACTION_HITORIGOTO:
        msg = create_msg_of_hitorigoto()
    elif action == ACTION_TORIBIA:
        msg = create_msg_of_toribia()
    elif action == ACTION_QUOTE_MEIGEN:
        msg = create_msg_of_meigen()
    elif action == ACTION_WEEK_OF_DAY:
        msg = create_msg_of_week_of_day()
    elif action == ACTION_NASA_API:
        msg = create_msg_of_nasa_api()
    else:
        msg = ''
    print(msg)
    
    # send message
    if msg != '': send(msg)

def want_to_chat():
    flag = np.random.choice([True, False], p=[0.1, 0.9])
    return flag

def get_action():
    # action = np.random.choice([ACTION_NASA_API])
    action = np.random.choice(
        [
            ACTION_HITORIGOTO, 
            ACTION_QUOTE_MEIGEN, 
            ACTION_TORIBIA,
            ACTION_WEEK_OF_DAY,
            ACTION_NASA_API],
        p=[
            0.4, 
            0.05, 
            0.45,
            0.05,
            0.05])
    return action

def send(msg: str):
    res = requests.post(
       f'http://{HOST_NAME}:{PORT}/api/notifications',
        json.dumps({
        'new_notification':{
            'plant_id': PLANT_ID,
            'service_type': "TYPETALK",
            "notified_to_service": "false",
            "snapshot_id": None,
            "message": msg
            }
        })
    )
    if res.status_code != 201: return #error


ACTION_HITORIGOTO = "SOLILOGUY"            # 独り言
def create_msg_of_hitorigoto():
    message = np.random.choice([
        '今日のごはんは何かな〜',
        'やっほー',
        'ポンジュースのポンってなんだよ！',
        '水飽きた。ポンジュース飲みたい。',
        '水飽きた。コーヒー飲みたい。',
        '水飽きた。ファンタ飲みたい。',
        '水飽きた。レッドブル飲みたい。',
        'ねむたくなってきちゃった',
        '今日もがんばろー',
        'どんどんどーなつどーんといこー',
        'パンツァーフォー♪',
        'こころぴょんぴょん',
        'おいっすー',
        'うぃす',
        '最近どう？',
        'やっはろー'
    ])
    return message

ACTION_TORIBIA = "TORIBIA"
def create_msg_of_toribia():
    message = np.random.choice([
        '牡蠣は生涯で何度も性別を変えるんだってー',
        'しろくまってみんな左利きなんだよ',
        '世界で一番多い名前知ってる？ムハンマド、、だよ',
        'カタツムリの歯ってさ・・・25000本あるんだって',
        'だから！コーヒーって豆じゃないんだってば！！種子なんだってば！！',
        'いつもヨーロピアンブレンド飲んで気取ってるけどさぁ、あれは欧州生まれじゃないからね！'
        '難しく考えなくていいんじゃない？生きてれば矛盾することもあるよ。1円玉1枚作るのに材料費は3円かかるんだって。そんなもんよ。',
        '人ってさ、生まれてから死ぬまでの間で寝ているときに10匹以上のクモを食べてるんだって。そう考えたら怖いものなんてなくない？',
        'かぼちゃを英語で言ってみて？？？正解は、、、、、スクワッシュ！パンプキンだと思った？？思ったよね？？？ぷぷwww',
        'パフェ〜〜〜パフェ食べたい〜〜〜。知ってる？パフェの語源はパーフェクトなんだって',
        '喉が痛いときはマシュマロ食べると痛みが和らぐよ。ほんとだよ？ゼラチンがね、喉を保護してくれるんだって。',
        '新製品の販売テストは静岡県で行われることが多いんだって。なんでか知ってる？県民の年代とか職業とか物価とか生活費が平均的だから偏りなくデータがとれるからだって！',
        'タイのバンコクの正式名称は、クルンテープ・プラマハーナコーン・アモーンラッタナコーシン・マヒンタラーユッタヤー・マハーディロックポップ・ノッパラット・ラーチャタニーブリーロム・ウドムラーチャニウェートマハーサターン・アモーンピマーン・アワターンサティット・サッカタッティヤウィサヌカムプラシット。ロックなの？ポップなの？なんなの？？',
        'トウモロコシさんから聞いたんだけど、粒の数は必ず偶数になってるんだって',
        '救急車呼ぶときは119番だけど、そこまでじゃないと思うけど不安〜ってときない？そういうときは7119にかけるといいんだよ。',
        'ビールいっぱいで100万個の脳細胞が死ぬんだって。いや、だから飲むなってことじゃなくてさ、それでも生きていけるって話。',
        'このまえさ、キュウリさんがギネス記録持ってるって自慢してきたんだ。でも世界で一番栄養がない野菜っていうギネスだから笑っちゃった。',
        'サハラ砂漠のサハラは砂漠って意味だから',
        'サルサソースのサルサはソースって意味だから',
        '音楽好き？世界一長い曲知ってる？演奏が終わるまでに６３９年かかるんだって',
        'そんなに焦るらないで〜。缶切りが発明されたのだって、缶詰が販売されてから４８年後なんだから。そんなもんだよ。',
        '知ってる？人一人の血管を全て繋げると地球２周半分の長さになるんだって。そう考えたら、世界と戦うなんて大した話じゃないよねー',
        'パソコン詳しい？じゃあ、パソコンのマウスを動かした時の長さの単位はなーんだ？？？答えは、「ミッキー」',
        'ドイツじゃ釣りするのに国家資格いるんだって',
        '東京特許許可局って言える？すごいね！でも知ってた？「東京特許許可局」なんて実在してないんだ',
        'マジ！？って江戸時代からある言葉だからね。。マジ？！',
        'ヤバい！！って江戸時代からある言葉だからね。ヤバい！！',
        'ガリガリ君が当たる確率は2~4%なのは常識でしょ',
        'オーストラリアのエロマンガ島に行ったときの話なんだけど・・・',
        'オランダのスケベニンゲンって街に行った時の話なんだけど・・・',
        '緑茶と紅茶とウーロン茶は全部同じ葉っぱなんだよ',
        '自動販売機のボタンを２つ同時に押してごらん？必ず左側の商品が出てくるから',
        'チョコレートは直訳すると「苦い水」なんだって',
        '新聞紙を折っていくと分厚くなるじゃん？42回折るとさ、38万km離れた月に届くんだって。',
        'マツコ・デラックスと木村拓哉は高校の同級生なんだって',
        'ローラースケートの開発者は初めて滑った時、止まり方を考えてなくて重症を負ったんだって。。',
        '甘いもの好き？カスタードクリームは拳銃の弾を受け止めることができるって知ってた？',
        'Twitterの鳥の名前は「Lally」っていうんだ',
        'ATMでお金を下ろすときに、1万円を「10千円」と入力すると千円札10枚で引き出すことができるよ',
        'ドラえもんの本体価格は20万円なんだって'
    ])
    return message

ACTION_QUOTE_MEIGEN = 'QUOTE_MEIGEN'       # 名言
def create_msg_of_meigen():
    # 名言教えるよAPI https://meigen.doodlenote.net/about_api.html
    res_meigen = requests.get('https://meigen.doodlenote.net/api/json.php?c=1')
    if(res_meigen.status_code == 200):
        json = res_meigen.json()
        meigen = json[0]['meigen']
        author = json[0]['auther']
        msg = f'{meigen} by {author}'
    else:
        msg = ''
    return msg

ACTION_WEEK_OF_DAY = 'WEEK_OF_DAY'       # 曜日つぶやき
def create_msg_of_week_of_day():
    d_week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水','Thu': '木', 'Fri': '金', 'Sat': '土'}
    key = now.strftime('%a')
    w = d_week[key]
    msg = f'きょうは{w}曜日だね〜'
    return msg

ACTION_NASA_API = 'NASA_API'
def create_msg_of_nasa_api():
    res = requests.get('https://api.nasa.gov/planetary/apod' + '?api_key=' + os.getenv('API_KEY_NASA'))
    if res.status_code == 200:
        json = res.json()
        msg = '疲れてる？これ見て癒されて'
        msg += '\n'
        msg += json['url']
    else:
        msg = ''
    return msg

if __name__ == "__main__":
    main()