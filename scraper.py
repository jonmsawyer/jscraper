#!/usr/bin/env python3

import sys
from pprint import pprint

from scrapers.Scraper import Scraper


if __name__ == '__main__':
    print('(1) Args:')
    pprint(sys.argv)
    scraper = Scraper()
    print('(1) In __main__: scraper = ', scraper)
    
    print('(2) Args:')
    pprint(sys.argv)
    scraper = scraper.get_scraper_class()()
    print('(2) In __main__: scraper = ', scraper)
    
    print('(3) Args:')
    pprint(sys.argv)
    scraper.handle()
    print('(3) In __main__: scraper = ', scraper)
