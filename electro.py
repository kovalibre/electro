import pprint
import time
import datetime

today = datetime.date.isoformat(datetime.date.today())
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
"888" - вывести словарь всех данных и завершить работу.\n \
"999" - завершить работу.\n \
 №: '

# переменная-заглушка, в качестве временного решения, как точка отсчета
# вместо прошлых показаний каких-либо счетчиков или других данных:
temporary_value = 0

# создаем словарь, в будущих версиях он будет не создаваться, а подгружаться
# и содержать в себе данные прошлых подсчетов
electro_database = {}
electro_database[today] = {}
electro_database[today][KVARTIRA] = {}
kvartira = electro_database[today][KVARTIRA]


def digit_data_input(string_for_check):
    # Цикл проверки строки ввода для целочисленных значений.
    # В случае получения иных данных выдает сообщение пользователю.
    # Возвращает целое число.
    digit_value = input(string_for_check)
    while digit_value.isdigit() == False:
        print()
        time.sleep(0.5)
        print(INPUT_ERROR)
        print()
        digit_value = input(string_for_check)
    return int(digit_value)


def float_data_input(string_for_check):
    # Цикл проверки строки ввода для float-значений.
    # В случае получения иных данных выдает сообщение пользователю.
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


def calculate_all_rooms_account(room_id):
    # Выводит на экран рассчет стоимости по всем комнатам.
    for num in range (room_num):
        room = electro_database[today][ROOM_N + str(num+1)]
    
        print ('Комната номер', num+1, ':')
        print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
        print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
        if room[DEBT] > 0:
            print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
        print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
        print()


def calculate_room_account (room_id):
    # Выводит на экран рассчет стоимости для указанной комнаты.
    room = electro_database[today][ROOM_N + str(room_id)]
    
    print ('Комната номер', room_id, ':')
    print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
    print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
    if room[DEBT] > 0:
        print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
    print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
    print()


print()
print('Запущена программа для рассчета оплаты потребленной электроэнергии в\
 коммунальной квартире №52.')
print('Версия: 0.0.3')
print('Сегодня на календаре: ', today)
print()
tarif = float_data_input('Текущий тариф (в руб.): ')
print()
room_num = digit_data_input('Укажите количество комнат в квартире: ')
print()
kvartira[METER] = digit_data_input('Введите показания общего счетчика: ')
print()

kvartira[TARIF] = tarif
kvartira[CONSUMPTION] = kvartira[METER] - temporary_value
kvartira[COMM_CONSUMPTION] = kvartira[CONSUMPTION]
kvartira[HUMANS] = 0

for num in range (room_num):
    electro_database[today][ROOM_N + str(num+1)] = {}
    room = electro_database[today][ROOM_N + str(num+1)]

    room[METER] = digit_data_input(
        'Введите показания счетчика комнаты номер '+ str(num+1) + ': ')
    room[HUMANS] = digit_data_input('Количество проживающих в комнате: ')
    room[DEBT] = float_data_input('Долг за прошедший период (руб.): ')
    room[CONSUMPTION] = room[METER] - temporary_value
    room[ROOM_COST] = room[CONSUMPTION] * tarif
    kvartira[HUMANS] += room[HUMANS]
    kvartira[COMM_CONSUMPTION] -= room[METER]
    print()

kvartira[COMM_COST] = kvartira[COMM_CONSUMPTION] * tarif
kvartira[COMM_PER_PERSON] = kvartira[COMM_CONSUMPTION] * tarif / kvartira[HUMANS]

for num in range (room_num):
    room = electro_database[today][ROOM_N + str(num+1)]

    room[COMM_COST] = kvartira[COMM_PER_PERSON] * room[HUMANS]
    room[TOTAL] = room[COMM_COST] + room[ROOM_COST] + room[DEBT]

print()
room_id = digit_data_input(INSTRUCTION)
print()

while room_id != 999:
    if 0 < room_id <= room_num:
        print()
        calculate_room_account(room_id)
        print()
        room_id = digit_data_input(INSTRUCTION)
        print()
    elif room_id == 888:
        print()
        pprint.pprint(electro_database)
        print()
        time.sleep(1)
        input('Для завершения программы нажмите "Enter".')
        break
    elif room_id == 0:
        calculate_all_rooms_account(room_id)
        print()
        room_id = digit_data_input(INSTRUCTION)
        print()
    else:
        print()
        print(INPUT_ERROR)
        print()
        room_id = digit_data_input(INSTRUCTION)
        print()