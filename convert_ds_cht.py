# DeSmuMEのチートファイル usrcheat.dat を解析
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
        text1 = bin_text.decode('utf-8')
    except UnicodeDecodeError:
        print("デコード失敗")
        return None

    return text1

# 文字列の後の00をスキップ
# 4Byteのアライメント位置で停止
def skip_null(fr):
    while fr.tell() % 4 != 0:
        byte1 = fr.read(1)
        if byte1 != b'\x00':
            fr.seek(-1, 1)
            break

def convert_cht_file(fr, fw):
    # ヘッダー部分をスキップ
    fr.seek(0x100)

    # ゲームヘッダをリストに取得
    addr_list = []
    cnt = 0
    while cnt < 10000:
        title_head_bin = fr.read(16)
        addr = int.from_bytes(title_head_bin[8:12], 'little', signed=False)
        if addr != 0:
            addr_list.append(addr)
        else:
            break
        cnt += 1
    
    # ゲームデータを読み込む
    bin_text = bytearray()
    cnt = 0
    for addr1 in addr_list:
        print(f"{addr1:08X}")
        fr.seek(addr1, os.SEEK_SET)

        # ゲームタイトルを読み込む
        game_title = get_text_from_bin(fr)
        if game_title is None:
            break

        skip_null(fr)
        fw.write(game_title)
        
        # 全コード数(フォルダやチートコード) 値が大きすぎるならばぐっているので抜ける
        code_num = int.from_bytes(fr.read(2), 'little', signed=False)
        if code_num > 10000:
            break

        # マスター設定 (34Byte) をスキップ
        fr.read(34)
        
        # コード部
        # テキストのバイナリをUTF-8のテキストに置換
        folder_title = ""
        for i in range(code_num):
            bin_type = fr.read(4)
            #type1 = int.from_bytes(bin_type, 'little', signed=False)
            if (bin_type[3] & 0x10) > 0:
                # フォルダ以下のコード数
                code_list_num = bin_type[0]
                # フォルダ名
                folder_title = get_text_from_bin(fr)
                # 備考
                comment1 = get_text_from_bin(fr)
                skip_null(fr)
                print(f"folder title:{folder_title} comment:{comment1} code_list_num:{code_list_num}")
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
                
                if folder_title != "":
                    fw.write(f'\t{folder_title} {title1}\t"')
                else:
                    fw.write(f'\t{title1}\t"')
                code_list_cnt = 0
                for j in range(code_list_num):
                    code1 = int.from_bytes(fr.read(4), 'little', signed=False)
                    if code_list_cnt == 1:
                        fw.write(" ")
                    fw.write(f"{code1:08X}")
                    code_list_cnt += 1
                    if code_list_cnt == 2:
                        code_list_cnt = 0
                        if j < code_list_num - 1:
                            fw.write("\n")
                fw.write('"')
                fw.write("\n")
        cnt += 1
        if cnt > 200:
            break

# RetroArch用のchtファイルを出力する
def convert_cht_file2(fr, out_path):
    # ヘッダー部分をスキップ
    fr.seek(0x100)

    # ゲームヘッダをリストに取得
    addr_list = []
    cnt = 0
    while cnt < 10000:
        title_head_bin = fr.read(16)
        addr = int.from_bytes(title_head_bin[8:12], 'little', signed=False)
        if addr != 0:
            addr_list.append(addr)
        else:
            break
        cnt += 1
    
    # ゲームデータを読み込む
    bin_text = bytearray()
    cnt = 0
    for addr1 in addr_list:
        print(f"{addr1:08X}")
        fr.seek(addr1, os.SEEK_SET)

        # ゲームタイトルを読み込む
        game_title = get_text_from_bin(fr)
        if game_title is None:
            break
        skip_null(fr)

        # ファイル名に使用できない文字を変換
        game_title = game_title.replace('\\','_').replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('<','_').replace('>','_').replace('|','_')

        filepath = out_path + game_title + ".cht"
        with open(filepath, 'w') as fw:
            # 全コード数(フォルダやチートコード) 値が大きすぎるならばぐっているので抜ける
            code_num = int.from_bytes(fr.read(2), 'little', signed=False)
            if code_num > 10000:
                break

            # マスター設定 (34Byte) をスキップ
            fr.read(34)
            
            # コード部
            # テキストのバイナリをUTF-8のテキストに置換
            folder_title = ""
            code_cnt = 0
            for i in range(code_num):
                bin_type = fr.read(4)
                #type1 = int.from_bytes(bin_type, 'little', signed=False)
                if (bin_type[3] & 0x10) > 0:
                    # フォルダ以下のコード数
                    code_list_num = bin_type[0]
                    # フォルダ名
                    folder_title = get_text_from_bin(fr)
                    # 備考
                    comment1 = get_text_from_bin(fr)
                    skip_null(fr)
                    print(f"folder title:{folder_title} comment:{comment1} code_list_num:{code_list_num}")
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
                    
                    desc_text = ""
                    if folder_title != "":
                        desc1 = f'{folder_title} {title1}"'
                    else:
                        desc1 = title1
                    fw.write(f'cheat{code_cnt}_desc = "{desc1}"\n')

                    code_text = ""
                    for j in range(code_list_num):
                        code1 = int.from_bytes(fr.read(4), 'little', signed=False)
                        if j > 0:
                            code_text += "+"
                        code_text += f"{code1:08X}"
                        
                    fw.write(f'cheat{code_cnt}_code = "{code_text}"\n')
                    fw.write(f"cheat{code_cnt}_enable = false\n")
                    code_cnt += 1
            fw.write(f"cheats = {code_cnt}")

        cnt += 1
        # if cnt > 100:
        #     break


if __name__ == "__main__":
    # with open('./resource/usrcheat_utf8.dat', 'rb') as fr:
    with open('./resource/usrcheat_utf8.dat', 'rb') as fr:
        convert_cht_file2(fr, './ds_cheats/')
        print('complete!!')
    
    # with open('./resource/usrcheat_utf8.dat', 'rb') as fr:
    # with open('./resource/usrcheat2.dat', 'rb') as fr:
    #     with open('./resource/ds_cheats.txt', 'w') as fw:
    #         convert_cht_file(fr, fw)
    #         print('complete!!')