import re
import fileinput

line_regex1 = re.compile(r".*new_weight\s*:\s*(\S*)")
line_regex2 = re.compile(r".*time\s*:\s*(\S*)")
s = raw_input()
is_weight = False
for s in fileinput.input():
    if not is_weight:
        ls=line_regex1.search(s)
        if (ls):
            print(ls.group(1)),
            is_weight=True
    else:
        ls = line_regex2.search(s)
        if (ls):
            print(ls.group(1))
            is_weight = False


