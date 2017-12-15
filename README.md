# booklogtobibliacsv

## 概要

[ブクログ](http://booklog.jp/)に登録した書籍情報を、[ビブリア](http://biblia-app.tumblr.com/)に登録するためのツールです。

## 使い方

### 準備

本ツールを利用するには下記の環境が必要です。

- Python3.x
- 楽天ブックスAPIを実行するためのアプリID
  - 変換時に書籍のサムネイル画像などを取得するために必要です

### ブクログのCSVをビブリアの形式に変換

- [ブクログのエクスポートページ](http://booklog.jp/export)にアクセスして本棚のデータをエクスポート
- 下記コマンドでビブリアの形式に変換
- 変換後のCSVファイルをDropbox復旧機能を利用してビブリアに登録

```
$ pip install chardet
$ export RAKUTEN_APP_ID=XXXXXXXXX
$ python booklog_to_biblia_csv.py <ブクログでエクスポートしたCSVファイル>
```
