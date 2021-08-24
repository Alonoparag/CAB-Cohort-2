from modules.create_search_urls import create_search_urls
from modules.search import products_page_list_scraper
from modules.product import scrape_product
from modules.print_message import print_message
import datetime

def scrape_process(product, session, ua, test=False, verbose=False, log=False):
    """
    scrape process for individual product categories.
    Assumes:
         product -  dict dervied from product_list.yml containing
                                                        product_name: str
                                                        main_url: str
                                                        secondary_url: str
                                                        yml_file: str
         session - session object
         ua - fake_useragent.UserAgent instance
         test - boolean default value is False
         verbose - boolean default value is False
         log - boolean fefault value is False
    Returns:
         None
    """
    
    
    if not test:
        product_search_output_json_path = product['path'] + f'{product["product_name"]}_search_output.jsonl'
        product_data_json_path = product['path'] + f'{product["product_name"]}_data.jsonl'
        product_log_path = product['path']+f'{product["product_name"]}_log_{datetime.datetime.now().isoformat(sep="_",timespec="seconds")}.txt' if log else None
        log_file = open(product_log_path,'w') if log else None

        pages_url_list = create_search_urls(product['main_url'], product['secondary_url'],log_file=log_file, verbose = verbose, log=log)
        assert type(pages_url_list)==list, 'Error: The result of create_search_urls must be of type list'
        
        products_url_list = products_page_list_scraper(session, ua, pages_url_list, product_search_output_json_path, log_file=log_file,test=test,verbose = verbose, log = log)
        assert type(products_url_list)==list, 'Error: The result of create_search_urls must be of type list'
        if log or verbose:
            message = '='*50,f'\t\t\tScraping {len(products_url_list)} products','\n','='*50
            print_message(message,log_file,verbose,log)
        scrape_product(session, ua, products_url_list, product['yml_file'], product_data_json_path, log_file=log_file,verbose = verbose, log = log )
        if log_file: log_file.close()
    else:
        product_search_output_json_path = product['path'] + f'{product["product_name"]}_search_output_test_{datetime.datetime.now().isoformat(sep="_",timespec="seconds")}.jsonl'
        product_data_json_path = product['path'] + f'{product["product_name"]}_data_test_{datetime.datetime.now().isoformat(sep="_",timespec="seconds")}.jsonl'
        product_log_path = product['path']+f'{product["product_name"]}_log_test_{datetime.datetime.now().isoformat(sep="_",timespec="seconds")}.txt' if log else None
        log_file = open(product_log_path,'w') if log else None

        pages_url_list = create_search_urls(product['main_url'], product['secondary_url'], verbose = verbose, log=log)[:1]
        assert type(pages_url_list)==list, 'Error: The result of create_search_urls must be of type list'

        products_url_list = products_page_list_scraper(session, ua, pages_url_list, product_search_output_json_path, log_file=log_file,test=test,verbose = verbose, log = log)
        assert type(products_url_list)==list, 'Error: The result of create_search_urls must be of type list'
        if log or verbose:
            message = '='*50,f'\t\t\tScraping {len(products_url_list)} products','\n','='*50
            print_message(message,log_file,verbose,log)

        scrape_product(session, ua, products_url_list, product['yml_file'], product_data_json_path, log_file=log_file, verbose = verbose, log = log)
        if log_file: log_file.close()
