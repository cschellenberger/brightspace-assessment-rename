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
            "104840-170649 - Pal Patel - Nov 26, 2025 933 PM"
        )
        assert result == ("Pal Patel", "Nov 26, 2025 933 PM")
    
    def test_parse_brightspace_name_with_leading_dot(self, renamer):
        """Test parsing a name with leading dot (data entry quirk)."""
        result = renamer.parse_brightspace_name(
            "104860-170649 - . Karanvir Singh - Nov 20, 2025 1059 PM"
        )
        assert result == (". Karanvir Singh", "Nov 20, 2025 1059 PM")
    
    def test_parse_brightspace_hyphenated_name(self, renamer):
        """Test parsing a hyphenated student name."""
        result = renamer.parse_brightspace_name(
            "104848-170649 - Jueszel Morgan-Mcleggon - Nov 28, 2025 1036 PM"
        )
        assert result == ("Jueszel Morgan-Mcleggon", "Nov 28, 2025 1036 PM")
    
    def test_parse_brightspace_short_id(self, renamer):
        """Test parsing with shorter ID numbers."""
        result = renamer.parse_brightspace_name(
            "24573-170649 - Boluwatife Akinrinola - Nov 28, 2025 1134 PM"
        )
        assert result == ("Boluwatife Akinrinola", "Nov 28, 2025 1134 PM")
    
    def test_parse_non_brightspace_name(self, renamer):
        """Test that non-Brightspace names return None."""
        assert renamer.parse_brightspace_name("index.html") is None
        assert renamer.parse_brightspace_name("random folder") is None
    
    # Tests for standardize_folder_name
    def test_standardize_folder_basic(self, renamer):
        """Test basic folder name standardization."""
        result = renamer.standardize_folder_name(
            "104840-170649 - Pal Patel - Nov 26, 2025 933 PM"
        )
        assert result == "pal_patel_nov_26_2025_933_pm"
    
    def test_standardize_folder_with_leading_dot(self, renamer):
        """Test folder with leading dot preserves the dot."""
        result = renamer.standardize_folder_name(
            "104860-170649 - . Karanvir Singh - Nov 20, 2025 1059 PM"
        )
        assert result == ".karanvir_singh_nov_20_2025_1059_pm"
    
    def test_standardize_folder_hyphenated_name(self, renamer):
        """Test hyphenated student name converts hyphens to underscores."""
        result = renamer.standardize_folder_name(
            "104848-170649 - Jueszel Morgan-Mcleggon - Nov 28, 2025 1036 PM"
        )
        assert result == "jueszel_morgan_mcleggon_nov_28_2025_1036_pm"
    
    def test_standardize_folder_lowercase_first_name(self, renamer):
        """Test name with lowercase first letter."""
        result = renamer.standardize_folder_name(
            "104851-170649 - ayoola Akinloye - Nov 28, 2025 110 AM"
        )
        assert result == "ayoola_akinloye_nov_28_2025_110_am"
    
    def test_standardize_folder_special_chars_in_name(self, renamer):
        """Test that special characters are removed from names."""
        result = renamer.standardize_folder_name(
            "104854-170649 - Ilma Qureshi - Nov 13, 2025 1013 PM"
        )
        assert result == "ilma_qureshi_nov_13_2025_1013_pm"
    
    # Tests for all real sample data
    def test_all_sample_brightspace_names(self, renamer):
        """Test all sample Brightspace folder names from real data."""
        test_cases = [
            ("104840-170649 - Pal Patel - Nov 26, 2025 933 PM", 
             "pal_patel_nov_26_2025_933_pm"),
            ("104841-170649 - Darus Kuwon - Nov 28, 2025 1131 PM", 
             "darus_kuwon_nov_28_2025_1131_pm"),
            ("104845-170649 - Grayson Chaikowsky - Nov 28, 2025 626 PM", 
             "grayson_chaikowsky_nov_28_2025_626_pm"),
            ("104847-170649 - Ben Chrenek - Nov 27, 2025 706 PM", 
             "ben_chrenek_nov_27_2025_706_pm"),
            ("104848-170649 - Jueszel Morgan-Mcleggon - Nov 28, 2025 1036 PM", 
             "jueszel_morgan_mcleggon_nov_28_2025_1036_pm"),
            ("104849-170649 - Olyvr Daigle - Nov 26, 2025 245 PM", 
             "olyvr_daigle_nov_26_2025_245_pm"),
            ("104851-170649 - ayoola Akinloye - Nov 28, 2025 110 AM", 
             "ayoola_akinloye_nov_28_2025_110_am"),
            ("104854-170649 - Ilma Qureshi - Nov 13, 2025 1013 PM", 
             "ilma_qureshi_nov_13_2025_1013_pm"),
            ("104856-170649 - Melody Bango - Nov 28, 2025 133 AM", 
             "melody_bango_nov_28_2025_133_am"),
            ("104858-170649 - Hamid Gilani - Nov 21, 2025 227 PM", 
             "hamid_gilani_nov_21_2025_227_pm"),
            ("104860-170649 - . Karanvir Singh - Nov 20, 2025 1059 PM", 
             ".karanvir_singh_nov_20_2025_1059_pm"),
            ("104863-170649 - Amy Persaud - Nov 28, 2025 331 PM", 
             "amy_persaud_nov_28_2025_331_pm"),
            ("108597-170649 - Feyi Babaleye - Nov 21, 2025 952 AM", 
             "feyi_babaleye_nov_21_2025_952_am"),
            ("24573-170649 - Boluwatife Akinrinola - Nov 28, 2025 1134 PM", 
             "boluwatife_akinrinola_nov_28_2025_1134_pm"),
            ("28746-170649 - Abdulrahman Almajid - Nov 28, 2025 649 PM", 
             "abdulrahman_almajid_nov_28_2025_649_pm"),
            ("45095-170649 - Nima Ghanbari - Nov 28, 2025 542 PM", 
             "nima_ghanbari_nov_28_2025_542_pm"),
            ("74609-170649 - . Harsimar Singh - Nov 28, 2025 639 PM", 
             ".harsimar_singh_nov_28_2025_639_pm"),
            ("80864-170649 - Anmolpreet Singh Panaich - Nov 28, 2025 1125 AM", 
             "anmolpreet_singh_panaich_nov_28_2025_1125_am"),
        ]
        
        for original, expected in test_cases:
            result = renamer.standardize_folder_name(original)
            assert result == expected, f"Failed for: {original}"
    
    def test_files_to_delete(self, renamer):
        """Test that index.html is in the delete list."""
        assert "index.html" in renamer.FILES_TO_DELETE
