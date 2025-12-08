# RSB

Repository for Sustainable Business - Advanced Financial Modeling Projects

## PDF Analysis Tool

This repository includes a Python-based PDF analyzer tool that can extract and analyze information from PDF files.

### Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

#### Analyze a specific PDF file

```bash
python pdf_analyzer.py "Advanced Financial Modeling Generative AI Investment Analysis Project.pdf"
```

#### Analyze with full text extraction

```bash
python pdf_analyzer.py --full "Advanced Financial Modeling_Time Series Analysis Project.pdf"
```

#### Analyze all PDFs in the current directory

```bash
python pdf_analyzer.py --all
```

#### Analyze all PDFs with full text extraction

```bash
python pdf_analyzer.py --all --full
```

### Features

- Extract PDF metadata (title, author, pages, size, etc.)
- Extract text content from PDF files
- Analyze all PDF files in a directory
- Preview first page or extract full text
- Command-line interface for easy usage

## Repository Contents

### PDF Documents
- Advanced Financial Modeling Generative AI Investment Analysis Project.pdf
- Advanced Financial Modeling_Time Series Analysis Project.pdf
- Advanced Financial Modeling_Time Value of Money Analysis Project.pdf

### Data Files
- co2-emissions-and-gdp.csv
- global-data-on-sustainable-energy (1).csv
- owid-energy-data.csv