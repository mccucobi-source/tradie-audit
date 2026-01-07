"""
Data Extraction Agent - Extracts structured data from invoices, statements, and quotes.
Uses Claude to intelligently parse financial documents.
"""

import os
import json
from pathlib import Path
from typing import Optional
import anthropic
from pydantic import BaseModel

# PDF processing
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

import pandas as pd

from src.templates.prompts import DATA_EXTRACTION_PROMPT


class Transaction(BaseModel):
    """A single financial transaction extracted from documents."""
    date: str
    customer_or_vendor: str
    description: str
    amount: float
    type: str  # "revenue" or "expense"
    category: str
    status: str
    line_items: list = []
    confidence: str = "medium"


class ExtractionResult(BaseModel):
    """Result from extracting a single document."""
    document_type: str
    file_path: str
    transactions: list[Transaction]
    extraction_notes: str = ""
    needs_review: bool = False
    api_cost: float = 0.0


class DataExtractor:
    """
    Extracts financial data from various document formats using Claude.
    
    Supports:
    - PDF invoices and statements
    - Excel/CSV exports from accounting software
    - Bank statement PDFs
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required. Set in environment or pass to constructor.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        self.total_cost = 0.0
        
        # Cost tracking (approximate, per 1M tokens)
        self.input_cost_per_1m = 3.00  # Claude Sonnet
        self.output_cost_per_1m = 15.00
    
    def extract_from_folder(self, folder_path: str) -> list[ExtractionResult]:
        """
        Extract data from all supported files in a folder.
        
        Args:
            folder_path: Path to folder containing customer documents
            
        Returns:
            List of ExtractionResult objects
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        results = []
        
        # Find all supported files
        supported_extensions = {'.pdf', '.xlsx', '.xls', '.csv'}
        files = [f for f in folder.iterdir() 
                 if f.is_file() and f.suffix.lower() in supported_extensions]
        
        print(f"Found {len(files)} files to process in {folder_path}")
        
        for file_path in files:
            print(f"  Processing: {file_path.name}")
            try:
                result = self.extract_from_file(str(file_path))
                results.append(result)
                print(f"    ✓ Extracted {len(result.transactions)} transactions")
            except Exception as e:
                print(f"    ✗ Error: {e}")
                # Create error result
                results.append(ExtractionResult(
                    document_type="error",
                    file_path=str(file_path),
                    transactions=[],
                    extraction_notes=f"Error processing file: {str(e)}",
                    needs_review=True
                ))
        
        print(f"\nTotal API cost: ${self.total_cost:.2f}")
        return results
    
    def extract_from_file(self, file_path: str) -> ExtractionResult:
        """
        Extract data from a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ExtractionResult with extracted transactions
        """
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        # Read file content based on type
        if suffix == '.pdf':
            content = self._read_pdf(path)
        elif suffix in {'.xlsx', '.xls'}:
            content = self._read_excel(path)
        elif suffix == '.csv':
            content = self._read_csv(path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        # Use Claude to extract structured data
        return self._extract_with_claude(content, str(path))
    
    def _read_pdf(self, path: Path) -> str:
        """Extract text content from PDF."""
        if pdfplumber is None:
            raise ImportError("pdfplumber required for PDF processing. Run: pip install pdfplumber")
        
        text_content = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
                
                # Also try to extract tables
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        table_text = "\n".join(["\t".join([str(cell) if cell else "" for cell in row]) for row in table])
                        text_content.append(f"\n[TABLE]\n{table_text}\n[/TABLE]")
        
        return "\n\n".join(text_content)
    
    def _read_excel(self, path: Path) -> str:
        """Read Excel file and convert to text representation."""
        df = pd.read_excel(path, sheet_name=None)  # Read all sheets
        
        content = []
        for sheet_name, sheet_df in df.items():
            content.append(f"[SHEET: {sheet_name}]")
            content.append(sheet_df.to_string())
        
        return "\n\n".join(content)
    
    def _read_csv(self, path: Path) -> str:
        """Read CSV file and convert to text representation."""
        df = pd.read_csv(path)
        return df.to_string()
    
    def _extract_with_claude(self, content: str, file_path: str) -> ExtractionResult:
        """
        Use Claude to extract structured data from document content.
        """
        # Truncate very long content to avoid excessive API costs
        max_content_chars = 50000
        if len(content) > max_content_chars:
            content = content[:max_content_chars] + "\n\n[CONTENT TRUNCATED - Document too long]"
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"{DATA_EXTRACTION_PROMPT}\n\n---\n\nDOCUMENT CONTENT:\n\n{content}"
                }
            ]
        )
        
        # Track costs
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        cost = (input_tokens / 1_000_000 * self.input_cost_per_1m + 
                output_tokens / 1_000_000 * self.output_cost_per_1m)
        self.total_cost += cost
        
        # Parse response
        response_text = message.content[0].text
        
        # Extract JSON from response (handle markdown code blocks)
        json_str = response_text
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0]
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            # If JSON parsing fails, return error result
            return ExtractionResult(
                document_type="error",
                file_path=file_path,
                transactions=[],
                extraction_notes=f"Failed to parse Claude response: {response_text[:500]}",
                needs_review=True,
                api_cost=cost
            )
        
        # Convert to ExtractionResult
        transactions = []
        for t in data.get("transactions", []):
            transactions.append(Transaction(
                date=t.get("date", "unknown"),
                customer_or_vendor=t.get("customer_or_vendor", "Unknown"),
                description=t.get("description", ""),
                amount=float(t.get("amount", 0)),
                type=t.get("type", "unknown"),
                category=t.get("category", "other"),
                status=t.get("status", "unknown"),
                line_items=t.get("line_items", []),
                confidence=t.get("confidence", "medium")
            ))
        
        return ExtractionResult(
            document_type=data.get("document_type", "unknown"),
            file_path=file_path,
            transactions=transactions,
            extraction_notes=data.get("extraction_notes", ""),
            needs_review=data.get("needs_review", False),
            api_cost=cost
        )
    
    def combine_results(self, results: list[ExtractionResult]) -> dict:
        """
        Combine extraction results into a unified dataset.
        
        Returns dict with:
        - all_transactions: list of all transactions
        - revenue_transactions: just revenue
        - expense_transactions: just expenses
        - summary: basic stats
        """
        all_transactions = []
        for result in results:
            for t in result.transactions:
                t_dict = t.model_dump() if hasattr(t, 'model_dump') else t.__dict__
                t_dict['source_file'] = result.file_path
                all_transactions.append(t_dict)
        
        revenue = [t for t in all_transactions if t['type'] == 'revenue']
        expenses = [t for t in all_transactions if t['type'] == 'expense']
        
        total_revenue = sum(t['amount'] for t in revenue)
        total_expenses = sum(t['amount'] for t in expenses)
        
        needs_review = [r.file_path for r in results if r.needs_review]
        
        return {
            'all_transactions': all_transactions,
            'revenue_transactions': revenue,
            'expense_transactions': expenses,
            'summary': {
                'total_files_processed': len(results),
                'total_transactions': len(all_transactions),
                'revenue_count': len(revenue),
                'expense_count': len(expenses),
                'total_revenue': total_revenue,
                'total_expenses': total_expenses,
                'gross_profit': total_revenue - total_expenses,
                'files_needing_review': needs_review,
                'total_extraction_cost': sum(r.api_cost for r in results)
            }
        }


# CLI for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_extractor.py <folder_path>")
        print("Example: python data_extractor.py ./data/john_smith")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    extractor = DataExtractor()
    results = extractor.extract_from_folder(folder_path)
    combined = extractor.combine_results(results)
    
    print("\n" + "="*50)
    print("EXTRACTION SUMMARY")
    print("="*50)
    print(f"Files processed: {combined['summary']['total_files_processed']}")
    print(f"Total transactions: {combined['summary']['total_transactions']}")
    print(f"Total revenue: ${combined['summary']['total_revenue']:,.2f}")
    print(f"Total expenses: ${combined['summary']['total_expenses']:,.2f}")
    print(f"Gross profit: ${combined['summary']['gross_profit']:,.2f}")
    print(f"API cost: ${combined['summary']['total_extraction_cost']:.2f}")
    
    if combined['summary']['files_needing_review']:
        print(f"\n⚠️  Files needing review:")
        for f in combined['summary']['files_needing_review']:
            print(f"  - {f}")

