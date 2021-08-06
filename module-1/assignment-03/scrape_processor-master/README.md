# Scrape_processor
Code originally created by Shekhar Biswas [Original code](https://github.com/shekharbiswas/scrape_processor)

Changes made by [Alon Parag](https://github.com/alonoparag):

## Dependencies:
* selectorlib
* yaml
* json
* browser-cookie3
* fake-useragent

## Flow scheme

![Workflow of scrape-processor](/app_schema.png)

## Usage
This project helps to get product information from the listed products on amazon web page.
1. *In product_list.yml* list the products that you want to scrape:
   * each product should have the following key-values:
     * product_name.
     * main_url (the url of the first page for that product).
     * and secondary_url (url representing the 2nd onwards pages of the product search).
     * yml_file - path to a yml file describing which selectors the scraper should use. must end with `_description.yml`.
     * path - the path to the product directory. use `/products/\[product_name\]`.
2. Running the app, you are required to specify the browser which is installed on your system by either using `-b` or `--browser` option. the app supports the following browsers:
   * Firefox,
   * Chrome,
   * Edge,
   * Opera,
   * Chromium.
3. run the app from the root directory as `python app.py -b \[browser\] [-t] [-v] [-l] [-s] [-h] -[V]`/
4. You can run the test suite either with unittest or pytest.
5. You may also use `-v/--verbose` to print messages to the console, and `-l/--log` to log the scrape process to a txt file, that will be created in the product directory specified by `product\['path'\]`.
6. In strict mode `-s/--strict` the app raises an EmptyYmlFileError if a product has an empty yml file. in non-strict mode the app prints a warning to the console and skips to the next product
7. lastly the `-t/--test` flag is used to debug the connection to the scraped site (www.amazon.com). it runs the app with th product processor, using the first search page, scraping the search information of the 1st ten products, and logging it to a file.



The youtube tutorial for the original app is here:

[![Web Scrape Amazon : Processor (Computer ) using Python](https://img.youtube.com/vi/0jY-ULpZq50/0.jpg)](https://www.youtube.com/watch?v=0jY-ULpZq50)


## Changelog (Alon Parag)
* Wrapped 'create_search_url.py','search.py','product.py' in a single app.
* automated scraping process.
* Solved captcha blocking from amazon by using a Http session and cookies.
* Enabled user to use options from command line.
* Added testing into the app.