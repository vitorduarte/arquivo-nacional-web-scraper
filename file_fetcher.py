import urllib
import requests
import ast
import time
import json
import os
import logging

import Colorer

from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M')

module_logger = logging.getLogger('Arquivo Nacional')

class Collection:
    def __init__(self, namespace):
        self.namespace = namespace
        self._get_name(self.namespace)

    def _get_name(self, namespace):
        with open('fundos/nome_fundos.json') as file:
            name_collections = json.load(file)
        try:
            name_collection = name_collections[namespace]
            self.name = name_collection
        except:
            print('Invalid collection name')
            exit(1)


class FileFetcher:
    # Ideally, the cookies will be taken using user credentials but
    # it is not working. I just take the cookies from browser and send here
    def __init__(self, collection, cookies={}):
        self.cookies = cookies
        self.logger = module_logger
        self.collection = collection

        self._add_file_handler()
        self._get_collection_info()

    # Add an file handler to store the log
    def _add_file_handler(self):
        formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')

        fh = logging.FileHandler('temp/{}.log'.format(self.collection.namespace))
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # Get information about a collection
    def _get_collection_info(self):
        first_page = self._get_page(1)
        collection_info = self._get_page_info(first_page)

        self.collection.num_pages = collection_info['page_total']
        self.collection.num_registries = collection_info['registries_total']
        self.logger.info('\n{}\n\tPages: {}\n\tRegistries: {}\n'.format(self.collection.name,
                                                                        self.collection.num_pages,
                                                                        self.collection.num_registries))

    # Get the download links to files
    def get_download_links(self, page_init=1, page_end=-1):

        # Check page_init and page_end
        if page_end == -1 or page_end > self.collection.num_pages:
            page_end = self.collection.num_pages

        if page_init > self.collection.num_pages:
            self.logger.error('Invalid value of initial page')

        # Get the urls
        links = []

        for i in range(page_init,page_end + 1):
            # Get page
            page = self._get_page(i)

            # Get links
            new_links = self._get_links(page)
            links = links + new_links

            self.logger.info('\nPage: {}/{} \nFetched Links: {}'.format(i,
                                                                        self.collection.num_pages,
                                                                        len(links)))

            # Save links of this page
            with open('links/{}/page{}.txt'.format(self.collection.name, i), 'w') as file:
                for link in new_links:
                    file.write(link + '\n')

        # Save all links
        with open('links/{}/{}-{}.txt'.format(self.collection.name, page_init, page_end), 'w') as file:
                for link in links:
                    file.write(link + '\n')

    # Open an page using pagination and return this data
    def _get_page(self, page_num):
        base_url = 'http://sian.an.gov.br/sianex/Consulta/resultado_pesquisa_pdf.asp'
        params = urllib.parse.urlencode({'Pages': page_num, 'input_pesqfundocolecao':self.collection.namespace })
        url = base_url + '?' + params

        r = None
        while r is None:
            try:
                r = requests.post(url, cookies=self.cookies)
                try:
                    parsed_r = BeautifulSoup(r.content, 'html.parser')
                    self._get_page_info(parsed_r)
                except:
                    cookies_string = input('Invalid cookies, type the cookie here: ')
                    cookies = cookies_string.replace("'", "\"")
                    self.cookies = ast.literal_eval(cookies)
                    r = None

            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(5)

        parsed_r = BeautifulSoup(r.content, 'html.parser')

        return parsed_r

    # Get links from an page
    def _get_links(self, page):
        data = page.findAll('a', class_='help_pesquisa', title="Fazer download do arquivo")
        new_links = [self._get_url(file) for file in data]
        return new_links

    # Return the url of an help_pesquisa response
    def _get_url(self, file):
        base_url = 'http://sian.an.gov.br/sianex/Consulta/download.asp'
        onclick = file.get('onclick')

        # Remove prefix
        prefix = 'javascript:fjs_Link_download('
        if onclick.startswith(prefix):
            onclick = onclick[len(prefix):]

        # Remove unused characters
        onclick = onclick.replace("'", '')
        onclick = onclick.replace(");", '')

        # Convert to url
        onclick = onclick.split(',')

        # Get parameters
        if len(onclick) == 3:
            params = urllib.parse.urlencode({'arquivo': onclick[0], 'NomeArquivo': onclick[1], 'apresentacao': onclick[2]})
        elif len(onclick) == 2:
            params = urllib.parse.urlencode({'arquivo': onclick[0], 'NomeArquivo': onclick[1]})
        else:
            params = urllib.parse.urlencode({'arquivo': onclick[0]})

        # Finish url
        url = base_url + '?' + params
        return url

    # Return information about a page
    def _get_page_info(self, page):
        script = page.findAll('script', type='text/javascript')[-1].text
        script = script.replace('var ', '')
        script = script.replace('\n', '')
        script = script.replace(' ', '')
        script = script.split(';')

        registries_total = int(script[0].split('=')[-1])
        page_registries = int(script[1].split('=')[-1])
        page_total = int(script[2].split('=')[-1])
        page = int(script[3].split('=')[-1])

        return {
            "registries_total": registries_total,
            "page_registries": page_registries,
            "page_total": page_total,
            "page": page,
        }

    # Download links in a folder
    def download_links(self, links, folder):
        total = len(links)

        for idx, link in enumerate(links):
            # Get queries
            url_parsed = urllib.request.urlparse(link)
            url_queries = dict(urllib.parse.parse_qsl(url_parsed.query))

            # Get file details
            filename = url_queries['NomeArquivo']
            collection_folder = self.collection.name

            download = False
            while not download:
                try:
                    path_file = os.path.join(folder, collection_folder, filename)
                    urllib.request.urlretrieve(link, path_file)
                    self.logger.info('\nFile: {}/{} \n\tFilename: {}'.format(idx,
                                                                               total,
                                                                               filename))
                    download = True
                except Exception as e:
                    self.logger.error('\nNão foi possível realizar o download, tentando novamente...\n{}'.format(e))
