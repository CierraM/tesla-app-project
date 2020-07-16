import pytest
from pytest import approx 
from tesla_app import cels_to_fahr
from tesla_app import fahr_to_cels
from tesla_app import executeCommand
from tesla_app import id


def test_cels_to_fahr():
    assert cels_to_fahr(75) == "167°F"
    assert cels_to_fahr(5) == "41°F"
    assert cels_to_fahr(32) == "89.6°F"
    assert cels_to_fahr(-2) == "28.4°F"
    assert cels_to_fahr(40) == "104°F"
    assert cels_to_fahr(22) == "71.6°F"
    1
def test_fahr_to_cels():
    assert fahr_to_cels(75) == pytest.approx(23.8889, .01)
    assert fahr_to_cels("75°F") == pytest.approx(23.8889, .01)
    assert fahr_to_cels("60") == pytest.approx(15.5556, .01)
    assert fahr_to_cels(90) == pytest.approx(32.2222, .01)
    assert fahr_to_cels("7m9h") == pytest.approx(26.1111, .01)
    assert fahr_to_cels(105) == pytest.approx(40.5556, .01)
    assert fahr_to_cels(-7) == pytest.approx(-21.6667, .01)

#executeCommand(url, command, *params)
# Test to make sure request is going through properly
def test_execute_command():
    assert executeCommand(f'/api/1/vehicles/{id}/command/honk_horn', 1) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/flash_lights', 2) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/door_unlock', 3) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/door_lock', 3) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/window_control', 4, {"lat": "0", "lon": "0", "command": "vent"}) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/charge_port_door_open', 5) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/set_charge_limit', 6, {"percent":90}) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/set_temps', 7, {"driver_temp":20,"passenger_temp":20}) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/auto_conditioning_start', 8) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/auto_conditioning_stop', 8) == True
    assert executeCommand(f'/api/1/vehicles/{id}/command/charge_port_door_close', 5) == True


pytest.main(["test_tesla_app.py"])