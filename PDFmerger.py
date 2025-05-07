import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Frame, Listbox, END, SINGLE
from PyPDF2 import PdfWriter

class PDFMergerMobileUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("360x640")
        self.root.configure(bg="#f0f0f0")

        self.files = []

        self.frame = Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=10, padx=20, fill="both", expand=True)

        Label(self.frame, text="📄 Select PDF Files", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)

        Button(self.frame, text="Browse PDFs", font=("Helvetica", 14), bg="#4CAF50", fg="white",
               height=2, command=self.select_files).pack(pady=5, fill="x")

        self.file_listbox = Listbox(self.frame, font=("Helvetica", 12), selectmode=SINGLE, height=6)
        self.file_listbox.pack(pady=10, fill="x")

        # Reorder buttons
        Button(self.frame, text="⬆ Move Up", font=("Helvetica", 12), command=self.move_up).pack(pady=2, fill="x")
        Button(self.frame, text="⬇ Move Down", font=("Helvetica", 12), command=self.move_down).pack(pady=2, fill="x")

        Label(self.frame, text="📝 Merged File Name", font=("Helvetica", 14), bg="#f0f0f0").pack(pady=(20, 5))

        self.name_entry = Entry(self.frame, font=("Helvetica", 14), justify="center")
        self.name_entry.pack(pady=5, ipadx=10, ipady=8, fill="x")

        Button(self.frame, text="🔗 Merge PDFs", font=("Helvetica", 14), bg="#2196F3", fg="white",
               height=2, command=self.merge_pdfs).pack(pady=20, fill="x")

    def select_files(self):
        selected = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if selected:
            self.files = list(selected)
            self.update_listbox()

    def update_listbox(self):
        self.file_listbox.delete(0, END)
        for file in self.files:
            self.file_listbox.insert(END, os.path.basename(file))

    def move_up(self):
        index = self.file_listbox.curselection()
        if not index or index[0] == 0:
            return
        i = index[0]
        self.files[i - 1], self.files[i] = self.files[i], self.files[i - 1]
        self.update_listbox()
        self.file_listbox.select_set(i - 1)

    def move_down(self):
        index = self.file_listbox.curselection()
        if not index or index[0] == len(self.files) - 1:
            return
        i = index[0]
        self.files[i + 1], self.files[i] = self.files[i], self.files[i + 1]
        self.update_listbox()
        self.file_listbox.select_set(i + 1)

    def merge_pdfs(self):
        if not self.files:
            messagebox.showerror("Error", "Please select PDF files first.")
            return
        filename = self.name_entry.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please enter a name for the merged PDF.")
            return
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        merger = PdfWriter()
        try:
            for pdf in self.files:
                merger.append(pdf)
            merger.write(filename)
            merger.close()
            messagebox.showinfo("Success", f"{filename} created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge: {e}")

if __name__ == "__main__":
    root = Tk()
    app = PDFMergerMobileUI(root)
    root.mainloop()