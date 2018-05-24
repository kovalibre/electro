import pprint
import datetime

DATE = 'Дата'
ROOM_NUM = 'Количество комнат'
TARIFF = 'Тариф на электроэнергию'
APARTMENT = 'Квартира'
ROOM_N = 'Комната №_'
METER = 'Показания счетчика'
HUMANS = 'Количество проживающих'
CONSUMPTION = 'Потребление энергии (кВт)'
COMMUNAL_COST = 'Стоимость коммунального потребления'
COMM_PER_PERSON = 'Стоимость коммунального потребления с человека'
ROOM_COST = 'Стоимость потребления в комнате'
DEBT = 'Задолженность'
TOTAL = 'ИТОГО'
INSTRUCTION = ' Чтобы получить рассчет по комнате, введите ее номер.\n \
"all" - чтобы получить рассчет по всем комнатам.\n \
"exit" - завершить работу.\n \
 №: '


class RecentData:
    """Класс, содержащий в качестве атрибутов значения данных прошлых 
    запусков программы."""
    def __init__(self, 
                 database: str, 
                 rooms: dict=None,
                 meter: int=0, 
                 number_of_rooms: int=0) -> None:
        self.database = database
        self.meter = meter
        self.number_of_rooms = number_of_rooms
        self.rooms = rooms
        
    def recieve(self, apartment: str=APARTMENT,
                      meter: str=METER,
                      room_num: str=ROOM_NUM) -> None:
        # Читает из базы данных словарь за последний запуск программы,
        # задает атрибутам значения из него. Если базы нет, 
        # оставляет нулевые значения.
        try:
            with open(self.database) as database:
                recent = []
                for line in database:
                    recent.append(eval(line))
            last_line = recent[-1]
            print()
            # временная строка для самоконтроля:
            pprint.pprint(last_line)
            print()
            print()
            self.meter = last_line[apartment][meter]
            self.number_of_rooms = last_line[apartment][room_num]
            self.rooms = last_line
        except FileNotFoundError:
            pass


class GeneralData:
    """Класс, содержащий в качестве атрибутов общие данниые по квартире,
    необходимые для рассчетов."""
    def __init__(self,
                 meter: int=None, 
                 number_of_rooms: int=None,
                 tariff: float=None,
                 consumption: int=None,
                 communal_per_person: int=None) -> None:
        self.meter = meter
        self.number_of_rooms = number_of_rooms
        self.tariff = tariff
        self.consumption = consumption
        self.communal_per_person = communal_per_person

    def input(self, recent_number_of_rooms: int, 
                    int_reader,
                    float_reader) -> None:
        # Вводим значения общих данных по квартире.
        self.tariff = float_reader('Текущий тариф (в руб.): ')
        print()
        if recent_number_of_rooms == 0:
            # При первом запуске указываем количество комнат.
            self.number_of_rooms = int_reader(
                                   'Укажите количество комнат в квартире: ')
            print()
        else:
            self.number_of_rooms = recent_number_of_rooms
        self.meter = int_reader('Введите показания общего счетчика: ')
        print()

    def calculate_consumption(self, recent_meter: int) -> None:
        # Рассчитываем общее потребление электроэнергии в квартире.
        self.consumption = self.meter - recent_meter

    def calculate_communal_per_person(self, rooms: dict, 
                                            room_n: str=ROOM_N,
                                            consumption: str=CONSUMPTION,
                                            humans: str=HUMANS) -> None:
        # Рассчитываем затраты на коммунальное потребление 
        # с каждого проживающего.
        persons = 0
        communal_consumption = self.consumption
        for num in range(self.number_of_rooms):
            room = rooms[room_n + str(num+1)]
            persons += room[humans]
            communal_consumption -= room[consumption]
        self.communal_per_person = (self.tariff * 
                                    communal_consumption) / persons


