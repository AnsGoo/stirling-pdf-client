# Stirling PDF Client

A Python client for the Stirling PDF API, providing a simple way to interact with Stirling PDF services.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Requirements](#requirements)
- [License](#license)

## Installation

You can install the package using pip:

```bash
pip install stirling_pdf_client
```

Or directly from the source:

```bash
pip install .
```

## Usage

Here's a basic example of how to use the Stirling PDF Client:

```python
from stirling_pdf_client import StirlingPDFClient

# Initialize the client with your Stirling PDF server URL
client = StirlingPDFClient(base_url='http://localhost:8080')

# Get the server uptime
uptime_info = client.get_uptime()
print(f"Server uptime: {uptime_info}")
```

## Features

- Simple and intuitive API
- Built on top of httpx for efficient HTTP requests
- Type hints for better IDE support

## Requirements

- Python 3.12 or higher
- httpx 0.28.1 or higher

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.