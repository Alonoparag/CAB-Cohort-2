import pandas as pd
import re
from datetime import datetime
from datetime import timedelta

sep='#'*30


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
        print(s, type(s))
    raise TypeError

def matching_loop(match,pattern,pattern_index,list_item_description,logfile):
    """
    looping logic for price matching
    Assumes:
            match - DataFrame object of current matches
            pattern - current regex pattern
            pattern_index - index of current word inside the item_description
            list_item_description - list of words from the description of the queried item
            logfile - TextIOWrapper object
    Returns:
            match - DataFrame object of current matches
            pattern - current regex pattern
            pattern_index - index of current word inside the item_description
    """
    # add a match group to the pattern
    pattern_index+=1
    pattern += create_pattern(list_item_description[pattern_index])
    ############################### #Logging ###############################
    logfile.writelines([f'\t\tCurrent pattern, iteration and matches\n',f'pattern: {pattern}, pattern index: {pattern_index}, matches: {match.shape[0]}\n'])

    match = match[match.stack().str.contains(pattern,case=False,regex=True).groupby(level=0).any()]
    return match, pattern, pattern_index

def single_match_logic(prod_dict, description,match,df_match_target,logfile):
    """
    Assumes:
        prod_dict - dict grouping sold items with product descriptions as keys
        description - the description of the sold item
        match - dataframe object representing matched items
        df_match_target - dataframe object of products to match to
        logfile - TextIOWrapper object
    Returns:
        prod_dict - dictionary object of grouped sold_product_descriptions
        df_match_target - dataframe object representing all the products
    """
    # change the price of the matched item
    ############################### #Logging ###############################
    logfile.write(f'{sep}\n\t\t\tMATCH FOUND\n{sep}\n')

    match_index = list(match['orgnl_index'])[0]
    prod_dict[description]['price']=match.at[match.index[0],'price']
    prod_dict[description]['matching_indices']=match_index
    df_match_target = df_match_target.drop(list(match.index),axis=0)
    return prod_dict, df_match_target

def multiple_match_logic(description,match,multiple_match_list,df_match_target,logfile):
    """
    Assumes:
            description - str, key from prod_dict
            match - dataframe object representing the matched products
            multiple_match_list - list of dictionaries representing mapping between matched descriptions and match indices of matching products
            df_match_target a dataframe object representing target products to match to
            logfile -  TextIOWrapper object
    Returns:
            multiple_match_list  - with the new description - indices pair
            df_match_target - matching products removed
    """
    ############################### #Logging ###############################
    logfile.writelines([f'{sep}\n\t\t\tMULTIPLE MATCHES FOUND\n{sep}\n',f'product: {description}, matches: {match.shape[0]}\n'])                
    match_index = list(match['orgnl_index'])
    multiple_match_list.append({'description':description,'matche_indices(orgnl_index)':match_index})
    
    df_match_target=df_match_target.drop(list(match.index),axis=0)
    return multiple_match_list, df_match_target

