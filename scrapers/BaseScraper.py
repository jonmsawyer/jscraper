#!/usr/bin/env python3

import os
import sys
import argparse
from pprint import pprint

class BaseScraper:
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
    
    def get_subparsers(self, *args, **kwargs):
        pass
    
    @staticmethod
    def sub_parser(*args, **kwargs):
        pass
    
    def handle(self, *args, **kwargs):
        raise NotImplementedError('handle() needs to be implemented.')
