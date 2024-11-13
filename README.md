# Web Scraper Pro 🕸️

A professional web scraping application built with Streamlit, powered by Firecrawl and OpenAI GPT-4.

⚠️ **Disclaimer**: This project is created for educational purposes only. Web scraping should only be performed with explicit permission from website owners. Always review and comply with the website's terms of service and robots.txt file before scraping.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Keys](#api-keys)
- [Suggested Project Structure](#suggested project-structure)
- [Technologies Used](#technologies-used)
- [Limitations & Legal Considerations](#limitations--legal-considerations)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Overview

Web Scraper Pro is a sophisticated web scraping application that combines the power of Firecrawl for data extraction and OpenAI's GPT-4 for intelligent data processing. The application features a user-friendly interface built with Streamlit, making it accessible for users of all technical levels.

## Features

- 🌐 User-friendly web interface
- 🔑 Secure API key management
- 🤖 AI-powered data extraction
- 📊 Data preview functionality
- 📥 Multiple export formats (CSV, Excel)
- ⚙️ Customizable extraction fields
- 🛡️ Comprehensive error handling
- 📱 Responsive design

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Required API keys:
  - Firecrawl API key
  - OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arad1367/Scraper_Pro_AI.git
cd web-scraper-pro
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install streamlit pandas openai firecrawl-py requests openpyxl xlsxwriter
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Enter your API keys in the sidebar

4. Input the target URL and configure scraping settings

5. Click "Start Scraping" to begin the extraction process

## API Keys

The application requires two API keys to function:

1. **Firecrawl API Key**: Used for web scraping functionality
2. **OpenAI API Key**: Required for intelligent data processing

Store your API keys securely and never commit them to version control.

## Suggested Project Structure (I did not use asstes folder, but you can!🍁)

```
web-scraper-pro/
├── app.py               # Main application file
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── assets/            # Project assets
│   └── logo.png       # Company logo
└── .gitignore         # Git ignore file
```

## Technologies Used

- **Streamlit**: Frontend framework
- **Firecrawl**: Web scraping engine
- **OpenAI GPT-4o mini**: Data processing
- **Pandas**: Data manipulation
- **Python**: Programming language

## Limitations & Legal Considerations

- This tool is for educational purposes only
- Always obtain permission before scraping any website
- Respect robots.txt files
- Follow rate limiting best practices
- Comply with websites' terms of service
- Do not scrape personal or sensitive information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**Dr. Pejman Ebrahimi**  
Research Assistant at University of Liechtenstein

📧 Contact:
- Academic: pejman.ebrahimi@uni.li
- Personal: pejman.ebrahimi77@gmail.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

⚠️ **Important Notice**: This project is created for educational and research purposes. The author and contributors are not responsible for any misuse of this tool. Always ensure you have permission before scraping any website.