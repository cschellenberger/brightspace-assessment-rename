# Brightspace Assessment Rename

A simple GUI application for standardizing folder names from Brightspace assessment downloads.

## Features

- **Easy-to-use GUI**: Browse and select Brightspace download folders with a simple click
- **Preview changes**: See exactly what folders will be renamed before committing
- **Brightspace-specific**: Parses the standard Brightspace folder format `{id}-{id} - {Name} - {Date Time}`
- **Standard naming format**: Converts folder names to `student_name_date_time` format
- **Preserves sorting**: Names starting with `.` (Brightspace data entry quirk) are preserved for consistent grading order
- **Auto-cleanup**: Automatically deletes `index.html` files from downloads
- **Safe operation**: Handles duplicate names automatically
- **Distributable**: Can be packaged as a standalone executable for easy sharing via SharePoint

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/cschellenberger/brightspace-assessment-rename.git
   cd brightspace-assessment-rename
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install the package:
   ```bash
   pip install -e .
   ```

5. (Optional) Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Running the Application

```bash
# After installation
brightspace-rename

# Or run directly
python -m brightspace_assessment_rename
```

### Using the GUI

1. Click **Browse...** to select a Brightspace assessment download folder
2. Click **Preview Changes** to see what folders will be renamed and files deleted
3. Review the changes in the preview panel
4. Click **Rename Folders** to apply the changes

### Naming Convention

Brightspace folders are converted from:

`{id}-{id} - {Student Name} - {Date Time}`

To the standardized format:

`student_name_date_time`

- All lowercase
- Spaces and hyphens replaced with underscores
- Special characters removed
- Leading dots preserved (for Brightspace data entry quirks)
- `index.html` files are deleted

**Examples:**

| Original | Renamed |
|----------|---------|
| `104840-170649 - Pal Patel - Nov 26, 2025 933 PM` | `pal_patel_nov_26_2025_933_pm` |
| `104860-170649 - . Karanvir Singh - Nov 20, 2025 1059 PM` | `.karanvir_singh_nov_20_2025_1059_pm` |
| `104848-170649 - Jueszel Morgan-Mcleggon - Nov 28, 2025 1036 PM` | `jueszel_morgan_mcleggon_nov_28_2025_1036_pm` |
| `index.html` | *(deleted)* |

## Building Standalone Executable

To create a distributable `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name brightspace-rename src/brightspace_assessment_rename/main.py
```

The executable will be created in the `dist/` folder.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src tests
ruff check src tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
