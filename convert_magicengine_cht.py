# Magic Engineのチートを

import copy
import re
import sys
import json
import os
import traceback

def convert_cht_file(file_path, fw):
    root_ext_pair = os.path.splitext(file_path)
    if len(root_ext_pair) >= 2:
        if root_ext_pair[1] != '.txt':
            print("file extension isn't 'txt'")
            return
    
    # basename1: 拡張子なしのファイル名
    file_path_split = os.path.splitext(file_path)
    basename1 =  os.path.splitext(os.path.basename(file_path))[0]
    
    output = "## " + basename1 + "\r\n"
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            # { +, 1, 0, 1, 0xF800C5, 255, "gold" } のような行の
            # 3つめ アドレス
            # 4つめ 値
            # 5つめ 説明
            # を取得する
            line = line.rstrip("} \n")
            params = line.split(',')
            if len(params) >= 7:
                addr = params[4].lstrip(" 0x")
                value = "{:02X}".format(int(params[5]))
                desc = params[6].strip(' "').strip('"')
                output += "{}\t{}:{}\r\n".format(desc, addr, value)
        
        fw.write(output)
        fw.write("\r\n")

if __name__ == "__main__":
    with open('./magic_engine/pce_cheats.txt', 'w') as fw:
        convert_cht_file('./magic_engine/ワルキューレの伝説 (J)_A3303978.txt', fw)
        print('complete!!')