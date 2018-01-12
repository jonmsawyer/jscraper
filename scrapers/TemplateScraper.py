#!/usr/bin/env python3

import os
import sys
import argparse
from pprint import pprint

class TemplateScraper:
    """Base class providing basic scraper functionality."""
    
    debug = False
    parser = None
    options = None
    scrapers = None
    no_help = None
    stdout = sys.stdout
    
    def __init__(self, name, *args, no_help=False, debug=False, **kwargs):
        self.debug = debug
        self.scrapers = {}
        self.name = name
        self.log('self.name:', self.name)
        self.scraper_type = name.split('Scraper')[0].lower().strip()
        if self.scraper_type == '':
            self.scraper_type = 'scraper'
        self.log('self.scraper_type:', self.scraper_type)
        self.no_help = no_help
        self.log('self.no_help:', self.no_help)
        self.parse_arguments()
        self.log('self.parse_args:')
        self.log(self.parse_args)
        self.log('before self.parser.parse_args()')
        self.options = self.parser.parse_args(self.parse_args).__dict__
        self.log('after self.parser.parse_args()')
    
    def log(self, *args, ending='\n', flush=True, **kwargs):
        if self.debug == False:
            return
        end = ending
        spacer = ''
        for arg in args:
            try:
                if type(arg) in (type(list()), type(tuple()), type(dict())):
                    print(spacer, end='', flush=flush)
                    pprint(arg)
                else:
                    print('{}{}'.format(spacer, arg), end='', flush=flush)
            except:
                pprint(arg)
            if spacer == '':
                spacer = ' '
        print('', end=end, flush=True)
    
    def parse_arguments(self, *args, **kwargs):
        prog = '{} {}'.format(list(sys.argv)[0], self.scraper_type)
        prog = prog.strip()
        self.log('parse_arguments(): prog:', prog)
        
        self.parse_args = list(sys.argv)[1:]
        self.log('parse_arguments(): self.parse_args:')
        pprint(self.parse_args)
        
        if self.name in ('Scraper', 'BaseScraper'):
            self.parse_args = self.parse_args[0:1]
        
        if self.no_help:
            self.parser = argparse.ArgumentParser(prog=prog,
                                              description='Scrape a URI resource for image.')
            self.log('before self.get_subparsers()')
            self.get_subparsers()
            self.log('after self.get_subparsers()')
        
        else:
            self.parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS,
                                              description='Scrape a URI resource for image.')
        if self.no_help:
            if '-h' in self.parse_args:
                self.parse_args.remove('-h')
            if '--help' in self.parse_args:
                self.parse_args.remove('--help')
        parser = self.parser
        parser.add_argument('-a', '--user-agent', metavar='USER_AGENT', type=str,
                            dest='user_agent', default='ScraperBot',
                            help='The user agent to report when downloading resources.')
        parser.add_argument('-c', '--cookie', metavar='COOKIE_FILE', type=str, dest='cookie_file',
                            help=('Use cookie file. If file does not exist, create it and use '
                                  'that cookie file. By default, cookies are stored in memory.'))
        parser.add_argument('-C', '--cert', metavar='CERTIFICATE', type=str, dest='cert_file',
                            help=('Used to authenticate a connection between an https, ftps, or '
                                  'ssh resource.'))
        parser.add_argument('-d', '--data-dir', metavar='DATA_DIR', type=str, dest='data_dir',
                            help=('Specify the data directory where the scraper is to save '
                                  'resource data. This directory contains the images where -D '
                                  'specifies where the data directory and metadata file go by '
                                  'default. Default is a rendom directory name stored inside -D.'))
        parser.add_argument('-r', '--recursive', action='store_true',
                            dest='recursive',
                            help='Scrape URIs recursively')
        parser.add_argument('-R', '--num-resources', metavar='NUM_RESOURCES', type=int,
                            choices=range(1, 10), dest='num_resources',
                            help='Download R number of resources at once.')
        parser.add_argument('-x', '--min-width', metavar='MIN_WIDTH', type=int,
                            dest='min_width', default=-1,
                            help='Scrape images that have a minimum width of X pixels.')
        parser.add_argument('-X', '--max-width', metavar='MAX_WIDTH', type=int,
                            dest='max_width', default=-1,
                            help='Scrape images that have a maximum width of X pixels.')
        parser.add_argument('-y', '--min-height', metavar='MIN_HEIGHT', type=int,
                            dest='min_height', default=-1,
                            help='Scrape images that have a minimum height of Y pixels.')
        parser.add_argument('-Y', '--max-height', metavar='MAX_HEIGHT', type=int,
                            dest='max_height', default=-1,
                            help='Scrape images that have a maximum height of Y pixels.')
        parser.add_argument('-U', '--username', metavar='USERNAME', type=str, dest='username',
                            help=('Username used to access the URI resource. Not used when the '
                                  'URI resource is a directory. Use "anonymous" for anonymous '
                                  'ftp(s).'))
        parser.add_argument('-P', '--password', metavar='PASSWORD', type=str, dest='password',
                            help=('Password used to access the URI resource. Not used when URI '
                                  'resource is a directory. Do not use a password for anonymous '
                                  'ftp(s) URIs. If this option is not passed in, then if -U is '
                                  'set, obtain the password from interactive input.'))
        
        parser.add_argument('uris', metavar='URI', type=str, nargs='*',
                            help=('The URI to scrape. Separate multiple URIs by spaces. The type '
                                  'of connection to the URI will depend on the format of the URI. '
                                  'Formats for URI: '
                                    '{sep}path{sep}to{sep}directory - URI is a directory resource. '
                                    'http://example.com/ - URI is an HTTP resource. '
                                    'https://example.com/ - URI is an HTTPS resource. ' 
                                    'ftp://example.com/ - URI is an FTP resource. '
                                    'ftps://example.com/ - URI is an FTPS resource. '
                                    'sftp://example.com/ - URI is an SFTP resource. '
                                    'ssh://example.com/ - URI is an SSH resource. '
                                 ).format(sep=os.path.sep))
    
    def get_subparsers(self, *args, **kwargs):
        pass
    
    @staticmethod
    def sub_parser(*args, **kwargs):
        pass
    
    def handle(self, *args, **kwargs):
        raise NotImplementedError('handle() needs to be implemented.')
