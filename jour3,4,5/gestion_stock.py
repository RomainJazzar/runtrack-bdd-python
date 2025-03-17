import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import csv

# Function to connect to the database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Alep2012..",  # Replace with your MySQL password
        database="store"
    )

# Refresh the product list
def refresh_products():
    for item in tree.get_children():
        tree.delete(item)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT p.id, p.name, p.description, p.price, p.quantity, c.name "
                   "FROM product p JOIN category c ON p.id_category = c.id")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    cursor.close()
    conn.close()

# Add a product
def add_product():
    name = entry_name.get()
    desc = entry_desc.get()
    price = entry_price.get()
    quantity = entry_quantity.get()
    id_cat = entry_id_cat.get()
    if name and price and quantity and id_cat:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) "
                           "VALUES (%s, %s, %s, %s, %s)", (name, desc, int(price), int(quantity), int(id_cat)))
            conn.commit()
            cursor.close()
            conn.close()
            refresh_products()
            messagebox.showinfo("Success", "Product added")
        except ValueError:
            messagebox.showwarning("Error", "Price and Quantity must be numbers")
    else:
        messagebox.showwarning("Error", "All fields are required")

# Modify a product
def modify_product():
    selected = tree.selection()
    if selected:
        product_id = tree.item(selected)['values'][0]
        name = entry_name.get()
        desc = entry_desc.get()
        price = entry_price.get()
        quantity = entry_quantity.get()
        id_cat = entry_id_cat.get()
        if name and price and quantity and id_cat:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s "
                               "WHERE id=%s", (name, desc, int(price), int(quantity), int(id_cat), product_id))
                conn.commit()
                cursor.close()
                conn.close()
                refresh_products()
                messagebox.showinfo("Success", "Product updated")
            except ValueError:
                messagebox.showwarning("Error", "Price and Quantity must be numbers")
        else:
            messagebox.showwarning("Error", "All fields are required")
    else:
        messagebox.showwarning("Error", "Select a product to modify")

# Delete a product
def delete_product():
    selected = tree.selection()
    if selected:
        product_id = tree.item(selected)['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        refresh_products()
        messagebox.showinfo("Success", "Product deleted")
    else:
        messagebox.showwarning("Error", "Select a product to delete")

# Export products to CSV
def export_to_csv():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    with open("products.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Description", "Price", "Quantity", "Category ID"])
        writer.writerows(cursor.fetchall())
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Exported to products.csv")

# Filter products by category
def filter_by_category():
    id_cat = entry_filter.get()
    if id_cat:
        for item in tree.get_children():
            tree.delete(item)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT p.id, p.name, p.description, p.price, p.quantity, c.name "
                       "FROM product p JOIN category c ON p.id_category = c.id WHERE p.id_category = %s", (id_cat,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        cursor.close()
        conn.close()
    else:
        refresh_products()

# Set up the Tkinter interface
root = tk.Tk()
root.title("Stock Management Dashboard")

# Frame for the product list
frame_list = tk.Frame(root)
frame_list.pack(pady=10)

tree = ttk.Treeview(frame_list, columns=("ID", "Name", "Description", "Price", "Quantity", "Category"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Description", text="Description")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")
tree.heading("Category", text="Category")
tree.pack()

# Frame for input fields
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1)

tk.Label(frame_inputs, text="Description").grid(row=1, column=0)
entry_desc = tk.Entry(frame_inputs)
entry_desc.grid(row=1, column=1)

tk.Label(frame_inputs, text="Price").grid(row=2, column=0)
entry_price = tk.Entry(frame_inputs)
entry_price.grid(row=2, column=1)

tk.Label(frame_inputs, text="Quantity").grid(row=3, column=0)
entry_quantity = tk.Entry(frame_inputs)
entry_quantity.grid(row=3, column=1)

tk.Label(frame_inputs, text="Category ID").grid(row=4, column=0)
entry_id_cat = tk.Entry(frame_inputs)
entry_id_cat.grid(row=4, column=1)

# Frame for buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add", command=add_product).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Modify", command=modify_product).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete", command=delete_product).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Export to CSV", command=export_to_csv).grid(row=0, column=3, padx=5)

# Frame for category filter
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Filter by Category ID").grid(row=0, column=0)
entry_filter = tk.Entry(frame_filter)
entry_filter.grid(row=0, column=1)
tk.Button(frame_filter, text="Apply Filter", command=filter_by_category).grid(row=0, column=2, padx=5)

# Load initial product list
refresh_products()

root.mainloop()