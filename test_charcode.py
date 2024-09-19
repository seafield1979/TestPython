import re
import sys
import json
import os

bin1 = b'\x8E\x63\x8B\x40\x8C\xB8\x82\xE7\x82\xC8\x82\xA2'
text1 = bin1.decode(encoding='sjis')
print(text1)

unicode1 = text1.encode('unicode-escape').decode('utf-8')
print(unicode1)