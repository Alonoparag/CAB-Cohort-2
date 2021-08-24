from selectorlib import Extractor
import requests
from fake_useragent import UserAgent
import datetime
import json
from time import sleep
import random
from modules.print_message import print_message

# Create an Extractor by reading from the YAML file
def scrape_product(session,ua,url_list, yml_file,json_file,log_file, verbose= False, log = False):
    e = Extractor.from_yaml_file(yml_file)
    def scrape(url):

        headers = {
            'Host': 'www.amazon.com',
            'user-agent': ua,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'dnt': '1',           
            'connection': 'keep-alive',
            'Upgra-Insecure-Requests': '1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
        }
        # Download the page using requests
        if verbose or log:
            message=('*'*20)+f"\nDownloading product from page {url} at {datetime.datetime.now().isoformat(sep='_',timespec='seconds')}"
            print_message(message,log_file,verbose=verbose,log=log)
        r = session.get(url, headers=headers)
        # Simple check to check if page was blocked (Usually 503)

        if "To discuss automated access to Amazon data please contact" in r.text:
            if verbose or log:
                message='\n'+f"Page {url} was blocked by Amazon. Please try using better proxies\n"+'\n','response:'+'\n'+'\n'.join([r_line[0] + ':\n\t' + r_line[1] for r_line in r.headers.items()])+'\n'
                print_message(message,log_file,verbose=verbose,log=log)            
            return None

        elif r.status_code > 500:
            if verbose or log:
                message = f'Page {url} must have been blocked by Amazon as the status code was {r.status_code}. response:'+'\n'+'\n'.join([r_line[0] + ':\n\t' + r_line[1] for r_line in r.headers.items()])+'\n'
                print_message(message,log_file,verbose=verbose,log=log) 
                return None

        # Pass the HTML of the page and create 
        if verbose or log:
            message=f'Scraper succesffuly accessed product in page {url}'
            print_message(message,log_file,verbose=verbose,log=log)
            
        return e.extract(r.text)

    with open(json_file, 'w') as outfile:
        j_list = []
        if verbose or log:
            message = ('-'*30)+'\nStarting to scrape product from list at '+datetime.datetime.now().isoformat(sep='_',timespec='seconds')+'\n'+('-'*30)
            print_message(message,log_file,verbose=verbose,log=log)
            
        for ind,url in enumerate(url_list):
            data = scrape(url)
            print('data:',bool(data))
            if data:
                try:
                    data['seller_link'] = 'https://www.amazon.com' + data['seller_link'] if data['seller_link'] else None
                    data['freq_bought_link'] = 'https://www.amazon.com' + data['freq_bought_link'] if data['freq_bought_link'] else None
                    j_list.append(data)
                except Exception as e:
                    j_list.append(data)
                    if verbose or log:
                        msg = '\n'.join([
                            '=' * 50,
                            f'At {datetime.datetime.now()}\n\n',
                            '\n\nURL:\t\t' + url,
                            str(e)
                        ])
                        print_message(msg,log_file,verbose=verbose,log=log)
            sleep(round(10*random.random()/2,2))

        outfile.write(json.dumps(j_list))
        if verbose or log:
            message = ('-'*30)+'\nFinished scraping products from list at '+datetime.datetime.now().isoformat(sep='_',timespec='seconds')+'\n'+('-'*30)
            print_message(message,log_file,verbose=verbose,log=log)
