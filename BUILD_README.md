# FileSorter Build Configuration

This directory contains the professional build configuration for FileSorter.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable:**
   ```bash
   python build.py
   ```

3. **Find your executable:**
   The built executable will be in the `release/` folder.

## Build Options

- **Clean build:** `python build.py` (default)
- **Skip cleanup:** `python build.py --no-clean`
- **Validate only:** `python build.py --validate-only`

## Directory Structure

```
FileSorter/
├── build.py              # Professional build script
├── requirements.txt      # All dependencies
├── README.md            # This file
├── LICENSE.txt          # License information
├── src/                 # Source code
│   ├── main.py         # Entry point
│   ├── gui.py          # Main GUI
│   ├── sorter.py       # Sorting logic
│   ├── utils.py        # Utilities
│   ├── icons/          # Application icons
│   ├── mappings/       # Default mappings
│   └── mapping_editor/ # Mapping editor module
├── build/              # Temporary build files (auto-generated)
├── dist/               # PyInstaller output (auto-generated)
└── release/            # Final executable location (auto-generated)
```

## Build Process

The build script performs these steps:

1. **Validation:** Checks dependencies and required assets
2. **Cleanup:** Removes previous build artifacts
3. **Spec Generation:** Creates optimized PyInstaller configuration
4. **Building:** Compiles the executable with PyInstaller
5. **Post-processing:** Organizes output and creates release info

## Customization

### Adding Dependencies
Add new packages to `requirements.txt` and ensure they're properly imported in the code.

### Including Additional Assets
Modify the `datas` section in the generated spec file or update the build script's `create_spec_file()` method.

### Build Optimization
The build script includes several optimizations:
- UPX compression for smaller executable size
- Exclusion of unnecessary modules
- Python optimization level 2
- Clean one-file executable output

## Troubleshooting

### Common Issues

1. **Missing tkinterdnd2:**
   ```bash
   pip install tkinterdnd2
   ```

2. **PyInstaller not found:**
   ```bash
   pip install pyinstaller
   ```

3. **Missing icons:**
   Ensure all `.ico` files exist in `src/icons/`

4. **Build fails:**
   Use `python build.py --validate-only` to check for issues

### Getting Help

If you encounter issues:
1. Run validation: `python build.py --validate-only`
2. Check the build output for specific error messages
3. Ensure all files in `src/` are present and accessible

## Advanced Usage

### Custom Build Configuration

You can modify `build.py` to customize:
- Executable name and version
- Included/excluded modules
- Compression settings
- Output directory structure
- Additional build steps

### Development Environment

For development, you can uncomment the development dependencies in `requirements.txt`:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking
- `pytest` for testing

Then install with:
```bash
pip install -r requirements.txt
```
