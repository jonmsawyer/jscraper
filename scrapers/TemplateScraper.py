#!/usr/bin/env python3

import os
import sys
import argparse
from pprint import pformat

class TemplateScraper:
    """Base class providing basic scraper functionality."""
    
    args = None
    kwargs = None
    debug = False
    log_counter = 1
    log_spacing = 12
    log_ending = '\n'
    parser = None
    options = None
    name = None
    driver = None
    filename = os.path.basename(__file__)
    stdout = sys.stdout
    prog = sys.argv[0]
    
    def __init__(self, driver, name, *args, no_help=False, debug=False, **kwargs):
        self.driver = driver
        self.args = driver.args
        self.kwargs = driver.kwargs
        self.debug = driver.debug
        self.log('self.debug:', self.debug)
        self.name = name
        self.log('self.name:', self.name)
        self.parse_arguments()
        self.log('self.parse_args:', self.parse_args)
        self.log('before self.parser.parse_args()')
        self.options = self.parser.parse_args(self.parse_args).__dict__
        self.log('after self.parser.parse_args()')
        self.log('prog:', self.prog)
    
    def log(self, *args, ending='\n', flush=True):
        '''Log the messages provided by args. If DEBUG is True, this method will print out the
        messages provided by args onto stdout.
        '''
        if not self.debug:
            return
        if self.log_ending != '':
            print('{:>{spacing}} {} | ' \
                  .format('({})'.format(self.log_counter),
                          self.filename,
                          spacing=self.log_spacing),
                  end='', flush=flush)
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
        print('', end=ending, flush=True)
        if self.log_ending != '':
            self.log_counter += 1
    
    def write(self, *args, ending='\n', flush=True):
        spacer = ''
        for arg in args:
            try:
                if isinstance(arg, (list, tuple, dict)):
                    printed = pformat(arg)
                    self.stdout.write('{}{}'.format(spacer, printed))
                else:
                    self.stdout.write('{}{}'.format(spacer, arg))
            except:
                printed = pformat(arg)
                self.stdout.write('{}{}'.format(spacer, printed))
            self.stdout.write(ending)
            if flush:
                self.stdout.flush()
            if spacer == '':
                spacer = ' '
    
    def parse_arguments(self, *args, **kwargs):
        self.parse_args = list(self.args)[1:] # remove calling program from args
        self.log('parse_arguments(): self.parse_args:', self.parse_args)
        
        parser = self.parser
        try:
            parser.add_argument('-a', '--user-agent', metavar='USER_AGENT', type=str,
                                dest='user_agent', default='ScraperBot',
                                help='The user agent to report when downloading resources.')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-c', '--cookie', metavar='COOKIE_FILE', type=str,
                                dest='cookie_file',
                                help=('Use cookie file. If file does not exist, create it and use '
                                      'that cookie file. By default, cookies are stored in '
                                      'memory.'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-C', '--cert', metavar='CERTIFICATE', type=str, dest='cert_file',
                                help=('Used to authenticate a connection between an https, ftps, '
                                      'or ssh resource.'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-d', '--data-dir', metavar='DATA_DIR', type=str, dest='data_dir',
                                help=('Specify the data directory where the scraper is to save '
                                      'resource data. This directory contains the images where -D '
                                      'specifies where the data directory and metadata file go by '
                                      'default. Default is a rendom directory name stored inside '
                                      '-D.'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-r', '--recursive', action='store_true',
                                dest='recursive',
                                help='Scrape URIs recursively')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-R', '--num-resources', metavar='NUM_RESOURCES', type=int,
                                choices=range(1, 10), dest='num_resources',
                                help='Download R number of resources at once.')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-x', '--min-width', metavar='MIN_WIDTH', type=int,
                                dest='min_width', default=-1,
                                help='Scrape images that have a minimum width of X pixels.')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-X', '--max-width', metavar='MAX_WIDTH', type=int,
                                dest='max_width', default=-1,
                                help='Scrape images that have a maximum width of X pixels.')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-y', '--min-height', metavar='MIN_HEIGHT', type=int,
                                dest='min_height', default=-1,
                                help='Scrape images that have a minimum height of Y pixels.')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-Y', '--max-height', metavar='MAX_HEIGHT', type=int,
                                dest='max_height', default=-1,
                                help='Scrape images that have a maximum height of Y pixels.')
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-U', '--username', metavar='USERNAME', type=str, dest='username',
                                help=('Username used to access the URI resource. Not used when '
                                      'the URI resource is a directory. Use "anonymous" for '
                                      'anonymous ftp(s).'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-P', '--password', metavar='PASSWORD', type=str, dest='password',
                                help=('Password used to access the URI resource. Not used when '
                                      'URI resource is a directory. Do not use a password for '
                                      'anonymous ftp(s) URIs. If this option is not passed in, '
                                      'then if -U is set, obtain the password from interactive '
                                      'input.'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('--debug', action='store_true',
                                     help=('Set this flag to display debug information.'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('-Z', metavar='Z', type=str, dest='Z', default='TemplateScraper-Z',
                                     help=('TemplateScraper-extended base option.'))
        except argparse.ArgumentError:
            pass
        try:
            parser.add_argument('uris', metavar='URI', type=str, nargs='+',
                                help=('The URI to scrape. Separate multiple URIs by spaces. The '
                                      'type of connection to the URI will depend on the format of '
                                      'the URI. Formats for URI: '
                                      '    {sep}path{sep}to{sep}directory (directory resource). '
                                      '    http://example.com/ (HTTP resource). '
                                      '    https://example.com/ (HTTPS resource). ' 
                                      '    ftp://example.com/ (FTP resource). '
                                      '    ftps://example.com/ (FTPS resource). '
                                      '    sftp://example.com/ (SFTP resource). '
                                      '    ssh://example.com/ (SSH resource).'
                                     ).format(sep=os.path.sep))
        except argparse.ArgumentError:
            pass
    
    def get_subparsers(self, *args, **kwargs):
        pass
    
    @staticmethod
    def sub_parser(*args, **kwargs):
        pass
    
    def handle(self, *args, **kwargs):
        raise NotImplementedError('handle() needs to be implemented.')
