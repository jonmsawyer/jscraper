#!/usr/bin/env python3
# pylint: disable=too-many-branches,too-many-statements

'''TemplateScraper is the base class for driving each image scraper template. Subclass
TemplateScraper then implement the `parse_arguments()`, `sub_parser()`, and `handle()` methods to
create your own customized scraper. See `GenericScraper` for an example.
'''

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
    
    def __init__(self, driver, name):
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
        '''Write args as a prettyfied string to stdout.
        
        TODO: Implement the passing of a `file`-like object in as an argument for custom output.
        '''
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
    
    def parse_arguments(self):
        '''Get the arguments parser and add arguments to it. Then parse `args` with the parser
        definition defined in the base class to obtain an `options` dict.
        
        In order that the derived classes can "override" command line arguments from these
        defaults, wrap a `try`-`except` block around each added argument. If that argument already
        exists, then this base class shall not attempt to add the argument.
        '''
        self.parse_args = list(self.args)[1:] # remove calling program and scraper from args
        if self.name in self.parse_args:
            self.parse_args.remove(self.name)
        self.log('parse_arguments(): self.parse_args:', self.parse_args)
        try:
            self.parser.add_argument('-a', '--user-agent', metavar='USER_AGENT', type=str,
                                     dest='user_agent', default='ScraperBot',
                                     help=('''\
The user agent to report when downloading resources.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-c', '--cookie', metavar='COOKIE_FILE', type=str,
                                     dest='cookie_file',
                                     help=('''\
Use cookie file. If file does not exist, create it
and use that cookie file. By default, cookies are
stored in memory.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-C', '--cert', metavar='CERTIFICATE_FILE', type=str,
                                     dest='cert_file',
                                     help=('''\
Used to authenticate a connection between an https,
ftps, or ssh resource.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-cf', '--config-file', metavar='CONFIG_FILE', type=str,
                                     dest='config_file',
                                     help=('''\
Use the configuration in the %(metavar)s in order
to avoid using command line options.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-dd', '--data-dir', metavar='DATA_DIR', type=str,
                                     dest='data_dir',
                                     help=('''\
Specify the data directory where the scraper is to
save resource data. This directory contains the
images where as option -dd specifies where the data
directory and metadata file go by default. May be
a relative or absolute location. Default is a
random directory name stored inside the current
working directory.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('--debug', action='store_true',
                                     help=('''\
Set this flag to display debug information.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-e', '--extensions', metavar='EXTENSIONS', type=str,
                                     dest='extensions',
                                     help=('''\
List of extensions separated by a comma (and no
space) to limit the scraper to. One or more of:
bmp, gif, jpg, jpeg, png, svg, psd, xcf. Example:
jpg,gif,png limit scraper to these file Extensions.
Default is all extensions.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-l', '--limit', metavar='LIMIT', type=int,
                                     dest='limit',
                                     help=('''\
Limit the scraper to N number of total downloads for
the given URI resources. Each URI resource has their
their own download count.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-lp', '--login-page', metavar='LOGIN_PAGE', type=str,
                                     dest='login_page',
                                     help=('''\
The login page for when option -lt is site.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-lt', '--login-type', metavar='LOGIN_TYPE', type=str,
                                     dest='login_type',
                                     help=('''\
The login type of the URI resource. One of: basic,
site, or cookie. basic is used for basic HTTP auth.
site is used for custom website login page. If
%(metavar)s is site, then option -pw is required.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-minw', '--min-width', metavar='MIN_WIDTH', type=int,
                                     dest='min_width',
                                     help=('''\
Download images that have a minimum width of W pixels.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-maxw', '--max-width', metavar='MAX_WIDTH', type=int,
                                     dest='max_width',
                                     help=('''\
Download images that have a maximum width of W pixels.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-minh', '--min-height', metavar='MIN_HEIGHT', type=int,
                                     dest='min_height',
                                     help=('''\
Download images that have a minimum height of H pixels.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-maxh', '--max-height', metavar='MAX_HEIGHT', type=int,
                                     dest='max_height',
                                     help=('''\
Download images that have a maximum height of H pixels.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-n', '--names', metavar='NAMES', type=str,
                                     dest='names',
                                     help=('''\
Regular expression of a filename to limit the
Scraper to. Does not include extension. See option -e
for limiting the scraper to specific extensions.
Default is all filenames.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-nf', '--no-follow', action='store_true',
                                     dest='no_follow',
                                     help=('''\
If this flag is set, do not populate the referrer
header on linked resources.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-nr', '--no-ratio', action='store_true',
                                     dest='no_ratio',
                                     help=('''\
Flag that disables fitting option -re images to their
aspect ratio, instead images are resized according
to exactly the value for option -re.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-od', '--output-dir', metavar='OUTPUT_DIR', type=str,
                                     dest='output_dir',
                                     help=('''\
Save the metadata file to directory location. Option
-dd specifies where the images will be stored. May
be a relative or absolute location. Default is
current working directory. '''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-ol', '--output-log', metavar='OUTPUT_LOG', type=str,
                                     dest='output_log',
                                     help=('''\
Filename used to log all activity by the scraper.
Default is no log file, just display output on
stdout.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-of', '--output-filename', metavar='OUTPUT_FILENAME',
                                     type=str, dest='output_log',
                                     help=('''\
Filename template string to rename downloaded images
as. If a duplicate filename already exists when
saving the resource, an ncremental placeholder will
be added to the end of the filename.

Note: Specifying a file extension other than %%e will
NOT convert the image to the new extension and type.

Examples:
  img##_%%d.%%e   Has a possible output of
                    "img01_2017-12-29.jpg" as the
                    image filename.
  img.%%e         Since "img.jpg" already exists in
                    this example, the filename will
                    be saved as img_1.jpg
Placeholders include:
  #[#[...]]       Places the resource counter in the
                    filename. If the number of #s
                    exceed the number of digits in
                    the counter, the result is zero
                    padded.
  %%n             Original filename, without the
                    extension.
  %%d(format)     Date format. %%d by itself is short
                    for YYYY-MM-DD. See Python\'s date
                    formatting documentation for a
                    complete list of formatting
                    placeholders at
                    https://docs.python.org/3/
                      library/datetime.html
                      #strftime-and-strptime-behavior
  %%w                Image width in pixels.
  %%h                Image height in pixels.
  %%fd(format)    Date format. %%fd by itself is
                    short for the file\'s mtime
                    YYYY-MM-DD. See %%d for a
                    reference to Python\'s date
                    formatting documentation.
  %%t             Time format. %%t by itself is short
                    for HH-mm-ss. See %%d for a
                    reference to Python's time
                    formatting documentation.
  %%e             Original file extension.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-pw', '--password', metavar='PASSWORD', type=str,
                                     dest='password',
                                     help=('''\
Password used to access the URI resource. Not used
when URI resource is a directory. Do not use a
password for anonymous ftp(s) URIs. If this option is
not passed in, then if option -un is set, obtain the
password from interactive input.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-r', '--recursive', action='store_true',
                                     dest='recursive',
                                     help=('''\
Scrape URIs recursively'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-R', '--num-resources', metavar='NUM_RESOURCES', type=int,
                                     choices=range(1, 10), dest='num_resources',
                                     help=('''\
Download R number of resources at once, where R is an
integer between 1 and 10, inclusive.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-re', '--resize', metavar='RESIZE', type=str,
                                     dest='resize',
                                     help=('''\
Resize images to XxY, where X is the width in pixels
and Y is the height in pixels, keeping aspect
ratio if option -nr is not invoked.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-rl', '--rate-limit', metavar='RATE_LIMIT', type=str,
                                     dest='rate_limit',
                                     help=('''\
Rate limit scraper and its simultaneous downloads to
N<units>. Units may be one of b for bytes, k for
kilobytes, m for megabytes, and g for gigabytes.
all units are per second. Example: 256k to rate
limit scraper to 256 kilobytes per second.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-s', '--sleep', metavar='SLEEP', type=float,
                                     dest='sleep',
                                     help=('''\
Randomly sleep between 0 and N seconds before
recursing into the next sub-level of resources.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-un', '--username', metavar='USERNAME', type=str,
                                     dest='username',
                                     help=('''\
Username used to access the URI resource. Not used
when the URI resource is a directory. Use "anonymous"
for anonymous ftp(s).'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-v', '--version', action='store_true',
                                     dest='version',
                                     help=('''\
Display the version of the scraper application and exit.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('-w', '--wait', metavar='WAIT', type=float,
                                     dest='wait',
                                     help=('''\
Randomly wait between 0 and N seconds before
downloading the next resource.'''))
        except argparse.ArgumentError:
            pass
        try:
            self.parser.add_argument('uri', metavar='URI', type=str, nargs='+',
                                     help=('''\
The URI to scrape. Separate multiple URIs by spaces.
The type of connection to the URI will depend on the
format of the URI. Formats for URI:
    {sep}path{sep}to{sep}directory (directory resource).
    http://example.com/ (HTTP resource).
    https://example.com/ (HTTPS resource). 
    ftp://example.com/ (FTP resource).
    ftps://example.com/ (FTPS resource).
    sftp://example.com/ (SFTP resource).
    ssh://example.com/ (SSH resource).''').format(sep=os.path.sep))
        except argparse.ArgumentError:
            pass
    
    @staticmethod
    def sub_parser(subparsers):
        '''A subparser is passed in as `subparsers`. Add a new subparser to the `subparsers` object
        then return that subparser. See `argparse.ArgumentParser` for details.
        
        Base class stub. Needs to be implemented.
        
        sub_parser() should be implemented like so:
        
        >>> def sub_parser(subparsers):
        >>>     parser = subparsers.add_parser('name_of_scraper',
        >>>                                    help=('Command line help text for the scraper.'))
        >>>     return parser
        '''
        raise NotImplementedError('sub_parser() needs to be implemented.')
    
    def handle(self):
        '''Main class method that drives the work on scraping the images for this derived class
        scraper.
        
        Base class stub. Needs to be implemented.
        
        sub_parser() should be implemented like so:
        
        >>> def handle():
        >>>     # main code to do work on scraping the images for this specific parser
        '''
        raise NotImplementedError('handle() needs to be implemented.')
