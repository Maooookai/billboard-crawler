## Billboard Data Crawler
### Introduction
This tool contains a series of spider that crawls Billboard chart data.
### Usage
1. Make sure you have python installed. Recommend python 3.10 or newer, but should also work on earlier python3. After installing python, install python requirements.  
`pip install requirements.txt`
2. Install latest Google Chrome and download corresponding chromedriver.  
You can download chromedriver from: https://chromedriver.chromium.org/downloads
3. Run the python script. For example `python 200.py`.
### Scripts
#### [200.py](200.py)
Crawls current Billboard 200 data. Including album title, artist, this week's rank, last week's rank, peak rank, weeks on the chart for 200 albums. And format them to a xlsx file. The filename is based on current date.
If loading website takes too long, you can click the cancel button on Chrome to skip loading. But make sure that rank information is already loaded.