"""Tests for the FileRenamer class."""

import pytest
from brightspace_assessment_rename.renamer import FileRenamer


class TestFileRenamer:
    """Test cases for FileRenamer."""
    
    @pytest.fixture
    def renamer(self):
        """Create a FileRenamer instance for testing."""
        return FileRenamer()
    
    def test_lowercase_conversion(self, renamer):
        """Test that filenames are converted to lowercase."""
        assert renamer.standardize_name("TestFile.PDF") == "testfile.pdf"
        assert renamer.standardize_name("UPPERCASE.TXT") == "uppercase.txt"
    
    def test_space_to_underscore(self, renamer):
        """Test that spaces are converted to underscores."""
        assert renamer.standardize_name("My File Name.txt") == "my_file_name.txt"
        assert renamer.standardize_name("multiple   spaces.doc") == "multiple_spaces.doc"
    
    def test_hyphen_to_underscore(self, renamer):
        """Test that hyphens are converted to underscores."""
        assert renamer.standardize_name("my-file-name.txt") == "my_file_name.txt"
        assert renamer.standardize_name("multiple---hyphens.doc") == "multiple_hyphens.doc"
    
    def test_special_characters_removed(self, renamer):
        """Test that special characters are removed."""
        assert renamer.standardize_name("file@name!.txt") == "filename.txt"
        assert renamer.standardize_name("test#file$name%.pdf") == "testfilename.pdf"
    
    def test_multiple_underscores_collapsed(self, renamer):
        """Test that multiple underscores are collapsed to one."""
        assert renamer.standardize_name("file___name.txt") == "file_name.txt"
        assert renamer.standardize_name("a _ b _ c.pdf") == "a_b_c.pdf"
    
    def test_extension_preserved(self, renamer):
        """Test that file extensions are preserved but lowercased."""
        assert renamer.standardize_name("file.PDF") == "file.pdf"
        assert renamer.standardize_name("document.DOCX") == "document.docx"
    
    def test_no_leading_trailing_underscores(self, renamer):
        """Test that leading/trailing underscores are removed."""
        assert renamer.standardize_name("_leading.txt") == "leading.txt"
        assert renamer.standardize_name("trailing_.txt") == "trailing.txt"
        assert renamer.standardize_name("_both_.txt") == "both.txt"
    
    def test_brightspace_typical_names(self, renamer):
        """Test typical Brightspace assessment filename patterns."""
        # Example: "John Smith - Assignment 1 - May 15, 2025 1030 AM.pdf"
        result = renamer.standardize_name("John Smith - Assignment 1 - May 15, 2025 1030 AM.pdf")
        assert result == "john_smith_assignment_1_may_15_2025_1030_am.pdf"
        
        # Example with special characters
        result = renamer.standardize_name("O'Connor, Mary - Quiz #2.docx")
        assert result == "oconnor_mary_quiz_2.docx"
