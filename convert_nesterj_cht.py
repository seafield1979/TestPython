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
# 	0x0044	1	0:無効, 1:有効
# 	0x0045	1	数値(0:10進,1:16進)
# 	0x0046	1	サイズ(1:1Byte, 2:2Byte, 3:3Byte, 4:4Byte)
import copy
import re
import sys
import json
import os

class CHT:
    def __init__(self):
        self.comment = ""
        self.addr = 0
        self.value = 0
        self.code = 0
        self.enable = False
        self.value_type = 1
        self.size = 1

    def write_to_bin(self, fw):
        fw.write(int.from_bytes(self.value, 'little', signed=False))

    def read_from_cht(self, fr, file_addr):
        # 0x00 comment
        fr.seek(file_addr)
        bin_comment = fr.read(32)
        self.comment = bin_comment.decode(encoding='sjis')
        self.comment = self.comment.replace('\x00','')

        # 0x24 addr
        fr.seek(file_addr + 0x24)
        bin_addr = fr.read(4)
        self.addr = int.from_bytes(bin_addr, 'little', signed=False)
        
        fr.seek(file_addr + 0x28)
        bin_value = fr.read(4)
        self.value = int.from_bytes(bin_value, 'little', signed=False)
        
        fr.seek(file_addr + 0x2C)
        bin_code = fr.read(4)
        self.code = int.from_bytes(bin_code, 'little', signed=False)

        fr.seek(file_addr + 0x34)
        bin_enable = fr.read(1)
        self.enable = int.from_bytes(bin_enable, 'little', signed=False) == 1

        fr.seek(file_addr + 0x35)
        bin_value_type = fr.read(1)
        self.value_type = int.from_bytes(bin_value_type, 'little', signed=False)

        fr.seek(file_addr + 0x36)
        bin_size = fr.read(1)
        self.size = int.from_bytes(bin_size, 'little', signed=False)

    def output_json(self, code_json):
        output = {}
        for i in range(self.size):
            output['Description'] = self.comment.encode('unicode-escape').decode('utf-8')
            if self.size > 1:
                output['Description'] += "-" + str(i+1)
            output['Type'] = 'NesCustom'
            output['Enabled'] = False # self.enable
            value1 = self.value >> (8 * i) & 0xff
            output['Codes'] = "{:04X}:{:02X}".format(self.addr + i, value1 )
            code_json.append(copy.copy(output))
        

def main(file_path):
    print('main')
    with open(file_path, 'rb') as fr:
        # ヘッダー部分
        fr.seek(4)
        code_num = int.from_bytes(fr.read(4), 'little', signed=False)
        
        print(f"code_num: {code_num}")
        #print(int.from_bytes(number_bin, 'little', signed=False))
        
        # コード部
        code_list = []
        addr = 16
        for i in range(code_num):
            print(i)
            code = CHT()
            code.read_from_cht(fr, addr)
            code_list.append(copy.copy(code))
            addr += 55
        print("end")

        # json用のデータを作成
        code_json = []
        for code in code_list:
            code.output_json(code_json)
            
        cheats = {'Cheats':code_json}
        json_str = json.dumps(cheats, ensure_ascii=False, indent=4)
        output = ""
        for line in json_str.split('\n'):
            line = line.replace('\\\\','\\')
            output += line + '\n'

        # ファイルパスから拡張子部分を分離
        # ./resource/tengai2.txt -> [0]: "./resource/tengai2", [1]: ".txt"
        file_path_split = os.path.splitext(file_path)
        if len(file_path_split) >= 2:
            file_output = file_path_split[0] + ".json"
            with open(file_output, 'w') as fw:
                fw.write(output)


main('./resource/nesterj_cheat.cht')
print('complete')