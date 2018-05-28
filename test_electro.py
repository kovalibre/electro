import pytest
import datetime
import pprint
from electro import (Apartment, Room, 
                    digit_data_input, float_data_input,
                    print_greetings,
                    recieve_recent_data,
                    input_data,
                    print_account,
                    run_calculations,
                    save_to_log, save_to_db)

def test_run_calculations():
    tariff = 2
    room1 = Room(meter=100, humans=1)
    room2 = Room(meter=150, humans=2)
    rooms = [room1, room2]
    recent1 = Room()
    recent2 = Room()
    recent_rooms = [recent1, recent2]
    communal_per_person = 25.0

    run_calculations(tariff, rooms, recent_rooms, communal_per_person)
    
     

"""
def test_electro():
    today = datetime.date.isoformat(datetime.date.today())
    recent = RecentData('')
    general = GeneralData()
    general.tariff = 10
    general.number_of_rooms = 1
    general.meter = 100
    rooms_data = {
        ROOM_N + '1': {
            METER: 50,
            HUMANS: 1,
            DEBT: 0.
        }
    }
    rooms = RoomsData(rooms_data)

    new_data = AllNewData()

    general.calculate_consumption(recent.meter)
    rooms.calculate_consumption(general.number_of_rooms,
                                recent.number_of_rooms,
                                recent.rooms)
    general.calculate_communal_per_person(rooms.rooms)
    rooms.calculate_accounts(general.number_of_rooms,
                             general.tariff,
                             general.communal_per_person)
    new_data.collect(today,
                     general.number_of_rooms,
                     general.meter,
                     general.tariff,
                     general.consumption,
                     general.communal_per_person,
                     rooms.rooms)

    assert 500 == new_data.data[ROOM_N + '1'][COMMUNAL_COST]
    assert 500 == new_data.data[ROOM_N + '1'][ROOM_COST]
"""