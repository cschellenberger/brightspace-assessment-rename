"""File renaming logic for standardizing file names."""

import re
from pathlib import Path


class FileRenamer:
    """Handles file renaming operations with standardized naming conventions."""
    
    def __init__(self):
        """Initialize the FileRenamer."""
        # Characters to replace with underscores
        self.replace_chars = re.compile(r'[\s\-]+')
        # Characters to remove entirely
        self.remove_chars = re.compile(r'[^\w\._]')
        # Multiple underscores
        self.multi_underscore = re.compile(r'_+')
    
    def standardize_name(self, filename: str) -> str:
        """
        Convert a filename to the standard format.
        
        Standard format: lowercase_with_underscores.ext
        
        Args:
            filename: The original filename (with or without extension)
            
        Returns:
            The standardized filename
        """
        # Separate name and extension
        path = Path(filename)
        name = path.stem
        extension = path.suffix.lower()
        
        # Convert to lowercase
        name = name.lower()
        
        # Replace spaces and hyphens with underscores
        name = self.replace_chars.sub('_', name)
        
        # Remove special characters (keep alphanumeric, underscore, dot)
        name = self.remove_chars.sub('', name)
        
        # Replace multiple underscores with single
        name = self.multi_underscore.sub('_', name)
        
        # Remove leading/trailing underscores
        name = name.strip('_')
        
        # Handle empty name edge case
        if not name:
            name = "unnamed"
        
        return f"{name}{extension}"
    
    def get_rename_preview(self, folder_path: Path) -> list[tuple[str, str]]:
        """
        Get a preview of all file renames in a folder.
        
        Args:
            folder_path: Path to the folder containing files
            
        Returns:
            List of tuples (original_name, new_name)
        """
        changes = []
        
        if not folder_path.exists() or not folder_path.is_dir():
            return changes
        
        for file_path in sorted(folder_path.iterdir()):
            if file_path.is_file():
                original_name = file_path.name
                new_name = self.standardize_name(original_name)
                changes.append((original_name, new_name))
        
        return changes
    
    def rename_files(self, folder_path: Path) -> int:
        """
        Rename all files in a folder to the standard format.
        
        Args:
            folder_path: Path to the folder containing files
            
        Returns:
            Number of files renamed
        """
        renamed_count = 0
        
        if not folder_path.exists() or not folder_path.is_dir():
            return renamed_count
        
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                original_name = file_path.name
                new_name = self.standardize_name(original_name)
                
                if original_name != new_name:
                    new_path = file_path.parent / new_name
                    
                    # Handle duplicate names by adding a number suffix
                    counter = 1
                    while new_path.exists():
                        stem = Path(new_name).stem
                        ext = Path(new_name).suffix
                        new_path = file_path.parent / f"{stem}_{counter}{ext}"
                        counter += 1
                    
                    file_path.rename(new_path)
                    renamed_count += 1
        
        return renamed_count
