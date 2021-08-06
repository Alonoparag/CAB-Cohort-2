import unittest
import yaml


class TestProductListYmlFile(unittest.TestCase):
    """
    Tests that each product listed in the product_list.yml file has valid entries for:
                                                                                    product_name
                                                                                    path
                                                                                    main_url
                   


                                                                 secondary_url
                                                                                    yml_file
    """
    def setUp(self):
        self.products=yaml.load(open('product_list.yml', 'r'), Loader=yaml.FullLoader)
    
    def test_entries(self):
        for product in self.products:
            with self.subTest(product=product):
                self.assertIn("product_name", product.keys(), msg=f'Error: {product} Product name not specified')
                #
                self.assertIn("path", product.keys(), msg=f'Error: The product {product["product_name"]} path is not specified in the productc_list.yml file')
                #
                self.assertIn("main_url", product.keys(), msg=f'Error: The product {product["product_name"]} markup is missing main_url. Please check product_list.yml')
                #
                self.assertIn('https://www.amazon.com/s?', product["main_url"], msg=f'Error: Wrong amazon serach URL in first list item. Check {product["product_name"]}\'s main_url in file product_list.yml ')
                #
                self.assertIn("secondary_url",product.keys(),  msg=f'Error: The product {product["product_name"]} markup is missing secondary_url. Please check product_list.yml')
                #
                self.assertIn('https://www.amazon.com/s?', product["secondary_url"], msg=f'Error: Wrong amazon serach URL in first list item. Check {product["product_name"]}\'s secondary_url in file product_list.yml ')
                #
                self.assertIn("yml_file", product.keys(),  msg=f'Error: The product {product["product_name"]} markup is missing yml_file. Please check product_list.yml')
                #
                self.assertIn("_description.yml", product["yml_file"], msg=f'Error: The product {product["product_name"]} yml_file path is invalid. a valid path ends with {product["product_name"]}_description.yml')
                #
                self.assertIsNotNone(yaml.load(open(product['yml_file'], 'r'), Loader=yaml.FullLoader), msg=f"_description.yml file of {product['product_name']} is empty. Please check readme file for instructions how to set a valid markup file")