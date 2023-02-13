# openaiwebscraper
Web Scraper
This is a Python-based web scraper that allows you to extract data from websites and store it in a CSV file. The tool is highly customizable, allowing you to specify the target websites, the data to extract, and how to clean and format it.

In addition to the web scraping features, this tool also includes a content analysis tool that checks the scraped code for security issues. This analysis is performed by communicating with the OpenAI API.

Usage
To use the web scraper, follow these steps:

Clone the repository to your local machine
Install the required dependencies (see requirements.txt)
Modify config.yaml to specify the target websites, data to extract, and any cleaning or formatting requirements.
Run main.py to start the web scraping process.
The content analysis tool is integrated with the web scraping tool and runs automatically after the data extraction process is complete.

Credits
This web scraper was developed by Antony Ngigge. It was built using Python and various open-source libraries, including:

Requests
Beautiful Soup
Pandas
OpenAI API
