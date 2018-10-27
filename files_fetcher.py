import urllib
import requests

from bs4 import BeautifulSoup

class FileFetcher:
    # Ideally, the cookies will be taken using user credentials but
    # it is not working. I just take the cookies from browser and send here
    def __init__(self, cookies):
        self.cookies = cookies

    # Get the download links to files
    #   int pageMax - max of pages to get links
    #   collections - list of collections to search
    def get_download_links(self, pageMax, collections):
        data = [('input_pesqfundocolecao', collection) for collection in collections]
        response = requests.post('http://sian.an.gov.br/sianex/Consulta/resultado_pesquisa_pdf.asp',
                                    cookies=self.cookies,
                                    data=data)

        parsed_response = BeautifulSoup(response.content, 'html.parser')
        file_data = parsed_response.findAll('a', class_='help_pesquisa', title="Fazer download do arquivo")
        links = [self.generateURL(file) for file in file_data]
        print(links[0])
        return links

        # return response

    # Return the url of an help_pesquisa response
    def generateURL(self, file):
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
