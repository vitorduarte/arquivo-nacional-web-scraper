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
    file_list = dc.generate_file_list()
    with open(link_file, 'w') as outfile:
        outfile.write('\n'.join(file_list))


if __name__ == "__main__":
    main()
