#!/usr/bin/env python3

'''TumblrScraper is a derived class of TemplateScraper for driving the twitter image scraper. This
image scraper will attempt to scrape any image off of any twitter profile using common known
methods to download those images.
'''

import os
import sys
import argparse

try:
    from scrapers.TemplateScraper import TemplateScraper
    from scrapers.ScraperDriver import ScraperDriver
except ImportError:
    from TemplateScraper import TemplateScraper
    from ScraperDriver import ScraperDriver


class TwitterScraper(TemplateScraper):
    """Twitter scraper class."""
    
    name = 'twitter'
    filename = os.path.basename(__file__)
    
    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, self.name, *args, **kwargs)
        self.log('name from TwitterScraper():', self.name)
    
    def parse_arguments(self):
        '''Get the arguments parser and add arguments to it. Then parse `args` with the parser
        definition defined in the base class to obtain an `options` dict.
        '''
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
        super().parse_arguments()
    
    @staticmethod
    def sub_parser(subparsers):
        '''A subparser is passed in as `subparsers`. Add a new subparser to the `subparsers` object
        then return that subparser. See `argparse.ArgumentsParser` for details.
        '''
        parser = subparsers.add_parser('twitter', help=('Invoke the twitter scraper to scrape '
                                                        'images off of twitter.com'))
        return parser
    
    def handle(self):
        '''Main class method that drives the work on scraping the images for this GenericScraper.
        '''
        self.write('Args:', self.args)
        self.write('Parser:', self.parser)
        self.write('Parsed options:', self.options)
        self.write('')
        self.write('This is the TwitterScraper.')


if __name__ == '__main__':
    # If TwitterScraper was invoked via the command line, initialize a driver and obtain the
    # TwitterScraper, then execute the main handle() method.
    
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = TwitterScraper(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
