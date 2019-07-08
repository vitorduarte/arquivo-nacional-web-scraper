#!/usr/bin/env python3

from file_treatment import DownloadCategory
import sys

def main():
    if len(sys.argv) < 3:
        print('Invalid usage')
        exit(1)

    file = sys.argv[1]
    folder = sys.argv[2]

    dc = DownloadCategory(file)
    dc.fix_name_in_folder(folder)


if __name__ == "__main__":
    main()
