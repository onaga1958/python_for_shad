import re
import sys

lines = [line.strip() for line in sys.stdin]

modules = set()

for line in lines:
    matches = re.finditer("from +([a-zA-Z\.]+) +import", line)
    for m in matches:
        modules.add(m.group(1))
        line = line.replace(m.group(0), '')

    matches = re.finditer("import +([a-zA-Z\.]+(, +[a-zA-Z\.]+)*)", line)
    for m in matches:
        for module in m.group(1).split(","):
            modules.add(module.strip())

print(", ".join([s for s in sorted(modules)]))
