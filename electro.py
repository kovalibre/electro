import pprint
import datetime

DATE = 'Дата'
ROOM_NUM = 'Количество комнат'
TARIF = 'Тариф на электроэнергию'
KVARTIRA = 'Квартира'
ROOM_N = 'Комната_'
METER = 'Показания счетчика'
HUMANS = 'Количество проживающих'
CONSUMPTION = 'Потребление энергии (кВт)'
COMM_COST = 'Стоимость коммунального потребления'
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
                 database: str='database.txt', 
                 meter: int=0, 
                 room_num: int=0,
                 rooms: dict={}) -> None:
        self.database = database
        self.meter = meter
        self.room_num = room_num
        self.rooms = rooms
        
    def recieve(self, kvartira: str=KVARTIRA,
                      meter: str=METER,
                      room_num: str=ROOM_NUM) -> None:
        # Читает из базы данных словарь за последний запуск программы,
        # задает атрибутам значения из него. Если базы нет, создает новый файл,
        # задает атрибутам нулевые значения.
        try:
            with open(self.database) as database:
                recent = []
                for line in database:
                    recent.append(eval(line))
            last_line = recent[-1]
            print()
            print('Данные за предыдущий период:')
            pprint.pprint(last_line)
            print()
            print()
            self.meter = last_line[kvartira][meter]
            self.room_num = last_line[kvartira][room_num]
            self.rooms = last_line
        except FileNotFoundError:
            pass


class GeneralData:
    """Класс, содержащий в качестве атрибутов общие данниые по квартире,
    необходимые для рассчетов."""
    def __init__(self,
                 meter: int=None, 
                 room_num: int=None,
                 tarif: float=None,
                 consumption: int=None,
                 communal_per_person: int=None) -> None:
        self.meter = meter
        self.room_num = room_num
        self.tarif = tarif
        self.consumption = consumption
        self.communal_per_person = communal_per_person

    def input(self, recent_room_num: int, 
                    int_reader,
                    float_reader) -> None:
        # Вводим значения общих данных по квартире.
        self.tarif = float_reader('Текущий тариф (в руб.): ')
        print()
        if recent_room_num == 0:
            # При первом запуске указываем количество комнат.
            self.room_num = int_reader('Укажите количество комнат в квартире: ')
            print()
        else:
            self.room_num = recent_room_num
        self.meter = int_reader('Введите показания общего счетчика: ')
        print()

    def calculate_consumption(self, recent_meter: int) -> None:
        # Рассчитываем общее потребление электроэнергии в квартире.
        self.consumption = self.meter - recent_meter

    def calculate_communal_per_person(self, rooms: dict, 
                                            room_n: str=ROOM_N,
                                            consumption: str=CONSUMPTION,
                                            humans: str=HUMANS) -> None:
        # Рассчитываем затраты на коммунальное потребление с каждого проживающего.
        persons = 0
        communal_consumption = self.consumption
        for num in range(self.room_num):
            room = rooms[room_n + str(num+1)]
            persons += room[humans]
            communal_consumption -= room[consumption]
        self.communal_per_person = self.tarif * communal_consumption / persons


class RoomsData:
    """Класс, содержащий в качестве атрибута 
    словари данных по каждой комнате."""
    def __init__(self, rooms: dict={}) -> None:
        self.rooms = rooms

    def input(self, room_num: int,
                    int_reader, 
                    float_reader,
                    room_n: str=ROOM_N,
                    meter: str=METER,
                    humans: str=HUMANS,
                    debt: str=DEBT) -> None:
        # Вводим значения данных по каждой комнате и заносим их в словарь.
        for num in range (room_num):
            self.rooms[room_n + str(num+1)] = {}
            room = self.rooms[room_n + str(num+1)]

            room[meter] = int_reader('Введите показания счетчика комнаты номер '
                                      + str(num+1) + ': ')
            room[humans] = int_reader('Количество проживающих в комнате: ')
            room[debt] = float_reader('Долг за прошедший период (руб.): ')
            print()
     
    def calculate_consumption(self, room_num: int,
                                    recent_room_num: int,
                                    recent_rooms: dict,
                                    room_n: str=ROOM_N,
                                    meter: str=METER,
                                    consumption: str=CONSUMPTION) -> None:
        # Рассчитываем потребление энергии в каждой комнате.
        if recent_room_num == 0:
            for num in range(room_num):
                room = self.rooms[room_n + str(num+1)]
                room[consumption] = room[meter]
        else:
            for num in range (room_num):
                room = self.rooms[room_n + str(num+1)]
                room[consumption] = (room[meter] - 
                                     recent_rooms[room_n + str(num+1)][meter])

    def calculate_accounts(self, room_num: int,
                                 tarif: float,
                                 communal_per_person: float,
                                 room_n: str=ROOM_N,
                                 consumption: str=CONSUMPTION,
                                 room_cost: str=ROOM_COST,
                                 communal_cost: str=COMM_COST,
                                 humans: str=HUMANS,
                                 debt: str=DEBT,
                                 total: str=TOTAL) -> None:
        # Рассчитываем стоимость потребления электроэнергии в каждой комнате,
        # затраты на коммунальный расход, исходя из числа проживающих в ней человек,
        # а также итоговую сумму счета по комнате.
        for num in range (room_num):
            room = self.rooms[room_n + str(num+1)]
            room[room_cost] = room[consumption] * tarif
            room[communal_cost] = communal_per_person * room[humans]
            room[total] = room[communal_cost] + room[room_cost] + room[debt]


