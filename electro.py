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
COMM_COST = 'Общая стоимость коммунального потребления'
COMM_PER_PERSON = 'Стоимость коммунального потребления с человека'
ROOM_COST = 'Стоимость потребления в комнате'
DEBT = 'Задолженность'
TOTAL = 'ИТОГО'
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
        print('ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ!')
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
            print('ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ!')
            print()
            float_value = input(string_for_check)
    return float(float_value)


def print_greetings(ver, date) -> None:
    # Выводит на экран приветствие, номер версии и текущую дату.
    print()
    print('Рассчет оплаты электроэнергии в коммунальной квартире.')
    print('Версия: ', ver)
    print('Сегодня на календаре: ', date)
    print()


def recieve_recent_data(datafile) -> dict:
    # Возвращает из базы словарь данных за последний запуск программы.
    # Если базы нет, создает новый файл со списком словарей внутри
    # и возвращает словарь с нулевыми значениями.
    try:
        with open(datafile) as database:
            recent = []
            for line in database:
                recent.append(eval(line))
    except FileNotFoundError:
        with open(datafile, 'x') as database:
            zero_data = {}
            zero_data[KVARTIRA] = {}
            zero_data[KVARTIRA][METER] = 0
            zero_data[KVARTIRA][ROOM_NUM] = 0
            print(zero_data, file=database)
        with open(datafile) as database:
            recent = []
            for line in database:
                recent.append(eval(line))
    return recent[-1]


def input_general_data(recent) -> dict:
    # Вводим значения общих данных по квартире и заносим их в словарь.
    gen_data = {}
    gen_data[TARIF] = float_data_input('Текущий тариф (в руб.): ')
    print()
    if recent[KVARTIRA][ROOM_NUM] == 0:
        # При первом запуске указываем количество комнат.
        gen_data[ROOM_NUM] = digit_data_input(
                            'Укажите количество комнат в квартире: ')
        print()
    else:
        gen_data[ROOM_NUM] = recent[KVARTIRA][ROOM_NUM]
    gen_data[METER] = digit_data_input('Введите показания общего счетчика: ')

    return gen_data


def input_rooms_data(gen_data) -> dict:   
    # Вводим значения данных по каждой комнате и заносим их в словарь.
    rms_data = {}
    for num in range (gen_data[ROOM_NUM]):
        rms_data[ROOM_N + str(num+1)] = {}
        room = rms_data[ROOM_N + str(num+1)]

        room[METER] = digit_data_input(
            'Введите показания счетчика комнаты номер '+ str(num+1) + ': ')
        room[HUMANS] = digit_data_input('Количество проживающих в комнате: ')
        room[DEBT] = float_data_input('Долг за прошедший период (руб.): ')
    return rms_data


def calculate_general_consumption(gen_data, recent) -> int:
    # Рассчитываем общее потребление электроэнергии в квартире, 
    return gen_data[METER] - recent[KVARTIRA][METER]


def calculate_rooms_consumption(gen_data, recent, rms_data) -> dict:
    # Рассчитываем потребление энергии в каждой комнате.
    rooms_cons = {}
    if recent[KVARTIRA][ROOM_NUM] == 0:
        for num in range(gen_data[ROOM_NUM]):
            r_num = ROOM_N + str(num+1)
            rooms_cons[r_num] = {}
            rooms_cons[r_num][CONSUMPTION] = rms_data[r_num][METER]
    else:
        for num in range (gen_data[ROOM_NUM]):
            r_num = ROOM_N + str(num+1)
            rooms_cons[r_num]= {}
            rooms_cons[r_num][CONSUMPTION] = (rms_data[r_num][METER] - 
                                              recent[r_num][METER])
    return rooms_cons


def calculate_communal_data(gen_data, rms_data, gen_cons, rms_cons) -> float:
    # Рассчитываем затраты на коммунальное потребление с каждого проживающего.
    humans = 0
    comm_cons = gen_cons

    for num in range(gen_data[ROOM_NUM]):
        r_num = ROOM_N + str(num+1)
        humans += rms_data[r_num][HUMANS]
        comm_cons -= rms_cons[r_num][CONSUMPTION]

    return gen_data[TARIF] * comm_cons / humans


