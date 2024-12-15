import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from transport.client import Client 
from transport.vehicle import Train, Airplane 
from transport.transportcompany import TransportCompany
class Transportapp:
    def __init__(person, root):
        person.company = TransportCompany("TransGo")
        root.title("TransGo")
        root.geometry("1500x750")
        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Экспорт результата", command=person.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="О программе", command=person.about)

        person.status = tk.StringVar()
        person.status.set("Готово")
        status_bar = tk.Label(root, textvariable=person.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        person.control_frame = tk.Frame(root)
        person.control_frame.pack()
        person.client_button = tk.Button(person.control_frame, text="Добавить клиента", command=person.add_client)
        person.client_button.grid(row=0, column=0, padx=10, pady=10)
        person.vehicle_button = tk.Button(person.control_frame, text="Добавить транспортное средство", command=person.add_vehicle)
        person.vehicle_button.grid(row=0, column=1, padx=10, pady=10)
        person.optimize_button = tk.Button(person.control_frame, text="Распределить грузы", command=person.optimize_cargo)
        person.optimize_button.grid(row=0, column=4, padx=10, pady=10)
        person.delete_client_button = tk.Button(person.control_frame, text="Удалить клиента", command=person.delete_client)
        person.delete_client_button.grid(row=0, column=5, padx=10, pady=10)

        person.data_frame = tk.Frame(root)
        person.data_frame.pack()
        person.clients_tree = ttk.Treeview(person.data_frame, columns=('Имя', 'Вес груза', 'VIP'), show='headings')
        person.clients_tree.heading('Имя', text = 'Имя')
        person.clients_tree.heading('Вес груза', text = 'Вес груза')
        person.clients_tree.heading('VIP', text = 'VIP')
        person.clients_tree.pack(side=tk.LEFT)

        person.vehicles_tree = ttk.Treeview(person.data_frame, columns=('ID', 'Тип', 'Грузоподъемность', 'Текущая загрузка'), show='headings')
        person.vehicles_tree.heading('ID', text = 'ID')
        person.vehicles_tree.heading('Тип', text = 'Тип')
        person.vehicles_tree.heading('Грузоподъемность', text = 'Грузоподъемность')
        person.vehicles_tree.heading('Текущая загрузка', text = 'Текущая загрузка')
        person.vehicles_tree.pack(side=tk.RIGHT)
    def add_client(self):
        client_window = tk.Toplevel()
        client_window.title("Добавить клиента")
        client_window.geometry("300x200")
        tk.Label(client_window, text="Имя:").grid(row=0, column=0)
        name_entry = tk.Entry(client_window)
        name_entry.grid(row=0, column=1)
        tk.Label(client_window, text="Вес груза:").grid(row=1, column=0)
        cargo_entry = tk.Entry(client_window)
        cargo_entry.grid(row=1, column=1)
        vip_var = tk.IntVar()
        vip_check = tk.Checkbutton(client_window, text="VIP", variable=vip_var)
        vip_check.grid(row=2, column=1)
        def save_client():
            try:
                name = name_entry.get()
                if not name.isalpha() or len(name) < 2:
                    raise ValueError("Имя клиента должно содержать только буквы и иметь минимум 2 символа")
                cargo_weight = float(cargo_entry.get())
                if cargo_weight <= 0 or cargo_weight > 10000:
                    raise ValueError("Вес груза должен быть положительным числом не более 10000 кг")
                is_vip = vip_var.get() == 1
                self.company.add_client(Client(name, cargo_weight, is_vip))
                self.status.set("Клиент добавлен")
                client_window.destroy()
                messagebox.showinfo("Успех", "Клиент добавлен!")
                self.update_clients_tree()
            except ValueError as e:
                self.status.set("Ошибка")
                messagebox.showerror("Ошибка", str(e))
                name_entry.delete(0, tk.END)
                cargo_entry.delete(0, tk.END)
        save_button = tk.Button(client_window, text="Сохранить", command=save_client)
        save_button.grid(row=3, column=1)
        cancel_button = tk.Button(client_window, text="Отмена", command=client_window.destroy)
        cancel_button.grid(row=3, column=0)
    def add_vehicle(self):
        vehicle_window = tk.Toplevel()
        vehicle_window.title("Добавить транспортное средство")
        vehicle_window.geometry("300x200")
        tk.Label(vehicle_window, text="Тип транспорта:").grid(row=0, column=0)
        vehicle_type_var = tk.StringVar()
        vehicle_type_dropdown = tk.OptionMenu(vehicle_window, vehicle_type_var, "Самолет", "Поезд")
        vehicle_type_dropdown.grid(row=0, column=1)
        tk.Label(vehicle_window, text="Грузоподъемность:").grid(row=1, column=0)
        capacity_entry = tk.Entry(vehicle_window)
        capacity_entry.grid(row=1, column=1)
        def save_vehicle():
            try:
                vehicle_type = vehicle_type_var.get()
                capacity = float(capacity_entry.get())
                if capacity <= 0:
                    raise ValueError("Грузоподъемность должна быть положительным числом")
                if vehicle_type == "Самолет":
                    max_altitude = float(simpledialog.askstring("Максимальная высота полета", "Введите максимальную высоту полета:"))
                    self.company.add_vehicle(Airplane(capacity, max_altitude))
                    self.status.set("Самолет добавлен")
                elif vehicle_type == "Поезд":
                    number_of_cars = int(simpledialog.askstring("Количество вагонов", "Введите количество вагонов:"))
                    self.company.add_vehicle(Train(capacity, number_of_cars))
                    self.status.set("Поезд добавлен")
                vehicle_window.destroy()
                messagebox.showinfo("Успех", f"{vehicle_type} добавлен!")
                self.update_vehicles_tree()
            except ValueError as e:
                self.status.set("Ошибка")
                messagebox.showerror("Ошибка", str(e))
                capacity_entry.delete(0, tk.END)
        save_button = tk.Button(vehicle_window, text="Сохранить", command=save_vehicle)
        save_button.grid(row=2, column=1)
        cancel_button = tk.Button(vehicle_window, text="Отмена", command=vehicle_window.destroy)
        cancel_button.grid(row=2, column=0)
    def optimize_cargo(self):
        used_vehicles = self.company.optimize_cargo_distribution()
        results = ""
        for vehicle in used_vehicles:
            results += str(vehicle) + "\n"
            for client in vehicle.clients_list:
                results += f"Клиент: {client.name}, груз: {client.cargo_weight} тонн, VIP: {'да' if client.is_vip else 'нет'}\n"
        messagebox.showinfo("Распределение грузов", results)
        self.status.set("Грузы распределены")
        self.update_vehicles_tree()
    def delete_client(self):
        delete_window = tk.Toplevel()
        delete_window.title("Удалить клиента")
        delete_window.geometry("300x100")
        tk.Label(delete_window, text="Имя клиента:").grid(row=0, column=0)
        name_entry = tk.Entry(delete_window)
        name_entry.grid(row=0, column=1)
        def remove_client():
            name = name_entry.get()
            client_to_remove = None
            for client in self.company.clients:
                if client.name == name:
                    client_to_remove = client
                    break
            if client_to_remove:
                self.company.clients.remove(client_to_remove) 
                delete_window.destroy()
                self.status.set("Клиент удален")
                messagebox.showinfo("Успех", "Клиент удален!")
                self.update_clients_tree() 
            else:
                messagebox.showerror("Ошибка! Клиента с таким именем нет")
                self.status.set("Ошибка")
        remove_button = tk.Button(delete_window, text="Удалить", command=remove_client)
        remove_button.grid(row=1, column=1)
        cancel_button = tk.Button(delete_window, text="Отмена", command=delete_window.destroy)
        cancel_button.grid(row=1, column=0)
    def export_results(self):
        messagebox.showinfo("Экспорт результата", "Функция экспорта еще не реализована")
    def about(self):
        messagebox.showinfo("О программе", "Лабораторная работа: номер\nВариант: номер\nФИО разработчика")
    def update_clients_tree(self):
        for row in self.clients_tree.get_children():
            self.clients_tree.delete(row)
        for client in self.company.clients:
            self.clients_tree.insert("", "end", values=(client.name, client.cargo_weight, "да" if client.is_vip else "нет"))
    def update_vehicles_tree(self):
        for row in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(row)
        for vehicle in self.company.vehicles:
            vehicle_type = "Самолет" if isinstance(vehicle, Airplane) else "Поезд"
            self.vehicles_tree.insert("", "end", values=(vehicle.vehicle_id, vehicle_type, vehicle.capacity, vehicle.current_load))
if __name__ == "__main__":
    root = tk.Tk()
    app = Transportapp(root)
    root.mainloop()
