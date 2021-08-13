import pickle
import pandas as pd
import re
import sys
import types
from datetime import datetime
import price_updater_lib as lib

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


    products=[(df_dslr,'dslr'),
    (df_keyboard,'keyboard'),
    (df_monitor,'monitor'),
    (df_mouse,'mouse'),
    (df_processor,'processor'),
    (df_smartphone,'smartphone')]

    for product in products:
        product[0]['rating']=product[0]['rating'].apply(lambda x: round(float(x.split(' out')[0]),2))
        product[0]['review_count']=product[0]['review_count'].apply(lambda x: int(''.join(x.split(','))))
        product[0]['price']=product[0]['price'].apply(lambda x: round(float(re.sub('[^1-9.]','',x)),2))
        product[0]['category']=product[1]
        # product[0].to_csv(f'assignment-03/project-ecommerce/datasets/ecom-sales_data/ecom-sales{product[1]}_processed.csv')

    df_products=pd.concat([product[0] for product in products])
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
            dict_sold_products[description]['formatted_description']=lib.replace_description(description)
            dict_sold_products[description]['price']=row['UnitPrice']
            dict_sold_products[description]['indices']=[ind]
        
    # items_without_description=[]

    logfile.write(f'sep\nBEGIN ITERATION\n\n')
    print('Begin matching on',len(list(dict_sold_products.values())), 'descriptions')

    product_cats={
        'processor':'processor',
        'dslr':'dslr',
        'camera':'dslr',
        'keyboard':'keyboard',
        'monitor':'monitor',
        'mouse':'mouse',
        'smartphone':'smartphone',
        'iphone':'smartphone',
        'ipad':'smartphone',
        'tablet':'smartphone',
        'galaxy':'smartphone',
        'smartwatch':'smartphone',
    }

    multiple_match_sales=[]
    unmatched_sales={}

    dict_sold_products,multiple_matches, unmatched_sales,df_match_target = lib.matching_wrapper(
                                                                                    df_products,
                                                                                    dict_sold_products,
                                                                                    multiple_match_sales,
                                                                                    unmatched_sales,
                                                                                    product_cats,
                                                                                    logfile,
                                                                                    errlog)
    
    if len(unmatched_sales) > 0:
        logfile.write(f'Matching on {len(unmatched_sales)} unmatched items\n')
        dict_sold_products,multiple_matches, unmatched_sales,df_match_target = lib.matching_wrapper(
                                                                                df_match_target,
                                                                                dict_sold_products,
                                                                                multiple_match_sales,
                                                                                unmatched_sales,
                                                                                product_cats,
                                                                                logfile,
                                                                                errlog,
                                                                                with_categories=False,
                                                                                on_unmatched=True)
        
    
    end = datetime.now()
    logfile.write(f'App finished at {end}. Finding correct prices took {end-begin}')
    pickle.dump(unmatched_sales,open('data/unmatched_sales.p','wb'))
    pickle.dump(multiple_match_sales,open('data/multiple_match_sales.p','wb'))
    # pickle.dump(items_without_description,open('data/items_without_description.p','wb'))
    pickle.dump(dict_sold_products,open('data/dict_sold_products.p','wb'))