class RoomsData:
    """Класс, содержащий в качестве атрибута 
    словари данных по каждой комнате."""
    def __init__(self, rooms: dict=None) -> None:
        self.rooms = rooms
        
    def input(self, number_of_rooms: int,
                    int_reader, 
                    float_reader,
                    room_n: str=ROOM_N,
                    meter: str=METER,
                    humans: str=HUMANS,
                    debt: str=DEBT) -> None:
        # Вводим значения данных по каждой комнате и заносим их в словарь.
        self.rooms = {}
        for num in range (number_of_rooms):
            self.rooms[room_n + str(num+1)] = {}
            room = self.rooms[room_n + str(num+1)]

            room[meter] = int_reader('Введите показания счетчика комнаты номер '
                                      + str(num+1) + ': ')
            room[humans] = int_reader('Количество проживающих в комнате: ')
            room[debt] = float_reader('Долг за прошедший период (руб.): ')
            print()
     
    def calculate_consumption(self, number_of_rooms: int,
                                    recent_number_of_rooms: int,
                                    recent_rooms: dict,
                                    room_n: str=ROOM_N,
                                    meter: str=METER,
                                    consumption: str=CONSUMPTION) -> None:
        # Рассчитываем потребление энергии в каждой комнате.
        if recent_number_of_rooms == 0:
            for num in range(number_of_rooms):
                room = self.rooms[room_n + str(num+1)]
                room[consumption] = room[meter]
        else:
            for num in range (number_of_rooms):
                room = self.rooms[room_n + str(num+1)]
                room[consumption] = (room[meter] - 
                                     recent_rooms[room_n + str(num+1)][meter])

    def calculate_accounts(self, number_of_rooms: int,
                                 tariff: float,
                                 communal_per_person: float,
                                 room_n: str=ROOM_N,
                                 consumption: str=CONSUMPTION,
                                 room_cost: str=ROOM_COST,
                                 communal_cost: str=COMMUNAL_COST,
                                 humans: str=HUMANS,
                                 debt: str=DEBT,
                                 total: str=TOTAL) -> None:
        # Рассчитываем стоимость потребления электроэнергии в каждой комнате,
        # затраты на коммунальный расход, исходя из числа проживающих в ней 
        # человек, а также итоговую сумму счета по комнате.
        for num in range (number_of_rooms):
            room = self.rooms[room_n + str(num+1)]
            room[room_cost] = room[consumption] * tariff
            room[communal_cost] = communal_per_person * room[humans]
            room[total] = room[communal_cost] + room[room_cost] + room[debt]


class AllNewData:
    """Класс, собирающий в себя все новые данные, чтобы выводить их
    пользователю и сохранять в базе данных."""
    def __init__(self, data: dict=None) -> None:
        self.data = data

    def collect(self, today: str,
                      number_of_rooms: int,
                      general_meter: int,
                      tariff: float,
                      general_consumption: int,
                      communal_per_person: int,
                      rooms: dict,
                      date: str=DATE,
                      room_num: str=ROOM_NUM,
                      trff: str=TARIFF,
                      apartment: str=APARTMENT,
                      meter: str=METER,
                      consumption: str=CONSUMPTION,
                      comm_per_person: str=COMM_PER_PERSON) -> None:
        gen_data = {}
        gen_data[date] = today
        gen_data[meter] = general_meter
        gen_data[trff] = tariff
        gen_data[room_num] = number_of_rooms
        gen_data[consumption] = general_consumption
        gen_data[comm_per_person] = communal_per_person
        self.data = {}
        self.data[apartment] = gen_data
        self.data.update(rooms)

    def output_all(self, number_of_rooms: int,
                         room_n: str=ROOM_N,
                         room_cost: str=ROOM_COST,
                         communal_cost: str=COMMUNAL_COST,
                         debt: str=DEBT,
                         total: str=TOTAL) -> None:
        # Выводит на экран счета для всех комнат.
        for num in range (number_of_rooms):
            room = self.data[room_n + str(num+1)]
        
            print ('Комната номер', num+1, ':')
            print ('Индивидуальное потребление: ', '%.2f' % room[room_cost], 'руб.')
            print ('За коммунальное: ', '%.2f' % room[communal_cost], 'руб.')
            if room[debt] > 0:
                print ('Задолженность: ', '%.2f' % room[debt], 'руб.')
            print ('ИТОГО: ', '%.2f' % room[total], 'руб.')
            print()

    def output_room(self, room_id: int,
                          room_n: str=ROOM_N,
                          room_cost: str=ROOM_COST,
                          communal_cost: str=COMMUNAL_COST,
                          debt: str=DEBT,
                          total: str=TOTAL) -> None:
        # Выводит на экран счет для указанной комнаты.
        room = self.data[room_n + str(room_id)]
        
        print ('Комната номер', room_id, ':')
        print ('Индивидуальное потребление: ', '%.2f' % room[room_cost], 'руб.')
        print ('За коммунальное: ', '%.2f' % room[communal_cost], 'руб.')
        if room[debt] > 0:
            print ('Задолженность: ', '%.2f' % room[debt], 'руб.')
        print ('ИТОГО: ', '%.2f' % room[total], 'руб.')
        print()

    def add_to_db(self, datafile: str) -> None:
        # Вносит данные в файл базы или создает новый.
        try:
            with open(datafile, 'a') as database:
                print(self.data, file=database)
        except FileNotFoundError:
            with open(datafile, 'x') as database:
                print(self.data, file=database)

    
