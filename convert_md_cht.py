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
    
    output = basename1
    with open(file_path, encoding="sjis") as f:
        for line in f:
            # FF2E63:0064	1P側体力 のような行の
            # 左右の項目を入れ替える
            line = line.rstrip("} \n")
            params = line.split("\t")
            if len(params) >= 2:
                output += "\t{}\t{}\r\n".format(params[1],params[0])
            
        fw.write(output)

if __name__ == "__main__":
    with open('./genesis/md_cheat.txt', 'w') as fw:
        convert_cht_file('./genesis/ああ播磨灘.txt', fw)
        print('complete!!')