import pathlib
import glob
import os
import sys
import traceback

import convert_nesterj_text

def tree(path, fw, layer=0, is_last=False, indent_current='　'):
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())

    # カレントディレクトリの表示
    current = path.split('/')[::-1][0]
    
    # 下の階層のパスを取得
    paths = [p for p in glob.glob(path+'/*') if os.path.isdir(p) or os.path.isfile(p)]
    def is_last_path(i):
        return i == len(paths)-1

    # 直下のファイルのみ処理
    for i, p in enumerate(paths):

        indent_lower = indent_current
        if layer != 0:
            indent_lower += '　　' if is_last else '│　'

        if os.path.isfile(p):
            if p.endswith('.cht'):
                try:
                    print(os.path.basename(p))
                    convert_nesterj_text.convert_cht_file(p,fw)
                except Exception as e:
                    t, v, tb = sys.exc_info()
                    print(traceback.format_exception(t,v,tb))
                    print(traceback.format_tb(e.__traceback__))
        
        # if os.path.isdir(p):
        #     tree(p, layer=layer+1, is_last=is_last_path(i), indent_current=indent_lower)


with open('./nesterj_cht_all/cheats.txt', 'w') as fw:
    tree("./nesterj_cht_all/", fw)
    print("complete!!")