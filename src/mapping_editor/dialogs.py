"""
dialogs.py

Dialog classes for FileSorter:
- NewMappingDialog: Create a new mapping, optionally importing from an existing mapping file.
- PatternDestDialog: Edit or add a pattern/destination mapping, with user-friendly layout and help.
- PatternBuilderDialog: Build simple fnmatch patterns without wildcards knowledge.
- AdvancedPatternBuilderDialog: Build regex patterns with guided options.

Author: Your Name
"""

import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import re

class NewMappingDialog(simpledialog.Dialog):
    """
    Dialog for creating a new mapping file, with optional import from an existing mapping.
    Shows the selected import file for user clarity.
    """
    def __init__(self, parent, title):
        self.mapping_name = None
        self.import_selected = False
        self.import_path = None
        super().__init__(parent, title)

    def body(self, master):
        """
        Build the dialog UI.
        """
        frame = ttk.Frame(master)
        frame.grid(sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Mapping Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=0, column=1, sticky="ew")
        self.name_entry.focus_set()

        self.import_var = tk.IntVar()
        self.import_check = ttk.Checkbutton(
            frame, text="Import from existing mapping", variable=self.import_var, command=self._toggle_import
        )
        self.import_check.grid(row=1, column=0, columnspan=2, sticky="w")

        self.import_btn = ttk.Button(frame, text="Browse...", command=self._browse_import, state="disabled")
        self.import_btn.grid(row=2, column=0, sticky="w")

        # Label to show selected file
        self.import_file_label = ttk.Label(frame, text="", foreground="#555")
        self.import_file_label.grid(row=2, column=1, sticky="w")

        return self.name_entry

    def _toggle_import(self):
        """
        Enable or disable the import button and clear the file label as needed.
        """
        if self.import_var.get():
            self.import_btn.config(state="normal")
        else:
            self.import_btn.config(state="disabled")
            self.import_path = None
            self.import_file_label.config(text="")

    def _browse_import(self):
        """
        Open a file dialog to select a mapping file to import, and display the file name.
        """
        path = filedialog.askopenfilename(
            title="Select Mapping File",
            filetypes=[("JSON Files", "*.json")]
        )
        if path:
            self.import_path = path
            # Show only the file name for clarity
            self.import_file_label.config(text=os.path.basename(path))
        else:
            self.import_file_label.config(text="")

    def validate(self):
        """
        Validate user input before closing the dialog.
        """
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a mapping name.", parent=self)
            return False
        if self.import_var.get() and not self.import_path:
            messagebox.showerror("Error", "Please select a mapping file to import.", parent=self)
            return False
        return True

    def apply(self):
        """
        Save the dialog results.
        """
        self.mapping_name = self.name_entry.get().strip()
        self.import_selected = bool(self.import_var.get())
        self.import_path = self.import_path

class PatternBuilderDialog(simpledialog.Dialog):
    """
    Dialog for building a filename pattern without needing to know wildcards or regex.
    Produces a fnmatch-style pattern.
    """
    def __init__(self, parent, title="Pattern Builder"):
        self.result_pattern = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Build your pattern:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.starts_with = tk.StringVar()
        self.contains = tk.StringVar()
        self.ends_with = tk.StringVar()
        self.extension = tk.StringVar()

        ttk.Label(master, text="Starts with:").grid(row=1, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.starts_with).grid(row=1, column=1, sticky="ew")

        ttk.Label(master, text="Contains:").grid(row=2, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.contains).grid(row=2, column=1, sticky="ew")

        ttk.Label(master, text="Ends with:").grid(row=3, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.ends_with).grid(row=3, column=1, sticky="ew")

        ttk.Label(master, text="Extension:").grid(row=4, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.extension).grid(row=4, column=1, sticky="ew")

        master.grid_columnconfigure(1, weight=1)
        return None

    def validate(self):
        if not (self.starts_with.get() or self.contains.get() or self.ends_with.get() or self.extension.get()):
            messagebox.showerror("Error", "Please fill at least one field.", parent=self)
            return False
        return True

    def apply(self):
        # Build fnmatch pattern
        pattern = ""
        if self.starts_with.get():
            pattern += self.starts_with.get()
        else:
            pattern += "*"
        if self.contains.get():
            pattern += "*" + self.contains.get() + "*"
        else:
            pattern += ""
        if self.ends_with.get():
            pattern += self.ends_with.get()
        else:
            pattern += "*"
        if self.extension.get():
            ext = self.extension.get()
            if not ext.startswith("."):
                ext = "." + ext
            pattern += ext
        self.result_pattern = pattern

