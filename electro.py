import pprint
import time
import datetime

DATE = 'Дата'
ROOM_NUM = 'Количество комнат'
TARIF = 'Тариф на электроэнергию'
KVARTIRA = 'Квартира'
ROOM_N = 'Комната_'
METER = 'Показания счетчика'
HUMANS = 'Количество проживающих'
CONSUMPTION = 'Потребление энергии (кВт)'
COMM_CONSUMPTION = 'Потребление в местах общего пользования (коммунальное)'
COMM_COST = 'Общая стоимость коммунального потребления'
COMM_PER_PERSON = 'Стоимость коммунального потребления с человека'
ROOM_COST = 'Стоимость потребления в комнате'
DEBT = 'Задолженность'
TOTAL = 'ИТОГО'
INPUT_ERROR = 'ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ!'
INSTRUCTION = ' Чтобы получить рассчет по комнате, введите ее номер.\n \
"0" - чтобы получить рассчет по всем комнатам.\n \
"888" - вывести словарь данных за предыдущий период и завершить работу.\n \
"999" - завершить работу.\n \
 №: '


def digit_data_input(string_for_check) -> int:
    # Цикл проверки строки ввода для целочисленных значений.
    # В случае получения иных данных выдает сообщение об ошибке пользователю.
    # Возвращает целое число.
    digit_value = input(string_for_check)
    while digit_value.isdigit() == False:
        print()
        time.sleep(0.5)
        print(INPUT_ERROR)
        print()
        digit_value = input(string_for_check)
    return int(digit_value)


def float_data_input(string_for_check) -> float:
    # Цикл проверки строки ввода для float-значений.
    # В случае получения иных данных выдает сообщение об ошибке пользователю.
    # Возвращает float.
    float_value = input(string_for_check)
    while True:
        try:
            float(float_value)
            break
        except ValueError:
            print()
            time.sleep(0.5)
            print(INPUT_ERROR)
            print()
            float_value = input(string_for_check)
    return float(float_value)


def recieve_recent_data() -> dict:
    # Возвращает из базы словарь данных за последний запуск программы.
    # Если базы нет, создает новый файл со списком словарей внутри
    # и возвращает словарь с нулевыми значениями.
    try:
        with open('database.txt') as database:
            recent = []
            for line in database:
                recent.append(eval(line))
    except FileNotFoundError:
        with open('database.txt', 'x') as database:
            zero_data = {}
            zero_data[KVARTIRA] = {}
            zero_data[KVARTIRA][METER] = 0
            zero_data[KVARTIRA][ROOM_NUM] = 0
            print(zero_data, file=database)
        with open('database.txt') as database:
            recent = []
            for line in database:
                recent.append(eval(line))
    return recent[-1]


def create_new_data_dict() -> dict:
    # Создает словарь для новых данных.
    new_data = {}
    new_data[KVARTIRA] = {}
    new_data[KVARTIRA][DATE] = today
    new_data[KVARTIRA][ROOM_NUM] = 0
    return new_data


def print_greetings():
    # Выводит на экран приветствие, номер версии и текущую дату.
    print()
    print('Рассчет оплаты электроэнергии в коммунальной квартире.')
    print('Версия: 0.1.0')
    print('Сегодня на календаре: ', today)
    print()


def input_general_data():
    # Вводим значения общих данных по квартире и заносим их в словарь.
    kvartira[TARIF] = float_data_input('Текущий тариф (в руб.): ')
    print()
    if recent_data[KVARTIRA][ROOM_NUM] == 0:
        # При первом запуске указываем количество комнат.
        kvartira[ROOM_NUM] = digit_data_input(
                             'Укажите количество комнат в квартире: ')
        print()
        # Ниже скрипт, который добавляет нулевые значения счетчика для каждой
        # комнаты согласно их количеству в словарь прошлых данных,
        # если программа запущена впервые.
        # СТОИТ ЛИ КАК-ТО ОБОСОБИТЬ ЭТОТ ФРАГМЕНТ В ОТДЕЛЬНУЮ ФУНКЦИЮ?
        for num in range (kvartira[ROOM_NUM]):
                recent_data[ROOM_N + str(num+1)] = {}
                room = recent_data[ROOM_N + str(num+1)]
                room[METER] = 0
                room[DEBT] = 0
    else:
        kvartira[ROOM_NUM] = recent_data[KVARTIRA][ROOM_NUM]
    kvartira[METER] = digit_data_input('Введите показания общего счетчика: ')
    print()


