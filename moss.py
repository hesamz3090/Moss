import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class Moss:
    """
    Web Crawler and Link Type Analyzer.
    Designed for passive link mapping and basic categorization of site resources.
    """

    def __init__(self, url, timeout=5, live=True):
        self.url = url
        self.hostname = urlparse(self.url).hostname
        self.timeout = timeout
        self.live = live
        self.level = 1

    def get_data(self, url_list):
        """
        Fetch content from a list of URLs with timeout.
        """
        request_list = []
        for idx, url in enumerate(url_list, start=1):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.encoding = response.apparent_encoding
                url_type = self.get_type(url)
                if self.live:
                    print(
                        f"[Level {self.level}] [{idx}/{len(url_list)}] Crawling: {response.url} [{response.status_code}] [{url_type}]")
                request_list.append({
                    'url': response.url,
                    'content_length': len(response.content),
                    'status_code': response.status_code,
                    'type': url_type,
                    'html': response.text,
                })
            except requests.RequestException:
                pass
        return request_list

    def extract_links(self, page_list):
        """
        Extract all valid anchor href links from the HTML pages.
        """
        link_list = set()
        for page in page_list:
            html = page['html']
            soup = BeautifulSoup(html, 'html.parser')
            for anchor in soup.find_all('a', href=True):
                link = anchor['href']
                if not link or link.startswith('#') or link == '/' or link == 'javascript:void(0)':
                    continue
                if 'http' not in link:
                    link = urljoin(self.url, link)
                parsed = urlparse(link)
                normalized = urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip('/'), '', '', ''))
                link_list.add(normalized)
        return link_list

    def get_type(self, url):
        """
        Categorize the URL based on patterns (email, image, social media, etc.).
        """
        internal_pattern = rf'://(www\.)?{re.escape(self.hostname)}'
        external_pattern = r'^(http|https)://'
        email_pattern = r'^mailto:'
        telephone_pattern = r'^tel:'
        social_pattern = r'(facebook\.com|twitter\.com|instagram\.com|x\.com|linkedin\.com|youtube\.com|telegram\.me|whatsapp\.com)'
        image_pattern = r'\.(jpg|jpeg|png|gif|bmp|webp)$'
        video_pattern = r'\.(mp4|avi|mov|mkv)$'
        audio_pattern = r'\.(mp3|wav|flac)$'
        download_pattern = r'\.(pdf|docx|pptx|xls|xlsx|txt|exe|doc)$'
        archive_pattern = r'\.(zip|tar|rar|gz|7z)$'
        font_pattern = r'\.(woff|woff2|ttf|otf)$'
        config_pattern = r'\.(json|xml|yaml|ini|conf)$'
        data_pattern = r'\.(csv|json)$'
        database_pattern = r'\.(db|sqlite|sql)$'
        frontend_pattern = r'\.(html|css|js)$'
        api_pattern = r'/api/'

        patterns = [
            (download_pattern, 'DOWNLOAD'),
            (email_pattern, 'EMAIL'),
            (telephone_pattern, 'TELEPHONE'),
            (social_pattern, 'SOCIAL'),
            (api_pattern, 'API'),
            (frontend_pattern, 'FRONTEND'),
            (image_pattern, 'IMAGE'),
            (video_pattern, 'VIDEO'),
            (audio_pattern, 'AUDIO'),
            (font_pattern, 'FONT'),
            (config_pattern, 'CONFIG'),
            (data_pattern, 'DATA'),
            (archive_pattern, 'ARCHIVE'),
            (database_pattern, 'DATABASE'),
            (internal_pattern, 'INTERNAL'),
            (external_pattern, 'EXTERNAL'),
        ]

        for pattern, data_type in patterns:
            if re.search(pattern, url):
                return data_type
        return 'EXTERNAL'

    def run(self):
        """
        Run the crawling and return collected page info.
        """
        result_list = []
        crawl_list = [self.url]
        visited_set = set()

        while crawl_list:
            data_list = self.get_data(crawl_list)

            result_list.extend(data_list)
            visited_set.update(crawl_list)
            crawl_list.clear()

            link_list = self.extract_links(data_list)

            external_list = []
            new_link = 0
            for link in link_list:
                url_type = self.get_type(link)
                if url_type == 'INTERNAL':
                    if link not in crawl_list and link not in visited_set:
                        crawl_list.append(link)
                        new_link += 1
                else:
                    if link not in visited_set and link not in external_list:
                        external_list.append(link)
                        visited_set.add(link)
                        new_link += 1

            result_list.extend(self.get_data(external_list))

            print(
                f'[+] Level {self.level} | Scanned: {len(result_list)} URLs | New Links: {new_link} | Queue: {len(crawl_list)}')
            self.level += 1
        return result_list
