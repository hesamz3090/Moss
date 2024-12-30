
# Moss Crawler

A Python web crawler that follows links up to a specified depth, classifies URLs based on patterns, and performs multi-threaded requests.

## About Moss Crawler

Moss is a simple web crawler built with Python that fetches a webpage, recursively follows links up to a specified depth, and classifies URLs into different categories (e.g., files, images, social links, etc.). It uses the `requests` and `BeautifulSoup` libraries for web scraping and multi-threading to speed up the crawling process.

## Dependencies:
Crawler depends on the `requests`, `beautifulsoup4` Python modules.
These dependencies can be installed using the requirements file:

## Installation

To install Moss Crawler, clone the repository and install the dependencies:

### Clone the repository:
```bash
git clone https://github.com/hesamz3090/moss.git
cd moss
```

### Installation on Windows:
```bash
c:\python3\python.exe -m pip install .
```

### Installation on Linux:
```bash
sudo pip install .
```

## Usage

| Short Form | Long Form   | Description                                      |
|------------|-------------|--------------------------------------------------|
| -u         | --url       | The base URL to start crawling from              |
| -d         | --depth     | The depth to which the crawler should follow links |
| -v         | --version   | Show program's version number and exit           |
| -h         | --help      | Show this help message and exit                  |

### Examples

* To crawl a single URL up to a specified depth:
```bash
moss --url "http://example.com" --depth 3
```

## Using Moss Crawler as a Module in Your Python Scripts

You can also use the Moss Crawler functionality directly in your Python scripts.

### Example:
```python
import moss
response_list = moss.main("http://example.com", 2)
```

The `main` function will return a list of unique responses, classified by URL type.

### Function Usage:
* **urls**: List of URLs to start crawling from (can be a file or a list of URLs).
* **depth**: The depth to which the crawler should follow links.

## License

Moss Moss is licensed under the MIT License. See the [LICENSE](https://github.com/hesamz3090/moss/blob/main/LICENSE) for more information.

## Version

**Current version is 1.0**
