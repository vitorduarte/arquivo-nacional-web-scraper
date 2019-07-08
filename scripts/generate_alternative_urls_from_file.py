#!/usr/bin/env python3

from file_treatment import File
import sys

def main():
    if len(sys.argv) < 2:
        print('Invalid usage')
        exit(1)

    file_names = sys.argv[1]
    link_file = sys.argv[2]
    new_urls = []

    with open(file_names, 'r') as f:
        names = f.read().split('\n')

    for filename in names:
        file = File()
        file.fetch_from_name(filename)
        new_urls.append(file.generate_alternative_url())

    with open(link_file, 'w') as outfile:
        outfile.write('\n'.join(new_urls))
if __name__ == "__main__":
    main()
