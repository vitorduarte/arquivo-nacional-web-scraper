import file_fetcher as ffch

cookies = {
    'ASPSESSIONIDQSSDCRBR': 'IFAPOMCCOOIBICHGKDIFFJIJ',
    '_ga': 'GA1.3.1979139345.1542291482',
    '_gid': 'GA1.3.1562914261.1542291482',
    '__utmc': '241364224',
    '__utmz': '241364224.1542291482.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'TS01aa4f71_77': '08b45f120fab28000937488a3647cfe4eb629b3cd44be91ac439c867668b6404f10b67a5afee2e78fa6266f493dbd60708d50d6d1482400016000ba4bba6b1ba9c54967a3ae4f6a71fe23388bebad47dbd83345ef2660273cc6562964759c3d44878ca018a018eff5275af0baba39dd6d086dfc95a95acad',
    'TS01aa4f71': '0155147e198de51f41d0d1eeac2badf5d102fb70e320679b197e0c0b21cbe6e6a0cf6c3f9b209fa64a12f20d6cd9128026cf2f7fec000bc511887eb8f64d721532abaa7731',
    '__utma': '241364224.1979139345.1542291482.1542291482.1542297408.2',
    '__utmt': '1',
    '__utmb': '241364224.1.10.1542297408',
    '_gat': '1',
}

collection = ffch.Collection('BR_DFANBSB_1M')
file_fetcher = ffch.FileFetcher(collection, cookies)

# page_init = file_fetcher.collection.
# page_end = 118

links = [line.rstrip('\n') for line in open('links/download2.txt', 'r')]
print(links)
file_fetcher.download_links(links, './downloads', max_simultaneus=5)
