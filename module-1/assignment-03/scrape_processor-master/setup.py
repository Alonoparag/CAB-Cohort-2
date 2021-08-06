from setuptools import setup,find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='scrape_processor_cab',
    version='1.1.0',
    description="""
                    web scrapring module for code academy berlin users
                    Originally written by Shekhar Biswas.
                    Modified and packaged by Alon Parag.
                """,
    long_description=readme(),
    classifiers=[
        'Development Status ::1 - Production', 
        'License :: OSI Approved :: MIT License',
        'Programming Language ::Python 3.9',
        'Topic :: Internet :: Web Scraping'
    ],
    keywords='scrape processor cab',
    author='Shekhar Biswas, Alon Parag',
    author_email='allon.parag@gmail.com',
    url='https://github.com/Alonoparag/scrape_processor',
    packages=find_packages(include=['scrape_processor','scrape_processor.*']),
    setup_requires='pytest-runner',
    tests_require=['pytest'],
    install_requires=['pytest',
        'pytest-runner',
        'scrape_processor',
        'selectorlib',
        'requests',
        'yaml',
        'json',
        'browser-cookie3',
        'fake-useragent',
        'random',
        'time',
        'datetime',
        ],
    license='MIT',
    zip_safe=False,include_package_data=True,

)