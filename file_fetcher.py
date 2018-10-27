import urllib
import requests

from bs4 import BeautifulSoup

class FileFetcher:
    # Ideally, the cookies will be taken using user credentials but
    # it is not working. I just take the cookies from browser and send here
    def __init__(self, cookies):
        self.cookies = cookies

    def _get_page(self, collections, page_total):
        base_url = 'http://sian.an.gov.br/sianex/Consulta/resultado_pesquisa_pdf.asp'
        params = urllib.parse.urlencode({'Pages': page_total})
        url = base_url + '?' + params

        data = [('input_pesqfundocolecao', collection) for collection in collections]

        r = requests.post(url, cookies=self.cookies, data=data)
        parsed_r = BeautifulSoup(r.content, 'html.parser')

        return parsed_r


    # Get the download links to files
    #   int pageMax - max of pages to get links
    #   collections - list of collections to search
    def get_download_links(self, collections, page_max=-1):

        # Do the first request
        first_page = self._get_page(collections, 1)
        page_info = self._get_page_info(first_page)
        if page_max == -1 or page_max > page_info['page_total']:
            page_max = page_info['page_total']

        print('-'*30)
        print("Total of registries: {}".format(page_info['registries_total']))
        print("Page max: {}".format(page_max))

        self._print_page_info(page_info)

        # Get the urls
        data = first_page.findAll('a', class_='help_pesquisa', title="Fazer download do arquivo")
        links = [self._get_url(file) for file in data]
        print('Registries: {}'.format(len(links)))
        print('-'*30)

        for i in range(2,page_max + 1):
            # Get page
            page = self._get_page(collections, i)
            page_info = self._get_page_info(page)
            self._print_page_info(page_info)

            data = first_page.findAll('a', class_='help_pesquisa', title="Fazer download do arquivo")
            new_links = [self._get_url(file) for file in data]
            links = links + new_links

            print('Actual: {}'.format(len(links)))
            print('-'*30)

        return links

        # return response

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
