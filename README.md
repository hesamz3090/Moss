```
     __  __  ____   ____   _____ 
    |  \/  |/ __ \ / __ \ / ____|
    | \  / | |  | | |  | | (___  
    | |\/| | |  | | |  | |\___ \ 
    | |  | | |__| | |__| |____) |
    |_|  |_|\____/ \____/|_____/  v2.0.0
  
    Author : Hesam Aghajani
    Contact: hesamz3090@gmail.com
    Description: A simple web crawler that classifies URLs and performs
```

# 🕷️ Moss Crawler
**Moss**  is a simple web crawler built with Python that fetches a webpage, recursively follows links up to a specified depth, and classifies URLs into different categories (e.g., files, images, social links, etc.). It uses the `requests` and `BeautifulSoup` libraries for web scraping and multi-threading to speed up the crawling process.

## 📦 Features
- #### 📌 There is no max depht
- 📄 File Links (PDF, ZIP, etc.)
- 🖼️ Image Links (PNG, JPG, SVG, etc.)
- 📨 Email Links
- 🔗 API Endpoints
- 🌐 Social Media Links
- 📦 Downloadable Files
- ❓ Unknown/Other Links
---

## 📌 Requirements

- Python 3.6+
- See `requirements.txt` for dependencies

---
## ⚙️ Installation

### Clone the repository:
```bash
git clone https://github.com/hesamz3090/moss.git
cd moss
pip install -r requirements.txt
```
Or install directly using pip (after packaging):

### Installation on Linux:
```bash
pip install .
```

## 🚀 Usage

| Argument        | Type      | Default     | Description                                                                      |
|-----------------|-----------|-------------|----------------------------------------------------------------------------------|
| url             | str       | Required    | The base URL to start crawling from. Must start with http:// or https://.        |
| --timeout       | int       | 5           | Timeout in seconds for each HTTP request.                                        |
| --max_depth     | int       | None        | limit crawling depth for a fast scan.                                            |
|
| --live          | flag      | True        | If enabled, prints real-time logs during crawling.                               |
|
| --format        | str       | csv         | Output format: either 'csv' or 'json'.                                           |
|
| --output        | str       | current dir | Directory path to save the output. If not provided, saves in the current folder. |
|
| -v              | flag      | —           | Displays the current version of the tool.                                        |
|

### Examples

```bash
moss "http://example.com"
moss python moss.py https://example.com --format json --output ./results
```
**Or**

```python
from moss import Moss
obj = Moss("http://example.com")
response_list = obj.run()
```

## 📁 Example Output

```json
[
  {
    "type": "Image",
    "url": "https://example.com/assets/logo.png",
    "status_code": 200,
    "content_length": 5432,
    "html": false
  },
  {
    "type": "File",
    "url": "https://example.com/files/report.pdf",
    "status_code": 200,
    "content_length": 1048576,
    "html": false
  },
  {
    "type": "Social",
    "url": "https://twitter.com/example",
    "status_code": 301,
    "content_length": 0,
    "html": false
  },
  "..."
]
```
Or
```csv
Type,URL,Status Code,Content Length,HTML
Image,https://example.com/assets/logo.png,200,5432,false
File,https://example.com/files/report.pdf,200,1048576,false
Social,https://twitter.com/example,301,0,<html><head>.... 
"..."
```

---
## 📝 License

Moss is licensed under the MIT License. See the [LICENSE](https://github.com/hesamz3090/moss/blob/main/LICENSE) for more information.
