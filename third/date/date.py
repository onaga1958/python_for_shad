import re
import sys

queries = [line for line in sys.stdin]
possible_forms = ['([0-9]{2}[-/.]){2}[0-9]{4}']
for query in queries:
    for form in possible_forms:
        m = re.search(form, query)
        if m.begin()
