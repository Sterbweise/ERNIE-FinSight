import PyPDF2
import pdfplumber
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Service for extracting text and metadata from PDF files"""
    
    @staticmethod
    def extract_text_pypdf2(pdf_path: str) -> str:
        """Extract text using PyPDF2 (fallback method)"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_pdfplumber(pdf_path: str) -> str:
        """Extract text using pdfplumber (primary method, better quality)"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {str(e)}")
            return ""
    
    @classmethod
    def extract_text(cls, pdf_path: str) -> str:
        """
        Extract text from PDF using multiple methods for best results
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If text extraction fails with all methods
        """
        # Try pdfplumber first (better quality)
        text = cls.extract_text_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text or len(text) < 100:
            logger.warning("pdfplumber extraction insufficient, trying PyPDF2")
            text = cls.extract_text_pypdf2(pdf_path)
        
        if not text or len(text) < 50:
            raise ValueError("Failed to extract meaningful text from PDF")
        
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        return text
    
    @staticmethod
    def get_pdf_metadata(pdf_path: str) -> dict:
        """
        Extract metadata from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    "title": metadata.get("/Title", "Unknown"),
                    "author": metadata.get("/Author", "Unknown"),
                    "pages": len(pdf_reader.pages),
                    "creator": metadata.get("/Creator", "Unknown"),
                }
        except Exception as e:
            logger.error(f"Metadata extraction failed: {str(e)}")
            return {
                "title": "Unknown",
                "author": "Unknown",
                "pages": 0,
                "creator": "Unknown"
            }
    
    @staticmethod
    def validate_pdf(pdf_path: str, max_size_mb: int = 10) -> tuple[bool, Optional[str]]:
        """
        Validate PDF file
        
        Args:
            pdf_path: Path to the PDF file
            max_size_mb: Maximum allowed file size in MB
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(pdf_path)
        
        # Check if file exists
        if not path.exists():
            return False, "File does not exist"
        
        # Check file extension
        if path.suffix.lower() != '.pdf':
            return False, "File must be a PDF"
        
        # Check file size
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
        
        # Try to open the PDF
        try:
            with open(pdf_path, 'rb') as file:
                PyPDF2.PdfReader(file)
        except Exception as e:
            return False, f"Invalid or corrupted PDF file: {str(e)}"
        
        return True, None