def input_rooms_data():
    # Вводим значения данных по каждой комнате и заносим их в словарь.
    for num in range (room_num):
        new_data[ROOM_N + str(num+1)] = {}
        room = new_data[ROOM_N + str(num+1)]

        room[METER] = digit_data_input(
            'Введите показания счетчика комнаты номер '+ str(num+1) + ': ')
        room[HUMANS] = digit_data_input('Количество проживающих в комнате: ')
        room[DEBT] = float_data_input('Долг за прошедший период (руб.): ')
        print()


def calculate_general_consumption():
    # Рассчитываем общее потребление электроэнергии в квартире, 
    kvartira[CONSUMPTION] = kvartira[METER] - recent_data[KVARTIRA][METER]


def calculate_rooms_consumption():
    # Рассчитываем потребление энергии в каждой комнате.
    for num in range (room_num):
        room = new_data[ROOM_N + str(num+1)]
        room[CONSUMPTION] = room[METER] - recent_data[ROOM_N + str(num+1)][METER]


def calculate_communal_costs():
    # Рассчитываем затраты на коммунальное потребление с каждого проживающего.
    kvartira[COMM_CONSUMPTION] = kvartira[CONSUMPTION]
    kvartira[HUMANS] = 0
    for num in range (room_num):
        room = new_data[ROOM_N + str(num+1)]
        kvartira[HUMANS] += room[HUMANS]
        kvartira[COMM_CONSUMPTION] -= room[CONSUMPTION]

    kvartira[COMM_COST] = kvartira[COMM_CONSUMPTION] * kvartira[TARIF]
    kvartira[COMM_PER_PERSON] = kvartira[TARIF] * (kvartira[COMM_CONSUMPTION] / 
                                                   kvartira[HUMANS])

def calculate_rooms_costs():
    # Рассчитываем стоимость потребления электроэнергии в каждой комнате,
    # затраты на коммунальный расход, исходя из числа проживающих в ней человек,
    # а также итоговую сумму счета по комнате.
    for num in range (room_num):
        room = new_data[ROOM_N + str(num+1)]

        room[ROOM_COST] = room[CONSUMPTION] * kvartira[TARIF]
        room[COMM_COST] = kvartira[COMM_PER_PERSON] * room[HUMANS]
        room[TOTAL] = room[COMM_COST] + room[ROOM_COST] + room[DEBT]
        


def output_all_rooms_account():
    # Выводит на экран счета для всех комнат.
    for num in range (room_num):
        room = new_data[ROOM_N + str(num+1)]
    
        print ('Комната номер', num+1, ':')
        print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
        print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
        if room[DEBT] > 0:
            print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
        print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
        print()


def output_room_account (room_id):
    # Выводит на экран счет для указанной комнаты.
    room = new_data[ROOM_N + str(room_id)]
    
    print ('Комната номер', room_id, ':')
    print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
    print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
    if room[DEBT] > 0:
        print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
    print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
    print()


def print_results_by_user_command():
    # Выводит на экран инструкцию для пользователя, и, в зависимости от
    # полученной команды, вызывает соответствующую функцию.
    print()
    room_id = digit_data_input(INSTRUCTION)
    print()
    while room_id != 999:
        # Пока не введена команда "999" (выход из программы), выполняется цикл:
        if 0 < room_id <= room_num:
            # получение счета по номеру комнаты,
            print()
            output_room_account(room_id)
            print()
            room_id = digit_data_input(INSTRUCTION)
            print()
        elif room_id == 0:
            # получение счета для всех комнат,
            output_all_rooms_account()
            print()
            room_id = digit_data_input(INSTRUCTION)
            print()
        elif room_id == 888:
            # получение словаря данных за предыдущий период,
            print()
            pprint.pprint(recent_data)
            print()
            time.sleep(1)
            input('Для завершения программы нажмите "Enter".')
            break
        else:
            # сообщение об ошибке в прочих случаях.
            print()
            print(INPUT_ERROR)
            print()
            room_id = digit_data_input(INSTRUCTION)
            print()


def add_new_data_to_database():
    # Вносит новые данные в файл базы.
    with open('database.txt', 'a') as database:
        print(new_data, file=database)


today = datetime.date.isoformat(datetime.date.today())
recent_data = recieve_recent_data()
new_data = create_new_data_dict()
kvartira = new_data[KVARTIRA]

print_greetings()
input_general_data()

room_num = kvartira[ROOM_NUM]

input_rooms_data()
calculate_general_consumption()
calculate_rooms_consumption()
calculate_communal_costs()
calculate_rooms_costs()

print_results_by_user_command()
add_new_data_to_database()