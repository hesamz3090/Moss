from urllib.parse import urlparse
import argparse
import time
import csv
import os
import warnings
from bs4 import XMLParsedAsHTMLWarning
import json
from moss import Moss

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Metadata constants
NAME = 'Moss'
VERSION = '2.0.0'
AUTHOR = 'Hesam Aghajani'
CONTACT = 'hesamz3090@gmail.com'
URL = 'https://github.com/hesamz3090/moss'
DESCRIPTIONS = 'A simple web crawler that classifies URLs and performs'


def banner():
    # Prints a fancy banner with tool info
    print(rf"""
    __  __  ____   ____   _____ 
    |  \/  |/ __ \ / __ \ / ____|
    | \  / | |  | | |  | | (___  
    | |\/| | |  | | |  | |\___ \ 
    | |  | | |__| | |__| |____) |
    |_|  |_|\____/ \____/|_____/  v{VERSION}

    Author : {AUTHOR}
    Contact: {CONTACT}
    Description: {DESCRIPTIONS}
    """)


def main():
    """
        Entry point when running as CLI tool.
        """
    parser = argparse.ArgumentParser(description='Moss Web Crawler by Hesam Aghajani')
    parser.add_argument('url', help='The base URL to start crawling from')
    parser.add_argument('--timeout', type=int, default=5, help='Timeout for each request (default=5)')
    parser.add_argument('--live', action='store_true', default=True,
                        help='Show live crawling output (default: enabled)')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv',
                        help='Output format: csv or json (default: csv)')
    parser.add_argument('--output', type=str, help='Output directory path (default: current folder)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')

    args = parser.parse_args()

    banner()

    if not args.url.startswith(('http://', 'https://')):
        print("[!] Error: URL must start with http:// or https:// (we can't assume SSL).")
        exit()
    start_time = time.time()

    crawler = Moss(args.url, timeout=args.timeout, live=args.live)
    result = crawler.run()

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n[*] Crawl finished. Total URLs scanned: {len(result)}")
    print(f"Time taken: {duration:.2f} seconds\n")

    base_name = f'moss_result_{urlparse(args.url).hostname}'
    output_dir = args.output or os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    if args.format == 'csv':
        csv_path = os.path.join(output_dir, base_name + '.csv')
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['url', 'status_code', 'content_length', 'type'])
            writer.writeheader()
            for item in result:
                writer.writerow({
                    'url': item['url'],
                    'status_code': item['status_code'],
                    'content_length': item['content_length'],
                    'type': item['type']
                })
        print(f"[✓] CSV saved to: {csv_path}")

    elif args.format == 'json':
        json_path = os.path.join(output_dir, base_name + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[✓] JSON saved to: {json_path}")


if __name__ == '__main__':
    main()
