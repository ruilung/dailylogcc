# dailylogcc

usage
----------
- need two parameters.
- i.g. dailylogcc.exe c:\log 14
- parameter1 is log folder
- parameter2 is days ago to clean gz file


function
------------
- find "*.log" in assing folder
- if last modify date is one day ago. gzip log file (delete log file)
- if last modify date of gzip file is older than assign value. delete it.
