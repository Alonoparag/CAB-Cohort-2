# 2nd Assignment: Capital Bikeshare

## Sprint 1:
This sprint was concerned with finding seasonal trends in bike use, and also effect of weather, traffic and pollution on bike use. The course supplied a dataset from UCI, 'day.csv' and 'hour.csv'.
* The task email was concerned with complaints from the last week (last week of april 2021), therefore I decided to use the data from Capital Bikeshare instead of the last week of the data supplied.
* also, the datasets from UCI contained no information about pollution and traffic. I used Selenium to mine data from an pollution monitoring [website]('http://www.cleanairpartners.net/historical-air-quality'), and created a data table which could be merged with the existing UCI datasets, 'pollution.csv'. the process of mining the data could be seen in 'scraper.ipynb' file.

## Final Presentation
* **IMPORTANT** bikeshare-final.csv is zipped in order to save space
1. Instructions for the project presentation could be found in either instructions.html or instructions.md

### Workflow
1. I chose to work with recent data, from may 2020 to april 2021. earlier data had different format and for the sake of berevity i chose not to integrate it to the current data.
2. I automated the data retrieval process using selenium, the script is available in downloader/downloader.py
3. The downloaded datasets were merged into 1 file using downloader/data_merger.ipynb.
4. Data was analyzed, code comments are available in the file presentation-code.ipynb
5. Comments on final presentaion are available at presentation.ipynb