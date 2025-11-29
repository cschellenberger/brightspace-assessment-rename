# Brightspace Assessment Rename

A simple GUI application for standardizing file names from Brightspace assessment downloads.

## Features

- **Easy-to-use GUI**: Browse and select folders with a simple click
- **Preview changes**: See exactly what files will be renamed before committing
- **Standard naming format**: Converts filenames to `lowercase_with_underscores.ext`
- **Safe operation**: Handles duplicate names automatically
- **Distributable**: Can be packaged as a standalone executable for easy sharing

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/brightspace-assessment-rename.git
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

1. Click **Browse...** to select a folder containing files to rename
2. Click **Preview Changes** to see what will be renamed
3. Review the changes in the preview panel
4. Click **Rename Files** to apply the changes

### Naming Convention

Files are converted to the following format:
- All lowercase
- Spaces and hyphens replaced with underscores
- Special characters removed
- Multiple underscores collapsed to single underscore

**Examples:**
| Original | Renamed |
|----------|---------|
| `John Smith - Assignment 1.pdf` | `john_smith_assignment_1.pdf` |
| `Mary O'Connor Quiz #2.docx` | `mary_oconnor_quiz_2.docx` |
| `UPPERCASE FILE.TXT` | `uppercase_file.txt` |

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
