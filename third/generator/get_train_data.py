import xml.etree.ElementTree as ET
from urllib.request import urlopen
import re


def clear_html(html):
    html = re.sub("<head>.*</head>", "", html, flags=re.DOTALL)
    html = re.sub('<pre>.*<pre>', '<pre><pre>', html)
    html = re.sub('<hr.*</body>', '</pre></pre></pre></body>',
                  html, flags=re.DOTALL)
    html = re.sub('<ul>.*</ul>', '', html)
    html = re.sub('<a.*>.*</a>', '', html)
    html = re.sub('<Улицы"', '"Улицы"', html)
    html = re.sub('---+', '', html)
    html = re.sub('.*pell.*', '', html)
    return html


def to_space(matchobj):
    return ''.join([' ' for _ in matchobj.group(0)])


def change(matchobj):
    pattern = matchobj.group(0)
    change_dict = {'а': 'б', 'б': 'в', 'в': 'ч', 'г': 'з', 'д': 'д',
                   'е': 'е', 'ж': 'ц', 'з': 'ъ', 'и': 'й', 'й': 'к',
                   'к': 'л', 'л': 'м', 'м': 'н', 'н': 'о', 'о': 'п',
                   'п': 'р', 'р': 'т', 'с': 'у', 'т': 'ф', 'у': 'х',
                   'ф': 'ж', 'х': 'и', 'ц': 'г', 'ч': 'ю', 'ш': 'ы',
                   'щ': 'э', 'ъ': 'я', 'ы': 'щ', 'ь': 'ш', 'э': 'ь',
                   'ю': 'а', 'я': 'с', 'ё': 'ё'}

    right_dict = {}
    for key, value in change_dict.items():
        right_dict[value] = key

    if pattern.islower():
        return right_dict[pattern].upper()
    else:
        return right_dict[pattern.lower()]


def change_letters(html):
    return re.sub('[а-яёА-ЯЁ]', change, html)


def url_to_file(url, begin, out_file_name='page.html'):
    with urlopen(url) as conn:
        data = conn.read()
        html = data.decode('windows-1251')

        if len(re.findall(begin, html[:500])) == 0:
            html = change_letters(html)

        html = clear_html(html)

    with open(out_file_name, 'w') as f:
        print(html, file=f)

    return out_file_name


def get_text(html, begin):
    try:
        tree = ET.parse(html)
    except ET.ParseError:
        return None
    root = tree.getroot()

    body = get_child(root, tag='body')
    body = get_child(body, tag='pre')
    body = get_child(body, tag='pre')

    text = body.text.strip()
    if re.match(begin, text) is None:
        return None
    else:
        return text


def get_child(body, child_attrib=None, attrib=None, tag='div'):
    for child in body:
        if (child.tag == tag and
            (attrib is None or (
             attrib in child.attrib and
             child.attrib[attrib][:len(child_attrib)] == child_attrib))):
            return child


def post_work(text):
    max_len = 0
    lines = [line.rstrip() for line in text.split('\n')]
    max_len = max(map(len, lines[:100]))
    lines = [line.strip() + ' '
             if len(line) == max_len
             else line.strip() + '\n'
             for line in lines]

    return "".join(lines)


def main():
    urls = ['http://lib.ru/RUFANT/BELAEW/prodavec.txt',
            'http://lib.ru/RUFANT/BELAEW/ariel.txt',
            'http://lib.ru/RUFANT/BELAEW/star_kec.txt',
            'http://lib.ru/RUFANT/BELAEW/doul.txt',
            'http://lib.ru/RUFANT/BELAEW/island.txt',
            'http://lib.ru/RUFANT/BELAEW/manfound.txt',
            'http://lib.ru/RUFANT/BELAEW/hojti.txt',
            'http://lib.ru/RUFANT/BELAEW/lordwrld.txt',
            'http://lib.ru/RUFANT/BELAEW/man-amhp.txt',
            'http://lib.ru/RUFANT/BELAEW/undwater.txt',
            'http://lib.ru/RUFANT/BELAEW/oko.txt']

    valid_begins = ['"Окаянный', 'Посвящаю', 'Авт', 'Констан', 'Большой',
                    'Снежная', 'Огромный', '- Не брызгайте', 'Наступила',
                    '- Жан', 'Книга']
    texts = []
    for url, begin in zip(urls, valid_begins):
        html = url_to_file(url, begin)
        text = get_text(html, begin)
        if text is None:
            continue
        texts.append(post_work(text))

    num_words = [len(text.split()) for text in texts]
    print('total words: {}'.format(sum(num_words)))

    with open('to_generator.txt', 'w') as f:
        print('generate --depth 2 --size 100', file=f)
        for text in texts:
            print(text, file=f)

# if __name__ == '__main__':
#     main()