class AllNewData:
    """Класс, собирающий в себя все необходимые данные, чтобы выводить их
    пользователю и сохранять в базе данных."""
    def __init__(self, data: dict={}) -> None:
        self.data = data

    def collect(self, today: str,
                      room_num: int,
                      general_meter: int, 
                      tarif: float,
                      general_consumption: int,
                      communal_per_person: int,
                      rooms: dict,
                      date: str=DATE,
                      number: str=ROOM_NUM,
                      trf: str=TARIF,
                      kvartira: str=KVARTIRA,
                      meter: str=METER,
                      consumption: str=CONSUMPTION,
                      comm_per_person: str=COMM_PER_PERSON) -> None:
        gen_data = {}
        gen_data[date] = today
        gen_data[meter] = general_meter
        gen_data[trf] = tarif
        gen_data[number] = room_num
        gen_data[consumption] = general_consumption
        gen_data[comm_per_person] = communal_per_person
        self.data[kvartira] = gen_data
        self.data.update(rooms)

    def output_all(self, room_num: int,
                         room_n: str=ROOM_N,
                         room_cost: str=ROOM_COST,
                         comm_cost: str=COMM_COST,
                         debt: str=DEBT,
                         total: str=TOTAL) -> None:
        # Выводит на экран счета для всех комнат.
        for num in range (room_num):
            room = self.data[room_n + str(num+1)]
        
            print ('Комната номер', num+1, ':')
            print ('Индивидуальное потребление: ', '%.2f' % room[room_cost], 'руб.')
            print ('За коммунальное: ', '%.2f' % room[comm_cost], 'руб.')
            if room[debt] > 0:
                print ('Задолженность: ', '%.2f' % room[debt], 'руб.')
            print ('ИТОГО: ', '%.2f' % room[total], 'руб.')
            print()

    def output_room(self, room_id: int,
                          room_n: str=ROOM_N,
                          room_cost: str=ROOM_COST,
                          comm_cost: str=COMM_COST,
                          debt: str=DEBT,
                          total: str=TOTAL) -> None:
        # Выводит на экран счет для указанной комнаты.
        room = self.data[room_n + str(room_id)]
        
        print ('Комната номер', room_id, ':')
        print ('Индивидуальное потребление: ', '%.2f' % room[room_cost], 'руб.')
        print ('За коммунальное: ', '%.2f' % room[comm_cost], 'руб.')
        if room[debt] > 0:
            print ('Задолженность: ', '%.2f' % room[debt], 'руб.')
        print ('ИТОГО: ', '%.2f' % room[total], 'руб.')
        print()

    def add_to_db(self, datafile: str='database.txt') -> None:
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
    while digit_value.isdigit() == False:
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


def print_greetings(ver: str, date: str) -> None:
    # Выводит на экран приветствие, номер версии и текущую дату.
    print()
    print('Рассчет оплаты электроэнергии в коммунальной квартире.')
    print('Версия: ', ver)
    print('Сегодня на календаре: ', date)
    print()


def print_results_by_user_command(room_num: int,
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
            new_data.output_all(room_num)
            print()
            command = str(input(instruction))
            print()
        else:
            while True:
                try:
                    if 0 < int(command) <= room_num:
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


version = '0.1.2'
today = datetime.date.isoformat(datetime.date.today())
datafile = 'database.txt'

print_greetings(version, today)

int_reader = lambda x: digit_data_input(x)
float_reader = lambda x: float_data_input(x)

recent = RecentData()
general = GeneralData()
rooms = RoomsData()
new_data = AllNewData()

recent.recieve()
general.input(recent.room_num, int_reader, float_reader)

room_num = general.room_num
rooms.input(room_num, int_reader, float_reader)

general.calculate_consumption(recent.meter)
rooms.calculate_consumption(room_num,
                            recent.room_num,
                            recent.rooms)
general.calculate_communal_per_person(rooms.rooms)
rooms.calculate_accounts(room_num, 
                         general.tarif, 
                         general.communal_per_person)
new_data.collect(today, 
                 room_num, 
                 general.meter, 
                 general.tarif,
                 general.consumption,
                 general.communal_per_person,
                 rooms.rooms)

print_results_by_user_command(room_num,
                              new_data)

new_data.add_to_db()