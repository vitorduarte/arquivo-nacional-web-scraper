#!/usr/bin/env python3

from file_treatment import File
import sys

def main():
    if len(sys.argv) < 2:
        print('Invalid usage')
        exit(1)

    name = sys.argv[1]


    file = File()
    file.fetch_from_name(name)
    print(file.generate_alternative_url())


if __name__ == "__main__":
    main()
