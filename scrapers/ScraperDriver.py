#!/usr/bin/env python3

'''ScraperDriver class used to passed in the driver argument to a new Scraper.
   
   usage:
       >>> from scrapers.Scraper import Scraper
       >>> from scrapers.ScraperDriver import ScraperDriver
       >>> driver = ScraperDriver()
       >>> scraper = Scraper(driver, *args)
'''

import os
from pprint import pformat


class ScraperDriver:
    '''Scraper driver that calls the apropriate scraper based on command line arguments.
    '''
    
    args = None
    kwargs = None
    debug = False
    log_counter = 1
    log_spacing = 4
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        if '--debug' in args:
            self.debug = True
    
    def log(self, *args, ending='\n', flush=True):
        '''Log the messages provided by args. If DEBUG is True, this method will print out the
        messages provided by args onto stdout.
        '''
        if self.debug is False:
            return
        filename = os.path.basename(__file__)
        print('{:>{spacing}} {} | '.format('({})'.format(self.log_counter),
                                           filename,
                                           spacing=self.log_spacing),
              end='',
              flush=flush)
        end = ending
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
        self.log_counter += 1
