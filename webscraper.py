# Import necessary libraries
import csv
import os
import requests
import re
from scrapy.http import TextResponse
from fake_useragent import UserAgent
import random
import time
import progressbar
import chardet

# Function to check if a proxy is working


def is_working():
    try:
        response = requests.get(
            'http://www.google.com', headers={'api_key': '63d8b7bde5e622166e4c7f1c'}, timeout=3)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


# Read the list of domains and their respective login pages from the CSV file
try:
    with open('domains.csv', 'r') as file:
        reader = csv.DictReader(file)
        domains = [row for row in reader]
except:
    print("Error reading domains.csv")
# Get the number of domains to be scraped
num_domains = len(domains)
# Initialize a variable to keep track of the progress
domain_progress = 0
# Initialize variables to store the start and end time
start_time = time.time()
end_time = 0
# Initialize the rate-limiting parameters
rate_limit_start = 0
rate_limit_end = 0
# define the total time
total_time = 0
# Create a file to store the domains that have already been scraped
try:
    with open("success.txt", "r") as f:
        success_domains = f.read().splitlines()
except:
    print("Error reading success.txt")
# Create a file to store the domains that cannot be scraped
try:
    with open("sslissues.txt", "r") as f:
        ssl_issues_domains = f.read().splitlines()
except:
    print("Error reading sslissues.txt")
# Create a file to store the domains that cannot be scraped
try:
    with open("unscraped.txt", "r") as f:
        unscraped_domains = f.read().splitlines()
except:
    print("Error reading unscraped.txt")
