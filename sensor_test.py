from conftest import wait
from conftest import SensorInfo
from typing import Callable
import logging
import pytest

log = logging.getLogger(__name__)

METHOD_ERROR_CODE = -32000
METHOD_ERROR_MSG = "Method execution error"


def test_sanity(get_sensor_info, get_sensor_reading):
    sensor_info = get_sensor_info()

    sensor_name = sensor_info.name
    assert isinstance(sensor_name, str), "Sensor name is not a string"

    sensor_hid = sensor_info.hid
    assert isinstance(sensor_hid, str), "Sensor hid is not a string"

    sensor_model = sensor_info.model
    assert isinstance(sensor_model, str), "Sensor model is not a string"

    sensor_firmware_version = sensor_info.firmware_version
    assert isinstance(
        sensor_firmware_version, int
    ), "Sensor firmware version is not a int"

    sensor_reading_interval = sensor_info.reading_interval
    assert isinstance(
        sensor_reading_interval, int
    ), "Sensor reading interval is not a string"

    sensor_reading = get_sensor_reading()
    assert isinstance(
        sensor_reading, dict
    ), "Sensor doesn't seem to register temperature"

    log.info("Sanity test passed")


def test_reboot(get_sensor_info, reboot_sensor):
    """
    Steps:
        1. Get original sensor info.
        2. Reboot sensor.
        3. Wait for sensor to come back online.
        4. Get current sensor info.
        5. Validate that info from Step 1 is equal to info from Step 4.
    """
    log.info("Get original sensor info")
    sensor_info_before_reboot = get_sensor_info()

    log.info("Reboot sensor")
    reboot_response = reboot_sensor()
    assert (
        reboot_response == "rebooting"
    ), "Sensor did not return proper text in response to reboot request"

    log.info("Wait for sensor to come back online")
    sensor_info_after_reboot = wait(
        func=get_sensor_info,
        condition=lambda x: isinstance(x, SensorInfo),
        tries=10,
        timeout=1,
    )

    log.info("Validate that info from Step 1 is equal to info from Step 4")
    assert (
        sensor_info_before_reboot == sensor_info_after_reboot
    ), "Sensor info after reboot doesn't match sensor info before reboot"


def test_set_sensor_name(get_sensor_info, set_sensor_name):
    """
    1. Set sensor name to "new_name".
    2. Get sensor_info.
    3. Validate that current sensor name matches the name set in Step 1.
    """

    expected_name = "new_name"

    log.info(f"Set sensor name to {expected_name}")
    set_sensor_name(expected_name)

    log.info("Get sensor info")
    sensor_info = get_sensor_info()

    log.info("Validate that current sensor name matches the name set in Step 1.")
    assert sensor_info.name == expected_name, "Sensor didn't set its name correctly"


def test_set_sensor_reading_interval(
    get_sensor_info, set_sensor_reading_interval, get_sensor_reading
):
    """
    1. Set sensor reading interval to 1.
    2. Get sensor info.
    3. Validate that sensor reading interval is set to interval from Step 1.
    4. Get sensor reading.
    5. Wait for interval specified in Step 1.
    6. Get sensor reading.
    7. Validate that reading from Step 4 doesn't equal reading from Step 6.
    """
    expected_reading_interval = 1

    log.info(f"Set sensor reading interval to {expected_reading_interval}")
    set_sensor_reading_interval(expected_reading_interval)

    log.info("Get sensor info")
    sensor_info = get_sensor_info()

    log.info("Validate that sensor reading interval is set to interval from Step 1")
    assert (
        sensor_info.reading_interval == expected_reading_interval
    ), "Sensor didn't set its reading interval correctly"

    log.info("Get sensor reading")
    sensor_reading_before_waiting = get_sensor_reading()

    log.info(
        "Wait for interval specified in Step 1 and get sensor reading and validate that reading from Step 4 doesn't equal reading from Step 6"
    )
    assert wait(
        func=get_sensor_reading,
        condition=lambda x: x != sensor_reading_before_waiting,
        tries=10,
        timeout=1,
    )


