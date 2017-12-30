#!/usr/bin/env python3

import sys
import imp
from pprint import pprint
import argparse

from .base import BaseScraper

SCRAPERS = ( 
    'scrapers.GenericScraper.GenericScraper',
    'scrapers.TumblrScraper.TumblrScraper',
    'scrapers.TwitterScraper.TwitterScraper',
)

def import_from_dotted_path(dotted_names, path=None):
    """ import_from_dotted_path('foo.bar') -> from foo import bar; return bar """
    next_module, remaining_names = dotted_names.split('.', 1)
    fp, pathname, description = imp.find_module(next_module, path)
    module = imp.load_module(next_module, fp, pathname, description)
    if hasattr(module, remaining_names):
        return getattr(module, remaining_names)
    if '.' not in remaining_names:
        return module
    return import_from_dotted_path(remaining_names, path=module.__path__)

class Scraper(BaseScraper):
    """Scraper class."""
    
    def __init__(self, *args, **kwargs):
        name = str(self.__class__).split('.')[1].split()[0]
        print('name from Scraper():', name)
        super().__init__(name, no_help=True, *args, **kwargs)
    
    def parse_arguments2(self, *args, **kwargs):
        prog = '{} {}'.format(list(sys.argv)[0], self.scraper_type)
        prog = prog.strip()
        print('prog:', prog)
        self.parse_args = ['scraper'] + list(sys.argv)[1:]
        self.parser = argparse.ArgumentParser(prog=prog,
                                              description='Scrape a URI resource for image.')
        print('before Scraper self.get_subparsers()')
        self.get_subparsers()
        print('after Scraper self.get_subparsers()')

    def get_subparsers(self, *args, **kwargs):
        print('in get_subparsers()')
        print('SCRAPERS:')
        pprint(SCRAPERS)
        subparsers = self.parser.add_subparsers(dest='scraper',
                                                description=('Description text goes here...'),
                                                help=('Invoke a particular scraper designed for '
                                                      'specific URI resources.'))
        for scraper in SCRAPERS:
            print('Importing {}... '.format(scraper), end='')
            cls = import_from_dotted_path(scraper)
            self.scrapers.update({scraper: cls})
            print('Done! Imported {}'.format(cls))
            cls.sub_parser(subparsers)
        print('self.scrapers:')
        pprint(self.scrapers)
    
    def get_scraper_class(self, *args, **kwargs):
        print('In get_scraper()')
        print('self.options = ')
        pprint(self.options)
        scraper = self.options.get('scraper')
        if scraper == 'generic':
            return self.scrapers.get('scrapers.GenericScraper.GenericScraper')
        elif scraper == 'tumblr':
            return self.scrapers.get('scrapers.TumblrScraper.TumblrScraper')
        elif scraper == 'twitter':
            return self.scrapers.get('scrapers.TwitterScraper.TwitterScraper')
        else:
            return self.__class__
    
    def handle(self, *args, **kwargs):
        print('Args:', sys.argv)
        print('Parser:', self.parser)
        print('Scrapers:', self.scrapers)
        print('Parsed options:')
        pprint(self.options)
        print('')
        print('This is just Scraper.')
