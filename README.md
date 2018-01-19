# jscraper

Demonstrating command line arguments for new scraper application.

## Getting Started

Clone the repository:

`git clone https://github.com/jonmsawyer/jscraper`

Install and activate a virtualenv for this project:

`pip install virtualenv virtualenv-wrapper`
`mkvirtualenv jscraper`

Install the requirements for this project:

`pip install -r requirements.txt`

Hack the code and lint the project (on Windows):

`lint` (must have installed requirements)

TODO - Test the code:

`test`

## Invoke the scraper

`python scraper.py --help`

In this project there are 3 supported scrapers, `generic`, `tumblr`, and
`twitter`.

When invoking the scrapers, note the inheritance and overriding of command line 
arguments.

## Invoke the generic scraper

`python scraper.py generic --help`

### Example

`python scraper.py generic http://example.com/`

Scrapes all images from `http://example.com/`.

## Invoke the tumblr scraper

`python scraper.py tumblr --help`

### Example

`python scraper.py tumblr cars`

Scrapes all images from the blog `cars.tumblr.com`.

## Invoke the twitter scraper

`python scraper.py twitter --help`

### Example

`python scraper.py twitter billgates`

Scrapes all images from the `billgates` twitter profile.

## Invoke the generic scraper as a standalone script

`python scrapers/GenericScraper.py --help`

On Windows, use a backslash for the directory separator.

## Invoke the tumblr scraper as a standalone script

`python scrapers/TumblrScraper.py --help`

On Windows, use a backslash for the directory separator.

## Invoke the twitter scraper as a standalone script

`python scrapers/TwitterScraper.py --help`

On Windows, use a backslash for the directory separator.

## Get debug information

Invoke `scraper.py` or any specific scraper with the `--debug` option to see the
internal debug statements used.
