#!/usr/bin/env python3
"""
PDF Merger Tool
A professional desktop application to merge multiple PDF files into one.
Uses tkinter for GUI and pypdf for PDF processing.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List
import shutil
from pypdf import PdfReader, PdfWriter
import threading


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # File list
        self.pdf_files: List[str] = []
        
        # Create GUI elements
        self.create_widgets()
        
        # Configure drag and drop
        self.setup_drag_drop()
    
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="PDF Merger Tool", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.add_btn = ttk.Button(
            button_frame, 
            text="Add PDF Files", 
            command=self.add_pdf_files
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.remove_btn = ttk.Button(
            button_frame, 
            text="Remove Selected", 
            command=self.remove_selected,
            state='disabled'
        )
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_all,
            state='disabled'
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_up_btn = ttk.Button(
            button_frame, 
            text="Move Up", 
            command=self.move_up,
            state='disabled'
        )
        self.move_up_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_down_btn = ttk.Button(
            button_frame, 
            text="Move Down", 
            command=self.move_down,
            state='disabled'
        )
        self.move_down_btn.pack(side=tk.LEFT, padx=5)
        
        # File list frame
        list_frame = ttk.LabelFrame(main_frame, text="PDF Files (Drag and drop available if tkinterdnd2 is installed)", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for file list
        columns = ('#1', '#2', '#3')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.file_tree.heading('#1', text='Order')
        self.file_tree.heading('#2', text='File Name')
        self.file_tree.heading('#3', text='Size')
        
        # Configure column widths
        self.file_tree.column('#1', width=60, minwidth=50)
        self.file_tree.column('#2', width=400, minwidth=200)
        self.file_tree.column('#3', width=100, minwidth=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event
        self.file_tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Add PDF files to begin merging.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Merge button frame
        merge_frame = ttk.Frame(main_frame)
        merge_frame.grid(row=4, column=0, pady=(10, 0))
        
        self.merge_btn = ttk.Button(
            merge_frame, 
            text="Merge PDFs", 
            command=self.merge_pdfs,
            state='disabled'
        )
        self.merge_btn.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            # Try to import tkinterdnd2 for drag and drop support
            try:
                from tkinterdnd2 import DND_FILES, TkinterDnD
                # Check if the root window supports drag and drop
                if hasattr(self.root, 'drop_target_register'):
                    self.root.drop_target_register(DND_FILES)
                    self.root.dnd_bind('<<Drop>>', self.on_drop)
                    print("Drag and drop support enabled")
                else:
                    print("Drag and drop not available - tkinterdnd2 not properly initialized")
            except ImportError:
                print("tkinterdnd2 not available - drag and drop disabled")
            except Exception as e:
                print(f"Drag and drop setup failed: {e}")
                
        except Exception as e:
            print(f"Error setting up drag and drop: {e}")
    
    def on_drop(self, event):
        """Handle drag and drop files"""
        files = self.root.tk.splitlist(event.data)
        self.add_files_from_list(files)
    
    def add_pdf_files(self):
        """Add PDF files using file dialog"""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if files:
            self.add_files_from_list(files)
    
    def add_files_from_list(self, files):
        """Add files from a list of file paths"""
        added_count = 0
        for file_path in files:
            if file_path.lower().endswith('.pdf') and file_path not in self.pdf_files:
                self.pdf_files.append(file_path)
                self.add_file_to_tree(file_path)
                added_count += 1
        
        if added_count > 0:
            self.update_status(f"Added {added_count} PDF file(s). Total: {len(self.pdf_files)}")
            self.update_button_states()
        else:
            messagebox.showwarning("No Files Added", "No valid PDF files were added or files already exist in the list.")
    
    def add_file_to_tree(self, file_path):
        """Add a file to the treeview"""
        try:
            file_name = os.path.basename(file_path)
            file_size = self.get_file_size(file_path)
            order = len(self.file_tree.get_children()) + 1
            
            self.file_tree.insert('', 'end', values=(order, file_name, file_size))
        except Exception as e:
            print(f"Error adding file to tree: {e}")
    
    def get_file_size(self, file_path):
        """Get human readable file size"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"
    
    def on_selection_change(self, event):
        """Handle treeview selection change"""
        selection = self.file_tree.selection()
        self.update_button_states()
    
    def update_button_states(self):
        """Update button states based on current selection and file list"""
        has_files = len(self.pdf_files) > 0
        has_selection = len(self.file_tree.selection()) > 0
        
        self.remove_btn.config(state='normal' if has_selection else 'disabled')
        self.clear_btn.config(state='normal' if has_files else 'disabled')
        self.merge_btn.config(state='normal' if has_files else 'disabled')
        
        # Update move buttons based on selection
        if has_selection:
            selected_items = self.file_tree.selection()
            first_selected = min([self.file_tree.index(item) for item in selected_items])
            last_selected = max([self.file_tree.index(item) for item in selected_items])
            
            self.move_up_btn.config(state='normal' if first_selected > 0 else 'disabled')
            self.move_down_btn.config(state='normal' if last_selected < len(self.pdf_files) - 1 else 'disabled')
        else:
            self.move_up_btn.config(state='disabled')
            self.move_down_btn.config(state='disabled')
    
    def remove_selected(self):
        """Remove selected files from the list"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        # Get selected indices
        selected_indices = sorted([self.file_tree.index(item) for item in selection], reverse=True)
        
        # Remove from treeview and file list
        for index in selected_indices:
            self.file_tree.delete(self.file_tree.get_children()[index])
            del self.pdf_files[index]
        
        # Reorder the treeview
        self.reorder_treeview()
        self.update_button_states()
        self.update_status(f"Removed {len(selection)} file(s). Total: {len(self.pdf_files)}")
    
    def clear_all(self):
        """Clear all files from the list"""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all files?"):
            self.file_tree.delete(*self.file_tree.get_children())
            self.pdf_files.clear()
            self.update_button_states()
            self.update_status("All files cleared.")
    
    def move_up(self):
        """Move selected files up in the list"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        selected_indices = sorted([self.file_tree.index(item) for item in selection])
        
        # Check if we can move up
        if selected_indices[0] == 0:
            return
        
        # Move files up
        for index in selected_indices:
            # Swap in file list
            self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
        
        # Refresh treeview
        self.refresh_treeview()
        
        # Restore selection
        new_selection = []
        for index in selected_indices:
            new_selection.append(self.file_tree.get_children()[index - 1])
        self.file_tree.selection_set(new_selection)
        
        self.update_button_states()
    
    def move_down(self):
        """Move selected files down in the list"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        selected_indices = sorted([self.file_tree.index(item) for item in selection], reverse=True)
        
        # Check if we can move down
        if selected_indices[0] >= len(self.pdf_files) - 1:
            return
        
        # Move files down
        for index in selected_indices:
            # Swap in file list
            self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
        
        # Refresh treeview
        self.refresh_treeview()
        
        # Restore selection
        new_selection = []
        for index in selected_indices:
            new_selection.append(self.file_tree.get_children()[index + 1])
        self.file_tree.selection_set(new_selection)
        
        self.update_button_states()
    
    def reorder_treeview(self):
        """Reorder the treeview to match file list order"""
        self.file_tree.delete(*self.file_tree.get_children())
        for file_path in self.pdf_files:
            self.add_file_to_tree(file_path)
    
    def refresh_treeview(self):
        """Refresh the treeview display"""
        self.reorder_treeview()
    
    def merge_pdfs(self):
        """Merge PDF files in a separate thread"""
        if not self.pdf_files:
            messagebox.showwarning("No Files", "Please add PDF files first.")
            return
        
        # Ask for output file
        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        # Start merging in a separate thread
        thread = threading.Thread(target=self._merge_pdfs_thread, args=(output_file,))
        thread.daemon = True
        thread.start()
    
    def _merge_pdfs_thread(self, output_file):
        """Merge PDF files in a background thread"""
        try:
            # Update UI
            self.root.after(0, self.start_progress)
            self.root.after(0, lambda: self.update_status("Merging PDF files..."))
            
            # Create PDF writer
            writer = PdfWriter()
            
            # Process each PDF file
            for i, file_path in enumerate(self.pdf_files):
                try:
                    # Update progress
                    progress_text = f"Processing file {i+1}/{len(self.pdf_files)}: {os.path.basename(file_path)}"
                    self.root.after(0, lambda text=progress_text: self.update_status(text))
                    
                    # Read PDF file
                    reader = PdfReader(file_path)
                    
                    # Add all pages to writer
                    for page in reader.pages:
                        writer.add_page(page)
                    
                except Exception as e:
                    error_msg = f"Error processing {os.path.basename(file_path)}: {str(e)}"
                    self.root.after(0, lambda msg=error_msg: messagebox.showerror("Processing Error", msg))
                    return
            
            # Write merged PDF
            self.root.after(0, lambda: self.update_status("Writing merged PDF..."))
            with open(output_file, 'wb') as output:
                writer.write(output)
            
            # Success
            success_msg = f"Successfully merged {len(self.pdf_files)} PDF files into:\n{output_file}"
            self.root.after(0, lambda: self.stop_progress())
            self.root.after(0, lambda: self.update_status(f"Merge completed! {len(self.pdf_files)} files merged."))
            self.root.after(0, lambda: messagebox.showinfo("Success", success_msg))
            
            # Ask if user wants to open the file
            self.root.after(0, lambda: self.ask_open_file(output_file))
            
        except Exception as e:
            error_msg = f"Error merging PDFs: {str(e)}"
            self.root.after(0, lambda: self.stop_progress())
            self.root.after(0, lambda: self.update_status("Merge failed."))
            self.root.after(0, lambda: messagebox.showerror("Merge Error", error_msg))
    
    def ask_open_file(self, file_path):
        """Ask user if they want to open the merged file"""
        if messagebox.askyesno("Open File", "Do you want to open the merged PDF file?"):
            try:
                os.startfile(file_path)  # Windows
            except AttributeError:
                try:
                    os.system(f'open "{file_path}"')  # macOS
                except:
                    try:
                        os.system(f'xdg-open "{file_path}"')  # Linux
                    except:
                        messagebox.showinfo("Info", f"File saved to: {file_path}")
    
    def start_progress(self):
        """Start progress bar animation"""
        self.progress.start(10)
        self.merge_btn.config(state='disabled')
    
    def stop_progress(self):
        """Stop progress bar animation"""
        self.progress.stop()
        self.merge_btn.config(state='normal')
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)


def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = PDFMergerApp(root)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
    except tk.TclError as e:
        if "no display name" in str(e).lower() or "$display" in str(e).lower():
            print("Error: No display available. This application requires a graphical environment.")
            print("Please run this application on a system with a GUI (Windows, macOS, or Linux with desktop environment).")
            print("\nAlternative: You can use the command-line version below:")
            print_command_line_usage()
        else:
            print(f"Error starting application: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def print_command_line_usage():
    """Print command-line usage instructions"""
    print("\n" + "="*60)
    print("COMMAND-LINE PDF MERGER (Alternative)")
    print("="*60)
    print("""
If you need to merge PDFs via command line, you can use this simple Python script:

```python
from pypdf import PdfReader, PdfWriter
import sys

def merge_pdfs(output_path, pdf_files):
    writer = PdfWriter()
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)
    
    with open(output_path, 'wb') as output:
        writer.write(output)
    print(f"Successfully merged {len(pdf_files)} files into {output_path}")

# Usage:
# merge_pdfs("output.pdf", ["file1.pdf", "file2.pdf", "file3.pdf"])
```
""")


if __name__ == "__main__":
    main()