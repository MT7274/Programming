# Martin Tran, Student Number: 32084076
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = None
selected_file = None
summary_dict = None

root = tk.Tk()
root.title("Martin Tran 32084076")

root.geometry("450x250")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

def browse_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        global selected_file
        selected_file = file_path

def upload_file():
    global data, summary_dict
    if selected_file:
        try:
            data = pd.read_csv(selected_file)

            required_columns = ['Department', 'Gender', 'Age', 'DistanceFromHome', 'HourlyRate', 'MaritalStatus', 'WorkLifeBalance', 'Attrition']
            if not all(col in data.columns for col in required_columns):
                messagebox.showerror("Error", "Missing required columns in the dataset.")
                data = None
                return

            summary_dict = {
                "Total Employees": len(data),
                "Unique Departments": ', '.join(data['Department'].unique()),
                "Employees per Department": data['Department'].value_counts().to_dict(),
                "Gender Count": data['Gender'].value_counts().to_dict(),
                "Age": {
                    "Minimum": int(data['Age'].min()),
                    "Maximum": int(data['Age'].max()),
                    "Average": round(data['Age'].mean(), 2)
                },
                "Distance From Home": {
                    "Minimum": int(data['DistanceFromHome'].min()),
                    "Maximum": int(data['DistanceFromHome'].max()),
                    "Average": round(data['DistanceFromHome'].mean(), 2)
                },
                "Hourly Rate": {
                    "Minimum": int(data['HourlyRate'].min()),
                    "Maximum": int(data['HourlyRate'].max()),
                    "Average": round(data['HourlyRate'].mean(), 2)
                },
                "Marital Status Percentages": (
                    data['MaritalStatus'].value_counts(normalize=True) * 100
                ).round(2).to_dict(),
                "Average Work Life Balance": round(data['WorkLifeBalance'].mean(), 2),
                "Total Attritions": int(data['Attrition'].value_counts().get('Yes', 0))
            }

            messagebox.showinfo("Upload Status", f"File '{selected_file}' uploaded and summary generated successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
    else:
        messagebox.showerror("Error", "No file selected")

def visualise_pie_chart():
    if data is None:
        messagebox.showerror("Error", "No data loaded")

    employee_amount = data['Department'].value_counts()

    if employee_amount.isnull().any() or (employee_amount == 0).any():
        messagebox.showerror("Error", "Data invalid")
        return

    pie_window = tk.Toplevel(root)
    pie_window.title("Employees Per Department")

    pie_window.geometry("600x600")
    pie_window.resizable(False, False)

    def absolute_value(val):
        total = sum(employee_amount)
        count = int(round(val * total / 100.0))
        return f'{count}'

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(employee_amount, labels=employee_amount.index, autopct=absolute_value, startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')

    pieCanvas = FigureCanvasTkAgg(fig, master=pie_window)
    pieCanvas.draw()
    pieCanvas.get_tk_widget().pack(pady=20)

    plt.close(fig)

def visualise_bar_graph():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return

    if 'MaritalStatus' not in data.columns:
        messagebox.showerror("Error", "Required column not found in file")
        return

    employee_amount = data['MaritalStatus'].value_counts()

    if employee_amount.empty:
        messagebox.showerror("Error", "Data invalid")
        return

    bar_window = tk.Toplevel(root)
    bar_window.title("Marital Status")
    bar_window.geometry("700x500")
    bar_window.resizable(False, False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(employee_amount.index, employee_amount.values, color='skyblue', edgecolor="black")

    ax.set_title("Marital Status")
    ax.set_xlabel("Marital Status")
    ax.set_ylabel("Number of Employees")
    plt.xticks(rotation=45)
    plt.tight_layout()

    barCanvas = FigureCanvasTkAgg(fig, master=bar_window)
    barCanvas.draw()
    barCanvas.get_tk_widget().pack(pady=20)

    plt.close(fig)

def visualise_bar_plot():
    if data is None:
        messagebox.showerror("Error", "No data loaded")
        return

    if 'MaritalStatus' not in data.columns:
        messagebox.showerror("Error", "Required column not found in file")
        return

    employee_amount = data['MaritalStatus'].value_counts()

    if employee_amount.empty:
        messagebox.showerror("Error", "Data invalid")
        return

    bar_window = tk.Toplevel(root)
    bar_window.title("Marital Status")
    bar_window.geometry("700x500")
    bar_window.resizable(False, False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(employee_amount.index, employee_amount.values, color='skyblue', edgecolor="black")

    ax.set_title("Marital Status")
    ax.set_xlabel("Marital Status")
    ax.set_ylabel("Number of Employees")
    plt.xticks(rotation=45)
    plt.tight_layout()

    barCanvas = FigureCanvasTkAgg(fig, master=bar_window)
    barCanvas.draw()
    barCanvas.get_tk_widget().pack(pady=20)

    plt.close(fig)

def view_dashboard_summary():
    if summary_dict is None:
        messagebox.showerror("Error", "No summary available. Upload File")
        return

    summary_window = tk.Toplevel(root)
    summary_window.title("Data Summary")
    summary_window.geometry("500x600")
    summary_window.resizable(True, True)

    tk.Label(summary_window, text="Data Summary", font=("Arial", 16, "bold")).pack(pady=10)

    text_widget = tk.Text(summary_window, wrap="word", font=("Arial", 10))
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    for key, value in summary_dict.items():
        if isinstance(value, dict):
            text_widget.insert("end", f"{key}:\n")
            for subkey, subval in value.items():
                text_widget.insert("end", f"  {subkey}: {subval}\n")
            text_widget.insert("end", "\n")
        else:
            text_widget.insert("end", f"{key}:\n{value}\n\n")

    text_widget.config(state="disabled")

def export_dashboard_summary():
    if summary_dict is None:
        messagebox.showerror("Error", "No summary available")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save Summary As")

    if file_path:
        try:
            with open(file_path, "w") as f:
                for key, value in summary_dict.items():
                    f.write(f"{key}:\n")
                    if isinstance(value, dict):
                        for subkey, subval in value.items():
                            f.write(f"  {subkey}: {subval}\n")
                    else:
                        f.write(f"{value}\n")
                    f.write("\n")
                messagebox.showinfo("Success", f"Summary exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {e}")

# File upload
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.grid(row=2, column=1, padx=10, pady=5, sticky='e')

file_label = tk.Label(root, text="No file selected", font=("Arial", 10), anchor='w', justify='left', wraplength=400)
file_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

browse_button = tk.Button(root, text="Browse File", command=browse_file)
browse_button.grid(row=1, column=1, padx=10, pady=10, sticky='e')

# Frame
control_frame = tk.Frame(root)
control_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Grid
control_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(1, weight=1)

#  Pie Chart
tk.Label(control_frame, text='Departments:', font=("Arial", 10)).grid(row=0, column=0, sticky='w')
tk.Button(control_frame, text="Pie Chart", font=("Arial", 10), command=visualise_pie_chart).grid(row=0, column=1, sticky='w')

# Bar Graph
tk.Label(control_frame, text='Marital Status:', font=("Arial", 10)).grid(row=1, column=0, sticky='w')
tk.Button(control_frame, text="Bar Graph", font=("Arial", 10), command=visualise_bar_graph).grid(row=1, column=1, sticky='w')

# Summary and ExportDashboard
tk.Label(control_frame, text='Dashboard Summary:', font=("Arial", 10)).grid(row=2, column=0, sticky='w')

tk.Button(control_frame, text="View summary", font=("Arial", 10), command=view_dashboard_summary).grid(row=2, column=1, sticky='w')
tk.Button(control_frame, text="Export Summary", font=("Arial", 10), command=export_dashboard_summary).grid(row=3, column=1, sticky='w')

# Window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.update_idletasks()

root.mainloop()