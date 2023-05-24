import sys
import ast
for line in sys.stdin:
    #print(type(line))
    res = ast.literal_eval(line)
    #print(res)
    #print(type(res))
    print(res["ip"][2])	