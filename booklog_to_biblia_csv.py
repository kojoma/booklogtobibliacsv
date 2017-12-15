# -*- coding: utf-8 -*-

import sys
import csv

from datetime import datetime
from typing import Dict

WANT_READ_STATE = ["読みたい", "積読"]

def __load_booklog_row(row: list) -> Dict[str, str]:
    book = {
        'title':         row[11],
        'author':        row[12],
        'publisher':     row[13],
        'isbn13':        row[2],
        'memo':          row[8],
        'impressions':   row[6],
        'rate':          __rate(row[4]),
        'want_read_flg':  __want_read_flg(row[5]),
        'thumbnail_url': "",
        'book_url':      "",
        'registered_at': __datetime_to_date(row[9]),
        'updated_at':    __datetime_to_date(row[9]),
    }
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

argvs = sys.argv
argc  = len(argvs)

if (argc != 2):
    print("Usage: # python %s <booklog_csv_file>" % (argvs[0]))
    sys.exit()

booklog_name = argvs[1]
unix_now = datetime.now().strftime('%s')
biblia_name = "books-%s.csv" % unix_now
print("convert csv file booklog: %s to biblia: %s" % (booklog_name, biblia_name))

try :
    biblia_rows = []

    with open(booklog_name, newline='', encoding='utf-8') as booklog_file:
        booklog_reader = csv.reader(booklog_file, delimiter=',', quotechar='"')

        for row in booklog_reader:
            book = __load_booklog_row(row)
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

    with open(biblia_name, 'w', newline='', encoding='utf-8') as biblia_file:
        biblia_writer = csv.writer(biblia_file, delimiter=',', quotechar='"', lineterminator='\n')
        biblia_writer.writerows(biblia_rows)

    print("completed convert!")

except FileNotFoundError as e:
    print("%s file is not found!" % (booklog_name))
except csv.Error as e:
    print(e)
