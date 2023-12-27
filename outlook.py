#!/usr/local/bin/python3 

import argparse
import os

# Command line arguments
def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(prog='tex2md.py',
                usage='%(prog)s [arguments]',
                description='Creates an outlook.pdf file for website.')
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

    # New pdf filename: outlook.pdf
    newPdfFile = os.path.join('pdfs', 'outlook.pdf')

    # Copy new file into outlook.pdf
    os.system(f'cp {pdfFile} {newPdfFile}')
    
    # Commit to GitHub main branch for website
    os.system(f'git add -f {newPdfFile}')
    os.system('git commit -m "Update with latest schedule"')
    os.system('git push origin main')
    os.system('git checkout gh-pages')
    os.system(f'git checkout main -- {newPdfFile}')
    os.system('git commit -m "Update with latest schedule"')
    os.system('git push origin gh-pages')
    os.system('git checkout main')

if __name__ == '__main__':
    main()