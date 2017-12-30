#!/usr/bin/env python3

import sys
import argparse
from pprint import pprint

from scrapers.base import BaseScraper


class GenericScraper(BaseScraper):
    """Generic scraper class."""
    
    def __init__(self, *args, **kwargs):
        name = str(self.__class__).split("'")[1].split('.')[1]
        print('name from GenericScraper():', name)
        super().__init__(name, *args, **kwargs)
    
    def parse_arguments(self, *args, **kwargs):
        super().parse_arguments(*args, **kwargs)
        parser = self.parser
        parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='GenericScraper-Z',
                            help='GenericScraper-extended base option.')
    
    @staticmethod
    def sub_parser(subparsers, *args, **kwargs):
        new_parser = subparsers.add_parser('generic', help=('Invoke the generic scraper to scrape '
                                                            'images off of any URI resource. This '
                                                            'is a general scraper and may not '
                                                            'grab every image.'))
        new_parser.add_argument('-V', metavar='V', type=str, dest='V', default='GenericScraper-V',
                               help='GenericScraper-only option')
        return new_parser
    
    def handle(self, *args, **kwargs):
        print('Args:', sys.argv)
        print('Parser:', self.parser)
        print('Scrapers:', self.scrapers)
        print('Parsed options:')
        pprint(self.options)
        print('')
        print('This is the GenericScraper.')
