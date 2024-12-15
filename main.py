from transport.client import Client
from transport.vehicle import Train,Airplane 
from transport.transportcompany import TransportCompany
def menu():
	transportcompany = TransportCompany("TransGo")
	while True:
		print("\nЧто вы хотите сделать?")
		print("1. Добавить клиента")
		print("2. Добавить транспортное средство")
		print("3. Показать все транспортные средства")
		print("4. Показать всех клиентов")
		print("5. Распределить грузы")
		print("6. Удалить клиента")
		print("7. Выйти из программы")
		choice = input("Выберите пункт из предложенного выше списка: ")
		if choice == "1":
			name=input("Введите имя клиента: ")
			weight=float(input("Введите вес груза в тоннах: "))
			is_vip_str = input("Это VIP клиент? (True/False): ").strip().lower() 
			is_vip = True if is_vip_str == 'true' else False
			transportcompany.add_client(Client(name, weight, is_vip))
		elif choice == "2":
			choice_type_vehicle=input("Выберите вид транспорта(самолет - 1,поезд - 2): ")
			if choice_type_vehicle=="1":
				capacity=float(input("Введите грузоподъёмность: "))
				max_altitude=input("Введите максимальную высоту полета: ")
				transportcompany.add_vehicle(Airplane(capacity,max_altitude))
			elif choice_type_vehicle=="2":
				capacity=float(input("Введите грузоподъёмность: "))
				number_of_cars=input("Введите количество вагонов: ")
				transportcompany.add_vehicle(Train(capacity,number_of_cars))
			else:
				print("Введен неправильный тип транспорта")
		elif choice == "3":
			print("\nТранспортные средства: ")
			if transportcompany.list_vehicles():
				for vehicle in transportcompany.list_vehicles():
					print(vehicle)
			else: 
				print("Нету транспортных средств!")
		elif choice == "4":
			print("\nКлиенты: ")
			if transportcompany.list_clients():
				for vehicle in transportcompany.list_vehicles():
					print(vehicle)
			else: 
				print("Нету транспортных средств!")
		elif choice == "5":
			transportcompany.optimize_cargo_distribution()
			print("\nГрузы успешно распределены!")
			print("\nРезультат распределения груза: ")
			for vehicle in transportcompany.vehicles:
				print(vehicle)
				for client in vehicle.clients_list:
						print(f"Клиент: {client.name}, груз: {client.cargo_weight} тонн, VIP: {'да' if client.is_vip else 'нет'}")
		elif choice == "6":
			find_to_deleteclient = input("Введите имя клиента: ")
			for client in transportcompany.clients:
				if client.name == find_to_deleteclient:
					transportcompany.clients.remove(client)
					print("Клиент удален!")
				else:
					print("Клиента с таким именем нет!")
			else:
				print("Неправильный выбор, попробуйте снова!")
		elif choice == "7":
			break
		else:
			print("Неправильный выбор, попробуйте снова")
if __name__ == "__main__":
    menu()
