import file_fetcher as ffch


cookies = {
    'f5_cspm': '1234',
    'ASPSESSIONIDSSQBCQAQ': 'PHJOJJGALAABBIHINKMJLBHC',
    '__utmc': '241364224',
    '__utmz': '241364224.1540492555.1.1.utmcsr=arquivonacional.gov.br|utmccn=(referral)|utmcmd=referral|utmcct=/br/consulta-ao-acervo/bases-de-dados.html',
    '_ga': 'GA1.3.1328606591.1540492555',
    'ASPSESSIONIDQSQCCQAR': 'NKGKPCMBJOHLOBGBGJIKJNMP',
    'TS01aa4f71_26': '012fe7252bc199769d2dd82aec5616e3c8f7be04114c51b9b5e5531dd277f4ac382f2225779c4c929210f5dfdb3bc0b087a1669b10fe4ef8651707f9dd5056ee905407ab1d',
    '__utma': '241364224.1328606591.1540492555.1540626470.1540629619.7',
    'ASPSESSIONIDSQQCCRBR': 'OEHDOOICEBBLBBGBIAIBKFGF',
    'ASPSESSIONIDSSRCDRBR': 'BFCCEJFAHGEPJOGAJBFFFKMJ',
    'ASPSESSIONIDQSSABRAQ': 'GHPJCFCBHINJMNLIPDKOPICE',
    'ASPSESSIONIDQQQDARBQ': 'IGJGBBPBLAIDDDOEDEIEMCJO',
    'TS01aa4f71_77': '08b45f120fab28007a54604087699f982e52c46b802cf88266e05b73acdd5270ef7ac23f92ef8a13b310a728157e7c1508a4a088e8824000a780ea601e9605fd3b3d1707b9458a245590c9e047c688f4fe2576026822cbc831c793aceb5459243b86c27c7bdb6643cf53e97aa5adb33ada8e07a3931593a6',
    'TS01aa4f71': '0155147e19cabd3c2bf3a81a851df501639e2610bc9713cabedb320ce313b62639caadad73fa6ae289afc0fc00b2ff3ad5af9924a7269041e97a90ef19b8057869398e66da93bb6d83b29361289af8a745a9455b5e86c6ddc58885c5a6c23eafa5b64f94e5bfa6fdd8fcf5a937d73d57bb6705eb405b31b32cee11bd8525d1d09ffd7f231dd546747dc12ebfe72d66f227048c99f8306136dba5388ace7221acce860c1cde4552bbc0468684e1df656d44aa7cf995',
}

collection = ffch.Collection('BR_RJANRIO_CNV')
file_fetcher = ffch.FileFetcher(cookies, collection)
file_fetcher.get_download_links(page_init=110, page_end=118)
