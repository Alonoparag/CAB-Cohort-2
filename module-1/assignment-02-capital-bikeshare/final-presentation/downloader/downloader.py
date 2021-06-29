from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import polling2, time
import subprocess
import os

def get_links(driver):
    """
    Assumes:
         driver a selenium webdriver
    Returns:
        a list of download urls.
         
    """
    return driver.execute_script('''
    let URLs = [];
    let cells = document.querySelectorAll('a');
    cells.forEach((cell)=>URLs.push(cell.href));
    return URLs
    ''')

def downloader(link):
    """
    Assumes:
         link is a string representing a URL
    Returns:
        None
         
    """
    path_datasets = '/home/alonp/Documents/CABerlin/module-1/assignment-02-capital-bikeshare/datasets'
    link_name = link.split("/")[-1]

    cmd_mkdir = ['mkdir', f'{path_datasets}/cbs-historical']
    cmd_curl=['curl', '-o', f'{path_datasets}/cbs-historical/{link_name}', link]
    cmd_unzip=['unzip', f'{path_datasets}/cbs-historical/{link_name}','-d',f'{path_datasets}/cbs-historical/']
    cmd_rmzip = ['rm',f'{path_datasets}/cbs-historical/{link_name}']
    subprocess.call(cmd_mkdir)

    print('='*10,f'Downloading {link_name}','='*10,sep='\n',end='\n')
    commands = [cmd_curl,cmd_unzip, cmd_rmzip]
    for cmd in commands:
        print(f'Executing {cmd[0]}')
        try:
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            out, err = p.communicate()
            for line in out.decode('utf-8').split('\n'):
                print(line)
        except:
            print(f'Error occoured while downloading {link_name}')


def download_data():
    # Method to implement retrieval of download links, downloading of objects from URL's and unzipping the data.
    delay = 10
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
    url ='https://s3.amazonaws.com/capitalbikeshare-data/index.html'
    driver.get(url)

    try:
        link = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        links = get_links(driver)
        links.pop()
        # downloader(links[0]) #TEST LINE
        for link in links[-12:]:
            downloader(link)
        os.system('rm -rf /home/alonp/Documents/CABerlin/module-1/assignment-02-capital-bikeshare/datasets/cbs-historical/__MACOSX')

    except TimeoutException as e:
        print(e, 'loading time exceeded 3 minutes', sep='\n')
    finally:
        driver.close()

if __name__ == '__main__':
    download_data()