# Максимальна версія прошивки сенсора -- 15
def test_update_sensor_firmware(get_sensor_info, update_sensor_firmware):
    """
    1. Get original sensor firmware version.
    2. Request firmware update.
    3. Get current sensor firmware version.
    4. Validate that current firmware version is +1 to original firmware version.
    5. Repeat steps 1-4 until sensor is at max_firmware_version - 1.
    6. Update sensor to max firmware version.
    7. Validate that sensor is at max firmware version.
    8. Request another firmware update.
    9. Validate that sensor doesn't update and responds appropriately.
    10. Validate that sensor firmware version doesn't change if it's at maximum value.
    """
    log.info("Set max firmware version")
    max_firmware_version = 15

    log.info("Get current sensor firmware version")
    current_sensor_firmware_version = get_sensor_info().firmware_version

    log.info("Repeat steps 1-4 until sensor is at max_firmware_version - 1")
    while current_sensor_firmware_version != max_firmware_version:

        log.info(
            "Validate that expected firmware version is +1 to current firmware version"
        )
        expected_firware_version = current_sensor_firmware_version + 1

        log.info("Request firmware update")
        update_sensor_firmware_response = update_sensor_firmware()

        log.info("Insure sensor is updating")
        assert update_sensor_firmware_response == "updating"

        log.info(
            "While sensor is updating to version 14 validate expected firmware version is current version"
        )
        assert wait(
            func=get_sensor_info,
            condition=lambda x: x.firmware_version == expected_firware_version,
            tries=15,
            timeout=1,
        )

        log.info("Sensor version is current version + 1")
        current_sensor_firmware_version += 1

    log.info("Request another firmware update")
    update_sensor_firmware_response = update_sensor_firmware()

    log.info(
        "Validate that sensor version is max, sensor doesn't update and responds appropriately"
    )
    assert update_sensor_firmware_response == "already at latest firmware version"
    assert get_sensor_info().firmware_version == max_firmware_version


@pytest.mark.parametrize("invalid_interval", [0.4, -1])
def test_set_invalid_sensor_reading_interval(
    get_sensor_info, set_sensor_reading_interval, invalid_interval
):
    """
    Test Steps:
        1. Get original sensor reading interval.
        2. Set interval to < 1
        3. Validate that sensor responds with an error.
        4. Get current sensor reading interval.
        5. Validate that sensor reading interval didn't change.
    """
    log.info("Get original sensor reading interval")
    original_sensor_reading_interval = get_sensor_info().reading_interval

    log.info("Set interval to < 1")
    log.info("Validate that sensor responds with an error")
    sensor_response = set_sensor_reading_interval(invalid_interval)
    assert sensor_response.get("code") and sensor_response.get(
        "message"
    ), "Sensor response doesn't seem to be an error"
    assert (
        sensor_response.get("code") == METHOD_ERROR_CODE
    ), "Error code doesn't match expected"
    assert (
        sensor_response.get("message") == METHOD_ERROR_MSG
    ), "Error message doesn't match expected"

    log.info("Get current sensor reading interval")
    log.info("Validate that sensor reading interval didn't change")
    assert (
        original_sensor_reading_interval == get_sensor_info().reading_interval
    ), "Sensor reading interval changed when it shouldn't have"


def test_set_empty_sensor_name(get_sensor_info, set_sensor_name):
    """
    Test Steps:
        1. Get original sensor name.
        2. Set sensor name to an empty string.
        3. Validate that sensor responds with an error.
        4. Get current sensor name.
        5. Validate that sensor name didn't change.
    """
    log.info("Get original sensor name")
    original_sensor_name = get_sensor_info().name

    log.info("Set sensor name to an empty string")
    log.info("Validate that sensor responds with an error")
    sensor_response = set_sensor_name("")
    assert sensor_response.get("code") and sensor_response.get(
        "message"
    ), "Sensor response doesn't seem to be an error"
    assert (
        sensor_response.get("code") == METHOD_ERROR_CODE
    ), "Error code doesn't match expected"
    assert (
        sensor_response.get("message") == METHOD_ERROR_MSG
    ), "Error message doesn't match expected"

    log.info("Get current sensor name")
    log.info("Validate that sensor name didn't change")
    assert (
        original_sensor_name == get_sensor_info().name
    ), "Sensor name changed when it shouldn't have"
