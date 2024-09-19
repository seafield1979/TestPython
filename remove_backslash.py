import re

def read_file():
    with open('./resource/tengai2_2.txt', 'w', encoding="utf-8") as fw:
        with open('./resource/tengai2_1.json', encoding="utf-8") as f:
            for line in f:
                line = line.replace('\\\\','\\')
                fw.write(line)
            

read_file()
