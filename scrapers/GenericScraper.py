#!/usr/bin/env python3

'''GenericScraper is a derived class of TemplateScraper for driving the generic image scraper. This
image scraper will attempt to scrape any image off of any URI resource using common known methods
to download those images.
'''

# pylint: disable=ungrouped-imports

import os
import sys
import argparse

try:
    from scrapers.TemplateScraper import TemplateScraper
    from scrapers.ScraperDriver import ScraperDriver
except (ModuleNotFoundError, ImportError):
    from TemplateScraper import TemplateScraper
    from ScraperDriver import ScraperDriver

try:
    from scrapers import SALC
except (ModuleNotFoundError, ImportError):
    from __init__ import SALC


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
                                              formatter_class=argparse.RawTextHelpFormatter,
                                              description='''\
Scrape one or more URI resources for images.''',
                                              epilog='''\
examples:
  $ python %(prog)s \\
            https://foo.example.com/
                        Scrape all images located at,
                        https://foo.example.com/, but do not recurse into
                        any other sub-resources.

  $ python %(prog)s \\
            -cf scraper.conf \\
            http://foo.example.com/
                        Read in all configuration options from the
                        configuration file `scraper.conf', then scrape all
                        images from http://foo.example.com/.

  $ python %(prog)s \\
            -nr 4 \\
            /usr/share/icons
                        Scrape all images located at the local directory,
                        /usr/share/icons, and recursively grab all
                        sub-resources under that directory downloading 4
                        simultaneous images until completed.

  $ python %(prog)s \\
            -a ScraperBot \\
            --cookie=cookie.txt \\
            -od images \\
            -e jpg,png \\
            -lt site \\
            -lp http://foo.example.com/login \\
            -l 512k \\
            --no-follow \\
            --names="^img[0-9]+" \\
            -un myuser \\
            -pw mypass \\
            -r \\
            -of log.txt \\
            -s 10 \\
            -w 7 \\
            -nr 10 \\
            http://foo.example.com/
                        Recursively scrape all images and sub-resources at
                        http://foo.example.com with the "ScraperBot" user
                        agent, using the cookie file "cookie.txt", storing
                        downloaded resources to local directory "images",
                        limiting all downloads to the jpg and png
                        extensions, with login type of "site", using
                        http://foo.example.com/login as the login page,
                        rate limiting downloads to 512Kbps, scraping
                        images no referrer URI (no follow), limiting file
                        names to grab to img#[#].{{jpg,png}}, with username
                        as "myuser" with password "mypass", outputting the
                        generated log file to "log.txt", sleeping between
                        0 and 10 seconds between each sub-resource get,
                        waiting between 0 and 7 seconds for each resource,
                        all while downloading 10 simultaneous resources
                        at once until completed.

  $ python %(prog)s
            -un anonymous \\
            ftps://bar.example.com/images
                        Recursively scrape all images at the ftps resource
                        located at bar.example.com/images, anonymously.

  $ python %(prog)s \\
            -r \\
            http://foo.bar.com/images \\
            http://bar.example.com/images/mirror1 \\
            http://qux.example.com/images/backup2
                        Recursively scrape http://foo.bar.com/images,
                        http://bar.example.com/images/mirror1, and
                        http://qux.example.com/images/backup2 into the
                        local current working directory.

  $ python %(prog)s --version
                        Display the version of scraper.py and exit.

  $ python %(prog)s --help
                        Show this help message for the generic scraper
                        and exit

{SALC}'''.format(SALC=SALC))
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
