import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. Création de la base de données et des tables si elles n'existent pas
# -----------------------------------------------------------------------------
def create_database_and_tables():
    """
    Cette fonction se connecte en tant que root sans spécifier de base de données,
    crée la base 'store' si elle n'existe pas, puis crée les tables 'category' et 'product'.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Alep2012.."
    )
    cursor = conn.cursor()
    
    # Créer la base de données si elle n'existe pas
    cursor.execute("CREATE DATABASE IF NOT EXISTS store")
    cursor.execute("USE store")
    
    # Créer la table 'category'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    
    # Créer la table 'product'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price INT,
            quantity INT,
            id_category INT,
            FOREIGN KEY (id_category) REFERENCES category(id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# -----------------------------------------------------------------------------
# 2. Classe pour gérer les opérations sur la base de données
# -----------------------------------------------------------------------------
class StoreDB:
    def __init__(self):
        """
        Initialise la connexion à la base de données 'store' et crée un curseur.
        """
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Alep2012..",
            database="store"
        )
        self.cursor = self.conn.cursor()
    
    def get_products(self, category_id=None):
        """
        Récupère tous les produits, ou seulement ceux d'une catégorie donnée.
        Le LEFT JOIN permet d'obtenir le nom de la catégorie.
        """
        if category_id:
            query = """
                SELECT product.id, product.name, product.description, product.price, product.quantity, category.name 
                FROM product 
                LEFT JOIN category ON product.id_category = category.id 
                WHERE category.id = %s
            """
            self.cursor.execute(query, (category_id,))
        else:
            query = """
                SELECT product.id, product.name, product.description, product.price, product.quantity, category.name 
                FROM product 
                LEFT JOIN category ON product.id_category = category.id
            """
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_categories(self):
        """
        Récupère toutes les catégories.
        """
        self.cursor.execute("SELECT * FROM category")
        return self.cursor.fetchall()
    
    def add_product(self, name, description, price, quantity, id_category):
        """
        Ajoute un produit dans la table 'product'.
        """
        query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, description, price, quantity, id_category))
        self.conn.commit()
    
    def update_product(self, id, name, description, price, quantity, id_category):
        """
        Met à jour un produit identifié par son id.
        """
        query = "UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s"
        self.cursor.execute(query, (name, description, price, quantity, id_category, id))
        self.conn.commit()
    
    def delete_product(self, id):
        """
        Supprime un produit identifié par son id.
        """
        query = "DELETE FROM product WHERE id = %s"
        self.cursor.execute(query, (id,))  # Notez la virgule pour créer un tuple à un élément
        self.conn.commit()
    
    def close(self):
        """
        Ferme le curseur et la connexion.
        """
        self.cursor.close()
        self.conn.close()

# -----------------------------------------------------------------------------
# 3. Interface graphique Tkinter pour le tableau de bord
# -----------------------------------------------------------------------------
class StockDashboard:
    def __init__(self, master):
        self.master = master
        master.title("Gestion de Stock")
        self.db = StoreDB()
        
        # Cadre supérieur pour le tableau (Treeview)
        self.frame_top = tk.Frame(master)
        self.frame_top.pack(pady=10)
        
        # Cadre inférieur pour les contrôles (entrées et boutons)
        self.frame_bottom = tk.Frame(master)
        self.frame_bottom.pack(pady=10)
        
        # Création d'un Treeview pour afficher les produits
        self.tree = ttk.Treeview(self.frame_top, columns=("ID", "Name", "Description", "Price", "Quantity", "Category"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Category", text="Category")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Ajout d'une scrollbar verticale
        scrollbar = ttk.Scrollbar(self.frame_top, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Création des champs d'entrée pour les informations du produit
        self.label_name = tk.Label(self.frame_bottom, text="Name:")
        self.label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(self.frame_bottom)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)
        
        self.label_description = tk.Label(self.frame_bottom, text="Description:")
        self.label_description.grid(row=1, column=0, padx=5, pady=5)
        self.entry_description = tk.Entry(self.frame_bottom)
        self.entry_description.grid(row=1, column=1, padx=5, pady=5)
        
        self.label_price = tk.Label(self.frame_bottom, text="Price:")
        self.label_price.grid(row=0, column=2, padx=5, pady=5)
        self.entry_price = tk.Entry(self.frame_bottom)
        self.entry_price.grid(row=0, column=3, padx=5, pady=5)
        
        self.label_quantity = tk.Label(self.frame_bottom, text="Quantity:")
        self.label_quantity.grid(row=1, column=2, padx=5, pady=5)
        self.entry_quantity = tk.Entry(self.frame_bottom)
        self.entry_quantity.grid(row=1, column=3, padx=5, pady=5)
        
        self.label_category = tk.Label(self.frame_bottom, text="Category:")
        self.label_category.grid(row=0, column=4, padx=5, pady=5)
        # Utilisation d'une Combobox pour sélectionner la catégorie
        self.combo_category = ttk.Combobox(self.frame_bottom, state="readonly")
        self.combo_category.grid(row=0, column=5, padx=5, pady=5)
        
        # Boutons d'actions
        self.btn_add = tk.Button(self.frame_bottom, text="Add Product", command=self.add_product)
        self.btn_add.grid(row=2, column=0, padx=5, pady=5)
        
        self.btn_update = tk.Button(self.frame_bottom, text="Update Product", command=self.update_product)
        self.btn_update.grid(row=2, column=1, padx=5, pady=5)
        
        self.btn_delete = tk.Button(self.frame_bottom, text="Delete Product", command=self.delete_product)
        self.btn_delete.grid(row=2, column=2, padx=5, pady=5)
        
        self.btn_export = tk.Button(self.frame_bottom, text="Export CSV", command=self.export_csv)
        self.btn_export.grid(row=2, column=3, padx=5, pady=5)
        
        self.btn_chart = tk.Button(self.frame_bottom, text="Show Chart", command=self.show_chart)
        self.btn_chart.grid(row=2, column=4, padx=5, pady=5)
        
        self.btn_filter = tk.Button(self.frame_bottom, text="Filter by Category", command=self.filter_by_category)
        self.btn_filter.grid(row=2, column=5, padx=5, pady=5)
        
        # Chargement des catégories dans la combobox et des produits dans le tableau
        self.load_categories()
        self.load_products()
    
    def load_categories(self):
        """
        Charge les catégories depuis la base et les place dans la combobox.
        On stocke également les catégories dans un dictionnaire {nom: id} pour faciliter la récupération.
        """
        categories = self.db.get_categories()
        self.categories = {cat[1]: cat[0] for cat in categories}  # cat[1] = name, cat[0] = id
        self.combo_category['values'] = list(self.categories.keys())
    
    def load_products(self, category_id=None):
        """
        Recharge le Treeview avec la liste des produits.
        Si category_id est précisé, on filtre par catégorie.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = self.db.get_products(category_id)
        for product in products:
            self.tree.insert("", "end", values=product)
    
    def add_product(self):
        """
        Récupère les données des champs d'entrée et ajoute un produit.
        """
        name = self.entry_name.get()
        description = self.entry_description.get()
        try:
            price = int(self.entry_price.get())
            quantity = int(self.entry_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be integers")
            return
        category_name = self.combo_category.get()
        id_category = self.categories.get(category_name, None)
        if not name or not category_name:
            messagebox.showerror("Error", "Name and Category are required")
            return
        self.db.add_product(name, description, price, quantity, id_category)
        self.load_products()
    
    def update_product(self):
        """
        Met à jour le produit sélectionné avec les nouvelles données saisies.
        Si un champ est vide, il garde la valeur actuelle.
        """
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No product selected")
            return
        product_data = self.tree.item(selected)['values']
        product_id = product_data[0]
        name = self.entry_name.get() or product_data[1]
        description = self.entry_description.get() or product_data[2]
        try:
            price = int(self.entry_price.get() or product_data[3])
            quantity = int(self.entry_quantity.get() or product_data[4])
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be integers")
            return
        category_name = self.combo_category.get() or product_data[5]
        id_category = self.categories.get(category_name, None)
        self.db.update_product(product_id, name, description, price, quantity, id_category)
        self.load_products()
    
    def delete_product(self):
        """
        Supprime le produit sélectionné.
        """
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No product selected")
            return
        product_data = self.tree.item(selected)['values']
        product_id = product_data[0]
        self.db.delete_product(product_id)
        self.load_products()
    
    def export_csv(self):
        """
        Exporte la liste des produits en stock dans un fichier CSV.
        """
        products = self.db.get_products()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Name", "Description", "Price", "Quantity", "Category"])
            for product in products:
                writer.writerow(product)
        messagebox.showinfo("Export CSV", f"Products exported to {file_path}")
    
    def show_chart(self):
        """
        Affiche un graphique simple représentant la quantité totale par catégorie.
        """
        products = self.db.get_products()
        data = {}
        for product in products:
            category = product[5] if product[5] else "Uncategorized"
            data[category] = data.get(category, 0) + product[4]
        categories = list(data.keys())
        quantities = list(data.values())
        
        plt.figure(figsize=(8,6))
        plt.bar(categories, quantities)
        plt.xlabel("Category")
        plt.ylabel("Total Quantity")
        plt.title("Total Quantity per Category")
        plt.show()
    
    def filter_by_category(self):
        """
        Filtre l'affichage des produits selon la catégorie sélectionnée dans la combobox.
        """
        category_name = self.combo_category.get()
        id_category = self.categories.get(category_name, None)
        self.load_products(id_category)

# -----------------------------------------------------------------------------
# 4. Lancement de l'application
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Créer la base et les tables si elles n'existent pas déjà
    create_database_and_tables()
    
    root = tk.Tk()
    app = StockDashboard(root)
    root.mainloop()
    
    # Fermer la connexion à la base une fois l'application fermée
    app.db.close()