class AdvancedPatternBuilderDialog(simpledialog.Dialog):
    """
    Dialog for building a regex pattern with guided options.
    Produces a regex pattern wrapped in slashes.
    """
    def __init__(self, parent, title="Advanced Pattern Builder"):
        self.result_pattern = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Build an advanced pattern (Regex):").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.starts_with = tk.StringVar()
        self.contains = tk.StringVar()
        self.ends_with = tk.StringVar()
        self.extension = tk.StringVar()
        self.digits = tk.BooleanVar()
        self.letters = tk.BooleanVar()
        self.ignore_case = tk.BooleanVar()

        ttk.Label(master, text="Starts with:").grid(row=1, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.starts_with).grid(row=1, column=1, sticky="ew")

        ttk.Label(master, text="Contains:").grid(row=2, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.contains).grid(row=2, column=1, sticky="ew")

        ttk.Label(master, text="Ends with:").grid(row=3, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.ends_with).grid(row=3, column=1, sticky="ew")

        ttk.Label(master, text="Extension:").grid(row=4, column=0, sticky="e")
        ttk.Entry(master, textvariable=self.extension).grid(row=4, column=1, sticky="ew")

        ttk.Checkbutton(master, text="Contains digits", variable=self.digits).grid(row=5, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(master, text="Contains letters", variable=self.letters).grid(row=6, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(master, text="Ignore case", variable=self.ignore_case).grid(row=7, column=0, columnspan=2, sticky="w")

        master.grid_columnconfigure(1, weight=1)
        return None

    def validate(self):
        if not (self.starts_with.get() or self.contains.get() or self.ends_with.get() or self.extension.get() or self.digits.get() or self.letters.get()):
            messagebox.showerror("Error", "Please fill at least one field or select an option.", parent=self)
            return False
        return True

    def apply(self):
        regex = "^"
        if self.starts_with.get():
            regex += re.escape(self.starts_with.get())
        if self.contains.get():
            regex += ".*" + re.escape(self.contains.get()) + ".*"
        if self.digits.get():
            regex += ".*\\d+.*"
        if self.letters.get():
            regex += ".*[A-Za-z]+.*"
        if self.ends_with.get():
            regex += re.escape(self.ends_with.get()) + "$"
        else:
            regex += ".*"
        if self.extension.get():
            ext = self.extension.get()
            if not ext.startswith("."):
                ext = "." + ext
            regex += re.escape(ext) + "$"
        flags = ""
        if self.ignore_case.get():
            flags = "(?i)"
        self.result_pattern = f"/{flags}{regex}/"

class PatternDestDialog(simpledialog.Dialog):
    """
    Dialog for adding or editing a pattern/destination mapping.
    Provides a clean, user-friendly layout that resizes intelligently.
    Includes buttons for pattern builders.
    """
    def __init__(self, parent, title, template_dir, destinations, initial_pattern=None, initial_dest=None):
        self.pattern = None
        self.dest = None
        self.template_dir = template_dir
        self.destinations = destinations
        self.initial_pattern = initial_pattern
        self.initial_dest = initial_dest
        super().__init__(parent, title)

    def body(self, master):
        # Create a content frame with padding that will hold all widgets
        content_frame = ttk.Frame(master, padding=(16, 16, 16, 8))
        content_frame.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # --- Pattern row with builder buttons ---
        ttk.Label(content_frame, text="Pattern:").grid(row=0, column=0, sticky="w", pady=(0, 8))
        pattern_row = ttk.Frame(content_frame)
        pattern_row.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        pattern_row.grid_columnconfigure(0, weight=1)
        self.pattern_entry = ttk.Entry(pattern_row)
        self.pattern_entry.grid(row=0, column=0, sticky="ew")
        builder_btn = ttk.Button(pattern_row, text="Pattern Builder...", command=self._open_pattern_builder)
        builder_btn.grid(row=0, column=1, padx=(5, 0))
        adv_builder_btn = ttk.Button(pattern_row, text="Advanced...", command=self._open_advanced_pattern_builder)
        adv_builder_btn.grid(row=0, column=2, padx=(5, 0))
        self.pattern_entry.insert(0, self.initial_pattern or "")
        self.pattern_entry.focus_set()

        # --- Destination ---
        ttk.Label(content_frame, text="Destination:").grid(row=1, column=0, sticky="w", pady=(0, 8))
        self.dest_combo = ttk.Combobox(content_frame, values=self.destinations, state="readonly")
        self.dest_combo.grid(row=1, column=1, sticky="ew", pady=(0, 8))
        if self.initial_dest:
            self.dest_combo.set(self.initial_dest)
        elif self.destinations:
            self.dest_combo.set(self.destinations[0])

        # --- Help Text ---
        info = (
            "Tip: Use * as a wildcard, or use the Pattern Builder for help.\n"
            "Advanced: Use slashes /.../ for regex patterns (e.g. /Invoice_\\d+\\.pdf/)."
        )
        info_label = ttk.Label(content_frame, text=info, foreground="#666", font=("Segoe UI", 9), anchor="w", justify="left")
        info_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

        # --- Resizing Logic ---
        self.resizable(True, False)
        dest = self.initial_dest if self.initial_dest else (self.destinations[0] if self.destinations else "")
        min_width = 450
        width = max(min_width, 8 * len(dest) + 150)
        height = 190
        self.after(10, lambda: self.geometry(f"{width}x{height}"))

        return self.pattern_entry

    def _open_pattern_builder(self):
        dlg = PatternBuilderDialog(self, "Pattern Builder")
        if dlg.result_pattern:
            self.pattern_entry.delete(0, tk.END)
            self.pattern_entry.insert(0, dlg.result_pattern)

    def _open_advanced_pattern_builder(self):
        dlg = AdvancedPatternBuilderDialog(self, "Advanced Pattern Builder")
        if dlg.result_pattern:
            self.pattern_entry.delete(0, tk.END)
            self.pattern_entry.insert(0, dlg.result_pattern)

    def validate(self):
        """
        Validate user input before closing the dialog.
        """
        pattern = self.pattern_entry.get().strip()
        dest = self.dest_combo.get().strip()
        if not pattern:
            messagebox.showerror("Error", "Please enter a pattern.", parent=self)
            return False
        if not dest:
            messagebox.showerror("Error", "Please select a destination.", parent=self)
            return False
        return True

    def apply(self):
        """
        Save the dialog results.
        """
        self.pattern = self.pattern_entry.get().strip()
        self.dest = self.dest_combo.get().strip()

# Simple tooltip helper for user-friendliness
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack(ipadx=4, ipady=2)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()