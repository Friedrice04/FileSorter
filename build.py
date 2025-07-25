"""Simple build script for FileSorter."""
import os
import sys
import shutil
import subprocess
from pathlib import Path

class FileSorterBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.src_dir = self.root_dir / "src"
        
    def clean(self):
        """Remove previous build artifacts."""
        print("Cleaning previous builds...")
        dirs_to_clean = [self.root_dir / "build", self.root_dir / "dist"]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
        
        spec_file = self.root_dir / "FileSorter.spec"
        if spec_file.exists():
            spec_file.unlink()
    
    def validate(self):
        """Quick validation of dependencies and assets."""
        try:
            import tkinterdnd2
            import PyInstaller
        except ImportError as e:
            print(f"Missing dependency: {e.name}")
            print("Install with: pip install -r requirements.txt")
            return False
        
        required_files = [
            self.src_dir / "main.py",
            self.src_dir / "icons" / "sorterIcon.ico"
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                print(f"Missing file: {file_path}")
                return False
        
        return True
    
    
    def build(self):
        """Build the executable."""
        print("Building FileSorter executable...")
        
        if not self.validate():
            return False
        
        self.clean()
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name=FileSorter",
            "--onefile",
            "--noconsole",
            "--distpath=./dist",
            "--workpath=./build",
            "--add-data", "src/icons/*;src/icons",
            "--icon", "src/icons/sorterIcon.ico",
            "--add-data", "src/mappings/example.json;src/mappings",
            "src/main.py"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ Build successful! Executable is in ./dist/FileSorter.exe")
            return True
        except subprocess.CalledProcessError:
            print("❌ Build failed")
            return False

def main():
    builder = FileSorterBuilder()
    success = builder.build()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
