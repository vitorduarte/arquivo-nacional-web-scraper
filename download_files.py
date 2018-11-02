import file_fetcher as ffch

cookies = {}

collection = ffch.Collection('BR_RJANRIO_CNV')
file_fetcher = ffch.FileFetcher(collection, cookies)

page_init = 1
page_end = 118

links = [line.rstrip('\n') for line in open('links/{}/{}-{}.txt'.format(collection.name, page_init, page_end), 'r')]
file_fetcher.download_links(links, './downloads')
