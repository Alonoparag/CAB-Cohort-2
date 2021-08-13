import pickle
import pandas as pd
import re
import sys
import types
from datetime import datetime

def create_pattern(description_item):
    """
    Helper function that turns an item from the description into a regex pattern item to be used for the query
    Assumes:
         description_item - str
    Returns:
         a str compatible with regex to be searched on the whole string.
    """
    pre_pattern = ''.join(['\\' + c if c in '[]().^+$*?{},\\|<>#!=/' else c for c in description_item])
    return '(?=.*'+pre_pattern+')'

def replace_description(s):
    """
    replaces word seperator in product description with a single seperator for later processing
    Assumes:
        s-string
    Returns:
        string
    """
    try:
        s=re.sub('( \+ )|( \- )|(, )|( \| )','*-*',s)
        s=re.sub('\s','*-*',s)
        return s
    except:
        print(ind, s, type(s))
    raise TypeError

with open('log.txt','w') as logfile, open(f'error_log_{datetime.now()}.txt', 'w') as errlog:
    begin = datetime.now()
    
    logfile.write(f'Welcome!\nApp initialized at{begin}\n\n')

    # Loading csv files into dataframes
    print('Loading datasets')
    df_dslr=pd.read_csv('datasets/ecom-sales_data/ecom-sales/dslr.csv')
    df_keyboard=pd.read_csv('datasets/ecom-sales_data/ecom-sales/keyboard.csv')
    df_monitor=pd.read_csv('datasets/ecom-sales_data/ecom-sales/monitor.csv')
    df_mouse=pd.read_csv('datasets/ecom-sales_data/ecom-sales/mouse.csv')
    df_processor=pd.read_csv('datasets/ecom-sales_data/ecom-sales/processor.csv')
    df_smartphone=pd.read_csv('datasets/ecom-sales_data/ecom-sales/smartphone.csv')
    df_sales=pd.read_csv('datasets/ecom-sales_data/ecom-sales/sales.csv')


    #removing null values from sales
    df_sales.dropna(subset=['Description'], inplace=True,)
    df_sales.reset_index(inplace=True, drop=True)


    products=[df_dslr,
    df_keyboard,
    df_monitor,
    df_mouse,
    df_processor,
    df_smartphone]

    df_products=pd.concat(products)
    df_products.reset_index(inplace=True)
    df_products.rename(columns={'index':'orgnl_index'}, inplace=True)

    df_products.sort_values('review_count', ascending=False, inplace=True)
    df_products.drop_duplicates(inplace=True, subset=['title','price'], keep='first')
    df_products.reset_index(inplace=True,drop=True)
        
    sep='#'*30


    dict_sold_products = {}


    #group products to a dict
    print('Grouping sold items')
    for ind, row in df_sales.iterrows():
        description=df_sales.at[ind, 'Description']
        if description in dict_sold_products.keys():
            dict_sold_products[description]['indices'].append(ind)
        else:
            dict_sold_products[description]={}
            dict_sold_products[description]['description']=description
            dict_sold_products[description]['formatted_description']=replace_description(description)
            dict_sold_products[description]['price']=row['UnitPrice']
            dict_sold_products[description]['indices']=[ind]
        
    unmatched_sales=[]
    multiple_match_sales=[]
    # items_without_description=[]

    counter=1


    logfile.write(f'sep\nBEGIN ITERATION\n\n')
    print('Begin matching on',len(list(dict_sold_products.values())), 'descriptions')
    df_match_target = df_products.copy()

    for description,values in list(dict_sold_products.items()):
      try:
        #split the product description by '*-*'
        list_item_description = values['formatted_description'].split('*-*')

    ############################### #Logging ###############################
        logfile.writelines(['\t\tDescribing Items\n',f'description: {list_item_description}\n'])

        pattern = create_pattern(list_item_description[0])
        pattern_index = 0

        # pre_pattern = ''.join(['\\' + c if c in '[]().^+$*?{},\\|<>#!=/' else c for c in list_item_description[pattern_index]])
        match = df_match_target[df_match_target.stack().str.contains(pattern,case=False,regex=True).groupby(level=0).any()]
        # while the number of matching rows is larger than 1 or there are more patterns to match to

        ############################### #Logging ###############################
        logfile.writelines(['\t\tCurrent pattern, iteration and matches:\n',f'pattern: {pattern} pattern index: {pattern_index} matches: {match.shape[0]}\n',f'{match.shape[0]>1} {pattern_index<len(list_item_description)}\n'])
############################## #end Logging ###############################
        while match.shape[0]>1 and pattern_index<len(list_item_description)-1:
        # add a match group to the pattern
            pattern_index+=1
            pattern += create_pattern(list_item_description[pattern_index])
    ############################### #Logging ###############################
            logfile.writelines([f'\t\tCurrent pattern, iteration and matches\n',f'pattern: {pattern}, pattern index: {pattern_index}, matches: {match.shape[0]}\n'])

            match = match[match.stack().str.contains(pattern,case=False,regex=True).groupby(level=0).any()]
            
        if match.shape[0]==1:
        # change the price of the matched item
        ############################### #Logging ###############################
            logfile.write(f'{sep}\n\t\t\tMATCH FOUND\n{sep}\n')

            match_index = list(match['orgnl_index'])[0]
            dict_sold_products[description]['price']=match.at[match.index[0],'price']
            dict_sold_products[description]['matching_indices']=match_index
            df_match_target.drop(list(match.index),axis=0,inplace=True)
        elif match.shape[0]>1:
        ############################### #Logging ###############################
            logfile.writelines([f'{sep}\n\t\t\tMULTIPLE MATCHES FOUND\n{sep}\n',f'pattern: {pattern}, pattern index: {pattern_index}, matches: {match.shape[0]}\n'])                
            match_index = list(match['orgnl_index'])
            multiple_match_sales.append({'description':description,'matche_indices(orgnl_index)':match_index})
        
            df_match_target.drop(list(match.index),axis=0,inplace=True)
        
        elif match.shape[0]<1:
        ############################### #Logging ###############################
            logfile.write(f'{sep}\n\t\t\tNO MATCHES FOUND\n{sep}\n')
            unmatched_sales.append(description)
        # breaking from looping over the item caegories
        del pattern
        del match
    #handling no matching categories
        
        logfile.write(f'iteration: {counter}\n')
        print(f'iteration: {counter}\n')
        counter+=1
        logfile.write(f'unmatched items: {len(unmatched_sales)}\nMultiple matches: {len(multiple_match_sales)}\n\n END ITERATION\n{sep}\n')
      except Exception as e:
        print('exception occured')
        import traceback
        errlog.writelines([f'{sep}\nERROR\n{sep}',traceback.format_exc()
                          ])
        raise e
    end = datetime.now()
    logfile.write(f'App finished at {end}. Finding correct prices took {end-begin}')
    pickle.dump(unmatched_sales,open('data/unmatched_sales2.p','wb'))
    pickle.dump(multiple_match_sales,open('data/multiple_match_sales2.p','wb'))
    # pickle.dump(items_without_description,open('data/items_without_description2.p','wb'))
    pickle.dump(dict_sold_products,open('data/dict_sold_products2.p','wb'))