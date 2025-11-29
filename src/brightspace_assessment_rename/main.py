"""Main entry point for the Brightspace Assessment Rename application."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from .renamer import FileRenamer


class Application(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        
        self.title("Brightspace Assessment Rename")
        self.geometry("600x400")
        self.minsize(500, 350)
        
        self.renamer = FileRenamer()
        self.selected_folder: Path | None = None
        
        self._create_widgets()
        self._create_layout()
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Header
        self.header_label = ttk.Label(
            self,
            text="Brightspace Assessment File Renamer",
            font=("Segoe UI", 14, "bold")
        )
        
        # Folder selection frame
        self.folder_frame = ttk.LabelFrame(self, text="Select Folder", padding=10)
        self.folder_path_var = tk.StringVar(value="No folder selected")
        self.folder_label = ttk.Label(
            self.folder_frame,
            textvariable=self.folder_path_var,
            wraplength=450
        )
        self.browse_button = ttk.Button(
            self.folder_frame,
            text="Browse...",
            command=self._browse_folder
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview", padding=10)
        self.preview_text = tk.Text(
            self.preview_frame,
            height=10,
            width=60,
            state="disabled",
            font=("Consolas", 9)
        )
        self.scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient="vertical",
            command=self.preview_text.yview
        )
        self.preview_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Action buttons
        self.button_frame = ttk.Frame(self)
        self.preview_button = ttk.Button(
            self.button_frame,
            text="Preview Changes",
            command=self._preview_changes,
            state="disabled"
        )
        self.rename_button = ttk.Button(
            self.button_frame,
            text="Rename Files",
            command=self._rename_files,
            state="disabled"
        )
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w"
        )
    
    def _create_layout(self):
        """Arrange widgets in the window."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        # Header
        self.header_label.grid(row=0, column=0, pady=(10, 5), padx=10)
        
        # Folder selection
        self.folder_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.folder_frame.columnconfigure(0, weight=1)
        self.folder_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.browse_button.grid(row=0, column=1)
        
        # Preview
        self.preview_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Buttons
        self.button_frame.grid(row=3, column=0, pady=10)
        self.preview_button.pack(side="left", padx=5)
        self.rename_button.pack(side="left", padx=5)
        
        # Status bar
        self.status_bar.grid(row=4, column=0, sticky="ew", padx=5, pady=(0, 5))
    
    def _browse_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(title="Select folder with files to rename")
        if folder:
            self.selected_folder = Path(folder)
            self.folder_path_var.set(str(self.selected_folder))
            self.preview_button.configure(state="normal")
            self.rename_button.configure(state="disabled")
            self._clear_preview()
            self.status_var.set(f"Selected: {self.selected_folder.name}")
    
    def _clear_preview(self):
        """Clear the preview text area."""
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.configure(state="disabled")
    
    def _preview_changes(self):
        """Show preview of file renames."""
        if not self.selected_folder:
            return
        
        changes = self.renamer.get_rename_preview(self.selected_folder)
        
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        
        if not changes:
            self.preview_text.insert("end", "No files found or no changes needed.")
            self.status_var.set("No changes to make")
        else:
            for old_name, new_name in changes:
                if old_name != new_name:
                    self.preview_text.insert("end", f"• {old_name}\n")
                    self.preview_text.insert("end", f"  → {new_name}\n\n")
            
            change_count = sum(1 for old, new in changes if old != new)
            self.status_var.set(f"Found {change_count} file(s) to rename")
            
            if change_count > 0:
                self.rename_button.configure(state="normal")
        
        self.preview_text.configure(state="disabled")
    
    def _rename_files(self):
        """Execute the file renaming operation."""
        if not self.selected_folder:
            return
        
        confirm = messagebox.askyesno(
            "Confirm Rename",
            "Are you sure you want to rename the files?\n\n"
            "This action cannot be undone automatically."
        )
        
        if confirm:
            try:
                count = self.renamer.rename_files(self.selected_folder)
                messagebox.showinfo(
                    "Success",
                    f"Successfully renamed {count} file(s)."
                )
                self.status_var.set(f"Renamed {count} file(s)")
                self._preview_changes()  # Refresh preview
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
                self.status_var.set("Error during rename")


def main():
    """Run the application."""
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
