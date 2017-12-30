#!/usr/bin/env python3

import sys
import argparse
from pprint import pprint

from scrapers.base import BaseScraper


class TwitterScraper(BaseScraper):
    """Twitter scraper class."""
    
    def __init__(self, *args, **kwargs):
        name = str(self.__class__).split("'")[1].split('.')[1]
        print('name from TwitterScraper():', name)
        super().__init__(name, *args, **kwargs)
    
    def parse_arguments(self, *args, **kwargs):
        super().parse_arguments(*args, **kwargs)
        parser = self.parser
        parser.add_argument('-VOODOO', metavar='Z', type=str, dest='VOODOO', default='TwitterScraper-VOODOO',
                            help='TwitterScraper-extended base option.')
    
    @staticmethod
    def sub_parser(subparsers, *args, **kwargs):
        new_parser = subparsers.add_parser('twitter', help=('Invoke the twitter scraper to scrape '
                                                            'images off of twitter.com'))
        new_parser.add_argument('--begin-date', metavar='BEGIN_DATE', type=str, dest='begin_date',
                                default='1970-01-01 00:00:00.00',
                                help=('TwitterScraper-only option. Download images that have their '
                                      'modification date to be greater than BEGIN_DATE'))
        new_parser.add_argument('--end-date', metavar='END_DATE', type=str, dest='end_date',
                                default='2099-12-12 23:59:59.999',
                                help=('TwitterScraper-only option. Download images that have their '
                                      'modification date to be less than END_DATE'))
        return new_parser
    
    def handle(self, *args, **kwargs):
        print('Args:', sys.argv)
        print('Parser:', self.parser)
        print('Scrapers:', self.scrapers)
        print('Parsed options:')
        pprint(self.options)
        print('')
        print('This is TwitterScraper.')