def digit_data_input(string_for_check: str) -> int:
    # Цикл проверки строки ввода для целочисленных значений.
    # Возвращает целое число.
    digit_value = input(string_for_check)
    while not digit_value.isdigit():
        print()
        print('ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ!')
        print()
        digit_value = input(string_for_check)
    return int(digit_value)


def float_data_input(string_for_check: str) -> float:
    # Цикл проверки строки ввода для float-значений.
    # Возвращает float.
    float_value = input(string_for_check)
    while True:
        try:
            float(float_value)
            break
        except ValueError:
            print()
            print('ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ!')
            print()
            float_value = input(string_for_check)
    return float(float_value)


def print_greetings(version: str, date: str) -> None:
    # Выводит на экран приветствие, номер версии и текущую дату.
    print()
    print('Рассчет оплаты электроэнергии в коммунальной квартире.')
    print('Версия: ', version)
    print('Сегодня на календаре: ', date)
    print()


def print_results_by_user_command(number_of_rooms: int,
                                  new_data: AllNewData,
                                  instruction: str=INSTRUCTION,
                                  ):
    # Выводит на экран инструкцию для пользователя, и, в зависимости от
    # полученной команды, вызывает соответствующую функцию.
    print()
    command = str(input(instruction))
    print()
    while command != 'exit':
        # Пока не введена команда выхода из программы, выполняется цикл:
        if command == 'all':
            # получение счета для всех комнат,
            new_data.output_all(number_of_rooms)
            print()
            command = str(input(instruction))
            print()
        else:
            while True:
                try:
                    if 0 < int(command) <= number_of_rooms:
                        # получение счета по номеру комнаты,
                        print()
                        new_data.output_room(command)
                        print()
                        command = str(input(instruction))
                        print()
                    break
                except ValueError:
                    # сообщение об ошибке в прочих случаях.
                    print()
                    print('ВВЕДИТЕ КОРРЕКТНУЮ КОММАНДУ!')
                    print()
                    print()
                    command = str(input(instruction))
                    print()


def main():
    version = '0.1.4'
    today = datetime.date.isoformat(datetime.date.today())
    datafile = 'database.txt'
    int_reader = lambda x: digit_data_input(x)
    float_reader = lambda x: float_data_input(x)
    recent = RecentData(datafile)
    general = GeneralData()
    rooms = RoomsData()
    new_data = AllNewData()

    print_greetings(version, today)
    recent.recieve()

    general.input(recent.number_of_rooms,
                int_reader,
                float_reader)

    number_of_rooms = general.number_of_rooms

    rooms.input(number_of_rooms,
                int_reader,
                float_reader)
    general.calculate_consumption(recent.meter)
    rooms.calculate_consumption(number_of_rooms,
                                recent.number_of_rooms,
                                recent.rooms)
    general.calculate_communal_per_person(rooms.rooms)
    rooms.calculate_accounts(number_of_rooms,
                            general.tariff,
                            general.communal_per_person)
    new_data.collect(today,
                    number_of_rooms,
                    general.meter,
                    general.tariff,
                    general.consumption,
                    general.communal_per_person,
                    rooms.rooms)
    print_results_by_user_command(number_of_rooms,
                                new_data)

    new_data.add_to_db(datafile)

if __name__ == '__main__':
    main()