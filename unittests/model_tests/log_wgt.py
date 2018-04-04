import re
import fileinput

line_regex1 = re.compile(r".*old_weight\s*:\s*(\S*)\s*new_weight\s*:\s*(\S*)")
line_regex2 = re.compile(r".*time\s*:\s*(\S*)")
s = raw_input()
is_weight = False
old_weights = []
new_weights = []
times = []
for s in fileinput.input():
    if not is_weight:
        ls=line_regex1.search(s)
        if (ls):
            old_weights.append(ls.group(1)),
            new_weights.append(ls.group(2)),
            is_weight=True
    else:
        ls = line_regex2.search(s)
        if (ls):
            times.append(ls.group(1))
            is_weight = False

for i in range(len(times)):
    print int(times[i])-1, old_weights[i]
    print times[i], new_weights[i]


