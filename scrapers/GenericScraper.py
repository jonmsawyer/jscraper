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

class GenericScraper(TemplateScraper):
    """Generic scraper class."""
    
    name = 'generic'
    filename = os.path.basename(__file__)
    
    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, self.name, *args, **kwargs)
        self.log('name from GenericScraper():', self.name)
    
    def parse_arguments(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(prog=self.prog,
                                              description='Scrape a URI resource for images.')
        self.parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='GenericScraper-Z',
                                 help=('GenericScraper-extended base option.'))
        self.parser.add_argument('-V', metavar='V', type=str, dest='V', default='GenericScraper-V',
                                 help='GenericScraper-only option')
        super().parse_arguments(*args, **kwargs)
    
    @staticmethod
    def sub_parser(subparsers, *args, **kwargs):
        parser = subparsers.add_parser('generic',
                                       help=('Invoke the generic scraper to scrape images off '
                                             'of any URI resource. This is a general scraper '
                                             'and may not grab every image.'))
        return parser
    
    def handle(self, *args, **kwargs):
        self.write('Args:', self.args)
        self.write('Parser:', self.parser)
        self.write('Parsed options:', self.options)
        self.write('')
        self.write('This is the GenericScraper.')


if __name__ == '__main__':
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = GenericScraper(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
