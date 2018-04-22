import datetime
import time
import pprint

print('Запущена программа для рассчета оплаты потребленной электроэнергии в коммунальной квартире №52.')

now = datetime.date.isoformat(datetime.date.today())
print('Сегодня на календаре: ', now)
print()

# тут должна подгружаться база предыдущих запусков программы,
# но я еще не знаю, как работать с внешними файлами
k52 = {}
# временное значение для данных:
temp = 0

tarif = float(input('Текущий тариф (в руб.): '))
k52[now] = {'Tarif': tarif}
print()

room_num = int(input('Укажите количество комнат в квартире: '))
print()

watt_kv = int(input('Введите показания общего счетчика: '))
print()

k52[now]['Kvartira'] = {}
kvar = k52[now]['Kvartira']
kvar['Meter'] = watt_kv
cons_kv = watt_kv - temp
kvar['Consumption'] = cons_kv

joint_kv = cons_kv
humans_kv = 0
for num in range (room_num):
    k52[now]['Room_' + str(num+1)] = {}
    room = k52[now]['Room_' + str(num+1)]
    
    print('Введите показания счетчика комнаты номер', num+1, end=': ')
    watt = int(input())
    room['Meter'] = watt
    
    cons = watt - temp
    room['Consumption'] = cons
    
    personal = cons * tarif
    room['Personal_cost'] = personal
    
    humans = int(input('Количество проживающих в комнате: '))
    room['Humans'] = humans
    
    humans_kv += humans
    kvar['Humans'] = humans_kv
    
    debt = float(input('Задолженность за прошедший период (руб.): '))
    room['Debt'] = debt
    
    joint_kv -= watt
    kvar['Joint'] = joint_kv
    print()

input('Чтобы получить результат вычислений, нажмите "Enter". ')
print()

kvar['Joint_per_person'] = joint_kv * tarif / humans_kv
kvar['Joint_cost'] = joint_kv * tarif
j_per_per = kvar['Joint_per_person']

for num in range (len(k52[now]) - 2):
    room = k52[now]['Room_' + str(num+1)]
    
    joint = j_per_per * room['Humans']
    room['Joint_cost'] = joint
    
    room['Total'] = joint + room['Personal_cost'] + room['Debt']
    
    print ('Комната номер', num+1, ':')
    print ('Индивидуальное потребление: ', '%.2f' % room['Personal_cost'], 'руб.')
    print ('За коммунальное: ', '%.2f' % room['Joint_cost'], 'руб.')
    if room['Debt'] > 0:
        print ('Задолженность: ', '%.2f' % room['Debt'], 'руб.')
    print ('ИТОГО: ', '%.2f' % room['Total'], 'руб.')
    print()

time.sleep(1.4)
input('Для завершения программы нажмите "Enter".')

