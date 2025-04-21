
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

| Argument  | Type | Default     | Description                                                                      |
|-----------|------|-------------|----------------------------------------------------------------------------------|
| url       | str  | Required    | The base URL to start crawling from. Must start with http:// or https://.        |
| --timeout | int  | 5           | Timeout in seconds for each HTTP request.                                        |
|
| --live    | flag | True        | If enabled, prints real-time logs during crawling.                               |
|
| --format  | str  | csv         | Output format: either 'csv' or 'json'.                                           |
|
| --output  | str  | current dir | Directory path to save the output. If not provided, saves in the current folder. |
|
| -v        | flag | —           | Displays the current version of the tool.                                        |
|

### Examples

* To crawl a single URL up to a specified depth:
```bash
moss "http://example.com"
moss python moss.py https://example.com --format json --output ./results
```

## Using Moss Crawler as a Module in Your Python Scripts

You can also use the Moss Crawler functionality directly in your Python scripts.

### Example:
```python
from moss import Moss
obg = Moss("http://example.com")
response_list = obg.run()
```

The `main` function will return a list of unique responses, classified by URL type.

### Function Arguments:
* **urls**: str
* **timeout**: int
* **live**: bool

## License

Moss is licensed under the MIT License. See the [LICENSE](https://github.com/hesamz3090/moss/blob/main/LICENSE) for more information.

## Version

**Current version is 2.0**
