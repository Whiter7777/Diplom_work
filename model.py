from mysql.connector import connect, Error
from getpass import getpass

class Employee():
    def __init__(self, name):
        self.name = name

    def get_employee(self):
        """
        Поиск в базе данных по имени сотрудника. Возвращается роль сотрудника
        """
        pass


class Rack_type():
    def __init__(self, name, cell_x, cell_y, color, location, storage_time = 3, container_types = [], analysis_names = [], workflows = [], sample_statuses = []):
        self.name = name
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.color = color
        self.location = location
        self.storage_time = storage_time
        self.container_types = container_types
        self.analysis_names = analysis_names
        self.workflows = workflows
        self.sample_statuses = sample_statuses

    def set_rack_type(self):
        """Добавдение типа штатива в базу данных"""
        try:
            with connect(
                host="localhost",
                user=input("Имя пользователя"),
                password=getpass("Пароль: "),
            ) as connection:
                print(connection)
        except Error as e:
            print(e)

class Probe():
    def __init__(self, number):
        self.number = number

    def check_probe(self):
        """
        Проверка введенного значения на корректность
        """
        pass

    def get_probe(self):
        """
        Поиск в базе данных по номеру пробы. Возвращает текущие параметры из базы данных
        location, status, workflow, container_type, analysis_names
        """
        pass

