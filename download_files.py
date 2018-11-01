import file_fetcher as ffch

cookies = {}

file_fetcher = ffch.FileFetcher(cookies)
links = [line.rstrip('\n') for line in open('links-1-5890.txt', 'r')]

file_fetcher.download_links(links[0:10], './downloads')
