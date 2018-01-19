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


class TwitterScraper(TemplateScraper):
    """Twitter scraper class."""
    
    name = 'twitter'
    filename = os.path.basename(__file__)
    
    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, self.name, *args, **kwargs)
        self.log('name from TwitterScraper():', self.name)
    
    def parse_arguments(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(prog=self.prog,
                                              description='Scrape a URI resource for images.')
        self.parser.add_argument('-VOODOO', metavar='Z', type=str, dest='VOODOO',
                                 default='TwitterScraper-VOODOO',
                                 help='TwitterScraper-extended base option.')
        self.parser.add_argument('--begin-date', metavar='BEGIN_DATE', type=str, dest='begin_date',
                                 default='1970-01-01 00:00:00.00',
                                 help=('TwitterScraper-only option. Download images that have '
                                       'their modification date to be greater than BEGIN_DATE'))
        self.parser.add_argument('--end-date', metavar='END_DATE', type=str, dest='end_date',
                                default='2099-12-12 23:59:59.999',
                                help=('TwitterScraper-only option. Download images that have '
                                      'their modification date to be less than END_DATE'))
        super().parse_arguments(*args, **kwargs)
    
    @staticmethod
    def sub_parser(subparsers, *args, **kwargs):
        parser = subparsers.add_parser('twitter', help=('Invoke the twitter scraper to scrape '
                                                        'images off of twitter.com'))
        return parser
    
    def handle(self, *args, **kwargs):
        self.write('Args:', self.args)
        self.write('Parser:', self.parser)
        self.write('Parsed options:', self.options)
        self.write('')
        self.write('This is the TwitterScraper.')


if __name__ == '__main__':
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = TwitterScraper(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
