import re
import sys


forms = ['([0-9]{2}\.){2}[0-9]{4}',
         '([0-9]{2}\/){2}[0-9]{4}',
         '([0-9]{2}-){2}[0-9]{4}',
         '[0-9]{4}(\.[0-9]{2}){2}',
         '[0-9]{4}(\/[0-9]{2}){2}',
         '[0-9]{4}(-[0-9]{2}){2}',
         '[0-9]{1,2}\s*([а-я]+)\s*[0-9]{4}']

valid_date = '^(' + '|'.join(forms) + ')$'

queries = [line.lower() for line in sys.stdin]

for query in queries:
    m = re.match(valid_date, query)
    if m is not None:
        print("YES")
    else:
        print("NO")
