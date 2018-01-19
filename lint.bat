@echo off

echo.
echo Begin.
echo PyLinting project files...
echo.
echo +==================================================================+ > pylint.out
echo. >> pylint.out
echo PyLinting scraper.py ...
echo PyLinting scraper.py ... >> pylint.out
pylint scraper.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting scrapers\Scraper.py ...
echo PyLinting scrapers\Scraper.py ... >> pylint.out
pylint scrapers\Scraper.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting scrapers\ScraperDriver.py ...
echo PyLinting scrapers\ScraperDriver.py ... >> pylint.out
pylint scrapers\ScraperDriver.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting scrapers\TemplateScraper.py ...
echo PyLinting scrapers\TemplateScraper.py ... >> pylint.out
pylint scrapers\TemplateScraper.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting scrapers\GenericScraper.py ...
echo PyLinting scrapers\GenericScraper.py ... >> pylint.out
pylint scrapers\GenericScraper.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting scrapers\TumblrScraper.py ...
echo PyLinting scrapers\TumblrScraper.py ... >> pylint.out
pylint scrapers\TumblrScraper.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting scrapers\TwitterScraper.py ...
echo PyLinting scrapers\TwitterScraper.py ... >> pylint.out
pylint scrapers\TumblrScraper.py >> pylint.out
echo.   
echo PyLinting complete^! Output was dumped to pylint.out
echo Finished!
echo.
