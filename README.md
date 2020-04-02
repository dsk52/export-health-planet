# DUMP HEALTH PLANET

headlth planet からデータ収集するスクリプトです

- Python 3.8.2

## セットアップ

```
$ python -m venv venv
$ source venv/bin/activate
or
$ source venv/bin/activate.fish

$ pip install -r requirements.txt
```

### アカウント登録と連携アプリを作成
Health Planetでアカウントを登録後、連携アプリを作成。Client ID、Client secretを取得。
https://www.healthplanet.jp/applications.do


### アクセストークンの取得とスクリプトへの追加
下記APIの仕様書を元に下記APIを使用し、アクセストークンを取得。

1. /oauth/auth
2. /oauth/token

[Health Planet API 仕様書　｜　Health Planet ヘルスプラネット](https://www.healthplanet.jp/apis/api.html)


```
$ cp .env.sample .env
$ direnv edit .
// HEALTH_ACCESS_TOKEN にアクセストークンを追加

$ direnv allow
```

## 実行

```
$ python health_status.py

# output to dist dir
```
