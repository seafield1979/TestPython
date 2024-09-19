import re

def line_func(line):
    re_title = re.compile('^#', re.UNICODE)
    if re_title.match(line):
        # print(f"title{line}")
        print(line.encode('unicode-escape'))



def read_file():
    with open('./resource/tengai2.txt', encoding="utf-8") as f:
        for line in f:
            line_func(line)


def read_file_all(file_path):
    try:
        with open(file_path, mode='r', encoding="utf-8") as f:
            text = f.read()
            print(text)
    except (FileNotFoundError, TypeError) :
        print('ファイルが開けませんでした:' + file_path)
    except:
        print('何らかのエラーが発生')

def write_to_file():
    with open('./resource/output2.txt', 'w') as fw:
        fw.write("a"+"\n")
        fw.write("a")
        fw.write("a")


# write_to_file()
read_file_all('resource/text1.txt')
