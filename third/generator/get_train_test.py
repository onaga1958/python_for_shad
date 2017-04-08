import xml.etree.ElementTree as ET
from urllib.request import urlopen
import re


def try_to_clear(html):
    html = re.sub("<head>.*</head>", "", html, flags=re.DOTALL)
    html = re.sub('<pre>.*<pre>', '<pre><pre>', html)
    html = re.sub('<hr.*</body>', '</pre></pre></pre></body>', html, flags=re.DOTALL)
    html = re.sub('<ul>.*</ul>', '', html)
    html = re.sub('<a.*>.*</a>', '', html)
    html = re.sub('<Улицы"', '"Улицы"', html)
    return html


def to_space(matchobj):
    return ''.join([' ' for _ in matchobj.group(0)])


def url_to_file(url, out_file_name='page.html'):
    with urlopen(url) as conn:
        data = conn.read()
        html = data.decode('windows-1251')
        html = try_to_clear(html)

    with open(out_file_name, 'w') as f:
        print(html, file=f)

    return out_file_name


def get_text(html):
    tree = ET.parse(html)
    root = tree.getroot()

    body = get_child(root, tag='body')
    body = get_child(body, tag='pre')
    body = get_child(body, tag='pre')
    return body.text.strip()


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
    max_len = max(map(len, lines))
    lines = [line.strip() + ' ' if len(line) == max_len else line.strip() + '\n'
             for line in lines]

    return "".join(lines)


def main():
    urls2 = ['http://lib.ru/RUFANT/BELAEW/prodavec.txt',
             'http://lib.ru/RUFANT/BELAEW/ariel.txt',
             'http://lib.ru/RUFANT/BELAEW/island.txt']

    texts = []
    for url in urls2:
        html = url_to_file(url)
        text = get_text(html)
        texts.append(post_work(text))

    num_words = [len(text.split()) for text in texts]
    print('total words: {}'.format(sum(num_words)))

    with open('to_generator.txt', 'w') as f:
        print('generate --depth 3 --size 100', file=f)
        for text in texts:
            print(text, file=f)

if __name__ == '__main__':
    main()
