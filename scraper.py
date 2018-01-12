#!/usr/bin/env python3

import sys
from pprint import pprint

from scrapers.Scraper import Scraper


if __name__ == '__main__':
    print('{} (1) Args:'.format(__file__))
    pprint(sys.argv)
    scraper = Scraper(debug=True)
    print('{} (1) In __main__: scraper = '.format(__file__), scraper)
    
    print('{} (2) Args:'.format(__file__))
    pprint(sys.argv)
    scraper = scraper.get_scraper_class()()
    print('{} (2) In __main__: scraper = '.format(__file__), scraper)
    
    print('{} (3) Args:'.format(__file__))
    pprint(sys.argv)
    scraper.handle()
    print('{} (3) In __main__: scraper = '.format(__file__), scraper)
