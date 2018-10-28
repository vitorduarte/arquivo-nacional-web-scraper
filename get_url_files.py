import file_fetcher as ffch


cookies = {
    'INSERT HERE THE TOKEN FIELDS'
}


file_fetcher = ffch.FileFetcher(cookies)
collections = [line.rstrip('\n') for line in open('collections.txt')]

response = file_fetcher.get_download_links(['1'])

with open('all_links.txt', 'w') as the_file:
        for item in response:
            the_file.write(item + '\n')
