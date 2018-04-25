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

# переменная-заглушка, в качестве временного решения, как точка отсчета
# вместо прошлых показаний каких-либо счетчиков или других данных:
temporary_value = 0

# создаем словарь, в будущих версиях он будет не создаваться, а подгружаться
# и содержать в себе данные прошлых подсчетов
electro_database = {}
electro_database[today] = {}
electro_database[today][KVARTIRA] = {}
electro_database[today][TARIF] = {}

kvartira = electro_database[today][KVARTIRA]
tarif = electro_database[today][TARIF]

print('Запущена программа для рассчета оплаты потребленной электроэнергии в\
 коммунальной квартире №52.')
print('Версия: 0.0.3')
print('Сегодня на календаре: ', today)
print()
tarif = float(input('Текущий тариф (в руб.): '))
print()
room_num = int(input('Укажите количество комнат в квартире: '))
print()
kvartira[METER] = int(input('Введите показания общего счетчика: '))
print()

kvartira[CONSUMPTION] = kvartira[METER] - temporary_value
kvartira[COMM_CONSUMPTION] = kvartira[CONSUMPTION]
kvartira[HUMANS] = 0

for num in range (room_num):
    electro_database[today][ROOM_N + str(num+1)] = {}
    room = electro_database[today][ROOM_N + str(num+1)]

    print('Введите показания счетчика комнаты номер', num+1, end=': ')
    room[METER] = int(input())
    room[HUMANS] = int(input('Количество проживающих в комнате: '))
    room[DEBT] = float(input('Задолженность за прошедший период (руб.): '))
    room[CONSUMPTION] = room[METER] - temporary_value
    room[ROOM_COST] = room[CONSUMPTION] * tarif
    kvartira[HUMANS] += room[HUMANS]
    kvartira[COMM_CONSUMPTION] -= room[METER]
    print()

input('Чтобы получить результат вычислений, нажмите "Enter". ')
print()

kvartira[COMM_COST] = kvartira[COMM_CONSUMPTION] * tarif
kvartira[COMM_PER_PERSON] = kvartira[COMM_CONSUMPTION] * tarif / kvartira[HUMANS]

for num in range (room_num):
    room = electro_database[today][ROOM_N + str(num+1)]
    
    room[COMM_COST] = kvartira[COMM_PER_PERSON] * room[HUMANS]
    room[TOTAL] = room[COMM_COST] + room[ROOM_COST] + room[DEBT]
    
    print ('Комната номер', num+1, ':')
    print ('Индивидуальное потребление: ', '%.2f' % room[ROOM_COST], 'руб.')
    print ('За коммунальное: ', '%.2f' % room[COMM_COST], 'руб.')
    if room[DEBT] > 0:
        print ('Задолженность: ', '%.2f' % room[DEBT], 'руб.')
    print ('ИТОГО: ', '%.2f' % room[TOTAL], 'руб.')
    print()

time.sleep(1)
input('Для завершения программы нажмите "Enter".')

# Для самоконтроля вывожу словарь использованных данных:
print()
pprint.pprint(electro_database)
input()
