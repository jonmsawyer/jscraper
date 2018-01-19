#!/usr/bin/env python3

'''GenericScraper is a derived class of TemplateScraper for driving the generic image scraper. This
image scraper will attempt to scrape any image off of any URI resource using common known methods
to download those images.
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


class GenericScraper(TemplateScraper):
    """Generic scraper class."""
    
    name = 'generic'
    filename = os.path.basename(__file__)
    
    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, self.name, *args, **kwargs)
        self.log('name from GenericScraper():', self.name)
    
    def parse_arguments(self):
        '''Get the arguments parser and add arguments to it. Then parse `args` with the parser
        definition defined in the base class to obtain an `options` dict.
        '''
        self.parser = argparse.ArgumentParser(prog=self.prog,
                                              description='Scrape a URI resource for images.')
        self.parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='GenericScraper-Z',
                                 help=('GenericScraper-extended base option.'))
        self.parser.add_argument('-V', metavar='V', type=str, dest='V', default='GenericScraper-V',
                                 help='GenericScraper-only option')
        super().parse_arguments()
    
    @staticmethod
    def sub_parser(subparsers):
        '''A subparser is passed in as `subparsers`. Add a new subparser to the `subparsers` object
        then return that subparser. See `argparse.ArgumentsParser` for details.
        '''
        parser = subparsers.add_parser('generic',
                                       help=('Invoke the generic scraper to scrape images off '
                                             'of any URI resource. This is a general scraper '
                                             'and may not grab every image.'))
        return parser
    
    def handle(self):
        '''Main class method that drives the work on scraping the images for this GenericScraper.
        '''
        self.write('Args:', self.args)
        self.write('Parser:', self.parser)
        self.write('Parsed options:', self.options)
        self.write('')
        self.write('This is the GenericScraper.')


if __name__ == '__main__':
    # If GenericScraper was invoked via the command line, initialize a driver and obtain the
    # GenericScraper, then execute the main handle() method.
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = GenericScraper(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
