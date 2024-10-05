# メガドライブのチートをRetroArchのチートに変換する
# input: チートコードのタイトルとコード
#   *P1 Max EXP
#   FFC00D:00FF
# ouput: RetroArchのchtファイル形式のコード
#   cheat4_code = "FFC00D:00FF"
#   cheat4_desc = "P1 Max EXP"

import re
import sys
import json
import os

# code_listを文字列に変換する
# @param[in]: codeの配列
# @return: jsonに書き込む形式のcode文字列
def encode_code_list(code_list):
    output = ""
    for code in code_list:
        if len(output) > 0:
            output += r'\r\n'
        output += code
    return output


def read_cheat_file(file_path):
    output = []
    cheat1 = {"desc":None, "code": []}
    
    # タイトル行の正規表現
    re_title = re.compile('^\s*\*', re.UNICODE)

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip('\n')
            # title line
            if re_title.match(line):
                if len(cheat1['code']) > 0:
                    output.append(cheat1.copy())
                    cheat1 = {"desc":None, "code": []}
                # 先頭の"*"とスペースを除去
                line = line.lstrip()
                line = line.lstrip('*')
                cheat1['desc'] = line
            else:
                # 空行は無視
                # F81250:FF のようなコード行を取得する
                line2 = line.strip()
                if len(line2) >= 8:
                    cheat1['code'].append(line2)
    if len(cheat1['desc']) > 0:
        output.append(cheat1.copy())

    return output


# ファイルから読み込んだチートを出力形式に変換する
def output_cheats(file_path, cheats):
    # 保存先のファイルパスを取得
    file_path_split = os.path.splitext(file_path)
    if len(file_path_split) < 2:
        return
    
    file_output = file_path_split[0] + ".cht"
    with open(file_output, 'w', encoding="utf-8", newline='\n') as f:
        cheat_cnt = 0
        for cheat in cheats:
            code_cnt = 0
            for code in cheat['code']:
                title = "cheat" + str(cheat_cnt)
                f.write( title + '_address = "0"\n')
                f.write( title + '_address_bit_position = "0"\n')
                f.write( title + '_big_endian = "false"\n')
                f.write( title + '_cheat_type = "1"\n')
                f.write( title + '_code = "' + code + '"\n')
                if len( cheat['code']) == 1:
                    f.write( title + '_desc = "' + cheat["desc"] + '"\n')
                else:
                    f.write( title + '_desc = "' + cheat["desc"] + '-' + str(code_cnt + 1) + '"\n')
                f.write( title + '_enable = "false"\n')
                f.write( title + '_handler = "0"\n')
                f.write( title + '_memory_search_size = "3"\n')
                f.write( title + '_repeat_add_to_address = "1"\n')
                f.write( title + '_repeat_add_to_value = "0"\n')
                f.write( title + '_repeat_count = "1"\n')
                f.write( title + '_rumble_port = "0"\n')
                f.write( title + '_rumble_primary_duration = "0"\n')
                f.write( title + '_rumble_primary_strength = "0"\n')
                f.write( title + '_rumble_secondary_duration = "0"\n')
                f.write( title + '_rumble_secondary_strength = "0"\n')
                f.write( title + '_rumble_type = "0"\n')
                f.write( title + '_rumble_value = "0"\n')
                f.write( title + '_value = "0"\n')
                code_cnt += 1
                cheat_cnt += 1
        f.write('cheats = "' + str(cheat_cnt) + '"\n')


# チートファイル変換
def convert_cht_file(file_path):
    print(f"convert_file: {file_path}")
    cheats = read_cheat_file(file_path)
    output_cheats(file_path, cheats)

    
if __name__ == "__main__": 
    file_path = "RetroArchCheartConverter/resource/input_md_cheat.txt"
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
    convert_cht_file(file_path)
    print("complete!!")