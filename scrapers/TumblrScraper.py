#!/usr/bin/env python3

import os
import sys
import argparse
from pprint import pformat

try:
    from scrapers.TemplateScraper import TemplateScraper
except ImportError:
    from TemplateScraper import TemplateScraper
try:
    from scrapers.ScraperDriver import ScraperDriver
except ImportError:
    from ScraperDriver import ScraperDriver

class TumblrScraper(TemplateScraper):
    """Tumblr scraper class."""
    
    name = 'tumblr'
    filename = os.path.basename(__file__)
    
    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, self.name, *args, **kwargs)
        self.log('name from TumblrScraper():', self.name)
    
    def parse_arguments(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(prog=self.prog,
                                              description='Scrape a URI resource for images.')
        self.parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='TumblrScraper-Z',
                                 help='TumblrScraper-extended base option.')
        self.parser.add_argument('--count', metavar='COUNT', type=int, dest='count',
                                 default=1000,
                                 help=('TumblrScraper-only option. Download at most COUNT images '
                                       'from each blog.'))
        super().parse_arguments(*args, **kwargs)
    
    @staticmethod
    def sub_parser(subparsers, *args, **kwargs):
        parser = subparsers.add_parser('tumblr',
                                       help=('Invoke the tumblr scraper to scrape images off '
                                             'of tumblr.com'))
        return parser
    
    def handle(self, *args, **kwargs):
        self.write('Args:', self.args)
        self.write('Parser:', self.parser)
        self.write('Parsed options:', self.options)
        self.write('')
        self.write('This is the TumblrScraper.')


if __name__ == '__main__':
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = TumblrScraper(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
