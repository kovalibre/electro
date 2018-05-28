import pprint
import datetime

class Apartment():
    # Класс, отвечающий за хранение и вычисление данных по квартире.
    def __init__(self,
                 meter=0):
        self.meter = meter
        
    def consumption(self, recent_apartment_meter):
        # Рассчет общего энергопотребления во всей квартире.
        return self.meter - recent_apartment_meter

    def communal_per_person(self, tariff, recent_apartment_meter, 
                            rooms, recent_rooms):
        # Рассчет стоимости энергии, потребленной в местах 
        # общего пользования, на каждого из жильцов.
        humans = 0
        rooms_consumption = 0
        r = 0
        for room in rooms:
            humans += room.humans
            recent_room = recent_rooms[r]
            rooms_consumption += room.consumption(recent_room.meter)
            r+=1
        return (self.meter - recent_apartment_meter - 
                rooms_consumption) * tariff / humans


class Room():
  # Класс, отвечающий за хранение и вычисление данных по конкретной комнате.
    def __init__(self,
                 meter=0,
                 humans=0,
                 debt=0):
        self.meter = meter
        self.humans = humans
        self.debt = debt
    
    def consumption(self, recent_room_meter):
        # Рассчет энергопотребления внутри комнаты.
        return self.meter - recent_room_meter

    def account(self, tariff, recent_room_meter, communal_per_person):
        # Вычисление счета по комнате, в трех пунктах: 
        # - Стоимость энергопотребления внутри комнаты, 
        # - Стоимость коммунальной энергии, исходя из числа жильцов,
        # - Долг. 
        # А также итоговая сумма этих величин.
        room_cost = tariff * (self.meter - recent_room_meter)
        communal_cost = communal_per_person * self.humans
        total = room_cost + communal_cost + self.debt
        return (room_cost, communal_cost, self.debt, total)


def digit_data_input(string_for_check):
    # Цикл проверки строки ввода для целочисленных значений.
    # Возвращает целое число.
    digit_value = input(string_for_check)
    while not digit_value.isdigit():
        print('\n ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ! \n')
        digit_value = input(string_for_check)
    return int(digit_value)


def float_data_input(string_for_check):
    # Цикл проверки строки ввода для float-значений.
    # Возвращает float.
    float_value = input(string_for_check)
    while True:
        try:
            float(float_value)
            break
        except ValueError:
            print('\n ВВЕДИТЕ КОРРЕКТНОЕ ЗНАЧЕНИЕ! \n')
            float_value = input(string_for_check)
    return float(float_value)


def print_greetings(version, date):
    # Выводит на экран приветствие, номер версии и текущую дату.
    print('\nРассчет оплаты электроэнергии в коммунальной квартире.')
    print('Версия: ', version)
    print('Сегодня на календаре: ', date, '\n')


def recieve_recent_data(db):
    # В зависимости от наличия файла базы данных, создает объект 
    # класса Apartment с предыдущим значением счетчика или с нулевым 
    # значением. А также список объектов класса Room с прошлыми показаниями 
    # или же пустой список.
    try:
        with open(db) as db:
            data = []
            for line in db:
                data.append(eval(line))
        last_data = data[-1]
        recent_apartment = Apartment(meter=last_data['apartment'])
        recent_rooms = []
        for room_meter in last_data['rooms']:
            room = Room(meter=room_meter)
            recent_rooms.append(room)        
    except FileNotFoundError:
        recent_apartment = Apartment()
        recent_rooms = []
    return (recent_apartment, recent_rooms)


def input_data(recent_rooms, int_reader, float_reader):
    # Блок ввода даннх от пользователя и создание объекта с текущей 
    # информацией по квартире.
    tariff = float_reader('Текущий тариф (в руб.): ')
    apartment = Apartment(meter=int_reader('\nПоказания общего счетчика: '))
    if  bool(recent_rooms) == False:
        # Если не были получены значения из базы данных, создаем 
        # объекты класса Room в необходимом количестве с нулевыми 
        # показаниями счетчика и заносим их в список "прошлых" комнат.
        num_of_rooms = int_reader('\nУкажите количество комнат в квартире: ')
        for num in range (num_of_rooms):
            room = Room()
            recent_rooms.append(room)
    else:
        num_of_rooms = len(recent_rooms)
    # Занесим данные в объекты комнат и составляем список из них.
    rooms = []
    for num in range(num_of_rooms):
        room = Room(meter=int_reader('\nПоказания счетчика комнаты номер '
                                      + str(num + 1) + ': '),
                    humans=int_reader('Количество проживающих в комнате: '),
                    debt=float_reader('Долг за прошедший период (руб.): '))
        rooms.append(room)
        print()
    return (tariff, apartment, rooms)


