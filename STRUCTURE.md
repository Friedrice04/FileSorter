# Project Structure Documentation

This document outlines the professional structure for building and distributing FileSorter.

## Directory Layout

```
FileSorter/                          # Root project directory
├── 📁 src/                          # Source code
│   ├── 🐍 main.py                   # Application entry point
│   ├── 🐍 gui.py                    # Main GUI application
│   ├── 🐍 sorter.py                 # File sorting logic
│   ├── 🐍 utils.py                  # Utility functions
│   ├── 📁 icons/                    # Application icons
│   │   ├── 🖼️ sorterIcon.ico        # Main application icon
│   │   ├── 🖼️ folder.ico            # Folder icon
│   │   └── 🖼️ pin.ico               # Pin icon
│   ├── 📁 mappings/                 # Default mapping files
│   │   ├── 📄 example.json          # Example mapping
│   │   └── 📁 example_template/     # Example template structure
│   └── 📁 mapping_editor/           # Mapping editor module
│       ├── 🐍 __init__.py
│       ├── 🐍 editor.py             # Main editor window
│       ├── 🐍 dialogs.py            # Dialog windows
│       ├── 🐍 mapping_table.py      # Pattern table widget
│       └── 🐍 template_tree.py      # Template tree widget
├── 🏗️ build.py                      # Professional build script
├── 🔧 requirements.txt              # Project dependencies
├── 📖 BUILD_README.md               # Build documentation
├── 🚀 build.bat                     # Windows quick build
├── 🚀 build.sh                      # Unix/Linux/Mac quick build
├── 🚫 .gitignore                    # Git ignore rules
├── 📜 LICENSE.txt                   # License information
├── 📖 README.md                     # Main project documentation
└── 📁 release/                      # Final executable output (generated)
    ├── 🎯 FileSorter.exe            # Built executable
    └── 📋 release_info.txt          # Build information
```

## Build Process Flow

### 1. Pre-Build Validation
- ✅ Check Python dependencies (`tkinterdnd2`, `pyinstaller`)
- ✅ Verify all required assets exist
- ✅ Validate source code integrity

### 2. Build Configuration
- 📝 Generate optimized PyInstaller spec file
- 🎯 Configure one-file executable output
- 🗜️ Enable UPX compression for smaller size
- 🚫 Exclude unnecessary modules

### 3. Compilation
- 🏗️ Run PyInstaller with optimized settings
- 📦 Bundle all dependencies and assets
- 🖼️ Embed application icon
- 🔇 Create windowed application (no console)

### 4. Post-Build Organization
- 🧹 Clean up temporary build files
- 📁 Move executable to `release/` folder
- 📋 Generate release information file
- ✅ Validate final output

## Key Features of Professional Structure

### 🎯 **One-Command Build**
```bash
python build.py
```

### 🔍 **Comprehensive Validation**
- Dependency checking
- Asset verification
- Pre-build validation
- Post-build verification

### 📦 **Optimized Output**
- Single executable file
- Minimal size with UPX compression
- All dependencies bundled
- Professional icon integration

### 🧹 **Clean Organization**
- Separate build and release directories
- Automatic cleanup of temporary files
- Clear separation of source and output
- Professional directory naming

### 🚀 **Cross-Platform Support**
- `build.bat` for Windows users
- `build.sh` for Unix/Linux/Mac users
- Universal `build.py` for all platforms

### 📚 **Documentation**
- Comprehensive build guide (`BUILD_README.md`)
- Inline code documentation
- Clear directory structure
- Troubleshooting guides

## Usage Examples

### Quick Build (Windows)
```cmd
build.bat
```

### Quick Build (Unix/Linux/Mac)
```bash
./build.sh
```

### Advanced Build Options
```bash
# Clean build (default)
python build.py

# Skip cleanup
python build.py --no-clean

# Validation only
python build.py --validate-only
```

## Maintenance

### Adding New Dependencies
1. Add to `requirements.txt`
2. Test with `python build.py --validate-only`
3. Build and test executable

### Adding New Assets
1. Place assets in appropriate `src/` subdirectory
2. Update `build.py` if needed for inclusion
3. Test build process

### Updating Build Configuration
- Modify `build.py` for build logic changes
- Update `requirements.txt` for dependency changes
- Adjust `.gitignore` for new file patterns

This structure provides a professional, maintainable, and user-friendly way to build and distribute your FileSorter application.
