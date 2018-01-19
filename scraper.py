#!/usr/bin/env python3

'''Scraper driver that calls the apropriate scraper based on command line arguments.
'''

import sys

from scrapers.Scraper import Scraper
from scrapers.ScraperDriver import ScraperDriver


if __name__ == '__main__':
    # If scraper.py was invoked via the command line, initialize a driver and obtain the scraper
    # associated with the scraper command line option, then execute the main handle() method.
    
    driver = ScraperDriver(*sys.argv)
    
    driver.log('Args:', sys.argv)
    
    scraper = Scraper(driver)
    driver.log('scraper =', scraper)
    
    scraper_class = scraper.get_scraper_class()
    
    scraper = scraper_class(driver)
    driver.log('scraper =', scraper)
    
    scraper.handle()
