
"""pywalled is a small scraping interface for 4walled.cc.

Usage: pywalled.py (-t TAGS) [-b BOARD] [-r RES]
                   [-t STYLE] [-f SFW] [-s SEARCH]

Options:
-h --help                     Show this message.
-t TAGS, --tags=TAGS          Keywords for search. For multiples, separate using comma with no space. Required.
-b BOARD, --board=BOARD       Which 4chan board to search. Accepts wg, hr, w, 7chan, all. Default is all
-r RES,--res=RES              Resolution. For multiple monitors use _
-t STYLE, --style=STYLE       exact, larger, or aspect. Default is larger.
-f SFW                        Force a SFW search. Options are Unrated, SFW, borderline, NSFW, all. Default all.
-s SEARCH, --search=SEARCH    Search type. Accepts search or random. Default is random.
"""


import os
import requests
from bs4 import BeautifulSoup
from docopt import docopt


def build_url(tags, board, res, style, sfw, search):
    base_url = 'http://4walled.cc/search.php?'

    if len(tags) > 1:
        tags = 'tags={}&'.format('+'.join(tags))
    else:
        tags = 'tags={}&'.format(tags[0])

    if board == 'wg':
        boardnum = 'board=2&'
    elif board == 'hr':
        boardnum = 'board=4&'
    elif board == 'w':
        boardnum = 'board=1&'
    elif board == '7chan':
        boardnum = 'board=3&'
    else:
        boardnum = 'board=&'
        print('Board not set, using default of \'All\'.')

    if not res:
        res = 'width_aspect=&'
        print('Resolution not set, using default of \'Any\'.')
    else:
        res = 'width_aspect={}&'.format(res)

    if not style:
        style = 'searchstyle=larger&'
        print('Style not set, using default of \'Equal|Greater\'')
    else:
        style = 'searchstyle={}&'.format(style)

    if sfw == 'unrated':
        sfwnum = 'sfw=-1&'
    elif sfw == 'sfw':
        sfwnum = 'sfw=0&'
    elif sfw == 'borderline':
        sfwnum = 'sfw=1&'
    elif sfw == 'nsfw':
        sfwnum = 'sfw=2&'
        print('NOTE: NSFW mode selected.')
    else:
        sfwnum = 'sfw=&'
        print('SFW not set, using default of \'All\'')

    if not search:
        search = 'search=random'
    else:
        search = 'search={}'.format(search)
        print('Search style not set, using default of \'Random\'')

    url = '{}{}{}{}{}{}{}'.format(base_url, tags, boardnum, res, style, sfwnum, search)
    return url


def get_show_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = []

    for link in soup.find_all('a'):
        ref = link.get('href')
        if 'show-' in ref:
            urls.append(ref)
    print('{} images found.'.format(len(urls)))
    return urls


def get_image_links(urls):
    image_links = []

    for link in urls:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.find_all('img'):
            image_links.append(item.get('src'))
    return image_links


def download_images(urls, tags):
    if not os.path.exists('./images'):
        os.mkdir('./images')
    for i, url in enumerate(urls):
        # this assumes 3-letter file extensions, may need fix if 4walled uses e.g. 'a.jpeg'
        filename = 'images/{}-{}.{}'.format(tags, i, url[-3:])
        print('Downloading {} to {}...'.format(url, filename))
        with open(filename, 'wb') as img:
            img.write(requests.get(url).content)


def main():
    args = docopt(__doc__)
    # print(args)

    tags = args['TAGS'].split(',')
    board = args['BOARD']
    res = args['RES']
    style = args['STYLE']
    sfw = args['SFW']
    search = args['SEARCH']

    url = build_url(tags, board, res, style, sfw, search)
    show_links = get_show_links(url)
    image_links = get_image_links(show_links)
    download_images(image_links, '_'.join(tags))


if __name__ == '__main__':
    main()
