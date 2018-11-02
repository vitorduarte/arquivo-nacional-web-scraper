import file_fetcher as ffch
all_collections = [line.rstrip('\n') for line in open('collections.txt')]

collection = ffch.Collection('BR_RJANRIO_CNV')
file_fetcher = ffch.FileFetcher(collection, cookies)
file_fetcher.get_download_links(page_init=1, page_end=2)