# Loop through each domain and scrape the website
#add credits section, the script has been written by Antony Ngigge and github profile is @antonyngigge
print("Scraping domains..." + " " + "Credits: Antony Ngigge")
for domain in domains:
    #calculate the percentage of domains done
    domain_progress += 1
    progress_percent = (domain_progress / num_domains) * 100
    print(f"Scraping domain {domain_progress} of {num_domains} ({round(progress_percent, 2)}%)")
    # Show progress bar in the cli and a percentage and estimated time remaining
    bar = progressbar.ProgressBar(maxval=num_domains)
    bar.start()
    bar.update(domain_progress)
    # Calculate the estimated time remaining
    end_time = time.time()
    total_time = end_time - start_time
    time_remaining = (total_time / domain_progress) * (num_domains - domain_progress)
    # print statement to include the name of the domain being scraping "scraping url|", percentage of domains scraped, total estimated time remaining to complete all domains
    print(f"Scraping {domain['domain']}|{round(progress_percent, 2)}%|{round(time_remaining, 2)}s remaining")
    # Check if the domain has already been scraped by checking if the domain is in the success.txt file, sslissues.txt file or unscraped.txt file. use the continue statement to skip the domain if it has already been scraped
    if domain['domain'] in success_domains or domain['domain'] in ssl_issues_domains or domain['domain'] in unscraped_domains or 'http://'+domain['domain'] in success_domains or 'http://'+domain['domain'] in ssl_issues_domains or 'http://'+domain['domain'] in unscraped_domains or 'https://'+domain['domain'] in success_domains or 'https://'+domain['domain'] in ssl_issues_domains or 'https://'+domain['domain'] in unscraped_domains or 'www.'+domain['domain'] in success_domains or 'www.'+domain['domain'] in ssl_issues_domains or 'www.'+domain['domain'] in unscraped_domains:
        print ('domain already scraped')
        continue
    else:
        # Make a GET request to scrape the HTML content of the website
        url = domain['domain']
        if not url.startswith('https://') and not url.startswith('http://'):
            url = 'http://' + url
        ua = UserAgent()
        headers = {'User-Agent': ua.random,
                   'Referer': 'https://www.google.com/',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'api_key': '63d8b7bde5e622166e4c7f1c'
                   }
        # Rate limiting: wait for a random delay of 1-3 seconds
        rate_limit_start = time.time()
        time.sleep(random.randint(1, 3))
        rate_limit_end = time.time()
        # Make a GET request
        redirect_count = 0
        response = None
        ssl_issues = False
        try:
            # Check if the proxy is working
            if is_working():
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    pass
                elif response.status_code == 301 or response.status_code == 302 or response.status_code == 307 or response.status_code == 308:
                    if redirect_count < 10:
                        redirect_url = response.headers['Location']
                        response = requests.get(redirect_url, headers=headers)
                        redirect_count += 1
            else:
                # If the proxy is not working, switch to a new proxy
                print('Switching proxy...')
                proxy = 'http://scrapingdog:APIKEY@proxy.scrapingdog.com:8081'
                proxy_dict = {
                    'http': proxy,
                    'https': proxy
                }
                response = requests.get(
                    url, headers=headers, proxies=proxy_dict)
        except requests.exceptions.SSLError as e:
            # If the request fails, log the domain, display the response it gets
            # and continue
            # Create a file to store the domains that cannot be scraped
            ssl_issues = True
            try:
                ssl_issues = open('sslissues.txt', 'a')
                ssl_issues.write(url + '\n')
            except:
                print("Error creating sslissues.txt")
            print('Error scraping domain: {} with response: {}'.format(url, e))
            continue
        except Exception as e:
            # If the request fails, log the domain, display the response it gets
            # and continue
            # Create a file to store the domains that cannot be scraped
            try:
                unscraped = open('unscraped.txt', 'a')
                unscraped.write(url + '\n')
            except:
                print("Error creating unscraped.txt")
            print('Error scraping domain: {} with response: {}'.format(url, e))
            continue
    # Parse the response to get the HTML content
    if response:
        content_type = response.headers.get("Content-Type")
        if "charset" in content_type:
            encoding = content_type.split("charset=")[-1]
        else:
            # Default to the encoding retrieved from the response
            encoding = "utf-8"
        try:
            html = response.content.decode(encoding)
            response = TextResponse(url, body=html, encoding=encoding)
        except UnicodeDecodeError:
            #continue to the next job
            pass
    if response:
        # Create a directory for each domain but 
        try:
            os.mkdir(domain['domain'])
        except:
            print(f"Error creating directory {domain['domain']}")
        # Get the HTML content
        html_content = response.text
        # Write the HTML content to a file
        try:
            file_name = domain['domain'] + '/index.html'
            with open(file_name, 'w', encoding=encoding) as file:
                file.write(html_content)
        except Exception as e:
            print(f"Error writing {file_name} with response: {e}")
        # Write the HTML content to a file
        try:
            # Get the login page
            login_url = domain['login_url']
            if not login_url.startswith('https://') and not login_url.startswith('http://'):
                login_url = 'http://' + login_url
            response = requests.get(login_url, headers=headers)
            if response.status_code == 200:
                pass
            elif response.status_code == 301 or response.status_code == 302 or response.status_code == 307 or response.status_code == 308:
                if redirect_count < 10:
                    redirect_url = response.headers['Location']
                    response = requests.get(redirect_url, headers=headers)
                    redirect_count += 1
            encoding = response.encoding if 'charset' in response.headers.get(
                'content-type', '').lower() else chardet.detect(response.content)['encoding']
            html = response.content.decode(encoding)
            response = TextResponse(url, body=html, encoding=encoding)
            html_content = response.text
            # Write the HTML content to a file
            file_name = domain['domain'] + '/login.html'
            with open(file_name, 'w', encoding=encoding) as file:
                file.write(html_content)
        except Exception as e:
            print(f"Error writing {file_name} with response: {e}")
        # Create a file to store a domain name that was successfully scraped
        if not ssl_issues:
            try:
                success = open('success.txt', 'a')
                success.write(url + '\n')
            except:
                print("Error creating success.txt")
# calculate the total time taken to scrape all the domains
end = time.time()
total_time = end - start
print('Total time taken to scrape all the domains: {} seconds'.format(
    total_time))

# Close the output files
unscraped.close()
success.close()
ssl_issues.close()

