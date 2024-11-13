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

class CHT:
    def __init__(self):
        self.comment = ""
        self.addr = 0       # アドレス
        self.value = 0      # 値
        self.code = 0       # 実行コード(WT,ADDなど MESENではWT以外対応していないためWT以外ならそのコードをスキップする)
        self.subcode_num = 0    # サブコード数
        self.enable = False # Enabled
        self.value_type = 1 # 数値(0:10進, 1:16進)
        self.size = 1       # サイズ(Byte)

    def write_to_bin(self, fw):
        fw.write(int.from_bytes(self.value, 'little', signed=False))

    def read_from_cht(self, fr, file_addr):
        # comment
        fr.seek(file_addr)
        bin_comment = fr.read(32)

        # bin_commentの\x00 以降に\x00以外が入るとデコードエラーになるため除去する
        flag1 = False
        bin_comment2 = bytearray()
        for b in bin_comment:
            if b == 0:
                if flag1 == False:
                    flag1 = True
                else:
                    break
            bin_comment2.append(b)

        self.comment = bin_comment2.decode(encoding='sjis')
        self.comment = self.comment.replace('\x00','')

        # addr
        fr.seek(file_addr + 0x24)
        bin_addr = fr.read(4)
        self.addr = int.from_bytes(bin_addr, 'little', signed=False)
        
        # value
        fr.seek(file_addr + 0x28)
        bin_value = fr.read(4)
        self.value = int.from_bytes(bin_value, 'little', signed=False)
        
        # code
        fr.seek(file_addr + 0x2C)
        bin_code = fr.read(4)
        self.code = int.from_bytes(bin_code, 'little', signed=False)

        # subcode_num
        fr.seek(file_addr + 0x30)
        bin_subcode = fr.read(4)
        self.subcode_num = int.from_bytes(bin_subcode, 'little', signed=False)

        # enable
        fr.seek(file_addr + 0x34)
        bin_enable = fr.read(1)
        self.enable = int.from_bytes(bin_enable, 'little', signed=False) == 1

        # value_type
        fr.seek(file_addr + 0x35)
        bin_value_type = fr.read(1)
        self.value_type = int.from_bytes(bin_value_type, 'little', signed=False)

        # size
        fr.seek(file_addr + 0x36)
        bin_size = fr.read(1)
        self.size = int.from_bytes(bin_size, 'little', signed=False)

        if self.code == 0 and self.addr <= 0xffff:
            return (True, 55)
        else:
            return (False, (1+self.subcode_num) * 55)
        
    def output_json(self, code_json):
        output = {}
        output['Description'] = self.comment.encode('unicode-escape').decode('utf-8')
        output['Type'] = 'NesCustom'
        output['Enabled'] = False # self.enable
        code_str = ""
        for i in range(self.size):
            if i > 0:
                code_str += '\\r\\n'
            value1 = self.value >> (8 * i) & 0xff
            code_str += "{:04X}:{:02X}".format(self.addr + i, value1 )
        output['Codes'] = code_str
        code_json.append(copy.copy(output))

def convert_cht_file(file_path):
    root_ext_pair = os.path.splitext(file_path)
    if len(root_ext_pair) >= 2:
        if root_ext_pair[1] != '.cht':
            print("file extension isn't 'cht'")
            return

    with open(file_path, 'rb') as fr:
        # ヘッダー部分
        fr.seek(4)
        code_num = int.from_bytes(fr.read(4), 'little', signed=False)
        
        # コード部
        code_list = []
        addr = 16
        for i in range(code_num):
            code = CHT()
            ret = code.read_from_cht(fr, addr)
            if ret[0] == True:
                code_list.append(copy.copy(code))
            addr += ret[1]
        
        # cht用のデータを作成
        code_cht = []
        index = 0
        output = "cheats = " + str(len(code_list)) + "\r\n"
        for code in code_list:
            output += "cheat" + str(index) + "_desc = " + '"' + code.comment + '"' + "\r\n"
            code_str = ""
            for i in range(code.size):
                if i > 0:
                    code_str += '+'
                value1 = code.value >> (8 * i) & 0xff
                code_str += "{:04X}:{:02X}".format(code.addr + i, value1 )
            output += "cheat" + str(index) + "_code = " + '"' + code_str + '"' + "\r\n"
            output += "cheat" + str(index) + "_enable = false" + "\r\n"
            index += 1
        
        dirname1 = os.path.dirname(file_path)

        # 出力先のフォルダ作成
        dirname2 = dirname1 + "/output"
        if not os.path.exists(dirname2):
            # ディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(dirname2)

        # ファイルパスから拡張子部分を分離
        # ./resource/tengai2.txt -> [0]: "./resource/tengai2", [1]: ".txt"
        file_path_split = os.path.splitext(file_path)
        filename =  os.path.splitext(os.path.basename(file_path))[0]
        if len(file_path_split) >= 2:
            file_output = dirname2 + "/" + filename + ".cht"
            with open(file_output, 'w') as fw:
                fw.write(output)

if __name__ == "__main__": 
    convert_cht_file('./nesterj_cht/うしおととら 深淵の大妖.cht')
    print('complete')