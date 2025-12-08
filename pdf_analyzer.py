#!/usr/bin/env python3
"""
PDF Analyzer - A tool to analyze PDF files in the repository
"""

import sys
import os
from pathlib import Path
import argparse

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)

# Constants
SUMMARY_PREVIEW_LENGTH = 500
FULL_PREVIEW_LENGTH = 1000


class PDFAnalyzer:
    """Analyze PDF files and extract information"""
    
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        if not self.pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
    
    def get_metadata(self):
        """Extract PDF metadata"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                info = {
                    'filename': self.pdf_path.name,
                    'size': f"{self.pdf_path.stat().st_size / 1024:.2f} KB",
                    'pages': len(pdf_reader.pages),
                }
                
                if metadata:
                    info['title'] = metadata.get('/Title', 'N/A')
                    info['author'] = metadata.get('/Author', 'N/A')
                    info['subject'] = metadata.get('/Subject', 'N/A')
                    info['creator'] = metadata.get('/Creator', 'N/A')
                    info['producer'] = metadata.get('/Producer', 'N/A')
                    info['creation_date'] = metadata.get('/CreationDate', 'N/A')
                
                return info
        except Exception as e:
            return {'error': str(e)}
    
    def extract_text(self, max_pages=None):
        """Extract text from PDF"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text_content = []
                pages_to_process = min(max_pages or len(pdf.pages), len(pdf.pages))
                
                for i, page in enumerate(pdf.pages[:pages_to_process]):
                    text = page.extract_text()
                    if text:
                        text_content.append(f"\n--- Page {i+1} ---\n{text}")
                
                return '\n'.join(text_content)
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def get_summary(self):
        """Get a summary of the PDF"""
        metadata = self.get_metadata()
        text = self.extract_text(max_pages=1)  # Just first page for summary
        
        summary = {
            'metadata': metadata,
            'first_page_preview': text[:SUMMARY_PREVIEW_LENGTH] + '...' if len(text) > SUMMARY_PREVIEW_LENGTH else text,
        }
        
        return summary
    
    def analyze(self, extract_full_text=False):
        """Perform full analysis of the PDF"""
        print(f"\n{'='*60}")
        print(f"Analyzing: {self.pdf_path.name}")
        print(f"{'='*60}\n")
        
        # Get metadata
        print("📄 Metadata:")
        print("-" * 60)
        metadata = self.get_metadata()
        for key, value in metadata.items():
            print(f"  {key.capitalize()}: {value}")
        
        # Extract text
        print(f"\n📝 Text Content:")
        print("-" * 60)
        if extract_full_text:
            text = self.extract_text()
            print(text)
        else:
            text = self.extract_text(max_pages=1)
            print("First page preview:")
            print(text[:FULL_PREVIEW_LENGTH] + '...' if len(text) > FULL_PREVIEW_LENGTH else text)
            print("\n(Use --full flag to extract all text)")


def analyze_all_pdfs_in_directory(directory='.', extract_full_text=False):
    """Analyze all PDF files in the given directory"""
    pdf_files = list(Path(directory).glob('*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s) in {directory}")
    
    for pdf_file in pdf_files:
        try:
            analyzer = PDFAnalyzer(pdf_file)
            analyzer.analyze(extract_full_text=extract_full_text)
            print()
        except Exception as e:
            print(f"Error analyzing {pdf_file.name}: {str(e)}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Analyze PDF files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a specific PDF file
  python pdf_analyzer.py "Advanced Financial Modeling Generative AI Investment Analysis Project.pdf"
  
  # Analyze a specific PDF with full text extraction
  python pdf_analyzer.py --full "Advanced Financial Modeling_Time Series Analysis Project.pdf"
  
  # Analyze all PDFs in the current directory
  python pdf_analyzer.py --all
  
  # Analyze all PDFs with full text extraction
  python pdf_analyzer.py --all --full
        """
    )
    
    parser.add_argument(
        'pdf_file',
        nargs='?',
        help='Path to the PDF file to analyze'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Analyze all PDF files in the current directory'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Extract full text from all pages (default: first page only)'
    )
    
    args = parser.parse_args()
    
    if args.all:
        analyze_all_pdfs_in_directory('.', extract_full_text=args.full)
    elif args.pdf_file:
        try:
            analyzer = PDFAnalyzer(args.pdf_file)
            analyzer.analyze(extract_full_text=args.full)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    else:
        # If no arguments provided, show help and analyze all PDFs
        parser.print_help()
        print("\n" + "="*60)
        print("No specific file provided. Analyzing all PDFs in current directory:")
        print("="*60)
        analyze_all_pdfs_in_directory('.', extract_full_text=False)


if __name__ == '__main__':
    main()
