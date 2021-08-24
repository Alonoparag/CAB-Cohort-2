import datetime
from modules.print_message import print_message

def create_search_urls(main_url,paged_url, log_file=None, verbose=False, log=False):
    """
    Assumes:
        main_url string representing first page url
        paged_url string representing 2nd page yrl
    Returns:
        list of product_urls 
    """
    url_list = []
    url_list.append(main_url)
    
    url_1 = paged_url.split('page=2')[0]+'page='
    url_2= paged_url.split('page=2')[1].split('r_pg_2')[0]+'r_pg_'
    if verbose or log:
        message= ('-'*30)+'\nCreating urls at '+datetime.datetime.now().isoformat(sep="_",timespec="seconds")+'\n'+('-'*30)
        print_message(message,log_file,verbose=verbose,log=log)
        
    for i in range(2,51):

        url = url_1 + str(i) + url_2 + str(i)
        url_list.append(url)
        if verbose or log:
            message = f'{datetime.datetime.now().isoformat(sep="_",timespec="seconds")}: Added {url} to url_list'
            print_message(message,log_file,verbose=verbose,log=log)

    if verbose or log:
        message= ('-'*30)+'\nURLs created succesfully '+datetime.datetime.now().isoformat(sep="_",timespec="seconds")+'\n'+('-'*30)
        print_message(message,log_file,verbose=verbose,log=log)

    return url_list
