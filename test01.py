import sys

def func1(arg1):
    print(f"func1:{arg1}")
    print("func1:" + arg1)


def func2():
    print("func2")
    a = 100
    b = 200
    c = 10
    print(hex(a) + hex(b) + hex(c))
    print("{:08X}{:08X}{:08X}".format(a, b, c))
    num1 = 10
    num2 = 100
    print("{:04X}{:08X}".format(num1, num2))

def func_format():
    number1 = 0x112233
    print(f"{number1:08X}")
    print("{:08X}".format(0x112233))    # 00112233


def func_list():
    list1 = []
    list1.append("aaa")
    list1.append("bbb")
    list1.append("ccc")
    cheat1 = {"title":"title1"}
    cheat1["list"] = list1
    for str1 in list1:
        print(str1)

func_format()
# print('hello world')
# a=1
# b="str1"
# print(str(a) + b)
# func1('aaa')
# func2()
# func_list()
# for arg in sys.argv:
#     print(arg)

# with open('./resource/tengai2.txt', encoding="utf-8") as fr:
#     with open('./resource/output1.txt', 'w', encoding="utf-8") as fw:
#         for line in fr:
#             title = line.encode('unicode-escape').decode('utf-8')
#             fw.write(title + '\n')