def calculate_rooms_accounts(gen_data, rms_data, rms_cons, comm_data) -> dict:
    # Рассчитываем стоимость потребления электроэнергии в каждой комнате,
    # затраты на коммунальный расход, исходя из числа проживающих в ней человек,
    # а также итоговую сумму счета по комнате.
    rooms_acc = {}
    for num in range (gen_data[ROOM_NUM]):
        r_num = ROOM_N + str(num+1)
        rooms_acc[r_num] = {}
        rooms_acc[r_num][ROOM_COST] = (rms_cons[r_num][CONSUMPTION] * 
                                       gen_data[TARIF])        
        rooms_acc[r_num][COMM_COST] = (comm_data * 
                                       rms_data[r_num][HUMANS])        
        rooms_acc[r_num][TOTAL]     = (rooms_acc[r_num][COMM_COST] + 
                                       rooms_acc[r_num][ROOM_COST] + 
                                       rms_data[r_num][DEBT])        
    return rooms_acc


def collect_new_data(today, gen_data, rms_data, gen_cons, rms_cons, 
                     comm_data, rms_acc) -> dict:
    n_data = {}
    gen_data[DATE] = today
    gen_data[CONSUMPTION] = gen_cons
    gen_data[COMM_PER_PERSON] = comm_data
    n_data[KVARTIRA] = gen_data
    for num in range (gen_data[ROOM_NUM]):
        rm_data = rms_data[ROOM_N + str(num+1)]
        rm_acc = rms_acc[ROOM_N + str(num+1)]
        rm_data.update(rm_acc)
        n_data[ROOM_N + str(num+1)] = rm_data
    return n_data


def output_room_account (room_id, n_data):
    # Выводит на экран счет для указанной комнаты.
    room = n_data[ROOM_N + str(room_id)]
    
    print ('Комната номер', room_id, ':')
    print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
    print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
    if room[DEBT] > 0:
        print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
    print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
    print()


def output_all_rooms_account(n_data):
    # Выводит на экран счета для всех комнат.
    for num in range (n_data[KVARTIRA][ROOM_NUM]):
        room = n_data[ROOM_N + str(num+1)]
    
        print ('Комната номер', num+1, ':')
        print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
        print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
        if room[DEBT] > 0:
            print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
        print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
        print()


def print_results_by_user_command(recent, n_data):
    # Выводит на экран инструкцию для пользователя, и, в зависимости от
    # полученной команды, вызывает соответствующую функцию.
    print()
    room_id = digit_data_input(INSTRUCTION)
    print()
    while room_id != 999:
        # Пока не введена команда "999" (выход из программы), выполняется цикл:
        if 0 < room_id <= n_data[KVARTIRA][ROOM_NUM]:
            # получение счета по номеру комнаты,
            print()
            output_room_account(room_id, n_data)
            print()
            room_id = digit_data_input(INSTRUCTION)
            print()
        elif room_id == 0:
            # получение счета для всех комнат,
            output_all_rooms_account(n_data)
            print()
            room_id = digit_data_input(INSTRUCTION)
            print()
        elif room_id == 888:
            # получение словаря данных за предыдущий период,
            print()
            pprint.pprint(recent)
            print()
            input('Для завершения программы нажмите "Enter".')
            break
        else:
            # сообщение об ошибке в прочих случаях.
            print()
            print('ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ!')
            print()
            room_id = digit_data_input(INSTRUCTION)
            print()


def add_new_data_to_database(n_data, datafile):
    # Вносит новые данные в файл базы.
    with open(datafile, 'a') as database:
        print(n_data, file=database)


version = '0.1.1'
today = datetime.date.isoformat(datetime.date.today())
datafile = 'database.txt'

print_greetings(version, today)

recent_data = recieve_recent_data(datafile)
general_data = input_general_data(recent_data)
rooms_data = input_rooms_data(general_data)

general_consumption = calculate_general_consumption(general_data, 
                                                    recent_data)

rooms_consumption = calculate_rooms_consumption(general_data,
                                                recent_data,
                                                rooms_data)

communal_data = calculate_communal_data(general_data,
                                        rooms_data,
                                        general_consumption,
                                        rooms_consumption)

rooms_accounts = calculate_rooms_accounts(general_data,
                                          rooms_data,
                                          rooms_consumption,
                                          communal_data)
new_data = collect_new_data(today,
                            general_data,
                            rooms_data,
                            general_consumption,
                            rooms_consumption,
                            communal_data,
                            rooms_accounts)

print_results_by_user_command(recent_data,
                              new_data)

add_new_data_to_database(new_data, datafile)