def match_with_categories(
                        list_item_description,
                        df_match_target,
                        product_cats,
                        prod_dict,
                        multiple_match_list,
                        unmatched_dict,
                        description,
                        values,
                        logfile):
    """
    Assumes:
            list_item_description - list object of words from string segments from the description
            df_match_target - dataframe object of products to match to
            product_cats - dict mapping product categories. used to decrease number of unmatched items because of no category match
            prod_dict - dict grouping sold items with product descriptions as keys
            multiple_match_list - list of sold items with multiple matches
            unmatched_dict - dictionary mapping between description of sold items without matches to their values
            description - str object representing current key of matching loop
            values - dict representing a value from prod_dict mapped to the key 'description'
            logfile - TextIOWrapper
    Returns:
            df_match_target - with matched rows dropped
            prod_dict - with updated prices for products
            multiple_match_list - with appended products with multiple matches
            unmatched_dict - with added products with no matches
    """

    list_categories=list(product_cats.keys())
    for category in list_categories:
        if re.search('(?=.*'+category+')',' '.join(list_item_description),flags=re.I):
            pattern = create_pattern(list_item_description[0])
            pattern_index = 0
            match=df_match_target[df_match_target['category']==product_cats[category]].copy()
            match = match[match.stack().str.contains(pattern,case=False,regex=True).groupby(level=0).any()]

            ############################### #Logging ###############################
            logfile.writelines(['\t\tCurrent pattern, iteration and matches:\n',f'pattern: {pattern} pattern index: {pattern_index} matches: {match.shape[0]}\n',f'{match.shape[0]>1} {pattern_index<len(list_item_description)}\n'])
            ############################## #end Logging ###############################
            while match.shape[0]>1 and pattern_index<len(list_item_description)-1:
                match, pattern, pattern_index=matching_loop(match, pattern, pattern_index, list_item_description, logfile)
                
            
            if match.shape[0]==1:
                prod_dict, df_match_target=single_match_logic(prod_dict,description,match,df_match_target,logfile)
            elif match.shape[0]>1:
                multiple_match_list, df_match_target = multiple_match_logic(description,match,multiple_match_list,df_match_target,logfile)
            elif match.shape[0]<1:
                ############################### #Logging ###############################
                logfile.write(f'{sep}\n\t\t\tNO MATCHES FOUND\n{sep}\n')
                unmatched_dict[description]=values
            break

        elif category == list_categories[-1]:
            #handling no matching categories
            logfile.write(f'{sep}\n\t\t\tNO CATEGORY FOUND\n{sep}\n')
            unmatched_dict[description]=values
    
    return df_match_target,prod_dict,multiple_match_list, unmatched_dict

def match_without_categories(list_item_description,
                                df_match_target,
                                prod_dict,
                                multiple_match_list,
                                unmatched_dict,
                                description,
                                values,
                                logfile,
                                on_unmatched=False):
    """
    Assumes:
            list_item_description - list object of words from string segments from the description
            df_match_target - dataframe object of products to match to
            prod_dict - dict grouping sold items with product descriptions as keys
            multiple_match_list - list of sold items with multiple matches
            unmatched_dict - dictionary mapping between description of sold items without matches to their values
            description - str object representing current key of matching loop
            values - dict representing a value from prod_dict mapped to the key 'description'
            logfile - TextIOWrapper
            on_unmatched - bool, representing switch for looping on unmatched items
    Returns:
            df_match_target - with matched rows dropped
            prod_dict - with updated prices for products
            multiple_match_list - with appended products with multiple matches
            unmatched_dict - with added products with no matches
    """
    
    pattern = create_pattern(list_item_description[0])
    pattern_index = 0
    match=df_match_target.copy()
    match = match[match.stack().str.contains(pattern,case=False,regex=True).groupby(level=0).any()]

    ############################### #Logging ###############################
    logfile.writelines(['\t\tCurrent pattern, iteration and matches:\n',f'pattern: {pattern} pattern index: {pattern_index} matches: {match.shape[0]}\n',f'{match.shape[0]>1} {pattern_index<len(list_item_description)}\n'])
    ############################## #end Logging ###############################
    while match.shape[0]>1 and pattern_index<len(list_item_description)-1:
        match, pattern, pattern_index=matching_loop(match, pattern, pattern_index, list_item_description, logfile)
        
    
    if match.shape[0]==1:
        prod_dict, df_match_target=single_match_logic(prod_dict,description,match,df_match_target,logfile)
        if on_unmatched:
            del unmatched_dict[description]
    elif match.shape[0]>1:
        multiple_match_list, df_match_target = multiple_match_logic(description,match,multiple_match_list,df_match_target,logfile)
        if on_unmatched:
            del unmatched_dict[description]
    elif match.shape[0]<1 and not on_unmatched:
        ############################### #Logging ###############################
        logfile.write(f'{sep}\n\t\t\tNO MATCHES FOUND\n{sep}\n')
        unmatched_dict[description]=values
            
    
    return df_match_target,prod_dict,multiple_match_list, unmatched_dict


