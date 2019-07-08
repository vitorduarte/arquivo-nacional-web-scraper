from urllib.parse import urlparse
from urllib.parse import parse_qs

import json
import sys
import os

# Define constants
DOWNLOAD_FINSH=72
DOWNLOAD_ERROR=33

class DownloadCategory:
    def __init__(self, category_file):
        self.category_file = category_file

    def fix_name_in_folder(self, folder):
        with open(self.category_file, 'r') as f:
            json_collection = json.load(f)

        for f in json_collection['children']:
            file = File()
            file.fetch_from_category(f)
            file.fix_filename(folder)

    def fix_name_in_category_file(self):
        with open(self.category_file, 'r') as f:
            json_collection = json.load(f)

        for f in json_collection['children']:
            file = File()
            file.fetch_from_category(f)
            f = file.fix_name_in_category()

        with open(self.category_file, 'w') as out_file:
            json.dump(json_collection, out_file)

    def generate_alternative_links(self):
        new_urls = []

        with open(self.category_file, 'r') as f:
            json_collection = json.load(f)

        for f in json_collection['children']:
            file = File()
            file.fetch_from_category(f)
            if file.state == DOWNLOAD_ERROR:
                new_url = file.generate_alternative_url()
                new_urls.append(new_url)

        return new_urls

    def generate_file_list(self):
        file_list = []
        with open(self.category_file, 'r') as f:
            json_collection = json.load(f)

        for f in json_collection['children']:
            file = File()
            file.fetch_from_category(f)
            file_list.append(file.name)

        return file_list

class File:
    def fetch_from_name(self, filename):
        self.name = filename
    def fetch_from_category(self, file):
        if 'state' in file:
            self.version = 1
            self.name = file['name']
            self.state = file['state']
            self.url = urlparse(file['info']['common']['uri'])
            self.file_data = file
        elif 'data' in file:
            self.version = 2
            self.name = file['data']['common']['name']
            self.state = file['data']['relation']['group']
            self.url = urlparse(file['data']['common']['uri'])
            self.file_data = file
        else:
            raise RuntimeError('Invalid file category data')
    def fix_filename(self, folder):
        if self.state == DOWNLOAD_FINSH and self.name.startswith('download.asp') :
            # Get new filename and path information
            new_name = parse_qs(self.url.query)['NomeArquivo'][0]
            file_old_path = folder + '/' + self.name
            file_new_path = folder + '/' + new_name

            # Check if path are valid
            file_new_valid =  os.path.isfile(file_new_path)
            file_old_valid = os.path.isfile(file_old_path)

            if file_old_valid and file_new_valid:
                download_asp_size = os.path.getsize(file_old_path)
                right_name_size = os.path.getsize(file_new_path)
                if download_asp_size > right_name_size:
                    os.rename(file_old_path,file_new_path)
                else:
                    os.remove(file_old_path)
            if file_old_valid and not file_new_valid:
                os.rename(file_old_path,file_new_path)



    def fix_name_in_category(self):
        if self.name.startswith('download.asp'):
            new_name = parse_qs(self.url.query)['NomeArquivo'][0]
            self.name = new_name
            if self.version == 1:
                self.file_data['name'] = new_name
            elif self.version == 2:
                self.file_data['data']['common']['name'] = new_name
                self.file_data['data']['common']['file'] = new_name
        return self.file_data

    def generate_alternative_url(self):
        base_url = 'http://imagem.sian.an.gov.br/acervo/derivadas'
        split_name = self.name.split('_')
        collection_name = '_'.join(split_name[0:3])

        if collection_name.lower() == "br_rjanrio_s7":
            new_url = '{}/{}/0/txt/{}/{}'.format(base_url, collection_name, split_name[3], self.name)
        elif collection_name.lower() == "br_rjanrio_v8":
            col_name_1=collection_name + '_' + split_name[3]
            col_name_2=col_name_1 + '_' + split_name[4]

            new_url = '{}/{}/{}/{}/{}/{}'.format(base_url, collection_name,
                                                'prontuarios_de_pessoas_fisicas_e_juridicas', col_name_1,
                                                col_name_2, self.name)
        elif collection_name.lower() == "br_dfanbsb_vax":
            col_name_1=collection_name + '_' + split_name[3]
            col_name_2=col_name_1 + '_' + split_name[4]
            if split_name[5] == "":
                idx_next = 6
            else:
                idx_next = 5

            col_name_3=col_name_2 + '_' + split_name[idx_next]

            digit=split_name[idx_next+1][1]

            if split_name[idx_next+1][2] != '0' and split_name[idx_next+1][2] != '.':
                digit = digit + split_name[idx_next+1][2]

            col_name_4=col_name_3 + '_' + digit


            new_url = '{}/{}/{}/{}/{}/{}/{}'.format(base_url,
                                                    collection_name,
                                                    col_name_1,
                                                    col_name_2,
                                                    col_name_3,
                                                    col_name_4,
                                                    self.name)
        elif collection_name.lower() == "br_dfanbsb_jf":
            col_name_1=collection_name + '_' + split_name[3]
            col_name_2=col_name_1 + '_' + split_name[4]
            col_name_3=col_name_2 + '_' + split_name[5]

            digit=int(split_name[6])

            col_name_4=col_name_3 + '_' + str(digit)


            new_url = '{}/{}/{}/{}/{}/{}/{}'.format(base_url,
                                                    collection_name,
                                                    col_name_1,
                                                    col_name_2,
                                                    col_name_3,
                                                    col_name_4,
                                                    self.name)
        else:
            split_end = -1
            if collection_name.lower() == "br_rjanrio_h4":
                split_end = -3
            new_url = '{}/{}'.format(base_url, collection_name)
            for elem in split_name[3:split_end]:
                new_url = '{}/{}'.format(new_url, elem)
            new_url = '{}/{}'.format(new_url, self.name)

        self.new_url = new_url
        return new_url
