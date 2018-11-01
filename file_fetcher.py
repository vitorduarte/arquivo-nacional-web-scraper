import urllib
import requests
import ast
import time
import json
import os

from bs4 import BeautifulSoup

class FileFetcher:
    # Ideally, the cookies will be taken using user credentials but
    # it is not working. I just take the cookies from browser and send here
    def __init__(self, cookies):
        self.cookies = cookies

        with open('fundos/nome_fundos.json') as nome_fundos:
            nome_fundos = json.load(nome_fundos)
        self.nome_fundos = nome_fundos

    # Get the download links to files
    #   int pageMax - max of pages to get links
    #   collections - list of collections to search
    def get_download_links(self, collections, page_init=1, page_max=-1):

        # Do the first request
        first_page = self._get_page(collections, 1)
        page_info = self._get_page_info(first_page)
        if page_max == -1 or page_max > page_info['page_total']:
            page_max = page_info['page_total']

        print('-'*30)
        print("Total of registries: {}".format(page_info['registries_total']))
        print("Page max: {}".format(page_max))

        # Get the urls
        links = []

        for i in range(page_init,page_max + 1):
            # Get page
            page = self._get_page(collections, i)
            page_info = self._get_page_info(page)
            self._print_page_info(page_info)

            data = first_page.findAll('a', class_='help_pesquisa', title="Fazer download do arquivo")
            new_links = [self._get_url(file) for file in data]
            links = links + new_links

            print('Actual: {}'.format(len(links)))
            print('-'*30)

            with open('links/links{}.txt'.format(i), 'w') as the_file:
                for link in new_links:
                    the_file.write(link + '\n')

        return links

    def download_links(self, links, folder):
        total = len(links)
        for idx, link in enumerate(links):
            # Get queries
            url_parsed = urllib.request.urlparse(link)
            url_queries = dict(urllib.parse.parse_qsl(url_parsed.query))

            # Get file details
            filename = url_queries['NomeArquivo']
            filename_splited = filename.split('_')
            collection = '_'.join(filename_splited[0:3])
            collection_folder = self.nome_fundos[collection]


            download = False
            while not download:
                try:
                    path_file = os.path.join(folder, collection_folder, filename)
                    urllib.request.urlretrieve(link, path_file)
                    print(idx + 1, "/", total)
                    print('-'*40)
                    print('Filename: {}'.format(filename))
                    print('Folder: {}'.format(collection_folder))
                    print('-'*40, "\n")
                    download = True
                except:
                    print('Não foi possível realizar o download, tentando novamente...\n')


    def _get_page(self, collections, page_total):
        base_url = 'http://sian.an.gov.br/sianex/Consulta/resultado_pesquisa_pdf.asp'
        params = urllib.parse.urlencode({'Pages': page_total})
        url = base_url + '?' + params

        data = [('input_pesqfundocolecao', collection) for collection in collections]

        r = None
        while r is None:
            try:
                r = requests.post(url, cookies=self.cookies, data=data)
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

    def _print_page_info(self, page_info):
        print('-'*30)
        print("Page: {}/{}\n".format(page_info['page'], page_info['page_total']))
