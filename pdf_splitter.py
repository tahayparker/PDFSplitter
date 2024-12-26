import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz  # PyMuPDF for secure PDF handling
import hashlib
from pathlib import Path

class PDFSplitterApp:
    """Main application class for PDF Splitter"""
    
    def __init__(self, root):
        """Initialize the application with root window and styling"""
        self.root = root
        self.root.title("PDF Splitter")
        self.root.geometry("800x500")  # Set initial window size
        self.root.resizable(False, False)  # Prevent window resizing
        
        # Define color scheme for dark theme
        self.colors = {
            'bg_dark': '#1E1E1E',      # Main background
            'bg_lighter': '#252526',    # Input fields background
            'teal_accent': '#006D5B',   # Primary accent color
            'teal_hover': '#005647',    # Hover state color
            'text': '#E0E0E0',          # Primary text color
            'text_secondary': '#AAAAAA', # Secondary text color
            'border': '#333333'         # Border color
        }
        
        # Configure ttk styles for widgets
        self.style = ttk.Style()
        
        # Configure frame style with dark background
        self.style.configure('TFrame', 
                            background=self.colors['bg_dark'])
        
        # Configure button style
        self.style.configure('TButton', 
                            padding=8,
                            font=('Segoe UI', 11),
                            background=self.colors['teal_accent'],
                            foreground=self.colors['text'])
        
        # Configure label style
        self.style.configure('TLabel', 
                            font=('Segoe UI', 11),
                            padding=5,
                            background=self.colors['bg_dark'],
                            foreground=self.colors['text'])
        
        # Configure header label style
        self.style.configure('Header.TLabel', 
                            font=('Segoe UI', 18, 'bold'),
                            foreground=self.colors['teal_accent'],
                            background=self.colors['bg_dark'],
                            padding=10)
        
        # Configure entry field style
        self.style.configure('TEntry', 
                            padding=5,
                            fieldbackground=self.colors['bg_lighter'],
                            foreground=self.colors['text'])
        
        # Configure progress bar style
        self.style.configure('Horizontal.TProgressbar',
                            background=self.colors['teal_accent'],
                            troughcolor=self.colors['bg_lighter'])
        
        # Set main window background
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Create UI elements and center window
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        """Create and arrange all UI widgets"""
        
        # Create main outer frame
        outer_frame = ttk.Frame(self.root)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create centered container frame
        container_frame = ttk.Frame(outer_frame, padding="30")
        container_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create header section
        header_frame = ttk.Frame(container_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add main title
        header_label = ttk.Label(
            header_frame, 
            text="📄 PDF Splitter",
            style='Header.TLabel'
        )
        header_label.pack()
        
        # Add subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Split your PDF documents with ease",
            font=('Segoe UI', 10),
            foreground=self.colors['text_secondary']
        )
        subtitle_label.pack()

        # Define entry widget styling
        entry_style = {
            'bg': self.colors['bg_lighter'],
            'fg': self.colors['text'],
            'insertbackground': self.colors['teal_accent'],  # Cursor color
            'relief': 'flat',
            'highlightthickness': 1,
            'highlightcolor': self.colors['teal_accent'],    # Focus highlight
            'highlightbackground': self.colors['border'],    # Normal border
            'font': ('Segoe UI', 11)
        }

        # Helper function to create consistent buttons
        def create_button(parent, text, command):
            """Create a styled button with hover effects"""
            button = tk.Button(
                parent,
                text=text,
                command=command,
                bg=self.colors['teal_accent'],
                fg=self.colors['text'],
                font=('Segoe UI', 11),
                padx=15,
                pady=5,
                border=0,
                cursor='hand2'
            )
            return button

        # Helper function to create input rows with consistent styling
        def create_input_row(parent, label_text, entry_width=55, has_button=True):
            """Create a row with label, entry field, and optional button"""
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=10)
            
            # Container for row contents
            content_frame = ttk.Frame(frame)
            content_frame.pack(expand=True)
            
            # Create label
            label = ttk.Label(content_frame, text=label_text, width=12, anchor='e')
            label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Create entry field
            entry = tk.Entry(
                content_frame,
                width=entry_width,
                **entry_style
            )
            entry.pack(side=tk.LEFT, padx=(0, 15))
            
            # Add button if required
            if has_button:
                button = create_button(content_frame, "Browse", None)
                button.pack(side=tk.LEFT)
                # Add spacer for alignment
                spacer = ttk.Frame(content_frame, width=0)
                spacer.pack(side=tk.LEFT, expand=True)
            else:
                # Add spacer when no button
                spacer = ttk.Frame(content_frame)
                spacer.pack(side=tk.LEFT, expand=True)
            
            return frame, entry, button if has_button else None

        # Create input file selection row
        file_frame, self.input_entry, browse_btn = create_input_row(container_frame, "Input PDF File:")
        self.input_path = tk.StringVar()
        self.input_entry.configure(textvariable=self.input_path)
        browse_btn.configure(command=self.browse_input)
        # Add hover effects
        browse_btn.bind('<Enter>', lambda e: browse_btn.configure(bg=self.colors['teal_hover']))
        browse_btn.bind('<Leave>', lambda e: browse_btn.configure(bg=self.colors['teal_accent']))

        # Create output directory selection row
        output_frame, self.output_entry, browse_out_btn = create_input_row(container_frame, "Output Folder:")
        self.output_path = tk.StringVar()
        self.output_entry.configure(textvariable=self.output_path)
        browse_out_btn.configure(command=self.browse_output)
        # Add hover effects
        browse_out_btn.bind('<Enter>', lambda e: browse_out_btn.configure(bg=self.colors['teal_hover']))
        browse_out_btn.bind('<Leave>', lambda e: browse_out_btn.configure(bg=self.colors['teal_accent']))

        # Create pages per split input row
        pages_frame, self.pages_entry, _ = create_input_row(container_frame, "Pages per split:", entry_width=15, has_button=False)
        self.pages_var = tk.StringVar(value="1")
        self.pages_entry.configure(textvariable=self.pages_var)

        # Create split button section
        button_frame = ttk.Frame(container_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        button_container = ttk.Frame(button_frame)
        button_container.pack(anchor='center')
        
        # Create main split button
        self.split_button = create_button(
            button_container,
            "Split PDF",
            self.split_pdf
        )
        self.split_button.configure(
            font=('Segoe UI', 12, 'bold'),
            padx=30,
            pady=12
        )
        self.split_button.pack()
        
        # Add hover effects to split button
        self.split_button.bind('<Enter>', lambda e: self.split_button.configure(bg=self.colors['teal_hover']))
        self.split_button.bind('<Leave>', lambda e: self.split_button.configure(bg=self.colors['teal_accent']))

        # Create progress bar (hidden initially)
        self.progress_frame = ttk.Frame(container_frame)
        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            length=500,
            mode='determinate'
        )
        self.progress.pack(pady=10)

    def center_window(self):
        """Center the application window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def browse_input(self):
        """Open file dialog for selecting input PDF"""
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.input_path.set(filename)

    def browse_output(self):
        """Open directory dialog for selecting output folder"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_path.set(directory)

    def validate_pdf(self, file_path):
        """Validate if the file is a legitimate PDF"""
        try:
            # Check file size (reject if > 100MB)
            if os.path.getsize(file_path) > 100 * 1024 * 1024:
                return False, "File is too large (max 100MB)"

            # Check file extension
            if not file_path.lower().endswith('.pdf'):
                return False, "Not a PDF file"

            # Basic PDF validation
            doc = fitz.open(file_path)
            if not doc.is_pdf:
                doc.close()
                return False, "Invalid PDF format"
            doc.close()
            return True, "Valid PDF"

        except Exception as e:
            return False, str(e)

    def split_pdf(self):
        """Main function to split the PDF file"""
        input_path = self.input_path.get()
        output_dir = self.output_path.get()
        
        # Validate user inputs
        try:
            pages_per_split = int(self.pages_var.get())
            if pages_per_split <= 0:
                messagebox.showerror("Error", "Pages per split must be a positive number")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for pages per split")
            return

        if not input_path or not output_dir:
            messagebox.showerror("Error", "Please select input file and output directory")
            return

        # Validate input PDF
        is_valid, message = self.validate_pdf(input_path)
        if not is_valid:
            messagebox.showerror("Error", f"Invalid PDF file: {message}")
            return

        try:
            # Open and process PDF
            doc = fitz.open(input_path)
            total_pages = doc.page_count
            
            # Check if even split is possible
            if total_pages % pages_per_split != 0:
                remainder = total_pages % pages_per_split
                message = (f"The PDF has {total_pages} pages which cannot be evenly split into "
                          f"{pages_per_split}-page segments.\n\n"
                          f"The last PDF would have only {remainder} pages.\n\n"
                          f"Suggested splits that would work:\n")
                
                # Calculate possible split sizes
                suggestions = []
                for i in range(1, min(total_pages + 1, 21)):
                    if total_pages % i == 0:
                        suggestions.append(str(i))
                
                message += ", ".join(suggestions[:5])
                
                if not messagebox.askyesno("Warning", message + "\n\nDo you want to continue anyway?"):
                    doc.close()
                    return

            # Get base name for output files
            input_basename = os.path.splitext(os.path.basename(input_path))[0]
            
            # Quick check for any existing file
            first_output = os.path.join(output_dir, f'{input_basename}_1.pdf')
            if os.path.exists(first_output):
                if not messagebox.askyesno("Warning", 
                    "Files with similar names already exist in the output folder. Do you want to overwrite them?",
                    icon='warning'):
                    doc.close()
                    return
            
            # Show and configure progress bar
            self.progress_frame.pack(fill=tk.X, pady=10)
            self.progress['value'] = 0
            
            # Calculate total number of splits
            num_splits = (total_pages + pages_per_split - 1) // pages_per_split
            self.progress['maximum'] = num_splits
            
            # Process each split
            for i in range(0, total_pages, pages_per_split):
                # Create new PDF document
                new_doc = fitz.open()
                
                # Add pages to new document
                end_page = min(i + pages_per_split, total_pages)
                new_doc.insert_pdf(doc, from_page=i, to_page=end_page-1)
                
                # Generate output filename
                base_name = f'{input_basename}_{i//pages_per_split + 1}.pdf'
                output_path = os.path.join(output_dir, base_name)
                
                # Save the split document
                new_doc.save(output_path, garbage=3, deflate=True)
                new_doc.close()
                
                # Update progress
                self.progress['value'] += 1
                self.root.update()

            # Clean up and show success message
            doc.close()
            messagebox.showinfo("Success", "PDF split successfully!")
            self.progress_frame.pack_forget()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.progress_frame.pack_forget()

# Application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop() 