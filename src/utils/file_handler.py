"""
File handling utilities for the audit agent.
Handles uploads, storage, and organization of customer documents.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import hashlib


class FileHandler:
    """
    Handles file operations for customer data.
    
    Organizes files into customer folders and tracks processing status.
    """
    
    def __init__(self, base_dir: str = "./data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def create_customer_folder(self, customer_name: str) -> Path:
        """
        Create a folder for a customer's documents.
        
        Args:
            customer_name: Customer/business name
            
        Returns:
            Path to customer folder
        """
        # Sanitize customer name for folder
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in customer_name)
        safe_name = safe_name.replace(' ', '_').lower()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{safe_name}_{timestamp}"
        
        customer_path = self.base_dir / folder_name
        customer_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (customer_path / "invoices").mkdir(exist_ok=True)
        (customer_path / "expenses").mkdir(exist_ok=True)
        (customer_path / "quotes").mkdir(exist_ok=True)
        (customer_path / "statements").mkdir(exist_ok=True)
        (customer_path / "other").mkdir(exist_ok=True)
        
        return customer_path
    
    def save_uploaded_file(
        self, 
        file_content: bytes, 
        filename: str, 
        customer_folder: Path,
        category: Optional[str] = None
    ) -> Path:
        """
        Save an uploaded file to the customer folder.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            customer_folder: Path to customer's folder
            category: Optional category (invoices, expenses, quotes, statements)
            
        Returns:
            Path to saved file
        """
        # Determine category from filename if not provided
        if not category:
            category = self._guess_category(filename)
        
        # Ensure category folder exists
        category_path = customer_folder / category
        category_path.mkdir(exist_ok=True)
        
        # Generate unique filename to avoid collisions
        file_path = category_path / filename
        if file_path.exists():
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{name}_{timestamp}{ext}"
            file_path = category_path / filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return file_path
    
    def _guess_category(self, filename: str) -> str:
        """Guess file category from filename."""
        filename_lower = filename.lower()
        
        if any(word in filename_lower for word in ['invoice', 'inv', 'receipt']):
            return "invoices"
        elif any(word in filename_lower for word in ['expense', 'cost', 'purchase', 'bill']):
            return "expenses"
        elif any(word in filename_lower for word in ['quote', 'estimate', 'proposal']):
            return "quotes"
        elif any(word in filename_lower for word in ['statement', 'bank', 'transaction']):
            return "statements"
        else:
            return "other"
    
    def list_customer_folders(self) -> list[dict]:
        """
        List all customer folders with metadata.
        
        Returns:
            List of dicts with folder info
        """
        folders = []
        
        for item in self.base_dir.iterdir():
            if item.is_dir():
                # Count files
                file_count = sum(1 for _ in item.rglob("*") if _.is_file())
                
                # Get creation time
                stat = item.stat()
                created = datetime.fromtimestamp(stat.st_ctime)
                
                folders.append({
                    "name": item.name,
                    "path": str(item),
                    "file_count": file_count,
                    "created": created.isoformat(),
                    "size_mb": sum(f.stat().st_size for f in item.rglob("*") if f.is_file()) / (1024 * 1024)
                })
        
        return sorted(folders, key=lambda x: x["created"], reverse=True)
    
    def get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of a file for deduplication."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def cleanup_old_folders(self, days_old: int = 90) -> list[str]:
        """
        Remove customer folders older than specified days.
        
        Args:
            days_old: Remove folders older than this many days
            
        Returns:
            List of removed folder names
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days_old)
        removed = []
        
        for item in self.base_dir.iterdir():
            if item.is_dir():
                stat = item.stat()
                created = datetime.fromtimestamp(stat.st_ctime)
                
                if created < cutoff:
                    shutil.rmtree(item)
                    removed.append(item.name)
        
        return removed


class OutputHandler:
    """
    Handles output file organization.
    """
    
    def __init__(self, base_dir: str = "./output"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def create_output_folder(self, customer_name: str) -> Path:
        """Create output folder for a customer's reports."""
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in customer_name)
        safe_name = safe_name.replace(' ', '_').lower()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{safe_name}_{timestamp}"
        
        output_path = self.base_dir / folder_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        return output_path
    
    def list_outputs(self) -> list[dict]:
        """List all output folders."""
        outputs = []
        
        for item in self.base_dir.iterdir():
            if item.is_dir():
                # Check for report files
                has_html = (item / "profit_leak_audit_report.html").exists()
                has_excel = (item / "profit_leak_audit_workbook.xlsx").exists()
                has_json = (item / "analysis_data.json").exists()
                
                stat = item.stat()
                created = datetime.fromtimestamp(stat.st_ctime)
                
                outputs.append({
                    "name": item.name,
                    "path": str(item),
                    "created": created.isoformat(),
                    "has_html": has_html,
                    "has_excel": has_excel,
                    "has_json": has_json,
                    "complete": has_html and has_excel
                })
        
        return sorted(outputs, key=lambda x: x["created"], reverse=True)


# Example usage
if __name__ == "__main__":
    # Test file handler
    handler = FileHandler()
    
    # Create a test customer folder
    folder = handler.create_customer_folder("Test Electrical")
    print(f"Created folder: {folder}")
    
    # List folders
    folders = handler.list_customer_folders()
    print(f"\nExisting folders: {len(folders)}")
    for f in folders[:5]:
        print(f"  - {f['name']}: {f['file_count']} files")

