import sys
import json
import os
import traceback

class SnesCheat:
    def __init__(self):
        self.name1 = ""
        self.code1 = ""

    def output_json(self):
        output = {}
        output['Description'] = self.name1.encode('unicode-escape').decode('utf-8')
        output['Type'] = "SnesProActionReplay"
        output['Enabled'] = False
        output['Codes'] = self.code1.replace(' + ', '\r\n').replace('=','').upper()
        return output


def is_utf8_file_with_bom(filename):
    '''utf-8 ファイルが BOM ありかどうかを判定する
    '''
    line_first = open(filename, encoding='utf-8').readline()
    return (line_first[0] == '\ufeff')


def open_file_with_utf8(filename):
    # utf-8 のファイルを BOM ありかどうかを自動判定して読み込む
    is_with_bom = is_utf8_file_with_bom(filename)
    encoding = 'utf-8-sig' if is_with_bom else 'utf-8'
    return open(filename, encoding=encoding).read()


def read_snes9x_cht(file_path):
    #with open(file_path, encoding="utf-8") as f:
    cheat1 = None
    list1 = []    
    lines = open_file_with_utf8(file_path).split('\n')
    for line in lines:
        line = line.replace('\n', '')
        if line == 'cheat':
            if cheat1 is None:
                cheat1 = SnesCheat()
        elif line == '':
            if cheat1 is not None:
                list1.append(cheat1)
                cheat1 = None
        else:
            line2 = line.strip()
            splitted = line2.split(':')
            if len(splitted) >= 2:
                data1 = splitted[1].strip()
                if splitted[0] == 'name':
                    cheat1.name1 = data1
                elif splitted[0] == 'code':
                    cheat1.code1 = data1
    return list1
    

# SNES9xのチートをMESEN形式で出力する
# param[in] SNES9x形式(SnesCheat)のリスト
# return json形式の文字列
def output_mesen_json(snes9x_cheats):
    mesen_cheats = []
    output = ""
    for cheat1 in snes9x_cheats:
        mesen_cheats.append(cheat1.output_json())

    cheats = {'Cheats':mesen_cheats}
    json_str = json.dumps(cheats, ensure_ascii=False, indent=4)
    for line in json_str.split('\n'):
        line = line.replace('\\\\','\\')
        output += line + '\n'
    return output

# SNES9xの.chtファイルを MESENの.jsonファイルに変換する
def convert_cht_file(file_path):
    cheats = read_snes9x_cht(file_path)
    mesen_json = output_mesen_json(cheats)

    # ファイルパスから拡張子部分を分離
    # ./resource/snes9x.cht -> [0]: "./resource/snes9x", [1]: ".cht"
    file_path_split = os.path.splitext(file_path)
    if len(file_path_split) >= 2:
        file_output = file_path_split[0] + ".json"
        with open(file_output, 'w') as fw:
            fw.write(mesen_json)
    

if __name__ == "__main__":
    convert_cht_file('./resource/Mother 2.cht')
    print('ok')
    print('complete')