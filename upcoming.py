#!/usr/local/bin/python3 

import argparse
import os

# Command line arguments
def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(prog='tex2md.py',
                usage='%(prog)s [arguments]',
                description='Create upcoming.pdf file for website.')
    parser.add_argument('-f', '--file', metavar='file', type=str,
                        default=argparse.SUPPRESS,
                        help='Latex file to convert')
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()

    # Directory
    texDir = os.path.dirname(args.file)
    
    # Original pdf filename (derived from tex file, if passed)
    pdfFile = args.file.replace('tex', 'pdf')
    
    # New pdf filename: upcoming.pdf
    newPdfFile = os.path.join('pdfs', 'upcoming.pdf')
    
    # Copy new file into upcoming.pdf
    os.system(f'cp {pdfFile} {newPdfFile}')
    
    # Commit to GitHub main branch for website
    os.system(f'touch {newPdfFile}')
    os.system(f'git add {newPdfFile}')
    os.system('git commit -m "Update with latest list"')
    os.system('git push origin main gh-pages')

if __name__ == '__main__':
    main()