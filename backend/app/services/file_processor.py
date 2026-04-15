"""
File processing service for handling uploaded files
"""
import os
import tempfile
import magic
import logging
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from app.core.config import settings

logger = logging.getLogger(__name__)

class FileProcessor:
    """Service for processing uploaded files"""
    
    def __init__(self):
        self.allowed_types = settings.ALLOWED_FILE_TYPES
        self.max_size = settings.MAX_FILE_SIZE
        self.upload_dir = settings.UPLOAD_DIR
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def validate_file(self, file: UploadFile) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file
        
        Args:
            file: UploadFile object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check file size
            file_size = 0
            content = await file.read(settings.MAX_FILE_SIZE + 1)
            file_size = len(content)
            
            if file_size > settings.MAX_FILE_SIZE:
                return False, f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
            
            # Reset file pointer
            await file.seek(0)
            
            # Check file type using magic
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(content[:1024])  # Read first 1KB for type detection
            
            if file_type not in self.allowed_types:
                return False, f"File type {file_type} not allowed. Allowed types: {', '.join(self.allowed_types)}"
            
            # Check file extension
            filename = file.filename.lower()
            if file_type == "text/plain" and not filename.endswith(".txt"):
                logger.warning(f"Text file with non-.txt extension: {filename}")
            
            if file_type == "text/csv" and not filename.endswith(".csv"):
                logger.warning(f"CSV file with non-.csv extension: {filename}")
            
            return True, None
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False, f"Error validating file: {str(e)}"
    
    async def save_file(self, file: UploadFile) -> Tuple[Optional[str], Optional[str]]:
        """
        Save uploaded file to temporary location
        
        Args:
            file: UploadFile object
            
        Returns:
            Tuple of (file_path, error_message)
        """
        try:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                dir=self.upload_dir,
                suffix=os.path.splitext(file.filename)[1] if file.filename else ".tmp"
            )
            
            # Write file content
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            
            logger.info(f"File saved to: {temp_file.name}")
            return temp_file.name, None
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return None, f"Error saving file: {str(e)}"
    
    async def extract_text(self, file_path: str, file_type: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract text from file based on file type
        
        Args:
            file_path: Path to the file
            file_type: MIME type of the file
            
        Returns:
            Tuple of (extracted_text, error_message)
        """
        try:
            if file_type == "text/plain":
                return await self._extract_text_from_txt(file_path)
            elif file_type == "text/csv":
                return await self._extract_text_from_csv(file_path)
            elif file_type == "application/pdf":
                return await self._extract_text_from_pdf(file_path)
            else:
                return None, f"Unsupported file type: {file_type}"
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return None, f"Error extracting text: {str(e)}"
    
    async def _extract_text_from_txt(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, None
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    text = f.read()
                return text, None
            except Exception as e:
                return None, f"Failed to read text file: {str(e)}"
    
    async def _extract_text_from_csv(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract text from CSV file"""
        try:
            import csv
            text_parts = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    text_parts.append(", ".join(row))
            
            return "\n".join(text_parts), None
        except Exception as e:
            return None, f"Failed to read CSV file: {str(e)}"
    
    async def _extract_text_from_pdf(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract text from PDF file"""
        try:
            import pdfplumber
            
            text_parts = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            
            if not text_parts:
                return None, "No text could be extracted from PDF"
            
            return "\n\n".join(text_parts), None
        except ImportError:
            return None, "PDF processing requires pdfplumber library"
        except Exception as e:
            return None, f"Failed to read PDF file: {str(e)}"
    
    def cleanup_file(self, file_path: str) -> bool:
        """
        Clean up temporary file
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {str(e)}")
            return False
    
    def get_file_info(self, file: UploadFile) -> dict:
        """
        Get file information
        
        Args:
            file: UploadFile object
            
        Returns:
            Dictionary with file information
        """
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": getattr(file, "size", None),
        }