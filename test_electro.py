import pytest
import datetime
import pprint
from electro import RecentData, GeneralData, RoomsData, AllNewData
from electro import ROOM_N, METER, HUMANS, DEBT, COMMUNAL_COST, ROOM_COST


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