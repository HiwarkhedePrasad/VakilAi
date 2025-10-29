"""
modules/ingestion.py
Document extraction and clause parsing
"""

import re
from typing import List, Dict
import pdfplumber
from docx import Document
import os

class DocumentExtractor:
   
    
    def __init__(self):
        self.clause_patterns = [
            r'\d+\.\s+',  
            r'\d+\.\d+\s+', 
            r'[A-Z][a-z]+\s+\d+:',  
            r'CLAUSE\s+\d+', 
        ]
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF, DOCX, or TXT file"""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.pdf':
                return self._extract_pdf(file_path)
            elif ext == '.docx':
                return self._extract_docx(file_path)
            elif ext == '.txt':
                return self._extract_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            raise Exception(f"Text extraction failed: {str(e)}")
    
    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
        return text.strip()
    
    def _extract_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise Exception(f"DOCX extraction failed: {str(e)}")
        return text.strip()
    
    def _extract_txt(self, file_path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            raise Exception(f"TXT extraction failed: {str(e)}")
        return text.strip()
    
    def parse_clauses(self, text: str) -> List[Dict]:
        """
        Parse document into individual clauses
        Returns list of clause objects
        """
        # Split by common clause patterns
        clauses = []
        
        # First, try structured splitting by numbered clauses
        numbered_clauses = re.split(r'\n(?=\d+\.)', text)
        
        if len(numbered_clauses) > 1:
            # Document has numbered structure
            for i, clause_text in enumerate(numbered_clauses):
                clause_text = clause_text.strip()
                if clause_text and len(clause_text) > 20:  # Ignore very short segments
                    clauses.append({
                        "id": i + 1,
                        "text": clause_text
                    })
        else:
            # No clear structure, split by paragraphs
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs):
                para = para.strip()
                if para and len(para) > 50:  # Only substantial paragraphs
                    clauses.append({
                        "id": i + 1,
                        "text": para
                    })
        
        # If still no clauses found, treat whole text as one clause
        if not clauses:
            clauses.append({
                "id": 1,
                "text": text
            })
        
        return clauses
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,;:()"\'-]', '', text)
        return text.strip()