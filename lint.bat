@echo off

echo.
echo Begin.
echo PyLinting project files...
echo.
echo +==================================================================+ > pylint.out
echo. >> pylint.out
echo PyLinting `scraper.py' ...
echo PyLinting `scraper.py' ... >> pylint.out
pylint scraper.py >> pylint.out
echo.
echo +==================================================================+ >> pylint.out
echo. >> pylint.out
echo PyLinting `scrapers' package ...
echo PyLinting `scrapers' package ... >> pylint.out
pylint scrapers >> pylint.out
echo.   
echo PyLinting complete^! Output was dumped to `pylint.out'
echo Finished!
echo.
