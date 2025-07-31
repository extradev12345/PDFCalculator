import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import webbrowser

import PyPDF2

def count_pages_in_folder(folder_path):
    total_pages = 0
    file_details = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    total_pages += num_pages
                    file_details.append((filename, num_pages))
            except Exception as e:
                file_details.append((filename, f"Error: {e}"))
    return total_pages, file_details

class PDFCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDFCalculator tool")
        self.root.geometry("576x640")
        self.root.resizable(False, False)
        self.root.configure(padx=15, pady=15, bg='#1e1e2f')
        try:
            self.root.iconbitmap('docs/pdc.ico')
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")


        self.style = ttk.Style()
        self._apply_theme()

        # --- Header ---
        header = tk.Label(root, text="📄 PDFCalculator - Printer Cost & Page Counter", 
                          font=("Segoe UI", 16, "bold"), bg='#1e1e2f', fg='#f0f0f5')
        header.grid(row=0, column=0, columnspan=3, pady=(0,15), sticky='ew')

        # Folder selection
        ttk.Label(root, text="Select PDF Folder:", background='#1e1e2f', foreground='#d4d4dc').grid(row=1, column=0, sticky='w')
        self.folder_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.folder_var, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(root, text="Browse", command=self.browse_folder).grid(row=1, column=2)

        # Total pages label
        self.page_label = ttk.Label(root, text="Total Pages: 0")
        self.page_label.grid(row=2, column=0, columnspan=3, sticky='w', pady=10)

        # Price per sheet
        ttk.Label(root, text="Price per Sheet:", background='#1e1e2f', foreground='#d4d4dc').grid(row=3, column=0, sticky='w')
        self.price_var = tk.DoubleVar(value=0.0)
        ttk.Entry(root, textvariable=self.price_var, width=10).grid(row=3, column=1, sticky='w')

        # Duplex printing option
        self.duplex_var = tk.BooleanVar()
        ttk.Checkbutton(root, text="Print on Both Sides (Duplex)", variable=self.duplex_var).grid(row=4, column=0, columnspan=2, sticky='w')

        # Pages per sheet spinbox
        ttk.Label(root, text="Pages per Sheet:", background='#1e1e2f', foreground='#d4d4dc').grid(row=5, column=0, sticky='w')
        self.pages_per_sheet = tk.IntVar(value=1)
        ttk.Spinbox(root, from_=1, to=16, textvariable=self.pages_per_sheet, width=5).grid(row=5, column=1, sticky='w')

        # Calculate cost button
        ttk.Button(root, text="Calculate Cost", command=self.calculate_cost).grid(row=6, column=2, pady=10)
        self.cost_label = ttk.Label(root, text="Estimated Cost: $0.00")
        self.cost_label.grid(row=6, column=0, columnspan=2, sticky='w')

        # Treeview for file listing
        self.tree = ttk.Treeview(root, columns=('Filename', 'Pages'), show='headings', height=15)
        self.tree.heading('Filename', text='Filename')
        self.tree.heading('Pages', text='Pages')
        self.tree.column('Filename', width=440)
        self.tree.column('Pages', width=100, anchor='center')
        self.tree.grid(row=7, column=0, columnspan=3, pady=10)

        # Footer branding
        footer = tk.Label(root, text="© 2025 Minius Lab — PDFCalculator", font=("Segoe UI", 9), bg='#1e1e2f', fg='#606070')
        footer.grid(row=8, column=0, columnspan=3, pady=(10,0), sticky='ew')

        import webbrowser

        # Inside __init__, after footer label creation
        doc_link = tk.Label(root, text="📖 Documentation", fg="#4ea1d3", bg='#1e1e2f', cursor="hand2", font=("Segoe UI", 10, "underline"))
        doc_link.grid(row=9, column=0, columnspan=3, sticky='w', pady=(5,0))
        doc_link.bind("<Button-1>", lambda e: self.open_docs())

        # Add this method to PDFCalculatorApp
        def open_docs(self):
            import os
            docs_path = os.path.abspath("docs/index.html")
            if os.path.exists(docs_path):
                webbrowser.open(f"file://{docs_path}")
            else:
                messagebox.showerror("Error", "Documentation file not found.\nExpected at:\n" + docs_path)


        # About Menu
        menubar = tk.Menu(root)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Documentation", command=self.opendocs)
        helpmenu.add_command(label="About PDFCalculator", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        root.config(menu=menubar)

    def _apply_theme(self):
        # Dark theme with pastel blue accent
        self.style.theme_use('clam')
        self.style.configure('.', background='#1e1e2f', foreground='#d4d4dc', fieldbackground='#252535', font=('Segoe UI', 10))
        self.style.configure('Treeview', background='#252535', foreground='#d4d4dc', fieldbackground='#252535', font=('Segoe UI', 9))
        self.style.map('Treeview', background=[('selected', '#3a3a5a')], foreground=[('selected', '#f0f0f5')])
        self.style.configure('TButton', background='#3a3a5a', foreground='#f0f0f5')
        self.style.map('TButton', background=[('active', '#5a5a80')])
        self.style.configure('TCheckbutton', background='#1e1e2f', foreground='#d4d4dc')
        self.style.configure('TLabel', background='#1e1e2f', foreground='#d4d4dc')

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_var.set(folder_path)
            self.total_pages, file_details = count_pages_in_folder(folder_path)
            self.page_label.config(text=f"Total Pages: {self.total_pages}")
            self.tree.delete(*self.tree.get_children())
            for file, pages in file_details:
                self.tree.insert('', 'end', values=(file, pages))

    def calculate_cost(self):
        try:
            pps = self.pages_per_sheet.get()
            duplex = self.duplex_var.get()
            price = self.price_var.get()

            if pps < 1:
                messagebox.showwarning("Warning", "Pages per sheet must be at least 1.")
                return

            sheets = self.total_pages / pps
            if duplex:
                sheets = sheets / 2

            sheets = int(sheets) + (0 if sheets.is_integer() else 1)
            cost = price * sheets

            self.cost_label.config(text=f"Estimated Cost: ${cost:.2f} for {sheets} sheets")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {e}")

    def opendocs(self):
        webbrowser.open('docs/index.html')

    def show_about(self):
        about_text = (
            "PDFCalculator v1.0\n"
            "Developed by Minius Lab © 2025\n\n"
            "Features:\n"
            "- Count total pages in PDFs inside a selected folder\n"
            "- Calculate printing cost based on price per sheet\n"
            "- Support duplex (double-sided) printing\n"
            "- Set pages per sheet for optimized printing\n\n"
            "For any queries, visit: https://miniuslab.com\n"
        )
        messagebox.showinfo("About PDFCalculator", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCalculatorApp(root)
    root.mainloop()
