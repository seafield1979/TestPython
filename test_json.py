import re
import sys
import json
import os

def test01():
    print("test01")
    s = '{"A": {"X": 1, "Y": 1.0, "Z": "abc"}, "B": [true, false, null, NaN, Infinity]}'
    d = json.loads(s)
    print(d)


def test02():
    print("test01")
    try:
        with open('resource/tengai2.json', mode='r', encoding="utf-8") as f:
            text = f.read()
            # print(text)
            json1 = json.loads(text)
            print('test01-2')
            for node in json1['Cheats']:
                print(node['Description'])
    except (FileNotFoundError, TypeError) :
        print('ファイルが開けませんでした:' + file_path)
    except:
        print('何らかのエラーが発生')
    

def main():
    test01()
    test02()


main()