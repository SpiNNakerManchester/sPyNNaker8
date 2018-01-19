import re
import fileinput

line_regex = re.compile(r".*ca\s*=\s*(\S*).*$")
for s in fileinput.input():
    ls=line_regex.search(s)
    if (ls):
        print(ls.group(1))

