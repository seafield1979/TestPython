import re
import sys
import json
import os

def test01():
    print('test01')
    number_int = 1000
    bin1 = number_int.to_bytes(4, 'big', signed=False)
    number_int2 = -9999999999
    bin2 = number_int2.to_bytes(8, 'big', signed=True)
    with open('./resource/output1.bin', 'wb') as fw:
        fw.write(bin1)
        fw.write(bin2)

# バイナリファイルを読み込む
def test02():
    print('test02')
    with open('./resource/output1.bin', 'rb') as fr:
        number_bin = fr.read(4)
        print(number_bin)
        print(int.from_bytes(number_bin, 'big', signed=False))
        number_bin2 = fr.read(8)
        print(number_bin2)
        print(int.from_bytes(number_bin2, 'big', signed=True))

# バイナリデータを生成
def test03():
    data = bytes(range(65,72))
    for b in data:
        print(b)

# バイナリファイルを直接編集
def test04():
    with open('./resource/test1.bin', 'rwb') as fr:

test01()
test02()
test03()

print('complete')