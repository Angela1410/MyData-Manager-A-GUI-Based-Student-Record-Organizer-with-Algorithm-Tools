import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json

student_records = []

def save_data():
    with open("students.json", "w") as file:
        json.dump(student_records, file)
    messagebox.showinfo("Saved", "Records saved!")

def load_data():
    global student_records
    try:
        with open("students.json", "r") as file:
            student_records = json.load(file)
        refresh_display()
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved file found.")

def add_record():
    name = simpledialog.askstring("Input", "Student Name:")
    student_id = simpledialog.askstring("Input", "Student ID:")
    grade = simpledialog.askfloat("Input", "Student Grade:")
    if name and student_id and grade is not None:
        student_records.append({"Name": name, "ID": student_id, "Grade": grade})
        refresh_display()

def edit_record():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        record = student_records[index]
        name = simpledialog.askstring("Edit", "New Name:", initialvalue=record["Name"])
        student_id = simpledialog.askstring("Edit", "New ID:", initialvalue=record["ID"])
        grade = simpledialog.askfloat("Edit", "New Grade:", initialvalue=record["Grade"])
        student_records[index] = {"Name": name, "ID": student_id, "Grade": grade}
        refresh_display()

def delete_record():
    selected = listbox.curselection()
    if selected:
        del student_records[selected[0]]
        refresh_display()

def refresh_display():
    listbox.delete(0, tk.END)
    for s in student_records:
        listbox.insert(tk.END, f"{s['Name']} | {s['ID']} | {s['Grade']}")

def bubble_sort(data, key):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j][key] > data[j+1][key]:
                data[j], data[j+1] = data[j+1], data[j]

def insertion_sort(data, key):
    for i in range(1, len(data)):
        temp = data[i]
        j = i - 1
        while j >= 0 and temp[key] < data[j][key]:
            data[j+1] = data[j]
            j -= 1
        data[j+1] = temp

def selection_sort(data, key):
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j][key] < data[min_idx][key]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]

def sort_records():
    method = sort_method.get()
    key = "Name" if sort_by.get() == "Name" else "Grade"
    if method == "Bubble":
        bubble_sort(student_records, key)
    elif method == "Insertion":
        insertion_sort(student_records, key)
    elif method == "Selection":
        selection_sort(student_records, key)
    refresh_display()

def linear_search(records, search_id):
    for i, record in enumerate(records):
        if record["ID"] == search_id:
            return i
    return -1

def binary_search(records, search_id):
    sorted_records = sorted(records, key=lambda x: x["ID"])
    left, right = 0, len(sorted_records) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_records[mid]["ID"] == search_id:
            return mid
        elif sorted_records[mid]["ID"] < search_id:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def search_record():
    search_id = simpledialog.askstring("Search", "Enter Student ID:")
    method = search_method.get()
    if method == "Linear":
        index = linear_search(student_records, search_id)
    else:
        index = binary_search(student_records, search_id)

    if index != -1:
        messagebox.showinfo("Found", f"Student found: {student_records[index]}")
    else:
        messagebox.showerror("Not Found", "Student ID not found.")

root = tk.Tk()
root.title("MyData Manager – Student Record Organizer")

frame = tk.Frame(root)
frame.pack(pady=10)

# Buttons
tk.Button(frame, text="Add", width=10, command=add_record).grid(row=0, column=0)
tk.Button(frame, text="Edit", width=10, command=edit_record).grid(row=0, column=1)
tk.Button(frame, text="Delete", width=10, command=delete_record).grid(row=0, column=2)
tk.Button(frame, text="Save", width=10, command=save_data).grid(row=0, column=3)
tk.Button(frame, text="Load", width=10, command=load_data).grid(row=0, column=4)

# Sorting Controls
tk.Label(root, text="Sort by:").pack()
sort_by = ttk.Combobox(root, values=["Name", "Grade"])
sort_by.set("Name")
sort_by.pack()

sort_method = ttk.Combobox(root, values=["Bubble", "Insertion", "Selection"])
sort_method.set("Bubble")
sort_method.pack()

tk.Button(root, text="Sort Records", command=sort_records).pack(pady=5)

# Search Controls
tk.Label(root, text="Search by ID using:").pack()
search_method = ttk.Combobox(root, values=["Linear", "Binary"])
search_method.set("Linear")
search_method.pack()

tk.Button(root, text="Search", command=search_record).pack(pady=5)

# Display Area
listbox = tk.Listbox(root, width=60)
listbox.pack(pady=10)

root.mainloop()