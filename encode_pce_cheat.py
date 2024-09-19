import re
import sys
import json
import os

def print_cheat1(cheat, fw):
    fw.write(cheat['Description'] + '\n')
    fw.write(cheat['Codes'] + '\n')


def print_cheat_all(cheats, fw):
    for cheat1 in cheats: 
        print_cheat1(cheat1, fw)


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


def main(file_path):
    output = []
    cheat1 = {"Description":"", "Type": "PceAddress", "Enabled": False, "Codes":""}
    code_list = []
    re_title = re.compile('^\s*\*', re.UNICODE)

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip('\n')
            if re_title.match(line):
                if len(code_list) > 0:
                    cheat1['Codes'] = encode_code_list(code_list)
                    output.append(cheat1.copy())
                    code_list.clear()
                # 先頭の"*"とスペースを除去
                line = line.lstrip()
                line = line.lstrip('*')
                title = line.encode('unicode-escape').decode('utf-8')
                cheat1['Description'] = title
            else:
                # 空行は無視
                # F81250:FF のようなコード行を取得する
                line2 = line.strip()
                if len(line2) >= 8:
                    code_list.append(line2)
    if len(cheat1['Description']) > 0:
        cheat1['Codes'] = encode_code_list(code_list)
        output.append(cheat1.copy())

    return output


file_path = "./resource/tengai2.txt"
if len(sys.argv) >= 2:
    file_path = sys.argv[1]
else:
    print("no input json file")
    sys.exit(0)

cheats = main(file_path)

# with open('./resource/output1.txt', 'w', encoding="utf-8") as fw:
#     print_cheat_all(cheats, fw)
cheats2 = {'Cheats':cheats}

json_str = json.dumps(cheats2, ensure_ascii=False, indent=4)
output = ""
for line in json_str.split('\n'):
    line = line.replace('\\\\','\\')
    output += line + '\n'

# ファイルパスから拡張子部分を分離
# ./resource/tengai2.txt -> [0]: "./resource/tengai2", [1]: ".txt"
file_path_split = os.path.splitext(file_path)
if len(file_path_split) >= 2:
    file_output = file_path_split[0] + ".json"
    with open(file_output, 'w', encoding="utf-8") as f:
        f.write(output)
else:
    print("error 2")

print("complete!!")