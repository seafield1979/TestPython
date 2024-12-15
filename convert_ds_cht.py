# NNNesterJのchtファイルをMESEN2のチートjsonファイルに変換
# ヘッダ部	
#   0x0000	4	2
# 	0x0004	4	コード数
# 	0x0008	4	ROM ID
# コード部	
#   0x0010	32	コメント
# 	0x0034	4	アドレス
# 	0x0038	4	値
# 	0x003C	4	実行コード
#   0x0040  4   サブコード数
# 	0x0044	1	0:無効, 1:有効
# 	0x0045	1	数値(0:10進,1:16進)
# 	0x0046	1	サイズ(1:1Byte, 2:2Byte, 3:3Byte, 4:4Byte)
import copy
import re
import sys
import json
import os
import traceback

def get_text_from_bin(fr):
    cnt = 0
    bin_text = bytearray()
    
    while cnt < 1000:
        byte1 = fr.read(1)
        # print(int.from_bytes(byte1, 'little'))
        if byte1 != b'\x00':
            bin_text.extend(byte1)
        else:
            break
        cnt += 1

    try:
        # game_title = bin_text.decode('utf-8')
        game_title = bin_text.decode('shift-jis')
    except UnicodeDecodeError:
        print("デコード失敗")
        return None

    return game_title

# 文字列の後のデータをスキップ
def skip_null(fr):
    cnt = 0
    while cnt < 100:
        byte1 = fr.read(1)
        if byte1 != b'\x00':
            fr.seek(-1, 1)
            break
        cnt += 1

def convert_cht_file(fr, fw):
    # ヘッダー部分をスキップ
    fr.seek(0x100)

    # ゲームヘッダをリストに取得
    addr_list = []
    cnt = 0
    while cnt < 10000:
        title_head_bin = fr.read(16)
        addr = int.from_bytes(title_head_bin[8:10], 'little', signed=False)
        if addr != 0:
            addr_list.append(addr)
        else:
            break
        cnt += 1
    
    # ゲームデータを読み込む
    bin_text = bytearray()
    for addr1 in addr_list:
        print(f"{addr1:08X}")
        fr.seek(addr1, os.SEEK_SET)

        # ゲームタイトルを読み込む
        game_title = get_text_from_bin(fr)
        if game_title is None:
            break
        skip_null(fr)
        
        # 全コード数(フォルダやチートコード) 値が大きすぎるならばぐっているので抜ける
        code_num = int.from_bytes(fr.read(2), 'little', signed=False)
        if code_num > 1000:
            break

        # マスター設定 (34Byte) をスキップ
        fr.read(34)
        
        # コード部
        # テキストのバイナリをUTF-8のテキストに置換
        for i in range(code_num):
            bin_type = fr.read(4)
            #type1 = int.from_bytes(bin_type, 'little', signed=False)
            if (bin_type[3] & 0x10) > 0:
                # フォルダ以下のコード数
                code_list_num = bin_type[0]
                # フォルダ名
                title1 = get_text_from_bin(fr)
                # 備考
                comment1 = get_text_from_bin(fr)
                skip_null(fr)
                print(f"folder title:{title1} comment:{comment1} code_list_num:{code_list_num}")
            else:
                # コード
                # コードタイトル
                title1 = get_text_from_bin(fr)
                # 備考
                comment1 = get_text_from_bin(fr)
                skip_null(fr)
                # コードリスト数
                code_list_num = int.from_bytes(fr.read(4), 'little', signed=False)
                print(f"  codes title:{title1} comment:{comment1} code_num:{code_list_num}")
                for j in range(code_list_num):
                    code1 = int.from_bytes(fr.read(4), 'little', signed=False)
                    # print(f"{code1:08X} ")



if __name__ == "__main__":
    with open('./resource/usrcheat2.dat', 'rb') as fr:
        with open('./resource/ds_cheats.txt', 'w') as fw:
            convert_cht_file(fr, fw)
            print('complete!!')