import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

class SearchApp(ttkb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Professional Search")
        self.geometry("600x400")
        self.minsize(400, 300)

        self.search_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="20 20 20 0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 20))

        # Search input
        self.search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            font=("Helvetica", 12),
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Search button
        search_button = ttk.Button(
            search_frame, 
            text="Enter",
            command=self.perform_search,
            style="Accent.TButton"
        )
        search_button.pack(side=tk.LEFT, padx=(10, 0))

        # Output frame
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)

        # Output box
        self.output_box = tk.Text(
            output_frame, 
            wrap=tk.WORD, 
            font=("Helvetica", 11),
            padx=10, 
            pady=10
        )
        self.output_box.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for output box
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_box.configure(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_var, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)

    def perform_search(self):
        query = self.search_var.get()
        if query:
            # Here you would typically perform the actual search
            # For this example, we'll just echo the search term
            results = f"Results would appear here."
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, results)
            self.status_var.set(f"Search completed for: {query}")
        else:
            self.status_var.set("Please enter a search term")

if __name__ == "__main__":
    app = SearchApp()
    app.mainloop()