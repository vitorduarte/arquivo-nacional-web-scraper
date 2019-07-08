import file_fetcher as ffch
# all_collections = [line.rstrip('\n') for line in open('collections.txt')]
all_collections = ["BR_DFANBSB_AAC","BR_DFANBSB_2M","BR_DFANBSB_AT3","BR_RJANRIO_FS","BR_DFANBSB_AT2","BR_DFANBSB_35","BR_RJANRIO_35","BR_DFANBSB_VAX","BR_DFANBSB_JF","BR_RJANRIO_X9","BR_RJANRIO_QL","BR_RJANRIO_D7","BR_RJANRIO_1S","BR_RJANRIO_RH","BR_RJANRIO_LC","BR_RJANRIO_ML","BR_DFANBSB_DP","BR_RJANRIO_4T","BR_RJANRIO_S7","BR_RJANRIO_F3","BR_DFANBSB_AQ","BR_RJANRIO_AQ","BR_RJANRIO_U2","BR_DFANBSB_HL","BR_DFANBSB_H4","BR_RJANRIO_H4","BR_RJANRIO_TN","BR_DFANBSB_V8","BR_RJANRIO_V8","BR_DFANBSB_XR","BR_RJANRIO_GJ","BR_DFANBSB_TS","BR_DFANBSB_HI","BR_DFANBSB_HJ","BR_DFANBSB_VAY","BR_DFANBSB_CZ"]

cookies = {
    'ASPSESSIONIDQCRBDSAD': 'FDDKGIEDFOALEJPMLMCIGNGD',
    '__utma': '241364224.1523884295.1545517022.1545517022.1545517022.1',
    '__utmc': '241364224',
    '__utmz': '241364224.1545517022.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '_ga': 'GA1.3.1523884295.1545517022',
    '_gid': 'GA1.3.731421984.1545517022',
    'TS01aa4f71_77': '08b45f120fab2800df8d53e789ac30c4ecde77c82fad6c47e65a4daaa7c913aa67a21b4243120bead8ee78dde7699c0208ed9a88df8240000559ccc9a11e52b7c15023c6efbdf0902e50b0301bfe275922bcbf25cdde1510d4459b889a7bafe2afa16e013ff4b683f09326e7e1dff7be1933087dbe94fac4',
    'TS01aa4f71': '0155147e19f58b77a62b601f82c15eeb164bc93a10d1a6d5b33b022151c7f49abbfb0639cfa8f2b2b7d62de9be8460a9053cef43e1c74acddc09cb02b61af19b23837627b5',
    '_gat': '1',
    '__utmt': '1',
    '__utmb': '241364224.31.10.1545517022',
}


for collection_name in all_collections:
    collection = ffch.Collection(collection_name)
    file_fetcher = ffch.FileFetcher(collection, cookies)
