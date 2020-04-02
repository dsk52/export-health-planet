import os
import requests
from datetime import datetime, timedelta
import calendar
import json
import csv
from requests.exceptions import HTTPError
from collections import OrderedDict

STATUS_API = 'https://www.healthplanet.jp/status/innerscan.json'
DATE_FORMAT = "%Y%m%d%H%M%S"

def one_month_health_status(today):
    """
    今月の測定記録を取得
    """
    this_month = calendar.monthrange(today.year, today.month)
    last_date = this_month[1]

    first_datetime = today.replace(day=1, hour=0, minute=0, second=0)
    last_datetime = today.replace(day=last_date, hour=23, minute=59, second=59)

    return fetch_health_status(start=first_datetime.strftime(DATE_FORMAT), end=last_datetime.strftime(DATE_FORMAT))

def fetch_health_status(start, end):
    """
    StatusのAPI から体重のデータを抜き出す
    @url https://www.healthplanet.jp/apis/api.html
    """
    HEALTH_ACCESS_TOKEN = os.environ.get('HEALTH_ACCESS_TOKEN')

    payload = {
        'access_token': HEALTH_ACCESS_TOKEN,
        'tag': '6021,6022,6023,6024,6025,6027,6028,6029', #体重,体脂肪率,筋肉量,筋肉スコア,内臓脂肪レベル,基礎代謝量,体内年齢,推定骨量
        'date': 0, # 登録日付
        'from': start,
        'to': end
    }

    response = requests.get('https://www.healthplanet.jp/status/innerscan.json', params=payload)
    return response.text


def readMockFile():
    path = 'sample_innerscan.json'
    with open(path) as f:
        datas = json.load(f)
    return datas

def formattingData(json_str):
    """
    計測日ベースで各データをまとめる
    """
    datas = json.loads(json_str)

    health_status_list = OrderedDict()
    for data in datas['data']:
        date = int(data['date'])
        health_status_list[date] = OrderedDict()

    for data in datas['data']:
        date = int(data['date'])
        tag = data['tag']
        keydata = data['keydata']
        health_status_list[date][tag] = keydata

    return health_status_list

def output(file_name, datas):
    output_dir = './dist/'
    os.makedirs(output_dir, exist_ok=True) # ディレクトリを作成

    output_path = output_dir + file_name
    json_file = open(output_path, 'w')
    json.dump(datas, json_file, indent=2)


if __name__ == '__main__':
    today = datetime.today()
    file_name = f'''{today.strftime("%Y%m")}.json'''
    health_status = one_month_health_status(today)
    # health_status = readMockFile()
    datas = formattingData(health_status)
    output(file_name, datas)
