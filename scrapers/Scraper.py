#!/usr/bin/env python3

'''Scraper class used to initialize other scrapers.

   usage:
       >>> from scrapers.Scraper import Scraper
       >>> from scrapers.ScraperDriver import ScraperDriver
       >>> driver = ScraperDriver()
       >>> scraper = Scraper(driver, *args)
'''

import os
import sys
import imp
from pprint import pformat
import argparse

try:
    from scrapers import SALC
except ImportError:
    from . import SALC


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

def get_scraper_names():
    '''Return a 2-tuple of scraper names as a list and scraper names as a string. Uses SCRAPERS
    attribute of this module to walk through. String is formatted like "name1 | name2 | name3".
    The names as a string is used in command line help.
    '''
    names = []
    names_str = ' [ {} ]'
    for scraper in SCRAPERS:
        cls = import_from_dotted_path(scraper)
        names.append(cls.name)
    names_str = names_str.format(' | '.join(names))
    return names, names_str


class Scraper:
    """Scraper class."""
    
    args = None
    kwargs = None
    debug = False
    log_counter = 1
    log_spacing = 8
    name = 'scraper'
    scrapers = None
    parser = None
    parse_args = None
    options = None
    stdout = sys.stdout
    driver = None
    log_ending = '\n'
    prog = None
    
    def __init__(self, driver):
        self.driver = driver
        self.args = driver.args
        self.kwargs = driver.kwargs
        self.debug = driver.debug
        self.log('self.debug:', self.debug)
        self.log('self.name:', self.name)
        self.scrapers = {}
        self.parse_args, self.options = self.parse_arguments()
        self.log('self.parse_args:', self.parse_args)
        self.log('self.options:', self.options)
    
    def log(self, *args, ending='\n', flush=True):
        '''Log the messages provided by args. If DEBUG is True, this method will print out the
        messages provided by args onto stdout.
        '''
        if not self.debug:
            return
        if self.log_ending != '':
            filename = os.path.basename(__file__)
            print('{:>{spacing}} {} | ' \
                  .format('({})'.format(self.log_counter), filename, spacing=self.log_spacing),
                  end='', flush=flush)
        end = ending
        self.log_ending = ending
        spacer = ''
        for arg in args:
            try:
                if isinstance(arg, (list, tuple, dict)):
                    printed = pformat(arg)
                    print('{}{}'.format(spacer, printed), end='', flush=flush)
                else:
                    print('{}{}'.format(spacer, arg), end='', flush=flush)
            except:
                printed = pformat(arg)
                print('{}{}'.format(spacer, printed), end='', flush=flush)
            if spacer == '':
                spacer = ' '
        print('', end=end, flush=True)
        if self.log_ending != '':
            self.log_counter += 1
    
    def parse_arguments(self):
        '''Parse the arguments as supplied by args. args is passed into python's
        argparse.parse_arguments() method to set options for Scraper.
        '''
        self.prog = self.args[0]
        self.log('self.parse_arguments() prog:', self.prog)
        
        parse_args = list(sys.argv)[1:]
        self.log('self.parse_arguments() parse_args:', parse_args)
        
        if self.name == 'scraper':
            parse_args = parse_args[0:1]
        
        scraper_names, scraper_names_str = get_scraper_names()
        del scraper_names
        
        self.parser = argparse.ArgumentParser(prog=self.prog,
                                              formatter_class=argparse.RawTextHelpFormatter,
                                              description='''\
Scrape one or more URI resources for images.''',
                                              epilog='''\
examples:
  $ python %(prog)s generic [OPTIONS] URI [URI ...]
                        Run the generic scraper. Run with --help option
                        for details.

  $ python %(prog)s twitter [OPTIONS] URI [URI ...]
                        Run the twitter scraper. Run with --help option
                        for details.

  $ python %(prog)s tumblr [OPTIONS] URI [URI ...]
                        Run the tumblr scraper. Run with --help option
                        for details.

  $ python %(prog)s --help
                        Show this help message and exit

{SALC}'''.format(SALC=SALC))
        self.parser.add_argument('scraper', action='store', nargs='?', default='scraper',
                                 help=('Pass in a scraper type to initialize that scraper. Choose '
                                       ' from one of {}.'.format(scraper_names_str)))
        self.parser.add_argument('--debug', action='store_true',
                                 help=('Set this flag to display debug information.'))
        
        options = self.parser.parse_args(parse_args).__dict__
        if options.get('scraper') != 'scraper':
            self.get_subparsers()
        options = self.parser.parse_args(parse_args).__dict__
        options['debug'] = self.debug
        return parse_args, options
        
    def get_subparsers(self):
        '''Load each scraper template class into self.scrapers dictionary, then add the subparser
        to the class.
        '''
        self.log('>>>> in get_subparsers()')
        self.log('SCRAPERS:', SCRAPERS)
        if SCRAPERS:
            subparsers = self.parser.add_subparsers(dest='scraper',
                                                    description=('Description text goes here...'),
                                                    help=('Invoke a particular scraper designed '
                                                          'for specific URI resources.'))
            self.log('subparsers:', subparsers)
        for scraper in SCRAPERS:
            self.log('Importing {}... '.format(scraper), ending='')
            cls = import_from_dotted_path(scraper)
            self.scrapers.update({scraper: cls})
            self.log('Done! Imported {}'.format(cls))
            cls.sub_parser(subparsers)
        self.log('self.scrapers:', self.scrapers)
        self.log('>>>> end get_subparsers()')
    
    def get_scraper_class(self):
        '''Get the class of one of the scrapers as defined by the 'scraper' option in SCRAPERS.
        '''
        self.log('<<<< In get_scraper_class()')
        self.log('self.options = ', self.options)
        scraper = self.options.get('scraper')
        if scraper == 'generic':
            scraper_class = self.scrapers.get('scrapers.GenericScraper.GenericScraper')
        elif scraper == 'tumblr':
            scraper_class = self.scrapers.get('scrapers.TumblrScraper.TumblrScraper')
        elif scraper == 'twitter':
            scraper_class = self.scrapers.get('scrapers.TwitterScraper.TwitterScraper')
        else:
            scraper_class = self.__class__
        scraper_class.prog = self.args[0] + ' ' + scraper
        self.log('<<<< end get_scraper_class()')
        return scraper_class
    
    def handle(self):
        '''After all command line options have been parsed, execute the main method (handle())
        of the object. Prints out command line help then exits with an error code because this
        method, ultimately, shouldn't run, but is here to remain consistent with the other
        `scrapers.*Scraper` classes.
        '''
        print(self.parser.format_help())
        sys.exit(1)
