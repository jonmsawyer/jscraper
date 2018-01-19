#!/usr/bin/env python3

'''TumblrScraper is a derived class of TemplateScraper for driving the tumblr image scraper. This
image scraper will attempt to scrape any image off of any tumblr blog.
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

class TumblrScraper(TemplateScraper):
    """Tumblr scraper class."""
    
    name = 'tumblr'
    filename = os.path.basename(__file__)
    
    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, self.name, *args, **kwargs)
        self.log('name from TumblrScraper():', self.name)
    
    def parse_arguments(self):
        '''Get the arguments parser and add arguments to it. Then parse `args` with the parser
        definition defined in the base class to obtain an `options` dict.
        '''
        self.parser = argparse.ArgumentParser(prog=self.prog,
                                              description='Scrape a URI resource for images.')
        self.parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='TumblrScraper-Z',
                                 help='TumblrScraper-extended base option.')
        self.parser.add_argument('--count', metavar='COUNT', type=int, dest='count',
                                 default=1000,
                                 help=('TumblrScraper-only option. Download at most COUNT images '
                                       'from each blog.'))
        super().parse_arguments()
    
    @staticmethod
    def sub_parser(subparsers):
        '''A subparser is passed in as `subparsers`. Add a new subparser to the `subparsers` object
        then return that subparser. See `argparse.ArgumentsParser` for details.
        '''
        parser = subparsers.add_parser('tumblr',
                                       help=('Invoke the tumblr scraper to scrape images off '
                                             'of tumblr.com'))
        return parser
    
    def handle(self):
        '''Main class method that drives the work on scraping the images for this TumblrScraper.
        '''
        self.write('Args:', self.args)
        self.write('Parser:', self.parser)
        self.write('Parsed options:', self.options)
        self.write('')
        self.write('This is the TumblrScraper.')


if __name__ == '__main__':
    # If TumblrScraper was invoked via the command line, initialize a driver and obtain the
    # TumblrScraper, then execute the main handle() method.
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = TumblrScraper(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