def print_account(room_id, room_cost, communal_cost, debt, total):
    # Вывод на экран детального счета по комнате.
    print('Комната номер', room_id, ':')
    print('Индивидуальное потребление: ', '%.2f' % room_cost, 'руб.')
    print('За коммунальное: ', '%.2f' % communal_cost, 'руб.')
    if debt > 0:
        print('Задолженность: ', '%.2f' % debt, 'руб.')
    print('ИТОГО: ', '%.2f' % total, 'руб.')
    print()
    

def run_calculations(tariff, rooms, recent_rooms, communal_per_person):
    # Выводит на экран инструкцию для пользователя, и, в зависимости от
    # полученной команды, вызывает соответствующую функцию.
    instruction = ('\n Чтобы получить рассчет по комнате, введите ее номер.\n'+
                   ' "all" - чтобы получить рассчет по всем комнатам.\n'+
                   ' "exit" - завершить работу.\n'+
                   ' №: ')
    command = input(instruction)
    print()
    while command != 'exit':
        # Пока не введена команда выхода из программы, выполняется цикл:
        if command == 'all':
            # получение счета для всех комнат,
            r=0
            for room in rooms:
                recent_room = recent_rooms[r]

                (room_cost, 
                 communal_cost, 
                 debt, total) = room.account(tariff, 
                                             recent_room.meter, 
                                             communal_per_person)
                                             
                print_account(r+1, room_cost, communal_cost, debt, total)
                print()
                r+=1
            command = input(instruction)
            print()
        else:
            while True: 
                try: 
                    if 0 < int(command) <= len(rooms):
                        # получение счета по номеру комнаты,
                        print()
                        room = rooms[int(command) - 1]
                        recent_room = recent_rooms[int(command) - 1]

                        (room_cost, 
                         communal_cost, 
                         debt, total) = room.account(tariff, 
                                                     recent_room.meter, 
                                                     communal_per_person)
                        print_account(command, 
                                      room_cost, 
                                      communal_cost, 
                                      debt, total)
                        command = input(instruction)
                        print()
                        break
                    else:
                        # сообщение об ошибке в прочих случаях.
                        print('\n ВВЕДИТЕ КОРРЕКТНУЮ КОММАНДУ! \n')
                        command = input(instruction)
                        print()
                        break
                except ValueError:
                    # сообщение об ошибке в прочих случаях.
                    print('\n ВВЕДИТЕ КОРРЕКТНУЮ КОММАНДУ! \n')
                    command = input(instruction)
                    print()
                    break


def save_to_log(log, today, tariff, apartment, rooms, recent_apartment,
                recent_rooms, communal_per_person):
    # Сохранение детальных данных в лог-файл в читабельном 
    # для пользователя виде.
    data = {}
    data['General'] = {}
    data['General']['Date'] = today
    data['General']['Tariff'] = tariff
    data['Apartment'] = {}
    data['Apartment']['Meter'] = apartment.meter
    data['Apartment']['Consumption'] = apartment.consumption(
                                                    recent_apartment.meter)
    data['Apartment']['Cost of communal consumption per person'] = (
                                                        communal_per_person)
    r=0
    for room in rooms:
        recent_room = recent_rooms[r]
        (room_cost, communal_cost, debt, total) = room.account(
                            tariff, recent_room.meter, communal_per_person)
        data['Room №_' + str(r+1)] = {}
        room_data = data['Room №_' + str(r+1)]
        room_data['Humans'] = room.humans
        room_data['Cost of consumption in the room'] = room_cost
        room_data['Cost of communal consumption in the room'] = communal_cost
        room_data['Debt'] = debt
        room_data['Total'] = total
        r+=1   
    try:
        with open(log, 'a') as log:
            print(data, file=log)
    except FileNotFoundError:
        with open(log, 'x') as log:
            print(data, file=log)


def save_to_db(db, apartment, rooms):
    # Сохранение показаний счетчиков в файл базы данных
    # с целью последующего чтения в данной программе.
    data = {}
    data['apartment'] = apartment.meter
    data['rooms'] = []
    rooms_data = data['rooms']
    for room in rooms:
        rooms_data.append(room.meter)
    try:
        with open(db, 'a') as db:
            print(data, file=db)
    except FileNotFoundError:
        with open(db, 'x') as db:
            print(data, file=db)


def main():
    version = '0.1.3'
    today = datetime.date.isoformat(datetime.date.today())
    db = 'database.txt'
    log = 'logfile.txt'
    int_reader = lambda x: digit_data_input(x)
    float_reader = lambda x: float_data_input(x)

    print_greetings(version, today)

    (recent_apartment, recent_rooms) = recieve_recent_data(db)

    (tariff, apartment, rooms) = input_data(recent_rooms, int_reader, 
                                 float_reader)

    communal_per_person = apartment.communal_per_person(tariff, 
                          recent_apartment.meter, rooms, recent_rooms)

    run_calculations(tariff, rooms, recent_rooms, communal_per_person)

    save_to_log(log, today, tariff, apartment, rooms, recent_apartment,
                recent_rooms, communal_per_person)
    
    save_to_db(db, apartment, rooms)


if __name__ == '__main__':
    main()