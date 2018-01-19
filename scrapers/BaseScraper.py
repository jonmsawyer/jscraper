#!/usr/bin/env python3

import os
import sys
import argparse
from pprint import pprint

class BaseScraper:
    """Base class providing basic scraper functionality."""
    
    def __init__(self, name, *args, no_help=False, debug=False, **kwargs):
