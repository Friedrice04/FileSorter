import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading

from src import sorter
from src.mapping_editor.editor import MappingEditor
from src import utils

# --- Constants ---
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
MAPPINGS_DIR = os.path.join(os.path.dirname(__file__), "mappings")
LAST_MAPPING_KEY = "last_mapping"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f)
    except Exception:
        pass

class FileSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")
        self.root.geometry("500x500")
        self.mapping_path = None
        self.deep_audit = tk.BooleanVar(value=False)
        self.settings = load_settings()
        self.root.minsize(300, 220)

        self._build_widgets()
        self._populate_mappings()

    def _show_help(self):
        message = (
            "File Sorter Help\n\n"
            "This tool sorts files into folders based on patterns defined in a mapping file.\n\n"
            "Folders to Sort:\n"
            "- Add one or more folders to the list. Each will be sorted according to the mapping.\n"
            "- You can drag and drop folders from Explorer into the list below to add them quickly.\n\n"
            "Deep Audit:\n"
            "When enabled, after sorting, the tool will recursively scan for misplaced files and move them to the correct folders.\n\n"
            "Use the Mapping Editor to create or modify mapping files.\n"
        )
        messagebox.showinfo("Help - File Sorter", message)

    def _build_widgets(self):
        mapping_frame = ttk.LabelFrame(self.root, text="Mapping File")
        mapping_frame.pack(fill="x", padx=10, pady=5)

        self.mapping_combo = ttk.Combobox(mapping_frame, state="readonly")
        self.mapping_combo.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.mapping_combo.bind("<<ComboboxSelected>>", self._on_mapping_selected)
        utils.ToolTip(self.mapping_combo, "Select a mapping file to use for sorting.")

        edit_btn = ttk.Button(mapping_frame, text="Edit/Create Mapping", command=self._open_mapping_editor)
        edit_btn.pack(side="left", padx=5)
        utils.ToolTip(edit_btn, "Open the mapping editor to create or modify mapping files.")

        folder_frame = ttk.LabelFrame(self.root, text="Folders to Sort (Drag folders here or use Add Folder...)")
        folder_frame.pack(fill="both", expand=True, padx=10, pady=5)

        listbox_frame = ttk.Frame(folder_frame)
        listbox_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        self.folder_listbox = tk.Listbox(listbox_frame, selectmode=tk.EXTENDED, bg="#ffffff")
        self.folder_listbox.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.folder_listbox.drop_target_register(DND_FILES)
        self.folder_listbox.dnd_bind('<<Drop>>', self._on_drop_folders)

        self.watermark_label = tk.Label(
            self.folder_listbox, text="FileSorter", font=("Arial", 16, "bold"), fg="#cccccc", bg="#ffffff"
        )
        self._update_watermark()

        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)
        self.folder_listbox.lift()

        button_frame = ttk.Frame(folder_frame)
        button_frame.pack(side="left", fill="y", padx=5, pady=5)

        add_folder_btn = ttk.Button(button_frame, text="Add Folder...", command=self._add_folder)
        add_folder_btn.pack(fill="x", pady=(0, 5))
        utils.ToolTip(add_folder_btn, "Add a folder to the list to be sorted.")

        remove_folder_btn = ttk.Button(button_frame, text="Remove Selected", command=self._remove_selected_folders)
        remove_folder_btn.pack(fill="x")
        utils.ToolTip(remove_folder_btn, "Remove selected folders from the list.")

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        folder_frame.rowconfigure(0, weight=1)
        folder_frame.columnconfigure(0, weight=1)

        deep_chk = ttk.Checkbutton(self.root, text="Deep Audit", variable=self.deep_audit)
        deep_chk.pack(padx=10, anchor="w")
        utils.ToolTip(deep_chk, "If checked, recursively move misplaced files to their correct folders after sorting.")

        button_row = ttk.Frame(self.root)
        button_row.pack(fill="x", padx=10, pady=5)

        self.sort_btn = ttk.Button(button_row, text="Sort Files", command=self._start_sort_thread)
        self.sort_btn.pack(side="left")
        utils.ToolTip(self.sort_btn, "Start sorting files according to the selected options.")

        help_btn = ttk.Button(button_row, text="Help", command=self._show_help)
        help_btn.pack(side="right")
        utils.ToolTip(help_btn, "Show help and usage instructions.")

        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x", padx=10, pady=5)
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side="left")
        self.progress_bar = ttk.Progressbar(status_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.folder_listbox.bind("<Configure>", lambda e: self._update_watermark())

    def _update_watermark(self):
        if self.folder_listbox.size() == 0:
            self.watermark_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.watermark_label.place_forget()

    def _populate_mappings(self):
        if not os.path.exists(MAPPINGS_DIR):
            os.makedirs(MAPPINGS_DIR)
        mapping_files = [f for f in os.listdir(MAPPINGS_DIR) if f.endswith(".json")]
        self.mapping_combo['values'] = mapping_files

        last_mapping = self.settings.get(LAST_MAPPING_KEY)
        if mapping_files:
            if last_mapping and last_mapping in mapping_files:
                self.mapping_combo.set(last_mapping)
                self.mapping_path = os.path.join(MAPPINGS_DIR, last_mapping)
            else:
                self.mapping_combo.current(0)
                self.mapping_path = os.path.join(MAPPINGS_DIR, mapping_files[0])
        else:
            self.mapping_path = None

    def _on_mapping_selected(self, event=None):
        selected = self.mapping_combo.get()
        if selected:
            self.mapping_path = os.path.join(MAPPINGS_DIR, selected)
            self.settings[LAST_MAPPING_KEY] = selected
            save_settings(self.settings)

    def _add_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory(mustexist=True, title="Select Folder to Sort")
        if folder and folder not in self.folder_listbox.get(0, tk.END):
            self.folder_listbox.insert(tk.END, folder)
        self._update_watermark()

    def _on_drop_folders(self, event):
        paths = self.root.tk.splitlist(event.data)
        for folder in paths:
            folder = folder.strip('"')
            if os.path.isdir(folder) and folder not in self.folder_listbox.get(0, tk.END):
                self.folder_listbox.insert(tk.END, folder)
        self._update_watermark()

    def _remove_selected_folders(self):
        for idx in reversed(self.folder_listbox.curselection()):
            self.folder_listbox.delete(idx)
        self._update_watermark()

    def _open_mapping_editor(self):
        def on_save_callback():
            selected = os.path.basename(self.mapping_path)
            self.settings[LAST_MAPPING_KEY] = selected
            save_settings(self.settings)
            self._populate_mappings()
            self.mapping_combo.set(selected)
        MappingEditor(self.root, on_save_callback=on_save_callback, mapping_path=self.mapping_path)

    def _start_sort_thread(self):
        self.sort_btn.config(state="disabled")
        self.status_label.config(text="Starting sort...")
        self.progress_bar['value'] = 0
        thread = threading.Thread(target=self._sort_files, daemon=True)
        thread.start()

    def _sort_files(self):
        mapping_path = self.mapping_path
        folders = self.folder_listbox.get(0, tk.END)
        if not mapping_path or not os.path.isfile(mapping_path):
            utils.show_error("Please select a valid mapping file.")
            self.sort_btn.config(state="normal")
            return
        if not folders:
            utils.show_error("Please add at least one folder to sort.")
            self.sort_btn.config(state="normal")
            return

        try:
            sorter_obj = sorter.FileSorter(mapping_path)
            deep_audit = self.deep_audit.get()
            self.progress_bar['maximum'] = len(folders)
            for i, folder in enumerate(folders):
                if os.path.isdir(folder):
                    self.status_label.config(text=f"Sorting {os.path.basename(folder)}...")
                    sorter_obj.sort_current_directory(folder)
                    if deep_audit:
                        self.status_label.config(text=f"Auditing {os.path.basename(folder)}...")
                        sorter_obj.deep_audit_and_sort(folder)
                self.progress_bar['value'] = i + 1
                self.root.update_idletasks()
            messagebox.showinfo("Success", "Files sorted successfully!")
        except Exception as e:
            utils.show_error(f"An error occurred during sorting:\n{e}")
        finally:
            self.sort_btn.config(state="normal")
            self.status_label.config(text="Ready")
            self.progress_bar['value'] = 0

def main():
    root = TkinterDnD.Tk()
    FileSorterGUI(root)
    root.mainloop()