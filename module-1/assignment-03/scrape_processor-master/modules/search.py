import selectorlib
from selectorlib import Extractor
import requests
import json
from time import sleep
import browser_cookie3
import datetime
import random
from modules.print_message import print_message
# Create an Extractor by reading from the YAML file

def products_page_list_scraper(session,ua, in_search_url_list ,json_path,log_file=None, test=False, verbose=False,log=False):
    """
    Assumes:
        session requests.Session object    
        in_search_url_list list of strings with urls
        json_path string denoting path for product_list jsonl files
        log_file string denoting error log text file
    Returns:
        search_url_list type list of individual products urls
    """
    e = Extractor.from_yaml_file('search.yml')
    
    def scrape(url, referer = None):

        headers = {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.amazon.com/' if not referer else referer,
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        # Download the page using requests
        if verbose or log:
            message=('*'*20)+f"\nDownloading products information from page {url} at {datetime.datetime.now().isoformat(sep='_',timespec='seconds')}"
            print_message(message,log_file,verbose=verbose,log=log)
        r=session.get(url,headers = headers)
        # Simple check to check if page was blocked (Usually 503)
        if "To discuss automated access to Amazon data please contact" in r.text:
            if verbose or log:
                message=f"Page {url} was blocked by Amazon. Please try using better proxies\n" 
                print_message(message,log_file,verbose=verbose,log=log)
            return None

        elif r.status_code > 500:
            if verbose or log:
                message=f"Page {url} must have been blocked by Amazon as the status code was {r.status_code}" 
                print_message(message,log_file,verbose=verbose,log=log)
            return None

        if verbose or log:
                message=f"Scraper successfuly accessed page {url}"
                print_message(message,log_file,verbose=verbose,log=log)
        return e.extract(r.text)
#################################################

    out_search_url_list = []

    with open(json_path, 'w') as outfile:
        if verbose or log:
            prologue=('-'*30)+'\nStarting to scrape products from search page at '+datetime.datetime.now().isoformat(sep='_',timespec='seconds')+'\n'+('-'*30)
            print_message(prologue,log_file,verbose=verbose,log=log)

        for ind,url in enumerate(in_search_url_list):
            data = scrape(url, referer = in_search_url_list[ind-1] if ind > 0 else None)
            j_list = []
        
            if data:
                products = data['products'][:10] if test else data['products']
                for product in products:
                    product['url'] = 'https://www.amazon.com' + product['url']
                    out_search_url_list.append(product['url'])
                    j_list.append(product)
                    sleep(round(10*random.random()/2,2))

        outfile.write(json.dumps(j_list))
        outfile.close()

        if verbose or log:
            epilogue= ('-'*30)+'\nFinished to scrape products from search page at '+datetime.datetime.now().isoformat(sep='_',timespec='seconds')+'\n'+('-'*30)
            print_message(epilogue,log_file,verbose=verbose,log=log)
            
    return out_search_url_list
