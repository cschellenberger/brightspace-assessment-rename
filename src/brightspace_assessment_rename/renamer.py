"""File renaming logic for standardizing Brightspace assessment folder names."""

import re
from pathlib import Path


class FileRenamer:
    """Handles folder renaming operations for Brightspace assessment downloads."""
    
    # Files to delete during rename operation
    FILES_TO_DELETE = {"index.html"}
    
    # Brightspace folder pattern: {numbers}-{numbers} - {Name} - {Date Time}
    BRIGHTSPACE_PATTERN = re.compile(
        r'^\d+-\d+\s*-\s*(.+?)\s*-\s*(\w+\s+\d+,\s+\d+\s+\d+\s*(?:AM|PM))$'
    )
    
    def __init__(self):
        """Initialize the FileRenamer."""
        # Characters to replace with underscores
        self.replace_chars = re.compile(r'[\s\-]+')
        # Characters to remove entirely (keep alphanumeric, underscore, dot)
        self.remove_chars = re.compile(r'[^\w\._]')
        # Multiple underscores
        self.multi_underscore = re.compile(r'_+')
    
    def parse_brightspace_name(self, folder_name: str) -> tuple[str, str] | None:
        """
        Parse a Brightspace folder name to extract student name and date.
        
        Format: {numbers}-{numbers} - {Name} - {Date Time}
        Example: "104840-170649 - Pal Patel - Nov 26, 2025 933 PM"
        
        Args:
            folder_name: The original Brightspace folder name
            
        Returns:
            Tuple of (student_name, date_time) or None if pattern doesn't match
        """
        match = self.BRIGHTSPACE_PATTERN.match(folder_name)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None
    
    def standardize_name(self, name: str) -> str:
        """
        Convert a name to the standard format: lowercase_with_underscores
        
        Args:
            name: The original name string
            
        Returns:
            The standardized name
        """
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
        
        return name
    
    def standardize_folder_name(self, folder_name: str) -> str:
        """
        Convert a Brightspace folder name to the standard format.
        
        Input:  "104840-170649 - Pal Patel - Nov 26, 2025 933 PM"
        Output: "pal_patel_nov_26_2025_933_pm"
        
        Input:  "104860-170649 - . Karanvir Singh - Nov 20, 2025 1059 PM"
        Output: ".karanvir_singh_nov_20_2025_1059_pm"
        
        Args:
            folder_name: The original Brightspace folder name
            
        Returns:
            The standardized folder name
        """
        parsed = self.parse_brightspace_name(folder_name)
        
        if parsed:
            student_name, date_time = parsed
            
            # Check if name starts with ". " (Brightspace data entry quirk)
            has_leading_dot = student_name.startswith('. ')
            if has_leading_dot:
                student_name = student_name[2:]  # Remove ". " prefix
            
            # Standardize both parts
            std_name = self.standardize_name(student_name)
            std_date = self.standardize_name(date_time)
            
            # Reconstruct with leading dot if originally present
            if has_leading_dot:
                return f".{std_name}_{std_date}"
            else:
                return f"{std_name}_{std_date}"
        else:
            # Fallback: just standardize the whole name
            return self.standardize_name(folder_name)
    
    def get_rename_preview(self, folder_path: Path) -> list[tuple[str, str]]:
        """
        Get a preview of all folder renames and files to delete.
        
        Args:
            folder_path: Path to the folder containing Brightspace subfolders
            
        Returns:
            List of tuples (original_name, new_name)
            Files to delete will show new_name as "[DELETE]"
        """
        changes = []
        
        if not folder_path.exists() or not folder_path.is_dir():
            return changes
        
        for item_path in sorted(folder_path.iterdir()):
            original_name = item_path.name
            
            if item_path.is_file():
                # Mark files for deletion if in delete list
                if original_name in self.FILES_TO_DELETE:
                    changes.append((original_name, "[DELETE]"))
            elif item_path.is_dir():
                new_name = self.standardize_folder_name(original_name)
                changes.append((original_name, new_name))
        
        return changes
    
    def rename_files(self, folder_path: Path) -> int:
        """
        Rename all Brightspace folders and delete index.html files.
        
        Args:
            folder_path: Path to the folder containing Brightspace subfolders
            
        Returns:
            Number of items renamed/deleted
        """
        action_count = 0
        
        if not folder_path.exists() or not folder_path.is_dir():
            return action_count
        
        for item_path in folder_path.iterdir():
            original_name = item_path.name
            
            if item_path.is_file():
                # Delete files in the delete list
                if original_name in self.FILES_TO_DELETE:
                    item_path.unlink()
                    action_count += 1
            elif item_path.is_dir():
                new_name = self.standardize_folder_name(original_name)
                
                if original_name != new_name:
                    new_path = item_path.parent / new_name
                    
                    # Handle duplicate names by adding a number suffix
                    counter = 1
                    while new_path.exists():
                        new_path = item_path.parent / f"{new_name}_{counter}"
                        counter += 1
                    
                    item_path.rename(new_path)
                    action_count += 1
        
        return action_count
