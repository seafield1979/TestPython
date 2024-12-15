import re
import sys
import json
import os

# バイナリをファイルに書き込み
def test01():
    print('*** test01')
    with open('./resource/output1.bin', 'wb') as fw:
        # 整数をバイナリに変換
        # 符号なしビッグエンディアン
        number_int = 1000
        bin1 = number_int.to_bytes(4, 'big', signed=False)
        fw.write(bin1)
        
        # 符号ありビッグエンディアン
        number_int2 = -9999999999
        bin2 = number_int2.to_bytes(8, 'big', signed=True)
        fw.write(bin2)

        # 符号なしリトルエンディアン4Byte
        number_int3 = 0x11223344
        bin3 = number_int3.to_bytes(4, 'little', signed=False)
        fw.write(bin3)
        
        # 文字列からバイト配列を作成
        text = "Hello World!!"
        bin_text = bytes(text, 'utf-8')
        # バイト配列の先頭8Byteを書き込み
        fw.write(bin_text[:8])

        # バイト配列
        array1 = bytes(range(65,71))  # bytes[65, 66, 67, 68, 69, 70]) ABCDEF
        fw.write(array1)


# バイナリファイルを読み込む
def test02():
    print('*** test02')
    with open('./resource/output1.bin', 'rb') as fr:
        # 符号なしビッグエンディアン4Byte
        number_bin = fr.read(4)
        print(number_bin)
        print(int.from_bytes(number_bin, 'big', signed=False))

        # 符号ありビッグエンディアン8Byte
        number_bin2 = fr.read(8)
        print(number_bin2)
        print(int.from_bytes(number_bin2, 'big', signed=True))

        # 符号なしリトルエンディアン4Byte
        number_bin3 = fr.read(4)
        print(number_bin3)
        print("{:016X}".format(int.from_bytes(number_bin3, 'little', signed=False)))

        # 文字列(8Byte)
        bin_text = fr.read(8)
        text = bin_text.decode('utf-8')
        print(text)

        # 配列6Byte
        array1 = fr.read(6)
        print(array1)
        

# バイナリデータを生成
def test03():
    print('*** test03')
    data = bytes(range(65,72))  # bytes[65, 66, 67, 68, 69, 70, 71]) ABCDEFG
    for b in data:
        print(b)
    # バイト配列から指定の範囲を抜き出す
    # [3:] は先頭 4Byte目から末尾まで(0から数えてのため 0,1,2,3 で4Byte目)
    data2 = data[2:]
    print(data2)

    # [:3] は末尾 4Byte目から先頭まで
    data3 = data[:3]
    print(data3)

    # [1:4] 2Byte目から3Byte目まで
    data4 = data[1:3]
    print(data4)

    #---------------------
    # Byte配列を拡張する
    #---------------------
    original_bytes = bytearray(b'Hello')
    new_size = 10

    # 新しいサイズの配列を作成し、元のデータをコピー
    extended_bytes = bytearray(new_size)
    extended_bytes[:len(original_bytes)] = original_bytes

    print(extended_bytes)  # 出力: bytearray(b'Hello\x00\x00\x00\x00\x00')

    #---------------------
    # Byte配列の文字列をデコード
    #---------------------
    # bytes1 = bytes([0xE3, 0x83, 0x86, 0xE3, 0x82, 0xB9, 0xE3, 0x83, 0x88])
    try:
        # bytes1 = bytes([0x1, 0xff])
        bytes1 = bytes([0x83, 0x41, 0x83, 0x43, 0x83, 0x68, 0x83, 0x8B, 0x90, 0x9D, 0x8E, 0x6D, 0x20, 0x83, 0x58, 0x81, 0x5B, 0x83, 0x60, 0x81, 0x5B, 0x83, 0x70, 0x83, 0x43, 0x87, 0x56, 0x20, 0x52, 0x65, 0x6D, 0x69, 0x78, 0x00])
        text1 = bytes1.decode('utf-8')
        print(text1)
    except UnicodeDecodeError:
        print("デコード失敗")


# バイナリファイルを直接編集
# def test04():
#     with open('./resource/test1.bin', 'rwb') as fr:


# test01()
# test02()
test03()

print('complete')