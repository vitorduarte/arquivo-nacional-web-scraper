#!/usr/bin/env python3

from file_treatment import DownloadCategory
import sys

def main():
    if len(sys.argv) < 2:
        print('Invalid usage')
        exit(1)

    file = sys.argv[1]

    dc = DownloadCategory(file)
    dc.fix_name_in_category_file()


if __name__ == "__main__":
    main()