def matching_wrapper(
                        df_match_target,
                        prod_dict,
                        multiple_match_list,
                        unmatched_dict,
                        product_cats,
                        logfile,
                        errlog,
                        with_categories=True,
                        on_unmatched = False,
                        ):
    """
    Assumes:
            df_match_target - dataframe object of products to match to
            prod_dict - dict grouping sold items with product descriptions as keys
            unmatched_dict - dictionary mapping between description of unmatched items to their values
            multiple_match_list - list of multiple matched items
            product_cats - dict mapping product categories. used to decrease number of unmatched items because of no category match
            logfile - TextIOWrapper object
            with_categories - boolean, used to switch matching with categories, default True
            on_unmatched - boolean, used to switch looping over unmatched items
    Returns:
            prod_dict - with updated prices
            multiple_match_list - populated with multiple matches
            unmatched_dict - populated with no matches
    """
    df_match_target = df_match_target.copy()
    counter=1

    timedeltas = []
    try:
        
        if not on_unmatched:

            for description,values in list(prod_dict.items()):
                loop_begin=datetime.now()
                #split the product description by '*-*'
                list_item_description = values['formatted_description'].split('*-*')
                
                ########################### #Logging ###############################
                logfile.writelines(['\t\tDescribing Items\n',f'description: {list_item_description}\n'])

                if with_categories:
                    df_match_target,prod_dict,multiple_match_list, unmatched_dict = match_with_categories(list_item_description,df_match_target,product_cats,prod_dict,multiple_match_list,unmatched_dict,description,values,logfile)
                else:
                    df_match_target,prod_dict,multiple_match_list, unmatched_dict=match_without_categories(list_item_description,df_match_target,prod_dict,multiple_match_list,unmatched_dict,description,values,logfile,on_unmatched)
                
                logfile.write(f'iteration: {counter}\n')
                print(f'iteration: {counter}\n')
                counter+=1
                logfile.write(f'unmatched items: {len(unmatched_dict)}\nMultiple matches: {len(multiple_match_list)}\n\n END ITERATION\n{sep}\n')
                timedeltas.append(datetime.now()-loop_begin)
        else:

            for description,values in list(unmatched_dict.items()):
                loop_begin=datetime.now()
                #split the product description by '*-*'
                list_item_description = values['formatted_description'].split('*-*')
                
                ########################### #Logging ###############################
                logfile.writelines(['\t\tDescribing Items\n',f'description: {list_item_description}\n'])

                if with_categories:
                    df_match_target,prod_dict,multiple_match_list, unmatched_dict = match_with_categories(list_item_description,df_match_target,product_cats,prod_dict,multiple_match_list,unmatched_dict,description,logfile)
                else:
                    df_match_target,prod_dict,multiple_match_list, unmatched_dict=match_without_categories(
                        list_item_description, 
                        df_match_target, 
                        prod_dict,  
                        multiple_match_list,
                        unmatched_dict, 
                        description,  
                        values,     
                        logfile,   
                        on_unmatched 
                        )
            
                logfile.write(f'iteration: {counter}\n')
                print(f'iteration: {counter}\n')
                counter+=1
                logfile.write(f'unmatched items: {len(unmatched_dict)}\nMultiple matches: {len(multiple_match_list)}\n\n END ITERATION\n{sep}\n')
                timedeltas.append(datetime.now()-loop_begin)

    except Exception as e:
        print('exception occured')
        import traceback
        errlog.writelines([f'{sep}\nERROR\n{sep}',traceback.format_exc()])
        raise e
    
    logfile.write(f'{sep}\nLOOP SUMMARY\n{sep}\nAverage time for item search: {sum(timedeltas, timedelta(0))/len(timedeltas)}\n{sep}\n{sep}\n')
    return prod_dict,multiple_match_list,unmatched_dict, df_match_target
