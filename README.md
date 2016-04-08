# pywalled
Command line interface to download images from 4walled.cc.

Requirements
---
- Python 3, pip3
- Docopt 0.6.1
- BeautifulSoup4


Installation
----
You can use pip to install both docopt and beautifulsoup4:

`pip3 install docopt beautifulsoup4`

And run using python:

`$>python3.5 pywalled.py [options]`

Usage
---
The available usage options are:

```
Usage: pywalled.py (-t <TAGS>) [-b BOARD] [-r RES]
                   [-y STYLE] [-f SFW] [-s SEARCH]

Options:
-h --help                     Show this message and exit.
-t TAGS, --tags=<TAGS>        Keywords for search. For multiples, separate using comma with no space.
                              Required, no default.
-b BOARD, --board=BOARD       Which 4chan board to search. Accepts wg, hr, w, 7chan, all. [default: all]
-r RES, --res=RES             Resolution. For multiple monitors use __. [default: any]
-y STYLE, --style=STYLE       exact, larger, or aspect. [default: larger]
-f SFW                        Force a SFW search. Options are Unrated, SFW, borderline, NSFW, all. [default: all]
-s SEARCH, --search=SEARCH    Search type. Accepts search or random. [default: random]
```

Alternatively, you can access this menu by using the `-h` or `--help` flags:

`$>python3.5 pywalled.py --help`
