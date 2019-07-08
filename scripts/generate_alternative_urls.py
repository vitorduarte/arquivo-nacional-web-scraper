#!/usr/bin/env python3

from file_treatment import DownloadCategory
import sys

def main():
    if len(sys.argv) < 3:
        print('Invalid usage')
        exit(1)

    file = sys.argv[1]
    link_file = sys.argv[2]

    dc = DownloadCategory(file)
    new_urls = dc.generate_alternative_links()
    with open(link_file, 'w') as outfile:
        outfile.write('\n'.join(new_urls))


if __name__ == "__main__":
    main()
