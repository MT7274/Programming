import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

data = None
selected_file = None

root = tk.Tk()
root.title("Simple Tkinter GUI")

root.geometry("550x350")

greeting_label = tk.Label(root, text="Hello", font=("Arial", 14))
greeting_label.grid(row=0, column=0, padx=10)

def on_button_click():
    messagebox.showinfo("Greeting", "Greets")

greeting_button = tk.Button(root, text="Click", command=on_button_click)
greeting_button.grid(row=0, column=1, padx=10)

def browse_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        global selected_file
        selected_file = file_path

def upload_file():
    global data
    if selected_file:
        data = pd.read_csv(selected_file)
        messagebox.showinfo("Upload Status", f"File '{selected_file} uploaded successfully")
    else:
        messagebox.showerror("Error", "No file selected")

def visualise_pie_chart():
    if data is None:
        messagebox.showerror("Error", "No data loaded")

    employeeAmount = data['Department'].value_counts()

    if employeeAmount.isnull().any() or (employeeAmount == 0).any():
        messagebox.showerror("Error", "Data invalid")
        return

    pie_window = tk.Toplevel(root)
    pie_window.title("Pie Chart")

    pie_window.geometry("600x600")
    pie_window.resizable(False, False)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(employeeAmount, labels=employeeAmount.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

    ax.axis('equal')

    plt.show()

pie_label = tk.Label(root, text='Click for pie chart:', font=("Arial", 10))
pie_label.grid(row=3, column=0, padx=10, pady=10)

pie_button = tk.Button(root, text="Pie Chart", font=("Arial", 10), command=visualise_pie_chart)
pie_button.grid(row=3, column=1, padx=10, pady=10)

upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

file_label = tk.Label(root, text="No file selected", font=("Arial", 14))
file_label.grid(row=1, column=0, padx=10, pady=10)

browse_button = tk.Button(root, text="Browse File", command=browse_file)
browse_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()