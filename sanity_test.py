from time import sleep
from requests.exceptions import JSONDecodeError


def test_sanity(get_sensor_info, get_sensor_reading):
    sensor_info = get_sensor_info()
    
    sensor_name = sensor_info.get("name")
    assert isinstance(sensor_name, str), "Sensor name is not a string"

    sensor_hid = sensor_info.get("hid")
    assert isinstance(sensor_hid, str), "Sensor hid is not a string"

    sensor_model = sensor_info.get("model")
    assert isinstance(sensor_model, str), "Sensor model is not a string"

    sensor_firmware_version = sensor_info.get("firmware_version")
    assert isinstance(sensor_firmware_version, int), "Sensor firmware version is not an int"

    sensor_reading_interval = sensor_info.get("reading_interval")
    assert isinstance(sensor_reading_interval, int), "Sensor reading interval is not a string"

    sensor_reading = get_sensor_reading()
    assert isinstance(sensor_reading, float), "Sensor doesn't seem to register temperature"

    print("Sanity test passed")


def test_reboot(get_sensor_info, sensor_reboot):
    """
    Steps:
        1. Get original sensor info.
        2. Reboot sensor.
        3. Wait for sensor to come back online.
        4. Get current sensor info.
        5. Validate  that info from Step 1 is equal to info in Step 4. 
    """
print("Get original sensor info")
sensor_info_before_reboot = get_sensor_info()

print("Reboot sensor")
reboot_response = sensor_reboot()
assert reboot_response == "rebooting", "Sensor did not return proper text in response to reboot request"

print("Wait for sensor to come back online")
sensor_info_after_reboot = None

for i in range(10):
    print(f"Waiting for sensor; attempt (i+1)")
    try:
        print("Get current sensor info")
        sensor_info_after_reboot = get_sensor_info()
        break
    except JSONDecodeError:
        print("Couldn't get sensor info")
        pass

    print("Sleepinf for 1 second")
    sleep(1)

print("Validate  that info from Step 1 is equal to info in Step 4") 
assert original_sensor_info == current_sensor_info, "Sensor info after reboot doesn't match sensor info before reboot"
