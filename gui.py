import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from models import Client, Product, Order
from db import load_data, save_data, get_next_id
from analysis import analyze_top_clients, analyze_orders_by_date, plot_top_clients, plot_orders_by_date

class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Shop Manager")
        self.data = load_data()
        self.clients = {k: Client(k, **v) for k, v in self.data['clients'].items()}
        self.products = {k: Product(k, **v) for k, v in self.data['products'].items()}
        self.orders = {k: Order(k, **v) for k, v in self.data['orders'].items()}
        
        self.create_widgets()

    def create_widgets(self):
        # Clients tab
        clients_frame = ttk.LabelFrame(self.root, text="Clients")
        clients_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(clients_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.client_name = ttk.Entry(clients_frame)
        self.client_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(clients_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.client_email = ttk.Entry(clients_frame)
        self.client_email.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(clients_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.client_phone = ttk.Entry(clients_frame)
        self.client_phone.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(clients_frame, text="City:").grid(row=3, column=0, padx=5, pady=5)
        self.client_city = ttk.Entry(clients_frame)
        self.client_city.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(clients_frame, text="Add Client", command=self.add_client).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Products tab
        products_frame = ttk.LabelFrame(self.root, text="Products")
        products_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(products_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.product_name = ttk.Entry(products_frame)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(products_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        self.product_price = ttk.Entry(products_frame)
        self.product_price.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(products_frame, text="Add Product", command=self.add_product).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Orders tab
        orders_frame = ttk.LabelFrame(self.root, text="Orders")
        orders_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(orders_frame, text="Client ID:").grid(row=0, column=0, padx=5, pady=5)
        self.order_client_id = ttk.Entry(orders_frame)
        self.order_client_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(orders_frame, text="Product IDs (comma-separated):").grid(row=1, column=0, padx=5, pady=5)
        self.order_product_ids = ttk.Entry(orders_frame)
        self.order_product_ids.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(orders_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.order_date = ttk.Entry(orders_frame)
        self.order_date.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(orders_frame, text="Add Order", command=self.add_order).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Analysis tab
        analysis_frame = ttk.LabelFrame(self.root, text="Analysis")
        analysis_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Button(analysis_frame, text="Top 5 Clients", command=self.show_top_clients).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(analysis_frame, text="Orders by Date", command=self.show_orders_by_date).grid(row=0, column=1, padx=5, pady=5)
        
        # Export/Import
        io_frame = ttk.LabelFrame(self.root, text="Import/Export")
        io_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Button(io_frame, text="Export to JSON", command=self.export_json).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(io_frame, text="Import from JSON", command=self.import_json).grid(row=0, column=1, padx=5, pady=5)

    def add_client(self):
        name = self.client_name.get()
        email = self.client_email.get()
        phone = self.client_phone.get()
        city = self.client_city.get()
        
        if not Client.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        if not Client.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone format")
            return
            
        next_id = str(get_next_id(self.data, 'clients'))
        self.clients[next_id] = Client(next_id, name, email, phone, city)
        self.data['clients'][next_id] = {
            'name': name, 'email': email, 'phone': phone, 'city': city
        }
        save_data(self.data)
        messagebox.showinfo("Success", "Client added")
        self.client_name.delete(0, tk.END)
        self.client_email.delete(0, tk.END)
        self.client_phone.delete(0, tk.END)
        self.client_city.delete(0, tk.END)

    def add_product(self):
        name = self.product_name.get()
        try:
            price = float(self.product_price.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price")
            return
            
        next_id = str(get_next_id(self.data, 'products'))
        self.products[next_id] = Product(next_id, name, price)
        self.data['products'][next_id] = {'name': name, 'price': price}
        save_data(self.data)
        messagebox.showinfo("Success", "Product added")
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)

    def add_order(self):
        client_id = self.order_client_id.get()
        product_ids_str = self.order_product_ids.get()
        date = self.order_date.get()
        
        if client_id not in self.clients:
            messagebox.showerror("Error", "Client not found")
            return
            
        try:
            product_ids = [pid.strip() for pid in product_ids_str.split(',') if pid.strip()]
            for pid in product_ids:
                if pid not in self.products:
                    raise ValueError("Product not found")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
            
        next_id = str(get_next_id(self.data, 'orders'))
        self.orders[next_id] = Order(next_id, client_id, product_ids, date)
        self.data['orders'][next_id] = {
            'client_id': client_id, 'product_ids': product_ids, 'date': date
        }
        save_data(self.data)
        messagebox.showinfo("Success", "Order added")
        self.order_client_id.delete(0, tk.END)
        self.order_product_ids.delete(0, tk.END)
        self.order_date.delete(0, tk.END)

    def show_top_clients(self):
        top = analyze_top_clients(self.data['orders'], self.data['clients'])
        plot_top_clients(top)

    def show_orders_by_date(self):
        daily = analyze_orders_by_date(self.data['orders'])
        plot_orders_by_date(daily)

    def export_json(self):
        filename = "export.json"
        save_data(self.data)
        messagebox.showinfo("Success", f"Data exported to {filename}")

    def import_json(self):
        filename = "data.json"
        if not os.path.exists(filename):
            messagebox.showerror("Error", "File not found")
            return
        self.data = load_data()
        self.clients = {k: Client(k, **v) for k, v in self.data['clients'].items()}
        self.products = {k: Product(k, **v) for k, v in self.data['products'].items()}
        self.orders = {k: Order(k, **v) for k, v in self.data['orders'].items()}
        messagebox.showinfo("Success", "Data imported")

