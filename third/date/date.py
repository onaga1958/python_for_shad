import re
import sys


valid_date = (r"((^(([0-9]{2}\.){2}[0-9]{4}|([0-9]{2}-){2}[0-9]{4}|" +
              "([0-9]{2}\/){2}[0-9]{4})$|^([0-9]{4}\.[0-9]{2}\.[0-9]" +
              "{2}|[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{4}\/[0-9]{2}\/" +
              "[0-9]{2})$)|^[0-9]{1,2}\s*([а-я]+)\s*[0-9]{4}$)")


delimiters = ['\.', '-', '\/']
possible_forms = (['([0-9]{2}' +
                   '{}'.format(d) +
                   '){2}[0-9]{4}'
                   for d in delimiters] +
                  ['[0-9]{4}(' +
                   '{}'.format(d) +
                   '[0-9]{2}){2}'
                   for d in delimiters] +
                  ['[0-9]{1,2}\s*[а-яё]+\s*[0-9]{4}'])


queries = [line.lower() for line in sys.stdin]

for query in queries:
    m = re.match(valid_date, query)
    if m is not None:
        print("YES")
    else:
        print("NO")
