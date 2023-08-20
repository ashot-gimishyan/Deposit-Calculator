import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import time

def calculate_interest():
    principal = float(principal_entry.get())
    annual_interest_rate = float(annual_interest_rate_entry.get()) / 100
    frequency = frequency_combobox.get()

    if frequency == "Yearly":
        periods_per_year = 1
    elif frequency == "Monthly":
        periods_per_year = 12
    elif frequency == "Quarterly":
        periods_per_year = 4

    years = []
    amounts = []

    year = 0
    amount = principal

    while amount < 1000000:
        years.append(year)
        amounts.append(amount)
        amount += amount * (annual_interest_rate / periods_per_year)
        year += 1

    plot_graph(years, amounts)

def plot_graph(years, amounts):
    graph_ax.clear()
    graph_ax.plot(years, amounts, marker='o', linestyle='-', color='b', label='Amount')
    graph_ax.set_xlabel("Years")
    graph_ax.set_ylabel("Amount")
    graph_ax.set_title("Compound Interest Growth")
    graph_ax.legend()
    graph_canvas.draw()

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"Year: {int(sel.target[0])}\nAmount: {sel.target[1]:.2f}"))

def save_graph():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        graph_fig.savefig(file_path, dpi=100)
        messagebox.showinfo("Saved", "Graph has been saved successfully.")

def animate_growth():
    principal = float(principal_entry.get())
    annual_interest_rate = float(annual_interest_rate_entry.get()) / 100
    years = []
    amounts = []

    year = 0
    amount = principal

    while amount < 1000000:
        years.append(year)
        amounts.append(amount)
        amount += amount * annual_interest_rate
        year += 1
        plot_graph(years, amounts)
        graph_canvas.draw()
        time.sleep(1)  # Задержка в секундах

app = tk.Tk()
app.title("Compound Interest Calculator")

frame = ttk.Frame(app, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

principal_label = ttk.Label(frame, text="Initial Deposit:")
principal_label.grid(row=0, column=0, sticky=tk.W)
principal_entry = ttk.Entry(frame)
principal_entry.grid(row=0, column=1)

annual_interest_rate_label = ttk.Label(frame, text="Annual Interest Rate (%):")
annual_interest_rate_label.grid(row=1, column=0, sticky=tk.W)
annual_interest_rate_entry = ttk.Entry(frame)
annual_interest_rate_entry.grid(row=1, column=1)

frequency_label = ttk.Label(frame, text="Interest Frequency:")
frequency_label.grid(row=2, column=0, sticky=tk.W)
frequency_var = tk.StringVar(value="Yearly")
frequency_combobox = ttk.Combobox(frame, textvariable=frequency_var, values=["Yearly", "Monthly", "Quarterly"])
frequency_combobox.grid(row=2, column=1)

calculate_button = ttk.Button(frame, text="Calculate", command=calculate_interest)
calculate_button.grid(row=3, columnspan=2)

save_button = ttk.Button(frame, text="Save Graph", command=save_graph)
save_button.grid(row=5, columnspan=2)

# Matplotlib setup
graph_frame = ttk.Frame(app, padding=10)
graph_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

graph_fig = Figure(figsize=(6, 4), dpi=100)
graph_ax = graph_fig.add_subplot(111)
graph_canvas = FigureCanvasTkAgg(graph_fig, master=graph_frame)
graph_canvas.get_tk_widget().pack()

app.mainloop()
