import pprint
import time
import datetime

TODAY = datetime.date.isoformat(datetime.date.today())
TARIF = 'Тариф на электроэнергию'
KVARTIRA = 'Квартира'
ROOM_N = 'Комната_'
METER = 'Счетчик'
HUMANS = 'Проживающих'
CONSUMPTION = 'Потребление'
COMM_CONSUMP = 'Коммунальное потребление'
COMM_COST = 'Общая стоимость коммунального потребления'
COMM_PER_PERSON = 'Стоимость коммунального потребления с человека'
ROOM_COST = 'Стоимость с комнаты'
DEBT = 'Задолженность'
TOTAL = 'ИТОГО'

# переменная-заглушка, в качестве временного решения, как точка отсчета
# вместо прошлых показаний каких-либо счетчиков или других данных:
temporary_value = 0

# создаем словарь, в будущих версиях он будет не создаваться, а подгружаться
# и содержать в себе данные прошлых подсчетов
k52 = {}
k52[TODAY] = {}
k52[TODAY][KVARTIRA] = {}
KV = k52[TODAY][KVARTIRA]

print('Запущена программа для рассчета оплаты потребленной электроэнергии в коммунальной квартире №52.')
print('Версия: 0.0.2')
print('Сегодня на календаре: ', TODAY)
print()
tarif = float(input('Текущий тариф (в руб.): '))
print()
room_num = int(input('Укажите количество комнат в квартире: '))
print()
watt_main = int(input('Введите показания общего счетчика: '))
print()

consumption_main = watt_main - temporary_value
communal_main = consumption_main
humans_main = 0

for num in range (room_num):
    print('Введите показания счетчика комнаты номер', num+1, end=': ')
    watt = int(input())
    humans = int(input('Количество проживающих в комнате: '))
    debt = float(input('Задолженность за прошедший период (руб.): '))
    consumption = watt - temporary_value
    
    k52[TODAY][ROOM_N + str(num+1)] = {}
    ROOM = k52[TODAY][ROOM_N + str(num+1)]
    
    ROOM[METER] = watt
    ROOM[HUMANS] = humans
    ROOM[DEBT] = debt
    ROOM[CONSUMPTION] = consumption
    ROOM[ROOM_COST] = consumption * tarif
    
    humans_main += humans
    communal_main -= watt
    print()

input('Чтобы получить результат вычислений, нажмите "Enter". ')
print()

k52[TODAY][TARIF] = tarif
KV[METER] = watt_main
KV[HUMANS] = humans_main
KV[CONSUMPTION] = consumption_main
KV[COMM_CONSUMP] = communal_main
KV[COMM_COST] = communal_main * tarif
KV[COMM_PER_PERSON] = communal_main * tarif / humans_main

for num in range (room_num):
    ROOM = k52[TODAY][ROOM_N + str(num+1)]
    
    ROOM[COMM_COST] = KV[COMM_PER_PERSON] * ROOM[HUMANS]
    ROOM[TOTAL] = ROOM[COMM_COST] + ROOM[ROOM_COST] + ROOM[DEBT]
    
    print ('Комната номер', num+1, ':')
    print ('Индивидуальное потребление: ', '%.2f' % ROOM[ROOM_COST], 'руб.')
    print ('За коммунальное: ', '%.2f' % ROOM[COMM_COST], 'руб.')
    if ROOM[DEBT] > 0:
        print ('Задолженность: ', '%.2f' % ROOM[DEBT], 'руб.')
    print ('ИТОГО: ', '%.2f' % ROOM[TOTAL], 'руб.')
    print()

time.sleep(1.4)
input('Для завершения программы нажмите "Enter".')

# Для самоконтроля вывожу словарь использованных данных:
print()
pprint.pprint(k52)
