"""Tests for the FileRenamer class with Brightspace folder names."""

import pytest
from brightspace_assessment_rename.renamer import FileRenamer


class TestFileRenamer:
    """Test cases for FileRenamer."""
    
    @pytest.fixture
    def renamer(self):
        """Create a FileRenamer instance for testing."""
        return FileRenamer()
    
    # Tests for parse_brightspace_name
    def test_parse_brightspace_standard_name(self, renamer):
        """Test parsing a standard Brightspace folder name."""
        result = renamer.parse_brightspace_name(
            "123456-789012 - John Smith - Nov 26, 2025 933 PM"
        )
        assert result == ("John Smith", "Nov 26, 2025 933 PM")
    
    def test_parse_brightspace_name_with_leading_dot(self, renamer):
        """Test parsing a name with leading dot (data entry quirk)."""
        result = renamer.parse_brightspace_name(
            "123456-789012 - . Jane Doe - Nov 20, 2025 1059 PM"
        )
        assert result == (". Jane Doe", "Nov 20, 2025 1059 PM")
    
    def test_parse_brightspace_hyphenated_name(self, renamer):
        """Test parsing a hyphenated student name."""
        result = renamer.parse_brightspace_name(
            "123456-789012 - Mary Smith-Jones - Nov 28, 2025 1036 PM"
        )
        assert result == ("Mary Smith-Jones", "Nov 28, 2025 1036 PM")
    
    def test_parse_brightspace_short_id(self, renamer):
        """Test parsing with shorter ID numbers."""
        result = renamer.parse_brightspace_name(
            "12345-789012 - Robert Johnson - Nov 28, 2025 1134 PM"
        )
        assert result == ("Robert Johnson", "Nov 28, 2025 1134 PM")
    
    def test_parse_non_brightspace_name(self, renamer):
        """Test that non-Brightspace names return None."""
        assert renamer.parse_brightspace_name("index.html") is None
        assert renamer.parse_brightspace_name("random folder") is None
    
    # Tests for standardize_folder_name
    def test_standardize_folder_basic(self, renamer):
        """Test basic folder name standardization."""
        result = renamer.standardize_folder_name(
            "123456-789012 - John Smith - Nov 26, 2025 933 PM"
        )
        assert result == "john_smith_nov_26_2025_933_pm"
    
    def test_standardize_folder_with_leading_dot(self, renamer):
        """Test folder with leading dot preserves the dot."""
        result = renamer.standardize_folder_name(
            "123456-789012 - . Jane Doe - Nov 20, 2025 1059 PM"
        )
        assert result == ".jane_doe_nov_20_2025_1059_pm"
    
    def test_standardize_folder_hyphenated_name(self, renamer):
        """Test hyphenated student name converts hyphens to underscores."""
        result = renamer.standardize_folder_name(
            "123456-789012 - Mary Smith-Jones - Nov 28, 2025 1036 PM"
        )
        assert result == "mary_smith_jones_nov_28_2025_1036_pm"
    
    def test_standardize_folder_lowercase_first_name(self, renamer):
        """Test name with lowercase first letter."""
        result = renamer.standardize_folder_name(
            "123456-789012 - james Wilson - Nov 28, 2025 110 AM"
        )
        assert result == "james_wilson_nov_28_2025_110_am"
    
    def test_standardize_folder_special_chars_in_name(self, renamer):
        """Test that special characters are removed from names."""
        result = renamer.standardize_folder_name(
            "123456-789012 - Sarah O'Brien - Nov 13, 2025 1013 PM"
        )
        assert result == "sarah_obrien_nov_13_2025_1013_pm"
    
    # Tests for various Brightspace folder name patterns
    def test_sample_brightspace_names(self, renamer):
        """Test sample Brightspace folder names with various patterns."""
        test_cases = [
            # Standard names
            ("123456-789012 - John Smith - Nov 26, 2025 933 PM", 
             "john_smith_nov_26_2025_933_pm"),
            ("234567-789012 - Jane Doe - Nov 28, 2025 1131 PM", 
             "jane_doe_nov_28_2025_1131_pm"),
            # Hyphenated names
            ("345678-789012 - Mary Smith-Jones - Nov 28, 2025 626 PM", 
             "mary_smith_jones_nov_28_2025_626_pm"),
            # Three-part names
            ("456789-789012 - Robert James Wilson - Nov 27, 2025 706 PM", 
             "robert_james_wilson_nov_27_2025_706_pm"),
            # Leading dot (data entry quirk)
            ("567890-789012 - . David Lee - Nov 20, 2025 1059 PM", 
             ".david_lee_nov_20_2025_1059_pm"),
            ("678901-789012 - . Sarah Chen - Nov 28, 2025 639 PM", 
             ".sarah_chen_nov_28_2025_639_pm"),
            # Lowercase first letter
            ("789012-789012 - james Wilson - Nov 28, 2025 110 AM", 
             "james_wilson_nov_28_2025_110_am"),
            # Short ID numbers
            ("12345-789012 - Emily Brown - Nov 28, 2025 1134 PM", 
             "emily_brown_nov_28_2025_1134_pm"),
            # AM/PM variations
            ("890123-789012 - Michael Davis - Nov 21, 2025 952 AM", 
             "michael_davis_nov_21_2025_952_am"),
            ("901234-789012 - Lisa Garcia - Nov 28, 2025 133 AM", 
             "lisa_garcia_nov_28_2025_133_am"),
        ]
        
        for original, expected in test_cases:
            result = renamer.standardize_folder_name(original)
            assert result == expected, f"Failed for: {original}"
    
    def test_files_to_delete(self, renamer):
        """Test that index.html is in the delete list."""
        assert "index.html" in renamer.FILES_TO_DELETE
