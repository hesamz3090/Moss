import sys
import threading
import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

# Author information
AUTHOR_NAME = "Hesam Aghjani"
AUTHOR_CONTACT = "hesamz3090@gmail.com"

# Version Information
VERSION = "1.0.0"


class Moss:
    """
    A simple web crawler to fetch and classify URLs based on various patterns.
    It checks the type of the URL (e.g., image, file, social media) and performs multi-threaded requests to gather data.
    """

    def check_type(self, url_list: list, hostname: str):
        """
        Classifies URLs based on predefined patterns.
        :param hostname: The hostname of the base URL.
        :param url_list: List of URLs to classify.
        :return: A list of URLs with their associated type.
        """
        # Define patterns for different URL types
        image_pattern = r'\.(jpg|jpeg|png|gif)$'
        file_pattern = r'\.(pdf|docx|pptx|zip|rar|csv|xls|xlsx|txt|exe)$'
        social_pattern = r'(t\.me|facebook\.com|twitter\.com|instagram\.com|x\.com|linkedin\.com|youtube\.com|telegram\.me|whatsapp\.com)'
        content_pattern = r'(%)'
        subdomain_pattern = rf'://((?!www\.).*?)\.{re.escape(hostname)}'

        patterns = [
            (file_pattern, 'FILE'),
            (image_pattern, 'IMAGE'),
            (content_pattern, 'CONTENT'),
            (social_pattern, 'SOCIAL'),
            (subdomain_pattern, 'SUBDOMAIN'),
        ]

        # Iterate over the URL list and classify
        for data in url_list:
            url = data['url']
            for pattern, data_type in patterns:
                if re.search(pattern, url):
                    data['type'] = data_type
                    break
            else:
                if hostname in url:
                    data['type'] = 'DIRECTORY'
                else:
                    data['type'] = 'EXTRA'

        return url_list

    def check_url(self, url_list: list):
        """
        Perform multi-threaded requests to check URLs and gather information.
        :param url_list: List of URLs to check.
        :return: A list of dictionaries containing information about each URL.
        """
        thread_list = []
        result_list = []
        result_lock = threading.Lock()

        def get_request(url, result):
            try:
                # Send GET request to the URL
                response = requests.get(url)
                with result_lock:
                    url_data = {
                        'hostname': response.url.split('/')[2],
                        'url': response.url,
                        'content_length': len(response.text),
                        'status_code': response.status_code,
                    }
                    result.append(url_data)
            except requests.RequestException:
                pass

        # Create and start threads for each URL
        for item in url_list:
            thread = threading.Thread(target=get_request, args=(item, result_list))
            thread_list.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()

        return result_list

    def clean_dict_list(self, unclean_dict: list):
        """
        Cleans the URL list by removing duplicates based on the URL.
        :param unclean_dict: List of dictionaries containing URL data.
        :return: A list of unique URLs.
        """
        unique_hostnames = set()
        result = []

        # Remove duplicates
        for item in unclean_dict:
            url = item.get('url')
            if url not in unique_hostnames:
                unique_hostnames.add(url)
                result.append(item)

        return result

    def __init__(self, url: str, depth: int = 1):
        """
        Initializes the Moss crawler with the given URL and depth.
        :param url: The base URL to start crawling from.
        :param depth: The maximum depth to crawl (default is 1).
        """
        self.url = url
        self.hostname = urlparse(url).hostname
        self.depth = depth

        self.result = {
            "result": [],
            'status': 'WORKING',
            'spend_time': 0,
        }

    def crawl(self):
        """
        Crawls the web starting from the base URL, following links up to the specified depth.
        :return: A list of visited URLs.
        """
        visited = set()
        not_visited = set()
        not_visited.add((self.url, 0))

        # Perform the crawl by visiting URLs and following links
        while not_visited:
            current_url, current_depth = not_visited.pop()
            visited.add(current_url)

            if self.depth == 0 or current_depth < self.depth:
                links = self.get_links(current_url)
                new_links = links - visited - {url for url, _ in not_visited}

                for link in new_links:
                    if self.hostname in link:
                        not_visited.add((link, current_depth + 1))
                    else:
                        visited.add(link)
        return list(set(visited))

    def get_links(self, url):
        """
        Fetches all the links from the given URL.
        :param url: The URL to fetch links from.
        :return: A set of unique links found on the page.
        """
        links = set()
        try:
            response = requests.get(url, timeout=2)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            for anchor in soup.find_all('a', href=True):
                link = anchor['href']
                if len(link) > 1:
                    link = urljoin(self.url, link)
                    if '#' not in link:
                        links.add(link)
            return links
        except requests.RequestException:
            return set()

    def run(self):
        """
        Runs the crawler and processes the URLs.
        :return: A dictionary containing the results of the crawl.
        """
        try:
            start_time = time.time()
            link_list = self.crawl()
            checked_link = self.check_url(link_list)
            unclean_list = self.check_type(checked_link, self.hostname)
            result = self.clean_dict_list(unclean_list)

            self.result['result'] = result
            self.result['spend_time'] = int(time.time() - start_time)
            self.result['status'] = 'COMPLETED'
            return self.result

        except Exception as error:
            error_type, error_name, error_traceback = sys.exc_info()
            error_file = error_traceback.tb_frame.f_code.co_filename
            error_line = error_traceback.tb_lineno
            self.result = {
                'status': 'ERROR',
                'error': {
                    'file': str(error_file),
                    'line': str(error_line),
                    'error': str(error),
                }
            }
            return self.result


def main():
    """
    Main function to parse arguments and run the crawler.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Moss Web Crawler')
    parser.add_argument('url', help='The base URL to start crawling from')
    parser.add_argument('--depth', type=int, default=1, help='The depth of the crawl (default is 1)')
    parser.add_argument('-v', '--version', action='version', version=VERSION, help="Show the version of the crawler")
    args = parser.parse_args()

    # Initialize the crawler and run it
    crawler = Moss(args.url, depth=args.depth)
    result = crawler.run()

    # Print the results
    if result['status'] == 'COMPLETED':
        print(f"\nCrawl completed in {result['spend_time']} seconds.")
        print(f"Found {len(result['result'])} unique URLs :")
        for url in result['result']:
            print(url['url'])
    else:
        print(f"\nAn error occurred: {result['error']}")


if __name__ == '__main__':
    main()
