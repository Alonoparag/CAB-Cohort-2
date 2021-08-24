import sys
import argparse
from modules.scraping_wrapper import scrape_process
from modules.exceptions import EmptyProductDescriptionException
import yaml
import requests
import browser_cookie3
from fake_useragent import UserAgent

VERSION = '1.1.0'
description= f"""
                    this package scrapes amazon for products and generate csv files with pre-given columns.
                    Please read readme file for use guidance.
                    originally created by Shekhar Biswas
                    modified into a library by Alon Parag 07.07.2021

            """

def get_cookies(browser):
    """
    helper function to get cookies from CLI argument -b/--browser
    Assumes:
            browser - a string representing a valid browser. A valid browser is a choice from the following list:
            {'chrome','firefox','opera','edge','chromium'}
    Returns:
            http.CookieJar instance
    """
    assert browser in ['chrome','firefox','opera','edge','chromium'], 'Error browser must be in \{chrome, firefox, opera, edge, chromium\}'
    if browser=='chrome':
        return browser_cookie3.chrome(domain_name='www.amazon.com')
    elif browser=='firefox':
        return browser_cookie3.firefox(domain_name='www.amazon.com')
    elif browser=='opera':
        return browser_cookie3.opera(domain_name='www.amazon.com')
    elif browser=='edge':
        return browser_cookie3.edge(domain_name='www.amazon.com')
    elif browser=='chromium':
        return browser_cookie3.chromium(domain_name='www.amazon.com')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=description,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-t,--test', action='store_true', default=False,help='Run scrape processor on the first 10 products of the first page of the category processors and log results. Use to debug for captcha issues with amazon')
    parser.add_argument('-l','--log',action='store_true', default=False,help='Log actions into a file')
    parser.add_argument("-V","--version",action='version',version=VERSION,help='Print version (capital V)')
    parser.add_argument('-v',"--verbose",action='store_true', default=False,help='print actions into console')
    parser.add_argument('-b', "--browser", choices=['chrome', 'firefox', 'opera', 'edge', 'chromium'], required=True, help='Required. Select browser from which to take cookies. options are: chrome, firefox, opera, edge, chromium', dest='browser')
    parser.add_argument('-s',"--strict",action='store_true',default=False,help='In strict mode an exception is raised if a description.yml file is empty. loose mode is skipping an empty product', dest='browser')
    
    args = parser.parse_args()
    ##################
    test = args.test
    verbose = args.verbose
    log = args.log
    strict=args.strict
    
    scrape_session = requests.Session()
    scrape_session.cookies.update(get_cookies(args.browser))
    products = yaml.load(open('product_list.yml', 'r'), Loader=yaml.FullLoader)
    ua=UserAgent().random


    if test:
        for product in products:
            if product['product_name'] == 'processor':
                scrape_process(product, scrape_session,ua, test=test, verbose=verbose, log=True)
    else:
        for p_i, product in enumerate(products):
            p_description=yaml.load(open(product['yml_file'], 'r'), Loader=yaml.FullLoader)
            if strict:
                if len(p_description) == 0:
                    raise EmptyProductDescriptionException(product['product_name'])
                else:
                    scrape_process(product, scrape_session, ua, verbose=verbose, log=log)
            else:
                try:
                    if len(p_description) == 0:
                        raise EmptyProductDescriptionException(product['product_name'])
                    else:
                        scrape_process(product, scrape_session, ua, verbose=verbose, log=log)
                except EmptyProductDescriptionException as e:
                    print(f'Warning: {product["product_name"]} description.yml file is empty. Scraper is skipping {product["product_name"]}. ')
