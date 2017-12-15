# -*- coding: utf-8 -*-

import sys
import csv
import json
import os

from time import sleep
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from chardet.universaldetector import UniversalDetector

from typing import Dict

WANT_READ_STATE = ["読みたい", "積読"]
RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = os.environ['RAKUTEN_APP_ID'] if "RAKUTEN_APP_ID" in os.environ else ""

def get_file_encode(file_name: str) -> str:
    try :
        detector = UniversalDetector()

        with open(booklog_name, mode='rb') as f:
            for binary in f:
                detector.feed(binary)
                if detector.done:
                    break
        detector.close()

        return detector.result['encoding']
    except FileNotFoundError as e:
        print("%s file is not found!" % (booklog_name))
        sys.exit()
    except csv.Error as e:
        print(e)
        sys.exit()

def load_booklog_row(row: list) -> Dict[str, str]:
    book = {
        'title':         row[11],
        'author':        row[12],
        'publisher':     row[13],
        'isbn13':        row[2],
        'memo':          row[8],
        'impressions':   row[6],
        'rate':          __rate(row[4]),
        'want_read_flg': __want_read_flg(row[5]),
        'registered_at': __datetime_to_date(row[9]),
        'updated_at':    __datetime_to_date(row[9]),
    }

    rakuten_book = __get_rakuten_book(book['isbn13'])
    book['thumbnail_url'] = rakuten_book['thumbnail_url']
    book['book_url']      = rakuten_book['book_url']

    return book

def __datetime_to_date(datetime_str: str) -> str:
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')

def __rate(rate_str: str) -> int:
    rate = 0

    if rate_str == "":
        rate = 0
    else:
        rate = int(rate_str, 10)

    return rate

def __want_read_flg(read_state: str) -> int:
    want_read_flg = 0

    if read_state in WANT_READ_STATE:
        want_read_flg = 1
    else:
        want_read_flg = 0

    return want_read_flg

# 楽天ブックスの書籍検索APIを使って、書籍情報を取得する
# APIについては https://webservice.rakuten.co.jp/api/booksbooksearch/ を参照
def __get_rakuten_book(isbn: str) -> Dict[str, str]:
    rakuten_book = {
        'thumbnail_url': "",
        "book_url": ""
    }

    if len(isbn) != 0:
        url = "%s?applicationId=%s&isbn=%s" % (RAKUTEN_BOOKS_API_URL, RAKUTEN_APP_ID, isbn)
        request = Request(url)

        try:
            response = urlopen(request)

            if response.getcode() == 200:
                content = json.loads(response.read().decode('utf-8'))

                if content['count'] > 0:
                    item = content['Items'][0]['Item']

                    rakuten_book['thumbnail_url'] = item['largeImageUrl']
                    rakuten_book['book_url']      = item['itemUrl']
        except HTTPError as e:
            print("rakuten api request failed. isbn: %s, reason: %d %s" % (isbn, e.code, e.reason))
        except URLError as e:
            print("rakuten api connection failed. isbn: %s, reason: %s" % (isbn, e.reason))

    return rakuten_book

def main():
    argvs = sys.argv
    argc  = len(argvs)

    if argc != 2:
        print("Usage: # python %s <booklog_csv_file>" % (argvs[0]))
        sys.exit()

    if len(RAKUTEN_APP_ID) == 0:
        print("please set system environment value RAKUTEN_APP_ID.")
        sys.exit()

    booklog_name = argvs[1]
    unix_now = datetime.now().strftime('%s')
    biblia_name = "books-%s.csv" % unix_now
    print("convert csv file booklog: %s to biblia: %s" % (booklog_name, biblia_name))

    try :
        biblia_rows = []

        encode = get_file_encode(booklog_name)
        with open(booklog_name, newline='', encoding=encode) as booklog_file:
            booklog_reader = csv.reader(booklog_file, delimiter=',', quotechar='"')

            for row in booklog_reader:
                book = load_booklog_row(row)
                biblia_rows.append((
                    book['title'],
                    "",
                    book['author'],
                    "",
                    book['publisher'],
                    book['isbn13'],
                    book['registered_at'],
                    book['memo'],
                    book['impressions'],
                    book['thumbnail_url'],
                    book['book_url'],
                    book['updated_at'],
                    book['want_read_flg'],
                    book['rate']
                ))

                print(".", end="", flush=True)
                sleep(1) # 楽天に対して、短時間に大量にリクエストしないよう1秒スリープ

        print("\n")

        with open(biblia_name, 'w', newline='', encoding='utf-8') as biblia_file:
            biblia_writer = csv.writer(biblia_file, delimiter=',', quotechar='"', lineterminator='\n')
            biblia_writer.writerows(biblia_rows)

        print("convert completed!")

    except FileNotFoundError as e:
        print("%s file is not found!" % (booklog_name))
    except csv.Error as e:
        print(e)

if __name__ == '__main__':
    main()
