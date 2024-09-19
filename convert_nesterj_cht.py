# NNNesterJのchtファイルをMESEN2のチートjsonファイルに変換

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

    def read_from_cht(self, fr):
        number_bin = fr.read(4)


def main():
    print('main')
    with open('./resource/nesterj_cheat.cht', 'rb') as fr:
        # ヘッダー部分
        fr.seek(fr.tell()+4)

        code_num = int.from_bytes(fr.read(4), 'little', signed=False)
        fr.seek(fr.tell()+4)
        
        print(f"code_num: {code_num}")
        #print(int.from_bytes(number_bin, 'little', signed=False))

        for i in range(code_num):
            print(i)


main()