#!/usr/bin/env python3

import sys
import argparse
from pprint import pprint

from scrapers.base import BaseScraper


class TumblrScraper(BaseScraper):
    """Tumblr scraper class."""
    
    def parse_arguments(self, *args, **kwargs):
        super().parse_arguments(*args, **kwargs)
        parser = self.parser
        parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='TumblrScraper-Z',
                            help='TumblrScraper-extended base option.')
    
    @staticmethod
    def sub_parser(subparsers, *args, **kwargs):
        new_parser = subparsers.add_parser('tumblr', help='tumblr help')
        new_parser.add_argument('--count', metavar='COUNT', type=int, dest='count',
                                default=1000,
                                help=('TumblrScraper-only option. Download at most COUNT images '
                                      'from each blog.'))
        return new_parser
    
    def handle(self, *args, **kwargs):
        print('Args:', sys.argv)
        print('Parser:', self.parser)
        print('Scrapers:', self.scrapers)
        print('Parsed options:')
        pprint(self.options)
        print('')
        print('This is the TumblrScraper.')